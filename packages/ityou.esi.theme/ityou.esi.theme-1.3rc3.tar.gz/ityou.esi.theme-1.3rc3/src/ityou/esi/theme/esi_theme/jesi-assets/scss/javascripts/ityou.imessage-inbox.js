/**
 *******************************************************************************
 *
 *  INBOX
 *
 *******************************************************************************
 */
function ItyouInbox() {
    this.messageTemplate = '#inbox-tmpl';
    this.messageList = '#imessage-inbox table > tbody';
    
    this.max = 20;
    this.filterMax = 5;
    
    this.minValue = 2;
    
    this.runningRequest = false;
    this.latestTimestamp = null;
    this.lastScrollTop = 0;
    
    this.user_id = $('#ESI_DATA').data('ityou-uid');
    
    this.runningStream = false;
    this.inboxStreamDelay = 5000;
    
    
    // brain
    this.cache = {
        // own userid
        userId: undefined,
        
        // handle view
        currentView: undefined,
        
        // lastScrolltop
        lastScrollTop: 0,
        
        // filter
        filter: undefined
    };
    
    
    // templates
    this.template = {
        messageTemplate: '#inbox-tmpl',
        do_messageTemplate: '#dialog-overview-tmpl'
    };
    
    // selectors
    this.selector = {
        messageList: '#imessage-inbox table > tbody',
    	dialogMessageList: '#dialog-overview-messages-list',
    	dialogLoadMoreTrigger: '#dialog-overview-load-more-trigger'
    };
    
    // settings
    this.settings = {
        max: 20,
        filterMax: 5,
        minValue: 2
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
    
    
    this.setSettings = function(settings) {
    	if(settings) {
    		this.settings = $.extend(this.settings, settings);
    	}
    	
    	return this;
    };
    
    
    
    // initialize inbox
    //this.init();
}


ItyouInbox.prototype = new Utilities();

//ActivityStream implements ClientTimezone
ItyouInbox.prototype.TimeConverter = new ClientTimezone();


ItyouInbox.prototype.init = function(settings) {
    this.setCache('userId', $('#ESI_DATA').data('ityou-uid'));
    this.setSettings(settings);
    
    // define in which template we are
    this.defineView();
    
    // get latest activities
    if(this.isInbox()) {
        //this.initEventHandler();
        this.eventHandler();
    
        this.getMessages(0);
    } else if(this.isDialogOverview()) {
    	this.eventHandler();
    	
    	this.getMessages(0);
    }


    //this.getMessages(0);
    //this.eventHandler();
    
    //this.inboxStream();
};


/**
 * define which page is currently viewed
 *
 * @return void
 */
ItyouInbox.prototype.defineView = function() {
    var pathname = document.location.pathname,
        matchAgainst = /@@message-inbox/i,
        elseMatchAgainst = /@@dialog-overview/i;
    
    if(matchAgainst.exec(pathname)) {
        this.setCache('currentView', 'inbox');
    
        return ;
    } else if(elseMatchAgainst.exec(pathname)) {
    	this.setCache('currentView', 'dialog-overview');
    	
    	return ;
    }
    
    this.setCache('currentView', undefined);
};


/**
 * simple helper to ask if we can build an astream
 *
 * @return boolean
 */
ItyouInbox.prototype.isInbox = function() {
    if(this.getCache('currentView') === 'inbox') {
        return true;
    }
    
    return false;
};

ItyouInbox.prototype.isDialogOverview = function() {
	if(this.getCache('currentView') === 'dialog-overview') {
		return true;
	}
	
	return false;
};


/**
 * get messages in inbox
 *
 * @param int offset
 */
ItyouInbox.prototype.getMessages = function(offset) {
    var $messageList = $(this.getOption('messageList', 'selector'));
    
    if(this.isInbox()) {
	    if(undefined !== this.filteredUsers) {
	        if(!this.runningRequest) {
	            this.runningRequest = true;
	            
	            this.clearFiltering();
	            this.showSpinner();
	            
	            var tmpUid = new Array();
	            $messageList.children().each(function() {
	                var $el = $(this).find('td[data-uid]');
	                
	                if($el.length > 0 && $.inArray($el.data('uid'), tmpUid) === -1) {
	                    tmpUid.push($el.data('uid'));
	                }
	            });
	            
	            var tmpOffsets = new Array();
	            $.each(tmpUid, $.proxy(function(k, v) {
	                tmpOffsets.push($messageList.children().find('td[data-uid="' + v + '"]').length);
	            }, this));
	            
	            offset = this.sortNumeric(tmpOffsets, 'desc')[0];
	            
	            this.fetchMessages(this.filteredUsers, offset);
	            this.timerCallback('filteredMessages', 'sortMessages');
	            
	            var timer = setInterval($.proxy(function() {
	                if(undefined !== this.returnValue) {
	                    clearInterval(timer);
	                
	                    if(this.returnValue.length > 0) {
	                        this.renderMessages(this.returnValue, 'append');
	                        
	                        this.sortByDate();
	                        
	                        this.loadMoreEvent();
	                    }
	                    
	                    this.runningRequest = false;
	                    this.hideSpinner();
	                }
	            }, this), 100);
	        }
	    } else {
	        if(!this.runningRequest) {
	            this.runningRequest = true;
	            
	            this.showSpinner();
	        
	            $.getJSON('@@ajax-messages', {action: 'get_messages', approved: 'all', max: this.max, offset: offset, omit_sender: this.user_id}, $.proxy(function(response) {
	            	$.each(response, $.proxy(function(i, val) {
	                	// need to change response[i][timestr]
	                	response[i]['timestr'] = this.TimeConverter.convertTime(val.timestamp);
	                }, this));
	            	
	                this.renderMessages(response, 'append');
	                this.runningRequest = false;
	                
	                if(response.length > 0) {
	                    this.loadMoreEvent();
	                }
	                
	                this.hideSpinner();
	            }, this));
	        }
	    }
    } else if(this.isDialogOverview()) {
    	if(undefined !== this.filteredUsers) {
	        if(!this.runningRequest) {
	            this.runningRequest = true;
	            
	            this.clearFiltering();
	            this.showSpinner();
	            
	            var tmpUid = new Array();
	            $messageList.children().each(function() {
	                var $el = $(this).find('td[data-uid]');
	                
	                if($el.length > 0 && $.inArray($el.data('uid'), tmpUid) === -1) {
	                    tmpUid.push($el.data('uid'));
	                }
	            });
	            
	            var tmpOffsets = new Array();
	            $.each(tmpUid, $.proxy(function(k, v) {
	                tmpOffsets.push($messageList.children().find('td[data-uid="' + v + '"]').length);
	            }, this));
	            
	            offset = this.sortNumeric(tmpOffsets, 'desc')[0];
	            
	            this.fetchMessages(this.filteredUsers, offset);
	            this.timerCallback('filteredMessages', 'sortMessages');
	            
	            var timer = setInterval($.proxy(function() {
	                if(undefined !== this.returnValue) {
	                    clearInterval(timer);
	                
	                    if(this.returnValue.length > 0) {
	                        this.renderMessages(this.returnValue, 'append');
	                        
	                        this.sortByDate();
	                        
	                        this.loadMoreEvent();
	                    }
	                    
	                    this.runningRequest = false;
	                    this.hideSpinner();
	                }
	            }, this), 100);
	        }
	    } else {
	        if(!this.runningRequest) {
	            this.runningRequest = true;
	            
	            if(offset === 0) {
	            	this.showSpinner();
	            }
	        
	            $.getJSON('@@ajax-messages', {action: 'get_messages', approved: 'all', max: 50, offset: offset, dialog: true}, $.proxy(function(response) {
	            	$.each(response, $.proxy(function(i, val) {
	                	// need to change response[i][timestr]
	                	response[i]['timestr'] = this.TimeConverter.convertTime(val.timestamp);
	                }, this));
	            	
	            	if(response.length > 0) {
	            		if(response.length > 2) {
	            			$('.new-message').removeClass('hidden');
	            		}
	            	}
	            	
	                this.renderMessages(response, 'append');
	                this.runningRequest = false;
	                
	                if(response.length > 0) {
                		this.getMessages(offset + 50);
	                }
	                
	                this.hideSpinner();
	            }, this));
	        }
	    }
    }
};


ItyouInbox.prototype.getLatestMessages = function() {
	var ajaxData;
	
	if(this.isInbox()) {
	    ajaxData = {
	        action: 'get_messages',
	        approved: 'all',
	        newer: true,
	        omit_sender: this.user_id
	    };
	} else if(this.isDialogOverview()) {
		ajaxData = {
			action: 'get_messages',
			approved: 'all',
			newer: true,
			dialog: true
		}
	}
    
    if(this.getLatestTimestamp()) {
        ajaxData = $.extend(ajaxData, {timestamp: this.getLatestTimestamp()});
    }
    
    //console.log(this.getLatestTimestamp());

    $.getJSON('@@ajax-messages', ajaxData, $.proxy(function(response) {
        if(response.length > 0) {
            this.setLatestTimestamp(response[0]['timestamp']);
            
            $.each(response, $.proxy(function(i, val) {
            	// need to change response[i][timestr]
            	response[i]['timestr'] = this.TimeConverter.convertTime(val.timestamp);
            }, this));
    
            this.renderMessages(response, 'prepend');
        }
    }, this));
};


ItyouInbox.prototype.renderMessages = function(data, direction) {
	if(this.isInbox()) {
	    $.each(data, $.proxy(function(index, val) {
	        var dataToRender = {};
	        
	        if(val.group === true) {
	            val.sender_id = val.receiver_id;
	            val.sender_portrait = val.receiver_portrait;
	            val.sender_name = val.receiver_name;
	        }
	        
	        dataToRender.hash = val.hash;
	        dataToRender.sender_name = val.sender_name;
	        dataToRender.sender_id = val.sender_id;
	        dataToRender.sender_portrait = val.sender_portrait;
	        dataToRender.timestr = val.timestr;
	        dataToRender.ploneTimeStamp = val.timestamp;
	        dataToRender.timeStamp = this.convertToUNIXTimestamp(val.timestamp);
	        dataToRender.approved = val.approved;
	        dataToRender.siteUrl = val.site_url;
	        dataToRender.group = val.group;
	
	        var strip = $('<div>' + val.message + '</div>').text();
	        dataToRender.msg = strip.substr(0,30) + (strip.length > 30 ? '...' : '');
	        
	        if(direction === 'append') {
	            $($(this.messageTemplate).render(dataToRender)).appendTo(this.messageList);
	        } else if(direction === 'prepend') {
	            $($(this.messageTemplate).render(dataToRender)).prependTo(this.messageList);
	        }
	    }, this));
	} else if(this.isDialogOverview()) {
		$.each(data, $.proxy(function(index, val) {
			var dataToRender = {},
				unread = 0;
			var changed = val.sender_id === this.user_id;
			var replace_text = true;
			
			if(val.group === true || val.sender_id === this.user_id) {
				val.sender_id = val.receiver_id;
				val.sender_portrait = val.receiver_portrait;
				val.sender_name = val.receiver_name;
			}
			
			var tmp = $('div[data-dialog="' + val.sender_id + '"]');
			
			if(tmp.length > 0) {
				unread = tmp.find('span.badge').length > 0 ? parseInt(tmp.find('span.badge').text()) : 0;
				
				if(tmp.data('timestamp') > val.timestamp) {
					replace_text = false;
				} else {
					tmp.remove();
				}
			}
			
			if(replace_text) {
				dataToRender.hash = val.hash;
		        dataToRender.sender_name = val.sender_name;
		        dataToRender.sender_id = val.sender_id;
		        dataToRender.sender_portrait = val.sender_portrait;
		        dataToRender.timestr = val.timestr;
		        dataToRender.ploneTimeStamp = val.timestamp;
		        dataToRender.timeStamp = this.convertToUNIXTimestamp(val.timestamp);
		        dataToRender.siteUrl = val.site_url;
		        dataToRender.group = val.group;
		        dataToRender.unread = val.unread + unread;
		        dataToRender.lastFromMe = changed;
		
		        var strip = $('<div>' + val.message + '</div>').text();
		        dataToRender.msg = strip.substr(0,30) + (strip.length > 30 ? '...' : '');
		        
		        if(direction === 'append') {
		            $($(this.template.do_messageTemplate).render(dataToRender)).appendTo(this.selector.dialogMessageList);
		        } else if(direction === 'prepend') {
		            $($(this.template.do_messageTemplate).render(dataToRender)).prependTo(this.selector.dialogMessageList);
		        }
			}
		}, this));
		
		// set latest timetamp
		var d = [];
		$(this.selector.dialogMessageList).find('> div[data-timestamp]').each(function() {
			d.push($(this).data('timestamp'));
		});
		
		this.setLatestTimestamp(this.maxDate(d));
	}
};

ItyouInbox.prototype.maxDate = function(dates) {
	var max = dates[0];
	
	for(var i = 1; i < dates.length; i++) {
		if(dates[i-1] < dates[i]) {
			max = dates[i];
		}
	}
	
	return max;
};


ItyouInbox.prototype.eventHandler = function() {
	if(this.isDialogOverview()) {
		$(this.getOption('dialogMessageList', 'selector')).on('click', '.user-information > .user-portrait + div', $.proxy(function(e) {
			location.href = $(e.currentTarget).find('a').attr('href');
		}, this));
	} else {
	    $('#imessage-inbox').on('change', 'thead input[type="checkbox"][name="selectAll"]', $.proxy(function(e) {
	        var $this = $(e.currentTarget),
	            $checkboxes = $('#imessage-inbox').find('tbody').find('input[type="checkbox"]');
	        
	        if($this.prop('checked')) {
	            this.checkAll($checkboxes);
	        } else {
	            this.uncheckAll($checkboxes);
	        }
	    }, this));
	    
	    
	    $('#imessage-inbox').on('change', 'tbody input[type="checkbox"]', $.proxy(function(e) {
	        var $this = $(e.currentTarget),
	            $checkAll = $('#imessage-inbox').find('thead').find('input[type="checkbox"][name="selectAll"]');
	        
	        if(!$this.prop('checked') && $checkAll.prop('checked')) {
	            $checkAll.prop('checked', false);
	        }
	    }, this));
	    
	    
	    $('#imessage-inbox').on('change', 'select[name="doWithSelected"]', $.proxy(function(e) {
	        var $this = $(e.currentTarget),
	            val = $this.val(),
	            $checked = $('#imessage-inbox').find('tbody').find('input[type="checkbox"]:checked');
	        
	        if(val.toLowerCase() === 'markasread' && $checked.length > 0) {
	            this.markAsRead($checked);
	        } else if(val.toLowerCase() === 'delete' && $checked.length > 0) {
	            this.deleteMessage($checked);
	        }
	    }, this));
	    
	    
	    $('#imessage-inbox').on('click', 'thead th.sortable', $.proxy(function(e) {
	        var $el = $(e.currentTarget),
	            direction = $el.data('sort-direction') || 'asc';
	        
	        switch($el.data('sort-by')) {
	            case 'date':
	                this.sortByDate($el, direction);
	                
	                break;
	        }
	    }, this));
	    
	    
	    $('#imessage-inbox').on('click', 'tbody tr', $.proxy(function(e) {
	        if(e.target.nodeName.toLowerCase() === 'td') {
	        	location.href = $(e.currentTarget).data('url');
	        }
	    }, this));
	    
	    
	    $('#imessage-inbox').on('click', 'button[data-action="markAsRead"]', $.proxy(function(e) {
	        this.markAsRead($(e.target));
	    }, this));
	    
	    $('#imessage-inbox').on('click', 'button[data-action="delete"]', $.proxy(function(e) {
	        this.deleteMessage($(e.target));
	    }, this));
	    
	    
	    $('#imessage-inbox').on('keyup', '#filter_inbox', $.proxy(function(e) {
	        this.filter(e);
	    }, this));
	    
	    
	    $('#imessage-inbox').on('click', '.inbox-clear-filter', $.proxy(function(e) {
	        this.resetInboxFilters();
	    }, this));
	}
};


ItyouInbox.prototype.sortByDate = function($el, direction) {
    var timestamps = [];
        
    $('#imessage-inbox').find('tbody td[data-unix]').each($.proxy(function(k, el) {
        timestamps.push($(el).data('unix'));
    }, this));
    
    if(undefined !== $el) {
        if(direction === 'asc') {
            $el.data('sort-direction', 'desc').removeClass('sort-desc').addClass('sort-asc');
        } else {
            $el.data('sort-direction', 'asc').removeClass('sort-asc').addClass('sort-desc');
        }
    } else {
        direction = 'desc';
    }

    timestamps = this.sortNumeric(timestamps, direction);

    var rows = [];

    $.each(timestamps, $.proxy(function(k, v) {
        var $row = $('#imessage-inbox').find('tbody td[data-unix="' + v + '"]').parents('tr');
        
        rows.push($row);
    }, this));

    this.tableSort($('#imessage-inbox').find('tbody'), rows);
};


ItyouInbox.prototype.loadMoreEvent = function() {
    var $tr = $('#imessage-inbox').find('tfoot .load-more-messages').parents('tr');
    $tr.removeClass('hidden');

    $('#imessage-inbox').one('click', 'tfoot .load-more-messages', $.proxy(function(e) {
        var offset = $('#imessage-inbox').find('table').find('tbody').children().length;
        
        this.getMessages(offset);
        
        $tr.addClass('hidden');
    }, this));

    $(window).one('scroll', $.proxy(function(e) {
        var loadMore = $('#imessage-inbox').find('tfoot .load-more-messages');
        
        var st = $(e.currentTarget).scrollTop();
    
        if(loadMore.is(':in-viewport') && loadMore.is(':visible') && st > this.lastScrollTop) {
            var offset = $('#imessage-inbox').find('table').find('tbody').children().length;
            
            this.getMessages(offset);
            
            $tr.addClass('hidden');
        } else {
            this.loadMoreEvent();
        }
        
        this.lastScrollTop = st;
    }, this));
};


ItyouInbox.prototype.checkboxStatus = function(els, status) {
    els.each($.proxy(function(k, el) {
        $(el).prop('checked', status);
    }, this));
};


ItyouInbox.prototype.checkAll = function(els) {
    this.checkboxStatus(els, true);
};


ItyouInbox.prototype.uncheckAll = function(els) {
    this.checkboxStatus(els, false);
};


ItyouInbox.prototype.markAsRead = function(el) {
    this.changeMessageStatus(el, 'message_read_by_receiver');
};


ItyouInbox.prototype.deleteMessage = function(el) {
    this.changeMessageStatus(el, 'message_hidden_by_receiver');
};


ItyouInbox.prototype.changeMessageStatus = function(el, state) {
    var hash = new Array();
    
    if(el.length > 1) {
        el.each($.proxy(function(k, elem) {
            hash.push($(elem).parents('tr').data('hash'));
        }, this));
    } else {
        hash.push(el.parents('tr').data('hash'));
    }
    
    $.getJSON('@@ajax-messages', {action: state, mids: JSON.stringify(hash)}, function() {
    	StatusFlags.prototype.imessageNotify.getNotify();
    });
    
    if(state === 'message_read_by_receiver') {
        this.renderReadMessages(hash);
    } else {
        this.renderDeletedMessages(hash);
    }
};


ItyouInbox.prototype.renderReadMessages = function(hash) {
    $.each(hash, $.proxy(function(k, val) {
        $('tr[data-hash="' + val + '"]').removeClass('unread')
                .find('button[data-action="markAsRead"]').remove();
    }, this));
};


ItyouInbox.prototype.renderDeletedMessages = function(hash) {
    $.each(hash, $.proxy(function(k, val) {
        var $el = $('tr[data-hash="' + val + '"]');
        
        $el.fadeOut(500, function() {
            $el.remove();
        });
    }, this));
};


ItyouInbox.prototype.inboxStream = function() {
	if(null === this.getLatestTimestamp() || undefined == this.getLatestTimestamp()) {
		var els = $('#imessage-inbox').find('tr[data-tiemstamp'),
			timestamps = new Array();
		
		$.each(els, $.proxy(function(k, el) {
			timestamps.push([$(el).data('hash'), $.trim($(el).find('td[data-unix]').data('unix'))]);
		}, this));
		
		timestamps = this.sortNumericArray(timestamps, 'desc');
        
        if(timestamps.length > 0) {
            var latestTimestamp = $('tr[data-hash="' + timestamps[0][0] + '"]').data('timestamp');
            
            this.setLatestTimestamp(latestTimestamp);
        }
	}
	
	this.getLatestMessages();
};


ItyouInbox.prototype.stopInboxStream = function() {
    if(this.runningStream) {
        this.runningStream = clearInterval(this.runningStream);
        this.setLatestTimestamp(null);
    }
};


ItyouInbox.prototype.setLatestTimestamp = function(timestamp) {
	if(this.isInbox()) {
		this.storage.local.set('imessageInboxTimestamp', timestamp);
		this.latestTimestamp = timestamp;
	} else if(this.isDialogOverview()) {
		this.storage.local.set('imessageDialogOverviewTimestamp', timestamp);
		this.latestTimestamp = timestamp;
	}
    
    return this;
};


ItyouInbox.prototype.getLatestTimestamp = function() {
    return this.latestTimestamp || (this.isInbox() ? this.storage.local.get('imessageInboxTimestamp') : this.storage.local.get('imessageDialogOverviewTimestamp'));
};

/*
ItyouInbox.prototype.showSpinner = function() {
    $('#imessage-inbox-spinner').show();
};

ItyouInbox.prototype.hideSpinner = function() {
    $('#imessage-inbox-spinner').hide();
};
*/


ItyouInbox.prototype.filter = function(keyEvent) {
    var $target = $(keyEvent.currentTarget);
    
    this.clearFiltering(true);

    if(undefined === this.keyupDelay || false === this.keyupDelay) {
        this.keyupDelay = setTimeout($.proxy(function() {
            var val = $target.val();
            
            if(val.length > this.minValue && val !== this.cachedVal) {
                this.cachedVal = val;
                
                this.stopInboxStream();
                this.clearFiltering();
                
                $(this.messageList).empty();;
                this.showSpinner();
                
                this.searchUser(val);
                this.timerCallback('filteredUsers', 'fetchFromDialog');
                
                this.keyupDelay = clearTimeout(this.keyupDelay);
            }
        }, this), 500);
    } else {
        this.keyupDelay = clearTimeout(this.keyupDelay);
    }
};


ItyouInbox.prototype.timerCallback = function(property, callback) {
    var timer = setInterval($.proxy(function() {
        if(undefined !== this[property]) {
            clearInterval(timer);

            var funcValue = this[callback]();
            
            if(undefined !== funcValue) {
                this.returnValue = funcValue;
            }
        }
    }, this), 100);
};


ItyouInbox.prototype.fetchFromDialog = function() {
    this.fetchMessages(this.filteredUsers);
    this.timerCallback('filteredMessages', 'sortMessages');
    
    var timer = setInterval($.proxy(function() {
        if(undefined !== this.returnValue) {
            clearInterval(timer);
            
            $(this.messageList).empty();
        
            if(this.returnValue.length > 0) {
                this.renderMessages(this.returnValue, 'append');
            } else {
                $($('#inbox-filter-nomatch-tmpl').render()).appendTo(this.messageList);
            }
            
            this.hideSpinner();
        }
    }, this), 100);
};


ItyouInbox.prototype.sortMessages = function() {
    var tmp = new Array();

    if(this.filteredMessages.length > 0) {
        // breaking outer arrays
        $.each(this.filteredMessages, $.proxy(function(k, value) {
            $.each(value, $.proxy(function(i, innerValue) {
                innerValue.unixTimestamp = this.convertToUNIXTimestamp(innerValue.timestamp);
                
                tmp.push(innerValue);
            }, this));
        }, this));
        
        // sorting
        return this.sortReverse(tmp, 'unixTimestamp');
    }
    
    return tmp;
};


ItyouInbox.prototype.searchUser = function(value) {
    var userList = new Array();

    $.getJSON('@@ajax-users', {action: 'query', q: value, l: 5}, $.proxy(function(response) {
        $.each(response, $.proxy(function(k, val) {
            userList.push(val.id);
        }, this));
        
        this.filteredUsers = userList;
    }, this));
};


ItyouInbox.prototype.fetchMessages = function(userlist, offset, messages) {
    if(undefined === messages) {
        messages = new Array();
    }
    
    if(undefined === offset) {
        offset = 0;
    }
    
    if(userlist.length === 0) {
        this.filteredMessages = messages;
        return ;
    }
    
    $.getJSON('@@ajax-messages', {action: 'get_messages', sender_id: userlist[0], approved: 'all', max: this.filterMax, offset: offset}, $.proxy(function(resp) {
        if(resp.length > 0 && resp[0].sender_id !== this.user_id) {
        	$.each(resp, $.proxy(function(i, val) {
            	// need to change response[i][timestr]
            	resp[i]['timestr'] = this.TimeConverter.convertTime(val.timestamp);
            }, this));
        	
            messages.push(resp);
        }
    
        return this.fetchMessages(userlist.slice(1, userlist.length), offset, messages);
    }, this));
};


ItyouInbox.prototype.sortReverse = function(data, property) {
    var tmp = data.sort(function(a, b) {
        a = a[property];
        b = b[property];
    
        return a-b;
    });
    
    tmp.reverse();
    
    return tmp;
};


ItyouInbox.prototype.clearFiltering = function(userlist) {
    this.filteredMessages = undefined;
    this.returnValue = undefined;
    
    if(undefined !== userlist) {
        this.filteredUsers = undefined;
    }
};


ItyouInbox.prototype.resetInboxFilters = function() {
    this.clearFiltering(true);
    
    $(this.messageList).empty();
    $('#filter_inbox').val('').blur();
    
    this.getMessages(0);
    this.inboxStream();
};








/**
 * Example Output:
 * [Array[3], Array[2]]
 *  0: Array[3]
 *    0: "lmeise"
 *    1: "Lisa Meise"
 *    2: "Li Mei"
 *  1: Array[2]
 *    0: "hmustermann"
 *    1: "Hans Mustermann"
 */
ItyouInbox.prototype.getAllSenderNames = function() {
    var uid = new Array(),
        sender = new Array();

    $('#imessage-inbox').find('td[data-uid]').each($.proxy(function(k, el) {
        var currentUid = $(el).data('uid'),
            currentName = $.trim($(el).text());

        if($.inArray(currentUid, uid) === -1) {
            uid.push(currentUid);
            sender.push([currentUid, currentName]);
        } else {
            $.each(sender, function(i, val) {
                if(currentUid === val[0] && $.inArray(currentName, val) === -1) {
                    val.push(currentName);
                }
            });
        }
    }, this));
    
    return sender;
};







