function StatusFlags(settings) {
	this.settings = $.extend({
		astream: {},
		inbox: {},
		imessage: {},
		whoisonline: {}
	}, settings);
	
	this.getSettings = function(key) {
		if(this.settings.hasOwnProperty(key)) {
			return this.settings[key];
		}
		
		return {};
	};
	
    this.delayStatus = $('#ESI_DATA').data('ityou-statusflags-delay') !== undefined ? $('#ESI_DATA').data('ityou-statusflags-delay') * 1000 : 5000;

    // astream options
    this.astreamBadge = '#activities-counter';
    
    /**
     * magic getter
     *
     * @param string option
     * @return mixed | undefined
     */
    this.getOption = function(option) {
        if(undefined !== this[option]) {
            return this[option];
        }
        
        return undefined;
    };
    
    /**
     * magic setter
     *
     * @param string option
     * @param mixed value
     * @return StatusFlags
     */
    this.setOption = function(option, value) {
        this[option] = value;
        return this;
    };
}


// StatusFlags extends Utilities
StatusFlags.prototype = new Utilities();

// ActivityStream
StatusFlags.prototype.astream = new ActivityStream();

// ItyouInbox
StatusFlags.prototype.inbox = new ItyouInbox();

// IMessageDialog
StatusFlags.prototype.dialog = new IMessageDialog();

// IMessageNotify
StatusFlags.prototype.imessageNotify = new IMessageNotify();

// IMessageCleanNewMessage
StatusFlags.prototype.cleanMessage = new IMessageCleanNewMessage();

// WhoIsOnline
StatusFlags.prototype.whoisonline = new WhoIsOnline();

// Clipboard
//StatusFlags.prototype.clipboard = new Clipboard();


/**
 * constructor function of StatusFlags
 *
 * @return void
 */
StatusFlags.prototype.init = function() {
	// init imessage scripts
	this.dialog.setSettings(this.getSettings('imessage')).init();
	this.cleanMessage.setSettings(this.getSettings('imessage')).init();
	this.inbox.setSettings(this.getSettings('inbox')).init();
	// set whoisonline settings
	this.whoisonline.setSettings(this.getSettings('whoisonline'));
	// set astream settings
	this.astream.setSettings(this.getSettings('astream'));
	
	
    // init notify
    this.astreamProcess();
    
    // init whoisonline
    this.whoisonlineProcess();

    // init StatusFlags only when a user id is set
    if($('#ESI_DATA').length > 0 && $('#ESI_DATA').data('ityou-uid') !== undefined) {
        // set userid
        this.setOption('userId', $('#ESI_DATA').data('ityou-uid'));
        
        // start streaming
        this.requestStatus();
    }
    
    //this.clipboard.init(this.getOption('userId'));
};


/**
 * do request
 *
 * @return void
 */
StatusFlags.prototype.requestStatus = function() {
    $.ajax({
        url: '@@ajax-statusflags',
        dataType: 'json',
        timeout: 30000,
        // event handler success
        success: $.proxy(function(response) {
            if(this.size(response) > 0) {
                this.processResponse(response);
            }
            
            setTimeout($.proxy(function() {
                this.requestStatus();
            }, this), this.getOption('delayStatus'));
        }, this),
        // event handler error
        error: $.proxy(function(XMLHttpRequest, textStatus, errorThrown) {
            this.log((new Date()).toISOString(), XMLHttpRequest, textStatus, errorThrown);
            
            if(textStatus.toLowerCase() === 'timeout') {
                this.log('Request timed out...');
                
                //this.requestStatus();
            }
            
            this.retry();
        }, this)
    });
};


StatusFlags.prototype.retry = function() {
	var t = setTimeout($.proxy(function() {
		this.requestStatus();
	}, this), 30000);
};


/**
 * process the response given by ajax request
 *
 * @param object values
 * @return void
 */
StatusFlags.prototype.processResponse = function(values) {
    if(values.hasOwnProperty('imessage') && parseInt(values.imessage) === 1) {
        this.imessageProcess();
    }
    
    if(values.hasOwnProperty('astream') && parseInt(values.astream) === 1) {
        this.astreamProcess();
    }
    
    if(values.hasOwnProperty('astream_comments') && parseInt(values.astream_comments) === 1) {
        this.astreamCommentsProcess();
    }
    
    if(values.hasOwnProperty('whoisonline') && parseInt(values.whoisonline) === 1) {
        this.whoisonlineProcess();
    }
};


/**
 * change text and visibility base on the value in notify sector
 *
 * @param string state
 * @param string value
 * @return void
 */
StatusFlags.prototype.notifyBadge = function(state, value) {
    var $badge = $(this.getOption(state + 'Badge'));
    
    $badge.text(value);
    
    if(value > 0) {
        $badge.removeClass('badge-hide');
    } else {
        $badge.addClass('badge-hide');
    }
};


/**
 * process imessage and call get_messages via ajax
 *
 * @return void
 */
StatusFlags.prototype.imessageProcess = function() {
    this.imessageNotify.getNotify();
    
    // if we are currently viewing the inbox, load new messages in inbox
    if(this.inbox.isInbox() || this.inbox.isDialogOverview()) {
        this.inbox.inboxStream();
    }
    
    // if we are currently vieweing the dialog, load new messages in dialog
    if(this.dialog.isDialog()) {
        this.dialog.updateDialog();
    }
};


/**
 * process astream and call count_latest_activities via ajax
 *
 * @return void
 */
StatusFlags.prototype.astreamProcess = function() {
    var latest_activity_timestamp = this.storage.local.get('activitiesTimestamp'); // activitiesTimestamp needs to be set with JSON.stringify()
    //var latest_activity_timestamp = window.ITYOU.storage.get('activitiesTimestamp');
    
    $.ajax({
        url: '@@ajax-notify',
        data: {
            action: 'count_latest_activities',
            timestamp: latest_activity_timestamp
        },
        dataType: 'json',
        // event handler success
        success: $.proxy(function(response) {
            this.notifyBadge('astream', response);
            
            if(response > 0) {
                this.astreamRenderer();
            }
        }, this)
    });
};


/**
 * 
 *
 * @return void
 */
StatusFlags.prototype.astreamRenderer = function() {
    // follow state
    var followInstalled = $('#astream-tabs').length > 0 ? true : false,
        // followState = all | follow
        followState = followInstalled ? ($('#astream-tabs').find('li.active').find('a').hasClass('astream-tab-all') ? 'all' : 'follow') : false;
    
    if(this.astream.isActivityStream()) {
        if(followInstalled) {
            this.astream.getActivities('get_latest_activities');
        } else {
            this.astream.getActivities('get_latest_activities');
        }
    }
};



StatusFlags.prototype.astreamCommentsProcess = function() {
    if(this.astream.isActivityStream()) {
        this.astream.getComments();
    }
};



StatusFlags.prototype.whoisonlineProcess = function() {
    this.whoisonline.getAll();
};























$(function() {
	var commentsModeratable = $('#ESI_DATA').data('ityou-comment-flag') === undefined ? false : (parseInt($('#ESI_DATA').data('ityou-comment-flag')) === 0 ? false : true);
	
	
    var statusFlags = new StatusFlags({
    	imessage: {
    		useWYSIWYG: false
    	},
    	whoisonline: {
    		refreshState: 1000
    	},
    	astream: {
    		moderatable: commentsModeratable
    	}
    });
    
    statusFlags.init();
});
