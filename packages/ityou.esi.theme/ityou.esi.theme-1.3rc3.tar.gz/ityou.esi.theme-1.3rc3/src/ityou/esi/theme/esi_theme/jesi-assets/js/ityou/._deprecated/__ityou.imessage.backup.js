(function($, window, document, _, undefined) {

    'use strict';

    _.libs.imessage = {
        name: 'ityou.imessage',
        
        version: '0.5',
        
        cache: {
            registered: false,
            notifyStream: null,
            dialogStream: null,
            selfId: null,
            messagePartnerId: null,
            
            receiverList: [],
            
            currentSelectedElement: null
        },
        
        settings: {
            animation: {
                speedDown: 400,
                speedUp: 200,
                removeHighlight: 1500
            },
            
            selector: {
                userForm: 'form#message_receiver',
                userFormIds: 'input#w_user_id',
                userFormInput: 'input#w_user_name',
                dialogContainer: '#message-stream ul.latest-messages',
                resultList: '.usersearch ul.users',
                receiverList: '#receiver_list ul',
                tinyMCE: '#message-textarea',
                notifyMessages: '.message-notify-list'
            },
            
            translation: {
                noMatch: '#imessage_no_match_found'
            },
            
            template: {
                dialogMessage: '#imessage-dialog-template',
                userSearch: '#imessage-usersearch-template',
                receiverList: '#imessage-receiverlist-template',
                notifyMessages: '#imessage-notify-template'
            },
            
            stream: {
                delay: {
                    notify: 30000,
                    dialog: 10000
                },
                max: 20
            },
            
            keyTimeout: 500,
            minInputLength: 1,
            debug: false
        },
        
        /**
         * Update a dialog
         *
         * @param object obj JSON Object
         */
        updateDialog: function(obj) {
            var _this = this,
                latestTimestamp = $(this.settings.selector.dialogContainer).find('li').last().find('span.timestamp').attr('id'),
                latestHash = $(this.settings.selector.dialogContainer).find('li').last().attr('id');
                
            console.log(latestHash);
            console.log(obj);
                
            if(undefined !== obj) {
                obj = _.helper.correctJsonURL(obj);
            
                if(obj.hash === latestHash) {
                    //$('#' + latestHash).remove();
                    $('#' + latestHash).find('.message').append(obj.message);
                    
                    return ;
                }
                
                obj.sent = true;
                
                $(this.settings.selector.dialogContainer).append(
                    $(_this.settings.template.dialogMessage).render(obj)
                );
            } else {
                $.getJSON(_.settings.ajax.remote + '@@ajax-messages' + _.settings.ajax.callback, {action: 'get_messages', sender_id: this.cache.messagePartnerId, timestamp: latestTimestamp, newer: true}, function(response) {
                    
                });
            }
        },
        
        /**
         *
         * @param string timestamp
         */
        getPreviousMessages: function(timestamp) {
            var _this = this;
        
            $.getJSON(_.settings.ajax.remote + '@@ajax-messages' + _.settings.ajax.callback, {action: 'get_dialog', sender_id: this.message_partner_id, timestamp: timestamp}, function(response) {
                if(response.length > 0) {
                    response = _.helper.correctJsonURL(response);
                    
                    // render
                    _this.render(response, false);
                }
            });
        },
        
        /**
         * @param object data JSON Object
         */
        render: function(data, append) {
            var _this = this;
            
            if(undefined === _this.cache.self) {
                _this.cache.self = $('#ESI_DATA').data('ityou-uid');
            }
            
            if(undefined === append) {
                append = true;
            }
        
            $.each(data, function(key, value) {
                var rendered;
                
                // value.hash
                if($('#' + value.hash).length > 0 && $('#' + value.hash).is(':last-child') === false) {
                    $('#' + value.hash).remove();
                } else if($('#' + value.hash).length > 0 && $('#' + value.hash).is(':last-child')) {
                    $('#' + value.hash).find('.message').html(value.message);
                
                    return ;
                }
                
                value.sent = _this.cache.self === value.sender_id;
                
                rendered = $($(_this.settings.template.dialogMessage).render(value));
                
                if(append === true) {
                    rendered
                        .appendTo(_this.settings.selector.dialogContainer)
                        .hide();
                } else {
                    rendered
                        .prependTo(_this.settings.selector.dialogContainer)
                        .hide();
                }

                rendered.slideDown(_this.settings.animation.speedDown);
            });
            
            if(data.length > 0 && append === true) {
                setTimeout(function() {
                    $('html, body').animate({scrollTop: $(document).height() + 'px'}, 1500);
                }, 1);
            }
        },
        
        /**
         * @param string value
         */
        searchUser: function(value) {
            var _this = this;
            
            var resultListWrapper = $(_this.settings.selector.userForm).find('.input_holder').find('.usersearch');
        
            $.getJSON(_.settings.ajax.remote + '@@ajax-users' + _.settings.ajax.callback, {action: 'query', q: value, l: 5}, function(response) {
                if(response.length > 0) {
                    response = _.helper.correctJsonURL(response);
                    
                    var list = $.extend([], _this.cache.receiverList);
                    list.push(_this.cache.selfId);
                    
                    response = _this.filterUserlist(response, list);
                    
                    if($(_this.settings.selector.userFormInput).is(':focus') === false) {
                        resultListWrapper.hide();
                    } else {
                        resultListWrapper.fadeIn('fast');
                    }

                    if(response.length > 0) {
                        _this.emptyResultlist();
                        $(_this.settings.selector.resultList)
                            .show()
                            .append($(_this.settings.template.userSearch).render(response));
                    } else {
                        _this.emptyResultlist();
                        $(_this.settings.selector.resultList)
                            .append('<li class="text-center nomatch-found"><em>' + $(_this.settings.translation.noMatch).text() + '</em></li>');
                            
                        resultListWrapper.fadeIn('fast');
                    }
                } else {
                    _this.emptyResultlist();
                    $(_this.settings.selector.resultList)
                        .append('<li class="text-center nomatch-found"><em>' + $(_this.settings.translation.noMatch).text() + '</em></li>');
                        
                    resultListWrapper.fadeIn('fast');
                }
            });
        },
        
        /**
         * @param array userObj An array of Objects
         * @param array userArr An array consisting of usernames which we want to filter out of the resultlist
         */
        filterUserlist: function(userObj, userArr) {
            if(userObj.length === 0 || userArr.length === 0) {
                return userObj;
            }
            
            if(undefined === userObj) {
                console.log('break here');
            }
            
            var tmpList = new Array(),
                self = this,
                found = -1;
                
            $.each(userObj, function(i, tmp) {
                $.each(userArr, function(k, val) {
                    if(tmp.id === val) {
                        // remove if found
                        userArr.splice(k, 1);
                        userObj.splice(i, 1);
                        
                        // call function again
                        self.filterUserlist(userObj, userArr);
                        
                        // define found so we can break the outer each loop
                        found = k;
                        return false;
                    }
                });
                
                if(found > -1) {
                    return false;
                }
            });
            
            return userObj;
        },
        
        /**
         * void
         */
        emptyUsersearch: function() {
            $(this.settings.selector.userFormInput).val('');
        },
        
        /**
         * void
         */
        emptyResultlist: function() {
            $(this.settings.selector.resultList).empty();
        },
        
        /**
         * void
         */
        hideResultlist: function() {
            $(this.settings.selector.resultList).hide();
        },
        
        /**
         * @param int    userid
         * @param string portrait
         */
        addToReceiverList: function(userid, portrait) {
            if($.inArray(userid, this.cache.receiverList) === -1) {
                this.cache.receiverList.push(userid);
                
                this.renderReceiverList({id: userid, portrait_url: portrait});
            }
            
            this.cache.currentSelectedElement = null;
        },
        
        /**
         * @param int userid
         */
        removeFromReceiverList: function(userid) {
            var tmp = this.cache.receiverList,
                _this = this;
            this.cache.receiverList = [];
            
            $.each(tmp, function(index, value) {
                if(value !== userid) {
                    _this.cache.receiverList.push(value);
                }
            });
        },
        
        renderReceiverList: function(obj) {
            $(this.settings.selector.receiverList).append($(this.settings.template.receiverList).render(obj));
        },
        
        /**
         * void
         */
        renderDialog: function() {
            var _this = this;
            
            /*$(this.settings.selector.dialogContainer).find('li').each(function() {
                var $this = $(this),
                    $receiver = $this.find('.message-text').find('a[href*="author"]').last();
                    
                var partnerRegExp = new RegExp(_this.cache.messagePartnerId, 'i');
                if($receiver.attr('href').match(partnerRegExp)) {
                    $this.addClass('message-sent');
                } else {
                    $this.addClass('message-received');
                }
            });*/
        },
        
        /**
         * void
         */
        dialogInterval: function() {
            var _this = this;
        
            if(!this.cache.dialogStream) {
                this.cache.dialogStream = setInterval(function() {
                    _this.dialogIntervalRequest();
                }, this.settings.stream.delay.dialog);
            }
        },
        
        /**
         * void
         */
        dialogIntervalRequest: function() {
            var _this = this,
                lastTimestamp = $(this.settings.selector.dialogContainer).find('li').last().find('.timestamp').attr('id'),
                lastHash = $(this.settings.selector.dialogContainer).find('li').last().attr('id');
        
            $.getJSON(_.settings.ajax.remote + '@@ajax-messages' + _.settings.ajax.callback, {
                action: 'get_messages',
                sender_id: _this.cache.messagePartnerId,
                timestamp: lastTimestamp,
                newer: true,
                approved: 'all'
            }, function(resp) {
                resp.reverse();
            
                _this.render(resp);
            });
            
            
            if($.isWindowActive()) {
                _this.markUnreadAsRead();
                
                $(this.settings.selector.dialogContainer).find('.message-unread').removeClass('message-unread');
            }
        },
        
        
        initDialog: function() {
            var _this = this;
            
            _.helper.showSpinner();
            
            $.getJSON(_.settings.ajax.remote + '@@ajax-messages' + _.settings.ajax.callback, {action: 'get_dialog', sender_id: _this.cache.messagePartnerId, approved: 'all', max: _this.settings.stream.max}, function(resp) {
                // TODO sorting?
                
                _this.render(resp);
                
                // remove spinner from DOM
                _.helper.hideSpinner();
                
                _this.markUnreadAsRead();
            });
        },
        
        highLightUS: function(el) {
            el.addClass('hover');
        },
        
        deHighLightUS: function(el) {
            el.removeClass('hover');
        },
        
        /**
         * void
         */
        notifyRequest: function() {
            var senderIds = [],
                self = this;
            
            $.getJSON(_.settings.ajax.remote + '@@ajax-messages' + _.settings.ajax.callback, {
                action: 'get_messages',
                approved: false,
                max: 100
            }, function(resp) {
                $('#messages-counter').text(resp.length);
                
                var tooltip,
                    sender = new Array(),
                    senderData = {};
                
                for(var msg in resp) {
                    if($.inArray(resp[msg].sender_id, sender) < 0) {
                        sender.push(resp[msg].sender_id);
                        
                        var strip = $($.trim(resp[msg].message)).text();
                        resp[msg].message = $.trim(strip.substr(0,30) + (strip.length > 30 ? '...' : ''));
                        
                        senderData[resp[msg].sender_id] = $.extend({}, {count: 1}, resp[msg]);
                    } else {
                        senderData[resp[msg].sender_id].count += 1;
                    }
                }
            
                if(resp.length > 0) {
                    $('#messages-counter').removeClass('badge-hide');
                    
                    if($('#notify-messages-box').length === 0) {
                        $($('#imessage-notify-wrapper-template').render()).appendTo('#notify-messages');
                    }
                } else {
                    $('#messages-counter').addClass('badge-hide');
                    
                    if($('#notify-messages-box').length > 0) {
                        $('#notify-messages-box').prev('.arrow-top').remove();
                        $('#notify-messages-box').remove();
                    }
                }
                
                self.renderNotifyDropdown(senderData);
            });
        },
        
        /**
         * @param object data contains the json response of ajax messages with
         *                    additional param count, counting all messages
         */
        renderNotifyDropdown: function(data) {
            var msgList = $('<ul/>'),
                self = this;
            
            $(this.settings.selector.notifyMessages).empty();
            
            $.each(data, function(k, v) {
                $($(self.settings.template.notifyMessages).render(v)).appendTo(msgList);
            });
            
            msgList.appendTo(this.settings.selector.notifyMessages);
        },
        
        /**
         * void
         */
        notifyInterval: function() {
            var _this = this;
            
            this.notifyRequest();
            
            if(!this.cache.notifyStream) {
                this.cache.notifyStream = setInterval(function() {
                    _this.notifyRequest();
                }, this.settings.stream.delay.notify);
            }
        },
        
        markUnreadAsRead: function() {
            var mids = new Array();
            
            $(this.settings.selector.dialogContainer).find('.message-unread').each(function() {
                mids.push($(this).attr('id'));
            });
            
            if(mids.length > 0) {
                this.messageRead(mids);
            }
        },
        
        /**
         * @param string state
         * @param string mid
         */
        messageRead: function(mid) {
            var mids = JSON.stringify(mid);
        
            $.getJSON(_.settings.ajax.remote + '@@ajax-messages' + _.settings.ajax.callback, {action: 'message_read_by_receiver', mids: mids});
        },
        
        strip_tags: function(str, allowed_tags) {
            var key = '',
                allowed = false;
                
            var matches = [],
                allowed_array = [];
                
            var allowed_tag = '',
                i = 0,
                k = '',
                html = '';
            
            var replacer = function(search, replace, str) {
                return str.split(search).join(replace);
            };
            
            if(allowed_tags) {
                allowed_array = allowed_tags.match(/([a-zA-Z0-9]+)/gi);
            }
            str += '';
            
            matches = str.match(/(<\/?[\S][^>]*>)/gi);
            
            for(key in matches) {
                if(isNaN(key)) {
                    continue;
                }
                
                html = matches[key].toString();
                allowed = false;
                
                for(k in allowed_array) {
                    allowed_tag = allowed_array[k];
                    i = -1;
                    
                    if(i != 0) {
                        i = html.toLowerCase().indexOf('<' + allowed_tag + '>');
                    }
                    if(i != 0) {
                        i = html.toLowerCase().indexOf('<' + allowed_tag + ' ');
                    }
                    if(i != 0) {
                        i = html.toLowerCase().indexOf('</' + allowed_tag);
                    }
                    
                    if(i == 0) {
                        allowed = true;
                        break;
                    }
                }
                
                if(!allowed) {
                    str = replacer(html, '', str);
                }
            }
            
            return str;
        },
        
        
        /**
         * Init is called by this.ITYOU
         */
        init: function() {
            var _this = this;
            
            // start notify interval
            //this.notifyInterval();
            
            // if message dialog is opened scroll down and render the dialog
            if(window.location.pathname && window.location.search) {
                if(window.location.pathname.match(/@@messages/i) && window.location.search.match(/\?sid=/i)) {
                    this.cache.messagePartnerId = window.location.search.match(/sid=[a-z]+/i)[0].split('=')[1];
                    
                    this.initDialog();
                    this.renderDialog();
                    this.dialogInterval();
                }
            }
            
            this.cache.selfId = _.session.get('userId');
        
            
            if(this.cache.registered === false) {
                // Init TinyMCE
                $(this.settings.selector.tinyMCE).tinymce({
                    script_url: '/tiny_mce_gzip.js',
                    content_css: '/portal_tinymce/@@tinymce-getstyle',
                    theme: 'advanced',
                    skin: 'plone',
                    plugins: 'paste',
                    theme_advanced_buttons1: 'bold,italic,underline,separator,justifyleft,justifycenter,justifyright,justifyfull,separator,bullist,numlist',
                    theme_advanced_buttons2: '',
                    theme_advanced_buttons3: '',
                    theme_advanced_toolbar_location: 'top',
                    
                    oninit: function(e) {},
                    
                    paste_preprocess: function(pl, o) {
                        o.content = _this.strip_tags(o.content, '<b><u><i><em><p><strong><small><ul><ol><li><a><img>');
                    }
                });
                
                // Event Handling for Button clicks
                $(document).on('click', '.messages-all-button, .messages-hideall-button, .messages-previous-button', function(e) {
                    e.preventDefault();
                    
                    var $target = $(e.target);
                    
                    if($target.hasClass('messages-all-button')) {
                        $(this).hide();
                        $('.messages-hideall-button').show();
                        $('.messages-previous-button').show();
                        $('#message-stream').find('.latest-messages').find('.latest-message').slideDown(999);
                    } else if($target.hasClass('messages-hideall-button')) {
                        $(this).hide();
		        		$('.messages-previous-button').hide();
		        		$('.messages-all-button').show();    		
        				$('#message-stream').find('.latest-messages').find('.latest-message').slideUp();
                    } else if($target.hasClass('messages-previous-button')) {
                        var oldest_message = $('#message-partner-id').find('li:first'),
                            timestamp = oldest_message.find('.timestamp:first').attr('id');
                            
                        _this.getPreviousMessages(timestamp);
                    } else {
                    
                    }
                });
                
                // Event Handling for saving a message
                $(document).on('click', '.message-save-button', function(e) {
                    e.preventDefault();
                    
                    if($(this).attr('disabled') === undefined) {
                        var content = $(_this.settings.selector.tinyMCE).tinymce().getContent(),
                            receiver = _this.cache.receiverList.join(','),
                            dialogView = false;
                            
                        if(receiver.length === 0 && window.location.pathname && window.location.pathname.match(/@@messages/i) && window.location.search && window.location.search.match(/\?sid=/i)) {
                            receiver = _this.cache.messagePartnerId;
                            dialogView = true;
                        }

                        if(content.length === 0 || receiver.length === 0) {
                            return false;
                        }
                        
                        $(this).attr('disabled', true);
                        
                        var $this = $(this);
                        
                        var hash = $('#message-stream').find('.latest-message').last().attr('id');
                        
                        $.ajax({
                            url: _.settings.ajax.remote + '@@ajax-messages' + _.settings.ajax.callback,
                            dataType: 'jsonp',
                            data: {action: 'post_message', hash: hash, message: content, receiver_id: receiver},
                            success: function(response) {
                                if(dialogView) {
                                    _this.updateDialog(response);
                                    $(_this.settings.selector.tinyMCE).html('');
                                    $this.prop('disabled', false);
                                } else {
                                    location.href = '/@@messages?sid=' + _this.cache.receiverList[0];
                                }
                            },
                            error: function(response) {
                                console.log(response);
                            }
                        });
                    }
                });
                
                $('#messages-controls').on('click', '.previous-messages-trigger', function() {
                    var $trigger = $(this),
                        $loader = $(this).parents('.well.previous-messages').find('.previous-messages-loader');
                        
                    //$.getJSON('@@ajax-messages', {
                    var $dialog = $(_this.settings.selector.dialogContainer),
                        messageCount = $dialog.children().length;
                        
                    $trigger.hide();
                    $loader.show();
                    
                    $.getJSON(_.settings.ajax.remote + '@@ajax-messages' + _.settings.ajax.callback, {action: 'get_dialog', sender_id: _this.cache.messagePartnerId, approved: 'all', max: _this.settings.stream.max, offset: messageCount}, function(resp) {
                        resp.reverse();
                    
                        _this.render(resp, false);
                        
                        $loader.hide();
                        $trigger.show();
                        
                        if(resp.length === 0) {
                            $trigger.parents('.well.previous-messages').hide();
                        }
                    });
                });
                
                // Event Handling for keyboard actions
                //  used in user search input
                $(document).on({
                    
                    keyup: function(e) {
                        var $input = $(this),
                            keyName = e.which || e.keyCode;
                            
                        if(keyName === 38 || keyName === 40) {
                            return;
                        }
                        
                        _this.cache.currentSelectedElement = null;
                    
                        if(_this.cache.keyTimeout) {
                            clearTimeout(_this.cache.keyTimeout);
                        }
                    
                        _this.cache.keyTimeout = setTimeout(function() {
                            if($input.val().length >= _this.settings.minInputLength) {
                                _this.cache.inputval = $input.val();
                                _this.searchUser($input.val());
                            } else {
                                _this.hideResultlist();
                            }
                        }, _this.settings.keyTimeout);
                    },
                    
                    keydown: function(e) {
                        var keyName = e.which || e.keyCode,
                            $cntr = $(this).parent().find(_this.settings.selector.resultList);
                    
                        switch(keyName) {
                            case 13: // enter
                                // adding first search result
                                if($cntr.find('li').length > 0 && $(this).val().length > 0) {
                                    if(!$cntr.find('li').first().hasClass('nomatch-found')) {
                                        if(_this.cache.currentSelectedElement) {
                                            _this.cache.currentSelectedElement.trigger('click');
                                        } else {
                                            $cntr.find('li').first().trigger('click');
                                        }
                                    }
                                }
                                break;
                                
                            case 9: // tab
                                // not action here
                                break;
                                
                            case 27: // esc
                                // cancel user search
                                // clear input and empty result list
                                _this.emptyResultlist();
                                break;
                                
                            case 38: // arrow up
                                // navigate between search results
                                if($cntr.find('li').length > 0) {
                                    var $currentEl = _this.cache.currentSelectedElement;
                                    
                                    if(!$currentEl) {
                                        _this.cache.currentSelectedElement = $cntr.find('li').first();
                                        _this.highLightUS(_this.cache.currentSelectedElement);
                                    } else {
                                        if($currentEl.prev().length > 0) {
                                            _this.deHighLightUS($currentEl);
                                            _this.cache.currentSelectedElement = $currentEl.prev();
                                            _this.highLightUS(_this.cache.currentSelectedElement);
                                        }
                                    }
                                }
                                break;
                                
                            case 40: // arrow down
                                // navigate between search results
                                if($cntr.find('li').length > 0) {
                                    var $currentEl = _this.cache.currentSelectedElement;
                                    
                                    if(!$currentEl) {
                                        _this.cache.currentSelectedElement = $cntr.find('li').first();
                                        _this.highLightUS(_this.cache.currentSelectedElement);
                                    } else {
                                        if($currentEl.next().length > 0) {
                                            _this.deHighLightUS($currentEl);
                                            _this.cache.currentSelectedElement = $currentEl.next();
                                            _this.highLightUS(_this.cache.currentSelectedElement);
                                        }
                                    }
                                }
                                break;
                        }
                    },
                    
                    blur: function(e) {},
                    
                    focus: function(e) {
                        $(this).trigger('keyup');
                    }
                    
                }, _this.settings.selector.userFormInput);
                
                // Prevent the form of the user search input from being submitted
                $(document).on('submit', _this.settings.selector.userForm, function(e) {
                    e.preventDefault();
                    return false; // internet explorer sucks
                });
                
                // Event Handling for mouse clicks
                //  depends on the target clicked
                $(document).on('click', function(e) {
                    var $target = $(e.target);
                    
                    if($target.parents('.usersearch').length > 0) {
                        if($target.parents('li').length > 0 || $target[0].nodeName.toLowerCase() === 'li') {
                            var noMatch = $target.parents('li').hasClass('nomatch-found') || $($target[0].nodeName).hasClass('nomatch-found');
                            if(!noMatch) {
                                var userid = $target.parents('li').find('a').attr('title') === undefined ? $target.find('a').attr('title') : $target.parents('li').find('a').attr('title'),
                                    img = $target.parents('li').find('img').attr('src') === undefined ? $target.find('img').attr('src') : $target.parents('li').find('img').attr('src');
                                
                                _this.addToReceiverList(userid, img);
                                
                                _this.hideResultlist();
                                _this.emptyUsersearch();
                            }
                        }
                    } else if($target.attr('id') === $(_this.settings.selector.userFormInput).attr('id')) {
                        ; // do nothing, event handler is binded above
                    } else if($target.hasClass('fa fa-times') && $target.parents('.remove').length > 0 && $target.parents('#receiver_list').length > 0) {
                        var containerid = $target.parents('.user').attr('id'),
                            userid = containerid.split('-')[1];

                        _this.removeFromReceiverList(userid);
                        
                        $('#' + containerid).parents('li').remove();
                    } else {
                        _this.hideResultlist();
                    }
                });
                
                // Event Handling message hide button
                $(document).on('click', '.message-hide-button', function(e) {
                    e.preventDefault();
                
                    $(this).parents('li').slideUp(_this.settings.animation.speedUp);
                    
                    $('.messages-all-button').show();
                });
                
                
                $(document).on('click', '.message-delete-button', function(e) {
                    e.preventDefault();
                    
                    var $tmp = $(this).parents('li.latest-message'),
                        hash = new Array();
                        
                    hash.push($tmp.attr('id'));
                    
                    // state = message_hidden_by_[receiver|sender]
                    var state = 'message_hidden_by_' + ($tmp.hasClass('message-received') ? 'receiver' : 'sender');
                    
                    if($tmp.hasClass('message-received') || $tmp.hasClass('message-sent')) {
                        $.getJSON('@@ajax-messages', {action: state, mids: JSON.stringify(hash)});
                    
                    
                        $tmp.fadeOut(400, function() {
                            $tmp.remove();
                        });
                    }
                });
                
            }
        }
    };

}(jQuery, this, this.document, this.ITYOU));







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
}


