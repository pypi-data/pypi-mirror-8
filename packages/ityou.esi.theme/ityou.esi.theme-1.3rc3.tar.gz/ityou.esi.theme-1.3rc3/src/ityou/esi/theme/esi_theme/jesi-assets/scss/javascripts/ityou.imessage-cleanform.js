//
// IMessageCleanNewMessage
// -----------------------------------------------------------------------------


function IMessageCleanNewMessage(settings) {

    // brain
    this.cache = {
        // own userid
        userId: undefined,
        
        // handle view
        currentView: undefined,
        partnerId: undefined,
        
        // search
        input_value: undefined,
        currentSelectedElement: undefined,
        receiverList: [],
        receiverGroupList: []
    };
    
    // animations
    this.animation = {
        speedDown: 400,
        speedUp: 200,
        removeHighlight: 1500
    };
    
    // selectors
    this.selector = {
        editor: '#message-textarea',
        editorControls: '.message-controls',
        // search
        form: '#message_receiver',
        ids: '#w_user_id',
        input: '#w_user_name',
        resultList: '.usersearch ul.users',
        receiverList: '#receiver_list ul',
        group: '.group-creation',
        groupName: '#group-name',
        // translation
        noMatch: '#imessage_no_match_found',
        // creation mode
        creation: '#create-dialog-as-groupchat',
        modal: '#imessage-message-successfully-sent'
    };
    
    // templates
    this.template = {
        search: '#imessage-usersearch-template',
        list: '#imessage-receiverlist-template'
    };
    
    // settings
    this.settings = {
        max: 10,
        minLength: 1,
        minContentLength: 2,
        minGroupnameLength: 3,
        waiting: 500,
        useGroups: false,
        useWYSIWYG: false
    };
    
    if(settings) {
    	this.settings = $.extend(this.settings, settings);
    }
    
    
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
    
    
    // initialize imessage clean new
    //this.init();
    
};



// extends Utilities
IMessageCleanNewMessage.prototype = new Utilities();

IMessageCleanNewMessage.prototype.Clipboard = new Clipboard();



/**
 * initialise clean new message
 *
 * return void
 */
IMessageCleanNewMessage.prototype.init = function(settings) {
    this.setCache('userId', $('#ESI_DATA').data('ityou-uid'));
    this.setSettings(settings);
    
    // define in which template we are
    this.defineView();
    
    // initialise
    if(this.isCleanNewMessage()) {
        this.initEventHandler();
        
        if(parseInt($(this.getOption('form', 'selector')).data('use-groups')) === 1) {
        	this.setOption('useGroups', true, 'settings');
        }
        
        if(this.getOption('useWYSIWYG', 'settings') === true) {
        	this.initTinyMCE();
        } else {
        	$(this.getOption('editor', 'selector')).autoGrow();
        	
        	this.Clipboard.addPasteControls();
        }
        
        if(this.getOption('useGroups', 'settings') === true) {
        	this.groups();
        }        
    }
};


/**
 * define which page is currently viewed
 *
 * @return void
 */
IMessageCleanNewMessage.prototype.defineView = function() {
    var pathname = document.location.pathname,
        matchAgainst = /@@messages/i,
        pathsearch = document.location.search;
    
    if(matchAgainst.exec(pathname) && pathsearch.length === 0) {
        this.setCache('currentView', 'clean_message');
    
        return ;
    }
    
    this.setCache('currentView', undefined);
    this.setCache('partnerId', undefined);
};


/**
 * simple helper to ask if we can build a dialog
 *
 * @return boolean
 */
IMessageCleanNewMessage.prototype.isCleanNewMessage = function() {
    if(this.getCache('currentView') === 'clean_message') {
        return true;
    }
    
    return false;
};


/**
 * 
 */
IMessageCleanNewMessage.prototype.groups = function() {
	$.ajax({
		url: '@@ajax-users',
		data: {
			action: 'groups'
		},
		dataType: 'json',
		// event handler success
		success: $.proxy(function(response) {
			// MR: solange keine bilder fuer gruppen existieren
			$.each(response, $.proxy(function(i, v) {
				response[i]['portrait'] = '/++resource++ityou.esi.theme.img/group_icon.png';
			}, this));
			
			this.storage.session.set('user_groups', response);
		}, this),
		// event handler success
		error: $.proxy(function(XMLHttpRequest, textStatus, errorThrown) {
            this.log(XMLHttpRequest, textStatus, errorThrown);
		}, this)
	});
};


