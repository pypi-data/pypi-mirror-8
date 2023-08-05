(function($, window, document, _, undefined) {

    'use strict';

    _.libs.activitystream = {
        name: 'ityou.activitystream',
        version: '0.2.1',
        
        cache: {
            registered: false,
            activityStream: null,
            commentStream: null,
            followTab: false
        },
        settings: {
            animation: {
                speedDown: 400,
                speedUp: 200,
                removeHighlight: 1500
            },
            selector: {
                wrapper: '#activity-stream',
                getMoreActivities: '.get-more-activities',
                activities: 'ul#activity-stream-list',
                comments: 'ul.activity-comment-list',
            },
            template: {
                activity: '#activity-stream-template',
                comment: '#comment-stream-template',
            },
            stream: {
                delay: {
                    activity: 30000,
                    comment: 60000
                }
            },
            debug: false,
            
            streamView: {
                activityStream: 'activity-stream',
                userprofileStream: 'author'
            }
        },
        /**
         * Get Activites
         * 
         * @type string state get_more_activities || get_latest_activities
         */
        getActivities: function(state, uid) {
            var _this = this,
                    timestamp = null;

            if(this.stopInterval() === false) {
                return ;
            }

            if(state === 'get_latest_activities') {
                timestamp = $(this.settings.selector.wrapper).find(this.settings.selector.activities).find('li.activity').first().attr('data-timestamp');
                // initial
                if(timestamp === undefined || timestamp === null) {
                    _.helper.showSpinner(this.settings.selector.wrapper + ' #content', 64);
                }
            } else if(state === 'get_more_activities') {
                timestamp = $(this.settings.selector.wrapper).find(this.settings.selector.activities).find('li.activity').last().attr('data-timestamp');
                _.helper.showSpinner(this.settings.selector.wrapper + ' #content', 32);
            } else {
                return;
            }
            
            //if(_.libs.mapping.settings.currentView === this.settings.streamView.activityStream) {
            if($('#uid').text().length === 0) {
                $.getJSON(_.settings.ajax.remote + '@@ajax-activities' + _.settings.ajax.callback, {action: state, timestamp: timestamp}, function(response) {
                    if (response.length > 0) {
                        response = _.helper.correctJsonURL(response);
                        
                        $.each(response, function(i, val) {
                            $.each(val.comments, function(k, com) {
                                response[i].comments[k].comment = response[i].comments[k].comment.replace(/\n/g, '<br />');
                            });
                        });

                        // insert new activity
                        if (state === 'get_latest_activities') {
                            if (timestamp === undefined || timestamp === null) {
                                $($(_this.settings.template.activity).render(response))
                                        .prependTo(_this.settings.selector.activities)
                                        .hide();
                                        
                                if(_this.cache.followTab === false) {
                                    $(_this.settings.selector.activities).find('li.activity').slideDown(_this.settings.animation.speedDown);
                                } else {
                                    $(_this.settings.selector.activities).find('li.activitiy.following').slideDown(_this.settings.animation.speedDown);
                                }
                            } else {
                                $($(_this.settings.template.activity).render(response))
                                        .prependTo(_this.settings.selector.activities)
                                        .hide()
                                        .addClass('new');
                                        
                                if(_this.cache.followTab === false) {
                                    $(_this.settings.selector.activities).find('li.activity')
                                        .slideDown(_this.settings.animation.speedDown, function() {
                                            _this.removeHighlight($(this));
                                        });
                                } else {
                                    $(_this.settings.selector.activities).find('li.activity.following')
                                        .slideDown(_this.settings.animation.speedDown, function() {
                                            _this.removeHighlight($(this));
                                        });
                                }
                            }
                        } else {
                            $($(_this.settings.template.activity).render(response))
                                    .appendTo(_this.settings.selector.activities)
                                    .hide();
                            
                            if(_this.cache.followTab === false) {
                                $(_this.settings.selector.activities).find('li.activity')
                                    .slideDown(_this.settings.animation.speedDown);
                            } else {
                                $(_this.settings.selector.activities).find('li.activity.following')
                                    .slideDown(_this.settings.animation.speedDown);
                            }
                        }

                        $('.comment-textarea').autoGrow();

                        _.storage.set('activitiesTimestamp', $(_this.settings.selector.wrapper).find(_this.settings.selector.activities).find('li').first().attr('data-timestamp'));
                        _.cache.activitiesTimestamp = _.storage.get('activitiesTimestamp');
                        
                        // allow to load more
                        $(_this.settings.selector.wrapper).find(_this.settings.selector.getMoreActivities).show();
                        
                        _this.markCommentAsOwn();
                        
                        $(_this.settings.selector.activities).find('li').each(function() {
                            $(this).css('overflow', '');
                        });
                    }
                    
                    _this.prepOverlay();

                    // remove spinner from DOM
                    _.helper.hideSpinner();
                }); // - getJSON
            //} else if(_.libs.mapping.settings.currentView === this.settings.streamView.userprofileStream) {
            } else {
                $.getJSON(_.settings.ajax.remote + '@@ajax-activities' + _.settings.ajax.callback, {action: state, timestamp: timestamp, uid: uid}, function(response) {
                    if(response.length > 0) {
                        response = _.helper.correctJsonURL(response);
                        
                        // insert new activity
                        if(state === 'get_latest_activities') {
                            if(timestamp === undefined || timestamp === null) {
                                $($(_this.settings.template.activity).render(response))
                                    .prependTo(_this.settings.selector.activities)
                                    .hide()
                                    .slideDown(_this.settings.animation.speedDown);
                            } else {
                                $($(_this.settings.template.activity).render(response))
                                    .prependTo(_this.settings.selector.activities)
                                    .hide()
                                    .addClass('new')
                                    .slideDown(_this.settings.animation.speedDown, function() {
                                        _this.removeHighlight($(this));
                                    });
                            }
                        } else {
                            $($(_this.settings.template.activity).render(response))
                                .appendTo(_this.settings.selector.activities)
                                .hide()
                                .slideDown(_this.settings.animation.speedDown);
                        }

                        $('.comment-textarea').autoGrow();
                        
                        _this.markCommentAsOwn();
                        
                        $(_this.settings.selector.userprofileActivities).find('li').each(function() {
                            $(this).css('overflow', '');
                        });
                    }
                    
                    _this.prepOverlay();
                    
                    // remove spinner from DOM
                    _.helper.hideSpinner();
                }); // - getJSON
            }
        },
        /**
         *
         */
        markCommentAsOwn: function() {
            $('.activity-comment').each(function() {
                var $this = $(this),
                    uid = $this.find('a[data-uid]').attr('data-uid');
                    
                if(uid === _.cache.userId) {
                    $('#' + $this.attr('id')).addClass('self');
                }
            });
        },
        /**
         * getCmments
         */
        getComments: function() {
            var _this = this,
                    timestamp = null,
                    commentTimestamps = [];

            if(this.stopInterval() === false) {
                return ;
            }

            $(this.settings.selector.comments).each(function() {
                $(this).find('li').each(function() {
                    commentTimestamps.push($(this).attr('data-timestamp'));
                });
            });

            timestamp = commentTimestamps.sort().reverse()[0];
            
            // if there are no comments, get timestamp of the latest activity, because there can't be published any comment with a date behind this one
            if(timestamp === undefined) {
                timestamp = $(this.settings.selector.wrapper).find(this.settings.selector.activities).find('li.activity').first().attr('data-timestamp');
            }

            $.getJSON(_.settings.ajax.remote + '@@ajax-activities' + _.settings.ajax.callback, {action: 'get_latest_comments', timestamp: timestamp}, function(response) {
                if (response.length > 0) {
                    response = _.helper.correctJsonURL(response);

                    $.each(response, function(key, value) {
                        var activityExists = $(_this.settings.selector.activities).find('#' + value.activity_hash).length > 0 ? true : false;
                        
                        if(activityExists === true) {
                            var tmp = $(_this.settings.selector.activities).find('#' + value.activity_hash).find(_this.settings.selector.comments).find('#' + value.hash);
                            
                            if (tmp.length > 0) {
                                //tmp.remove();
                                
                                tmp.find('p.user-comment').html(value.comment.replace(/\n/g, '<br />'));
                                
                            } else {

                                $($(_this.settings.template.comment).render(value))
                                        .appendTo(_this.settings.selector.activities + ' #' + value.activity_hash + ' ' + _this.settings.selector.comments)
                                        .hide()
                                        .addClass('new')
                                        .slideDown(_this.settings.animation.speedDown, function() {
                                            _this.removeHighlight($(this));
                                        });
                            
                            }
                                    
                                    
                            if(value.user_id === _.cache.userId) {
                                $('#' + value.hash).addClass('self');
                            }
                        }
                    });
                }
            });
        },
        /**
         * removeHighlight
         * 
         * @type object element
         */
        removeHighlight: function(element) {
            setTimeout(function() {
                element.removeClass('new');
            }, this.settings.animation.removeHighlight);
        },
        /**
         * save comment
         */
        saveComment: function(comment, parent_id) {
            var _this = this;

            if (comment === '' || comment === undefined || parent_id === undefined) {
                return;
            }
            
            var button = $('#' + parent_id).find('span.input-group-btn > button.comment-save');

            button
                .removeClass('comment-save')
                .addClass('disabled')
                .find('i')
                    .removeClass('fa-save')
                    .addClass('fa-spin fa-spinner');

            $.getJSON(_.settings.ajax.remote + '@@ajax-post-comment' + _.settings.ajax.callback, {comment: comment, hash: parent_id}, function(response) {
                if (response instanceof Object) {
                    var el = $('#' + parent_id);

                    el.find('.comment-textarea').val('');
                    el.find('.new-comment-container').hide();
                    el.find('.comment-controls').show();

                    if (_this.cache.commentStream !== null) {
                        clearInterval(_this.cache.commentStream);
                    }
                    
                    button
                        .addClass('comment-save')
                        .removeClass('disabled')
                        .find('i')
                            .addClass('fa-save')
                            .removeClass('fa-spin fa-spinner');

                    _this.getComments();
                    //_this.runInterval('comment');
                }
            }); // - getJSON
        },
        /**
         * run Interval
         * 
         * @type string state activity || comment
         */
        runInterval: function(state, uid) {
            var _this = this;
            
            if(state !== 'activity' && state !== 'comment') {
                return ;
            }
            
            if(state === 'activity') {
                if(this.cache.activityStream !== null) {
                    clearInterval(this.cache.activityStream);
                    this.cache.activityStream = null;
                }
                
                this.cache.activityStream = setInterval(function() {
                    _this.getActivities('get_latest_activities', uid);
                    // debug, shows only if settings.debug = true
                    _this.debug('ActivityInterval');
                }, _this.settings.stream.delay.activity);
            } else {
                if(this.cache.commentStream !== null) {
                    clearInterval(this.cache.commentStream);
                    this.cache.commentStream = null;
                }
                    
                this.cache.commentStream = setInterval(function() {
                    _this.getComments();
                    // debug, shows only if settings.debug = true
                    _this.debug('CommentInterval');
                }, _this.settings.stream.delay.comment);
            }
        },
        /**
         * stop interval
         */
        stopInterval: function() {
            var _this = this;
            
            if($(this.settings.selector.wrapper).offset() === undefined) {
                return this.clearStream();
            }
            
            return true;
        },
        /**
         *
         */
        clearStream: function() {
            clearInterval(this.cache.activityStream);
            clearInterval(this.cache.commentStream);
            
            this.cache.activityStream = null;
            this.cache.commentStream = null;
            
            this.debug('STOPPING ACTIVITY STREAM!');
            
            return false;
        },
        /**
         *
         */
        activityControls: function(state) {
            var _this = this,
                controls = $(this.settings.selector.wrapper).find('.activity-controls').length > 0 ? $(this.settings.selector.wrapper).find('.activity-controls') : $('.activity-controls'),
                activity = $(this.settings.selector.activities);
                
            switch(state) {
                case 'activity-hide':
                    controls.find('.show-all').removeClass('hidden').show();
                    if(activity.find('li:visible').length <= 0) {
                        controls.find('.hide-all').hide();
                    }
                    break;
                case 'activity-hide-all':
                    $(_this.settings.selector.getMoreActivities).hide();
                    
                    controls.find('.show-all').removeClass('hidden').show();
                    controls.find('.hide-all').hide();
                    break;
                case 'activity-show':
                    controls.find('.hide-all').show();
                    if(activity.find('li:not(:visible)').length <= 0) {
                        contros.find('.show-all').hide();
                    }
                    break;
                case 'activity-show-all':
                    $(_this.settings.selector.getMoreActivities).show();
                    
                    controls.find('.hide-all').show();
                    controls.find('.show-all').hide();
                    break;
            }
        },
        /**
         * Modal Dialog, Image Preview
         */
        prepOverlay: function() {
            var self = this;
        
            $('.linked-document').prepOverlay({
			    subtype: 'ajax',
			    width: '533px',
			    height: '50px',
	   			config: {
	    			onLoad: function(e) {
	    			    self.prepContentViews();
	    			}
	    		}
			});
			
			$('.Image').find('.linked-document').prepOverlay({
			    subtype: 'ajax',
			    width: '800px',
			    height: '50px',
	    		config: {
	    			onLoad: function(e) {
	    			    self.prepContentViews();
    			    }
	    		}
			});
        },
        //-
        prepContentViews: function() {
	        $(".show-preview #content-views").children().click(function() {
	        	var url = $(this).find("a").attr("href");
	        	if(url != undefined) {
	        		window.location = url;
	        	};
	        });
	        
	        $(".show-preview #content-views").children().each(function() {
	        	var menu_context = $(this).find("a").html();
	        	
	        	$(this).prepend('<div class="content-view-box"></div>');
	        	$(this).find(".content-view-box").html(menu_context).hide();
	        	$(this).find("a").html("");

	        });

	        $(".show-preview  #content-views").children().hover(function() {
	        	if($(this).find(".content-view-box").html().length > 1) {
	        		$(this).find(".content-view-box").show();
	        	};
	        }, function() {
	        	$(this).find(".content-view-box").hide();
	        });
		},
        /**
         * Initialize ActivityStream
         */
        construct: function() {
            var _this = this;
            
            if(_.settings.ASTREAM_ACTIVITY_DELAY !== undefined) {
                this.settings.stream.delay.activity = _.settings.ASTREAM_ACTIVITY_DELAY;
            }
            
            if(_.settings.ASTREAM_COMMENT_DELAY !== undefined) {
                this.settings.stream.delay.comment = _.settings.ASTREAM_COMMENT_DELAY;
            }
            
            if($('#JESI-PARAMS').length > 0) {
                if($('#ASTREAM_DELAY').length > 0) {
                    this.settings.stream.delay.activity = parseInt($('#ASTREAM_DELAY').text());
                    this.settings.stream.delay.comment = parseInt($('#ASTREAM_DELAY').text());
                }
            }

            // Register Event Handler if Module wasn't loaded before
            if (this.cache.registered === false) {

                /**
                 * Click Handler
                 * Hide a single activity
                 */
                $(document).on('click', this.settings.selector.wrapper + ' li.activity .activity-hide', function(e) {
                    e.preventDefault();

                    $(_this.settings.selector.activities).find($(this).attr('data-parent-hash')).slideUp(_this.settings.animation.speedUp, function() {
                        _this.activityControls('activity-hide');
                    });
                });
                
                /**
                 * Click Handler
                 * show all activities
                 */
                $(document).on('click', 'div.activity-controls .show-all', function(e) {
                    e.preventDefault();
                    
                    $(_this.settings.selector.activities).children().each(function() {
                        $(this).slideDown(_this.settings.animation.speedDown);
                    });
                    _this.activityControls('activity-show-all');
                });
                
                /**
                 * Click Handler
                 * hide all activities
                 */
                $(document).on('click', 'div.activity-controls .hide-all', function(e) {
                    e.preventDefault();
                    
                    $(_this.settings.selector.activities).children().each(function() {
                        $(this).slideUp(_this.settings.animation.speedUp);
                    });
                    _this.activityControls('activity-hide-all');
                });
                
                /**
                 * Click Handler
                 *
                 */
                $(document).on('click', 'li.activity .comment-write', function(e) {
                    e.preventDefault();
                    
                    $(_this.settings.selector.activities).children().each(function() {
                        $(this).find('.comment-input-group').hide();
                        $(this).find('.comment-textarea').val('');
                        $(this).find('.comment-write').show();
                    });
                    
                    $($(this).attr('data-parent-hash')).find('.comment-write').hide();
                    $($(this).attr('data-parent-hash')).find('.comment-input-group').removeClass('hidden').show();
                });
                
                /**
                 * Click Handler
                 *
                 */
                $(document).on('click', 'li.activity .comment-save', function(e) {
                    e.preventDefault();
                    
                    _this.saveComment($($(this).attr('data-parent-hash')).find('textarea').val(), $(this).attr('data-parent-hash').split('#')[1]);
                });
                
                /**
                 * Click Handler
                 *
                 */
                $(document).on('click', 'li.activity .comment-hide', function(e) {
                    e.preventDefault();
                    
                    $($(this).attr('data-parent-hash')).slideUp(_this.settings.animation.speedUp);
                    
                    var $this = $(this);
                    $(_this.settings.selector.activities + ' > li').each(function() {
                        if($(this).find($this.attr('data-parent-hash')).length != 0) {
                            $(this).find('.comment-show').removeClass('hidden').show();
                        }
                    });
                });
                
                /**
                 * Click Handler
                 *
                 */
                $(document).on('click', 'li.activity .comment-show', function(e) {
                    e.preventDefault();
                    
                    $(_this.settings.selector.activities).find($(this).attr('data-parent-hash')).find(_this.settings.selector.comments).find('li').not(':visible').each(function() {
                        $(this).slideDown(_this.settings.animation.speedDown);
                    });
                    
                    $(this).hide();
                });
                
                /**
                 * Thumbnail Preview Mouse Handler
                 */
                $(document).on('mouseenter', 'a.user-message', function() {
                    var thumb = $(this).parents('.well').find('.thumbnail-preview'),
                        thumbnail = thumb.find('img.lazy');
                    
                    if(thumbnail.attr('src') == undefined || thumbnail.attr('src') != thumbnail.data('original')) {
                        thumbnail.attr('src', thumbnail.data('original'));
                    }
                    
                    thumb.stop(true,true).fadeIn();
                    
                    $(this).mouseleave(function() {
                        setTimeout(function() {
                            if(!thumb.is(':hover')) {
                                thumb.fadeOut();
                            }
                        }, 200);
                    });
                    thumb.mouseleave(function() {
                        thumb.fadeOut();
                    });
                });
                
                
                
                
                $('#astream-tabs').on('click', 'a', function(e) {
                    e.preventDefault(); // li class: active
                
                    $('#astream-tabs').find('li').removeClass('active');
                    $(this).parents('li').addClass('active');
                
                    if($(this).hasClass('astream-tab-all')) {
                        _this.cache.followTab = false;
                    
                        $('li.activity').slideDown();
                    } else {
                        _this.cache.followTab = true;
                    
                        $('li.activity.not-following').slideUp();
                        $('li.activity.following').show();
                        
                        if($('li.activity.following').length < 10) {
                            _this.getActivities('get_more_activities');
                        }
                    }
                });
                
                
                
                // scroll event
		        $(window).on('scroll', function(e) {
		        
		            var lastActivity = $(_this.settings.selector.activities).find('li.activity:last'),
		                getMoreActivities = $(_this.settings.selector.getMoreActivities);
		            
		            if(lastActivity.length > 0 && getMoreActivities.is(':in-viewport') && getMoreActivities.is(':visible')) {
		                getMoreActivities.hide();
		                
		                var uid;
		                
		                if($('#uid').length > 0) {
		                    uid = $('#uid').text();
		                }
		            
		                _this.getActivities('get_more_activities', uid);
		            }
            	});
                
                
                /**
                 * Initialize ActivityStream and initialize Interval for real streaming
                 */
                if($('#uid').length === 0) {
                //if(_.libs.mapping.settings.currentView === this.settings.streamView.activityStream) {
                    //this.getActivities('get_latest_activities');
                    //this.runInterval('activity');
                    //this.runInterval('comment');
                //} else if(_.libs.mapping.settings.currentView === this.settings.streamView.userprofileStream) {
                } else {
                    /*var tmpUid = $('#uid').text();
                    
                    this.getActivities('get_latest_activities', tmpUid);
                    this.runInterval('activity', tmpUid);
                    this.runInterval('comment', tmpUid);*/
                }
                
                /**
                 * Thumbnail prepOverlay
                 */
                this.prepOverlay();
                
                /**
                 * comment positioning
                 */
                this.markCommentAsOwn();


                /**
                 * Register Plugin initialized in lib cache
                 */
                this.cache.registered = true;
            }
        },
        // Init is called by this.ITYOU
        init: function() {},
        /**
         * just for debugging
         */
        debug: function(msg) {
            if(this.settings.debug === true) {
                console.log(msg, new Date().toLocaleString());
            }
        }
    };

}(jQuery, this, this.document, this.ITYOU));