ItyouInbox.prototype = new Utilities();


ItyouInbox.prototype.init = function() {
    this.getMessages(0);
    this.eventHandler();
    
    this.inboxStream();
};


ItyouInbox.prototype.getMessages = function(offset) {
    if(undefined !== this.filteredUsers) {
        if(!this.runningRequest) {
            this.runningRequest = true;
            
            this.clearFiltering();
            this.showSpinner();
            
            var tmpUid = new Array();
            $(this.messageList).children().each(function() {
                var $el = $(this).find('td[data-uid]');
                
                if($el.length > 0 && $.inArray($el.data('uid'), tmpUid) === -1) {
                    tmpUid.push($el.data('uid'));
                }
            });
            
            var tmpOffsets = new Array();
            $.each(tmpUid, $.proxy(function(k, v) {
                tmpOffsets.push($(this.messageList).children().find('td[data-uid="' + v + '"]').length);
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
        
            $.getJSON('@@ajax-messages', {action: 'get_messages', approved: 'all', max: this.max, offset: offset}, $.proxy(function(response) {
                this.renderMessages(response, 'append');
                this.runningRequest = false;
                
                if(response.length > 0) {
                    this.loadMoreEvent();
                }
                
                this.hideSpinner();
            }, this));
        }
    }
};


ItyouInbox.prototype.getLatestMessages = function() { console.log(this.getLatestTimestamp());
    $.getJSON('@@ajax-messages', {action: 'get_messages', approved: 'all', newer: true, timestamp: this.getLatestTimestamp()}, $.proxy(function(response) {
        if(response.length > 0) {
            this.setLatestTimestamp(response[0]['timestamp']);
    
            this.renderMessages(response, 'prepend');
        }
    }, this));
};


ItyouInbox.prototype.renderMessages = function(data, direction) {
    $.each(data, $.proxy(function(index, val) {
        var dataToRender = {};
        
        dataToRender.hash = val.hash;
        dataToRender.sender_name = val.sender_name;
        dataToRender.sender_id = val.sender_id;
        dataToRender.sender_portrait = val.sender_portrait;
        dataToRender.timestr = val.timestr;
        dataToRender.ploneTimeStamp = val.timestamp;
        dataToRender.timeStamp = this.convertToUNIXTimestamp(val.timestamp);
        dataToRender.approved = val.approved;
        dataToRender.siteUrl = val.site_url;

        var strip = $(val.message).text();
        
        dataToRender.msg = strip.substr(0,15) + (strip.length > 15 ? '...' : '');
        
        if(direction === 'append') {
            $($(this.messageTemplate).render(dataToRender)).appendTo(this.messageList);
        } else if(direction === 'prepend') {
            $($(this.messageTemplate).render(dataToRender)).prependTo(this.messageList);
        }
    }, this));
};


ItyouInbox.prototype.eventHandler = function() {
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
            window.location.href = $(e.currentTarget).data('url');
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
    
    $.getJSON('@@ajax-messages', {action: state, mids: JSON.stringify(hash)});
    
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
    if(!this.runningStream) {
        this.runningStream = setInterval($.proxy(function() {
            if(null === this.getLatestTimestamp() || undefined === this.getLatestTimestamp()) {
                var els = $('#imessage-inbox').find('tr[data-timestamp]'),
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
        }, this), this.inboxStreamDelay);
    }
};


ItyouInbox.prototype.stopInboxStream = function() {
    if(this.runningStream) {
        this.runningStream = clearInterval(this.runningStream);
        this.setLatestTimestamp(null);
    }
};


ItyouInbox.prototype.setLatestTimestamp = function(timestamp) {
    this.storage.set('imessageInboxTimestamp', timestamp);
    this.latestTimestamp = timestamp;
    
    return this;
};


ItyouInbox.prototype.getLatestTimestamp = function() {
    return this.latestTimestamp;
};


ItyouInbox.prototype.showSpinner = function() {
    $('#imessage-inbox-spinner').show();
};

ItyouInbox.prototype.hideSpinner = function() {
    $('#imessage-inbox-spinner').hide();
};


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