/**
 *
 */
IMessageCleanNewMessage.prototype.search = function(value) {
    var $wrapper = $(this.getOption('form', 'selector')).find('.input_holder').find('.usersearch');
    
    $.ajax({
        url: '@@ajax-users',
        data: {
            action: 'query',
            q: value,
            l: this.getOption('max', 'settings')
        },
        dataType: 'json',
        // event handler success
        success: $.proxy(function(response) {
            var $resultList = $(this.getOption('resultList', 'selector'));
            
            if(response.length == 0 && $('#group-creation').length == 0) {
            	this.emptyResultList();
            	
            	setTimeout($.proxy(function() {
            		this.noMatch();
            	}, this), 1);
            	
            	$wrapper.fadeIn('fast');
            } else {
            	var list;
            	
            	if($('#group-creation').length > 0) {
            		list = [].concat(this.getCache('receiverList')).concat(this.getCache('receiverGroupList'));
            	} else {
            		list = [].concat(this.getCache('receiverList'));
            	}
            	list.push(this.getCache('userId'));
                
                // add groups if activated
                if(this.getOption('useGroups', 'settings') === true && $('#group-creation').length > 0) {
                	response = this.filterGroups(value).concat(response);
                }
                
                // filter myself and duplicates of the response 
                response = this.filter(response, list);
                
                if(!$(this.getOption('input', 'selector')).is(':focus')) {
                    $wrapper.hide();
                } else {
                    $wrapper.fadeIn('fast');
                }
                
                if(response.length > 0) {
                    this.emptyResultList();
                    $resultList.show().append($(this.getOption('search', 'template')).render(response));
                } else {
                    this.emptyResultList();
                    this.noMatch();
                    $wrapper.fadeIn('fast');
                }
            }
        }, this)
    });
};


/**
 * 
 */
IMessageCleanNewMessage.prototype.filterGroups = function(searchStr) {
	var groups = this.storage.session.get('user_groups'),
		output = [];
	
	if(searchStr === '@') {
		$.each(groups, $.proxy(function(key, value) {
			value.group = true;
			output.push(value);
		}, this));
	} else {	
		$.each(groups, $.proxy(function(key, value) {
			// value.name
			var regexp = new RegExp(searchStr, 'i');
	
			// found
			if(value.name.search(regexp) > -1) {
				value.group = true;
				
				output.push(value);
			}
		}, this));
	}
	
	return output;
};


/**
 *
 */
IMessageCleanNewMessage.prototype.filter = function(data, list) {
    if(data.length === 0 || list.length === 0) {
        return data;
    }
    
    if(!data) {
        this.log('ERROR IN FILTER');
    }
    
    var tmpList = [],
        found = -1;
        
    $.each(data, $.proxy(function(index, tmp) {
        $.each(list, $.proxy(function(key, value) {
        	if(tmp.id === value) {
                // remove if found
                list.splice(key, 1);
                data.splice(index, 1);
                
                // call me again
                this.filter(data, list);
                
                // define found so we can break the outer each loop
                found = key;
                return false;
            }
        }, this));
        
        if(found > -1) {
            return false;
        }
    }, this));
    
    //console.log(data);
    
    return data;
};



/**
 *
 */
IMessageCleanNewMessage.prototype.noMatch = function() {
    var no_match_found = $(this.getOption('noMatch', 'selector')).text(),
        $resultList = $(this.getOption('resultList', 'selector'));
        
    $resultList.append('<li class="text-center nomatch-found"><em>' + no_match_found + '</em></li>').show();
};


/**
 *
 */
