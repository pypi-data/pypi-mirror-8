//
// IMessageNotify
// -----------------------------------------------------------------------------

function IMessageNotify() {
    // brain
    this.cache = {
        userId: $('#ESI_DATA').data('ityou-uid')
    };
    
    // settings
    this.settings = {
        maxMessages: 500,
        maxLength: 30
    };
    
    // selector
    this.selector = {
        notify: '#notify-messages',
        notifyBox: '#notify-messages-box',
        messages: '.message-notify-list',
        counter: '#messages-counter'
    };
    
    // template
    this.template = {
        wrapper: '#imessage-notify-wrapper-template',
        dropdown: '#imessage-notify-template'
    };
    
    
    // get something from cache
    this.getCache = function(option) {
        if(this.cache.hasOwnProperty(option)) {
            return this.cache[option];
        }
        
        return undefined;
    };
    
    // set something to cache
    this.setCache = function(option, value) {
        this.cache[option] = value;
        return this;
    };
    
    // get option
    this.getOption = function(option, key) {
        if(undefined === key) {
            if(this.hasOwnProperty(option)) {
                return this[option];
            }
        } else {
            if(this.hasOwnProperty(key) && this[key].hasOwnProperty(option)) {
                return this[key][option];
            }
        }
        
        return undefined;
    };
    
    // set option
    this.setOption = function(option, value, key) {
        if(undefined === key) {
            this[option] = value;
        } else {
            this[key][option] = value;
        }
        
        return this;
    };
    
    
    // initialize imessage notify
    this.init();
}


// IMessageNotify extends Utilities
IMessageNotify.prototype = new Utilities();

//ActivityStream implements ClientTimezone
IMessageNotify.prototype.TimeConverter = new ClientTimezone();



/**
 *
 */
IMessageNotify.prototype.init = function() {
    this.getNotify();
};


/**
 *
 */
IMessageNotify.prototype.getNotify = function() {
    var senderIds = [];
    
    $.ajax({
        url: '@@ajax-messages',
        data: {
            action: 'get_messages',
            approved: false,
            max: this.getOption('maxMessages', 'settings'),
            omit_sender: this.getCache('userId')
        },
        dataType: 'json',
        // event handler success
        success: $.proxy(function(response) {
            var $counter = $(this.getOption('counter', 'selector')),
                $box = $(this.getOption('notifyBox', 'selector'));
                
            $counter.text(response.length);
            
            if(response.length > 0) {
                $counter.removeClass('hidden');
                
                $.each(response, $.proxy(function(i, val) {
                	// need to change response[i][timestr]
                	response[i]['timestr'] = this.TimeConverter.convertTime(val.timestamp);
                }, this));
                
                if($box.length === 0) {
                    $($(this.getOption('wrapper', 'template')).render()).appendTo(this.getOption('notify', 'selector'));
                }
            } else {
                $counter.addClass('hidden');
                
                if($box.length > 0) {
                    $box.prev('.arrow-top').remove();
                    $box.remove();
                }
            }
            
            response = this.filter(response);
            
            this.render(response);
        }, this)
    });
};


/**
 *
 */
IMessageNotify.prototype.render = function(data) {
    var msgList = $('<ul/>'),
        messages = this.getOption('messages', 'selector'),
        $tmpl = $(this.getOption('dropdown', 'template'));
        
    $(messages).empty();
    
    $.each(data, function(key, value) {
        $($tmpl.render(value)).appendTo(msgList);
    });
    
    msgList.appendTo(messages);
};


/**
 *
 */
IMessageNotify.prototype.filter = function(data) {
    var sender = [],
        senderData = {};
        
    $.each(data, $.proxy(function(key, value) {
        if(value.hasOwnProperty('group') && value.group === true) {
            data[key].sender_id = value.receiver_id;
            data[key].sender_name = value.receiver_name;
            data[key].sender_portrait = value.receiver_portrait;
        }
        
        if($.inArray(value.sender_id, sender) === -1) {
            sender.push(value.sender_id);
            
            var regex = /<br\s*[\/]?>/gi,
                tmp = $('<p/>').append($.trim(value.message.replace(regex, ' '))).text();

            value.message = tmp.substr(0, this.getOption('maxLength', 'settings')) + (tmp.length > this.getOption('maxLength', 'settings') ? '...' : '');

            senderData[value.sender_id] = $.extend({}, {count: 1}, value);
        } else {
            senderData[value.sender_id].count += 1;
        }
    }, this));
    
    return senderData;
};