IMessageCleanNewMessage.prototype.addToReceiverList = function(uid, portrait, name, group) {
	if(group) {
		var tmp = this.getCache('receiverGroupList');
		
		if($.inArray(uid, tmp) === -1) {
			tmp.push(uid);
			this.setCache('receiverGroupList', tmp);
			this.renderReceiverList({id: uid, portrait_url: portrait, group: true, name: name});
		}
	} else {
	    var tmp = this.getCache('receiverList');
	
	    if($.inArray(uid, tmp) === -1) {
	        tmp.push(uid);
	        this.setCache('receiverList', tmp);
	        this.renderReceiverList({id: uid, portrait_url: portrait, name: name, portal_url: $('#ESI_DATA').data('ityouPortalUrl')});
	    }
	}
	
	this.hideResultList();
	    
    this.setCache('currentSelectedElement', undefined);
    
    // show option to create a groupchat
    if(this.getCache('receiverGroupList').length > 0 || this.getCache('receiverList').length > 1) {
    	$(this.getOption('group', 'selector')).removeClass('hidden');
    }
};


/**
 *
 */
IMessageCleanNewMessage.prototype.removeFromReceiverList = function(uid, group) {
	if(group) {
		var tmp = [],
			current = this.getCache('receiverGroupList');
		
		$.each(current, $.proxy(function(index, value) {
			if(value !== uid) {
				tmp.push(value);
			}
		}, this));
		
		this.setCache('receiverGroupList', tmp);
	} else {
	    var tmp = [],
	        current = this.getCache('receiverList');
	    
	    $.each(current, $.proxy(function(index, value) {
	        if(value !== uid) {
	            tmp.push(value);
	        }
	    }, this));
	    
	    this.setCache('receiverList', tmp);
	}
	
	// hide option to create a groupchat
	if(this.getCache('receiverGroupList').length < 1 && this.getCache('receiverList').length < 2) {
		var groupCreation = $(this.getOption('group', 'selector')); 
    	
		groupCreation.addClass('hidden');
		groupCreation.find(this.getOption('groupName', 'selector')).val('');
		groupCreation.find(this.getOption('creation', 'selector')).prop('checked', false).trigger('change');
    }
};


/**
 *
 */
IMessageCleanNewMessage.prototype.renderReceiverList = function(data) {
    $(this.getOption('receiverList', 'selector')).append($(this.getOption('list', 'template')).render(data));
};



/**
 *
 */
IMessageCleanNewMessage.prototype.toggleHighlight = function(element, state) {
    if(state === true) {
        element.addClass('hover');
    } else {
        element.removeClass('hover');
    }
};


/**
 *
 */
IMessageCleanNewMessage.prototype.hideResultList = function() {
    $(this.getOption('resultList', 'selector')).hide();
    
    $(this.getOption('input', 'selector')).val('');
};


/**
 *
 */
IMessageCleanNewMessage.prototype.emptyResultList = function() {
    $(this.getOption('resultList', 'selector')).empty();
};



/**
 *
 */
IMessageCleanNewMessage.prototype.initTinyMCE = function() {
    $(this.getOption('editor', 'selector')).tinymce({
        script_url: 'tiny_mce_gzip.js',
        content_css: 'portal_tinymce/@@tinymce-getstyle',
        
        theme: 'advanced',
        skin: 'plone',
        
        plugins: 'paste',
        
        theme_advanced_buttons1: 'bold,italic,underline,separator,justifycenter,justifyright,justifyfull,separator,bullist,numlist',
        theme_advanced_buttons2: 'code',
        theme_advanced_buttons3: '',
        theme_advanced_toolbar_location: 'top',
        
        oninit: function(e) {},
        
        paste_preprocess: $.proxy(function(pl, o) {
            //o.content = this.stripTags(o.content, '<b><u><i><em><p><strong><small><ul><ul><li><a><img>');
            o.content = this.stripTags(o.content, '<img><strong><em><span><ul><ol><li><a><p>');
        }, this)
    });
};







//
// Event Handler Functions below
// -----------------------------------------------------------------------------

/**
 *
 */
IMessageCleanNewMessage.prototype.initEventHandler = function() {

    var $input = $(this.getOption('input', 'selector')),
        keyDelay = this.getOption('waiting', 'settings');
    
    
    // handle key events on input
    $(document).on({
    
        keyup: $.proxy(function(e) {
            var key = e.which;
            
            // 38 = uparrow
            // 40 = downarrow
            if(key === 38 || key === 40) {
                return ;
            }
            
            this.setCache('currentSelectedElement', undefined);
            
            if(this.getCache('key_timer')) {
                clearTimeout(this.getCache('key_timer'));
            }
            
            var t = setTimeout($.proxy(function() {
                if($input.val().length >= this.getOption('minLength', 'settings')) {
                    this.setCache('input_value', $input.val());
                    this.search($input.val());
                } else {
                    this.hideResultList();
                }
            }, this), keyDelay);
            
            this.setCache('key_timer', t);
        }, this),
        
        keydown: $.proxy(function(e) {
            var key = e.which,
                $resultList = $(this.getOption('resultList', 'selector'));
            
            //  9 = tab
            // 13 = enter
            // 27 = esc
            // 38 = uparrow
            // 40 = downarrow
            switch(key) {
            
                case 13: // adding first search result
                    if($resultList.find('li').length > 0 && $input.val().length >= this.getOption('minLength', 'settings') && !$resultList.find('li').first().hasClass('nomatch-found')) {
                        if(this.getCache('currentSelectedElement')) {
                            this.getCache('currentSelectedElement').trigger('click');
                        } else {
                            $resultList.find('li').first().trigger('click');
                        }
                    }
                    
                    break;
                    
                case 27: // cancel user search
                    this.hideResultList();
                    
                    break;
                    
                case 38:
                case 40: // navigate
                    if($resultList.find('li').length > 0) {
                        var $currentElement = this.getCache('currentSelectedElement');
                        
                        if(!$currentElement) {
                            this.setCache('currentSelectedElement', $resultList.find('li').first());
                            
                            this.toggleHighlight(this.getCache('currentSelectedElement'), true);
                        } else {
                            if(key === 38) { // navigate up
                                if($currentElement.prev().length > 0) {
                                    this.toggleHighlight($currentElement, false);
                                    this.setCache('currentSelectedElement', $currentElement.prev());
                                    this.toggleHighlight(this.getCache('currentSelectedElement'), true);
                                }
                            } else { // navigate down
                                if($currentElement.next().length > 0) {
                                    this.toggleHighlight($currentElement, false);
                                    this.setCache('currentSelectedElement', $currentElement.next());
                                    this.toggleHighlight(this.getCache('currentSelectedElement'), true);
                                }
                            }
                        }
                    }
                    
                    break;
            }
        }, this),
        
        blur: $.proxy(function(e) {
        
        }, this),
        
        focus: $.proxy(function(e) {
            $input.trigger('keyup');
        }, this)
    
    }, this.getOption('input', 'selector'));
    
    
    // prevent form submit
    $(this.getOption('form', 'selector')).on('submit', $.proxy(function(e) {
        e.preventDefault();
        
        return false; // IE
    }, this));
    
    
    // handle click events on document
    $(document).on('click', $.proxy(function(e) {
        var $target = $(e.target); //console.log($target);
        
        if($target.parents('.usersearch').length > 0) {
            var $li = $target[0].nodeName.toLowerCase() === 'li' ? $target : ($target.parents('li').length > 0 ? $target.parents('li') : false);

            if($li && !$li.hasClass('nomatch-found')) {
                var userid = $li.find('a').attr('title'),
                    img = $li.find('img').attr('src'),
                    name = $li.find('h2').text(),
                    isGroup = $li.find('a').data('group') ? true : false;
                
                if(isGroup) {
                	this.addToReceiverList(userid, img, name, true);
                } else {
                	this.addToReceiverList(userid, img, name);
                }
                
                $li.remove();
                
                if($('.usersearch').find('li').length === 0) {
                    this.hideResultList();
                }
            }
        } else if($target.attr('id') === $input.attr('id')) {
            ; // nothing to do here
        } else if($target.hasClass('remove') && $target.parents('#receiver_list').length > 0) {
        	var containerId = $target.parents('.thumbnail').attr('id'),
        		uid = containerId.split('-')[1],
        		isGroup = $('[data-group="' + uid + '"]').data('group') ? true : false,
				$li = isGroup ? $('[data-group="' + uid + '"]').parents('li') : $('#' + containerId).parents('li');
				
			if(isGroup) {
				this.removeFromReceiverList(uid, true);
			} else {
				this.removeFromReceiverList(uid);
			}
			
			$li.fadeOut(200, function() {
				$li.remove();
			});
        } else if($target.hasClass('fa fa-times') && $target.parents('.remove').length > 0 && $target.parents('#receiver_list').length > 0) {
            var containerId = $target.parents('.user').attr('id'),
                uid = containerId.split('-')[1],
                isGroup = $('[data-group="' + uid + '"]').data('group') ? true : false,
                $li = isGroup ? $('[data-group="' + uid + '"]').parents('li') : $('#' + containerId).parents('li');
            
            if(isGroup) {
            	this.removeFromReceiverList(uid, true);
            } else {
            	this.removeFromReceiverList(uid);
            }
            
            $li.fadeOut(200, function() {
                $li.remove();
            });
        } else if($target.parents(this.getOption('modal', 'selector')).length > 0) {
        	//document.location.reload();
        	document.location.href = '/@@dialog-overview';
        	console.log('hier')
        } else {
            this.hideResultList();
        }
        
        
        // save message
        
//        if($target.hasClass('message-save-button')) {
//        	if(this.getOption('useWYSIWYG', 'settings') === true) {
//	            if($(this.getOption('editor', 'selector')).tinymce().getContent().length >= this.getOption('minContentLength', 'settings') && (this.getCache('receiverList').length > 0 || this.getCache('receiverGroupList').length > 0)) {
//	                $('.mceIframeContainer').removeClass('has-error');
	            
//	                this.save($target);
//	            } else if($(this.getOption('editor', 'selector')).tinymce().getContent.length < this.getOption('minContentLength', 'settings')) {
//	                $('.mceIframeContainer').addClass('has-error');
//	            }
//        	} else {

/* #LM 2014-04-16 */
//        			$(this.getOption('editor', 'selector')).removeClass('has-error');      			
//        			this.save($target);
/* #LM 2014-04-16
//        		if($(this.getOption('editor', 'selector')).length >= this.getOption('minContentLength', 'settings') && (this.getCache('receiverList').length > 0 || this.getCache('receiverGroupList').length > 0)) {
//        			$(this.getOption('editor', 'selector')).removeClass('has-error');      			
//        			this.save($target);
//        		} else {
//        			$(this.getOption('editor', 'selector')).addClass('has-error');
//        		}
*/
//        	}
//        }
        
    }, this));
    
    
    // toggle group chat
    var $checkbox = $(this.getOption('creation', 'selector')),
        $groupName = $(this.getOption('group', 'selector')).find('.form-group');
    $checkbox.on('change', $.proxy(function(e) {
        if($checkbox.prop('checked')) {
            $groupName.removeClass('hidden');
        } else {
            $groupName.addClass('hidden');
        }
    }, this));
    
    
    $('#message-stream').on('click', 'button.message-save-button', $.proxy(function(e) {
    	var $target = $(e.currentTarget);
    	
    	if(this.getOption('useWYSIWYG', 'settings') === true) {
			if($(this.getOption('editor', 'selector')).tinymce().getContent().length >= this.getOption('minContentLength', 'settings') && (this.getCache('receiverList').length > 0 || this.getCache('receiverGroupList').length > 0)) {
				$('.mceIframeContainer').removeClass('has-error');
				this.save($target);
			} else if($(this.getOption('editor', 'selector')).tinymce().getContent.length < this.getOption('minContentLength', 'settings')) {
				$('.mceIframeContainer').addClass('has-error');
			}
    	} else {
    		/* #LM 2014-04-16 */
			$(this.getOption('editor', 'selector')).removeClass('has-error');      			
			this.save($target);
			/*
			 * #LM 2014-04-16
			
			if($(this.getOption('editor', 'selector')).length >= this.getOption('minContentLength', 'settings') && (this.getCache('receiverList').length > 0 || this.getCache('receiverGroupList').length > 0)) {
				$(this.getOption('editor', 'selector')).removeClass('has-error');      			
				this.save($target);
			} else {
				$(this.getOption('editor', 'selector')).addClass('has-error');
			}
			
			*/
    	}
    }, this));
};



/**
 *
 */
IMessageCleanNewMessage.prototype.save = function($el) {
    var tinymce = this.getOption('editor', 'selector');
    
    var buttonText = $el.text(),
        buttonLoader = '<i class="fa fa-spinner fa-spin"></i>';
        
    var receiver = this.getCache('receiverList'),
        groupReceiver = this.getCache('receiverGroupList');
        
    if(!$el.prop('disabled')) {
    	var content = '';
    	
    	if(this.getOption('useWYSIWYG', 'settings') === true) {
    		content = $(tinymce).tinymce().getContent();
    	} else {
    		content = $(tinymce).val();
    	}
    	
        //var content = $(tinymce).tinymce().getContent(),
        var groupName = $(this.getOption('group', 'selector')).find(this.getOption('groupName', 'selector')).val();
        
        if(content.length <= this.getOption('minContentLength', 'settings') || ($(this.getOption('creation', 'selector')).prop('checked') && groupName.length <= this.getOption('minGroupnameLength', 'settings'))) {
            return ;
        }
        
        $el.prop('disabled', true);
        $el.html(buttonLoader);
        
        var buttonData = {
            button: $el,
            text: buttonText
        };

        if($(this.getOption('creation', 'selector')).prop('checked') === true) {
            this.saveMessage('group', content, buttonData); // save as group chat --> redirection
        } else {
            if(receiver.length === 1) {
                this.saveMessage('single', content, buttonData); // single messages && one receiver --> redirection to dialog
            } else if(receiver.length > 1 || groupReceiver.length >= 1) {
                this.saveMessage('multi', content, buttonData); // single message multiple receiver --> modal dialog
            }
        }
    }
};


/**
 *
 */
IMessageCleanNewMessage.prototype.saveMessage = function(state, msg, button) {
    // state = single | multi | group
    
    var $modal = $(this.getOption('modal', 'selector'));
    
    var baseData = {
        action: 'post_message',
        dataType: 'json',
        message: msg
    };
    
    var data,
        userReceiver = this.getCache('receiverList'),
        groupReceiver = this.getCache('receiverGroupList');
        
    var action = 'post_message';
    
    if(state === 'single') { // single messages && one receiver
        data = $.extend({
            receiver_id: userReceiver[0]
        }, baseData);
    } else if(state === 'multi') { // single messages && multiple receiver/group as receiver
    
        if(groupReceiver.length === 0) { // only users, no group
            data = $.extend({
                receiver_id: userReceiver.join(',')
            }, baseData);
        } else if(userReceiver.length === 0) { // only groups, no user
            data = $.extend({
                receiver_group_id: groupReceiver.join(',')
            }, baseData);
        } else if(userReceiver.length > 0 && groupReceiver.length > 0) { // both
            data = $.extend({
                receiver_id: userReceiver.join(','),
                receiver_group_id: groupReceiver.join(',')
            }, baseData);
        }
    
    } else if(state === 'group') { // group chat
        var groupName = $(this.getOption('group', 'selector')).find(this.getOption('groupName', 'selector')).val();
    
        if(groupReceiver.length === 0) { // only users, no group
            data = $.extend({
                receiver_id: userReceiver.join(','),
                new_group: groupName
            }, baseData);
        } else if(userReceiver.length === 0) { // no users, only groups
            data = $.extend({
                receiver_group_id: groupReceiver.join(','),
                new_group: groupName
            }, baseData);
        } else if(userReceiver.length > 0 && groupReceiver.length > 0) {
            data = $.extend({
                receiver_id: userReceiver.join(','),
                receiver_group_id: groupReceiver.join(','),
                new_group: groupName
            }, baseData);
        }
    }
    
    
    if(data) {
        $.ajax({
            url: '@@ajax-messages',
            data: data,
            dataType: 'json',
            // event handler success
            success: $.proxy(function(response) {
                if(state === 'single') {
                    document.location.href = '/@@messages?sid=' + response.receiver_id;
                } else if(state === 'multi') {
                    $modal.modal();
                } else if(state === 'group') {
                    document.location.href = '/@@messages?rid=' + response.receiver_id;
                }
            }, this),
            // event handler error
            error: $.proxy(function(XMLHttpRequest, textStatus, errorThrown) {
                this.saveError(button, XMLHttpRequest, textStatus, errorThrown);
            }, this)
        });
    } else {
        this.saveError(button);
    }
        
};



/**
 *
 */
IMessageCleanNewMessage.prototype.saveError = function(button, xml, status, error) {
    alert('Send message failed, please try again');
    
    button.button.removeProp('disabled');
    button.button.text(button.text);
};

