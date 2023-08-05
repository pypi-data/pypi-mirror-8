function ActivityStream() {

    // brain
    this.cache = {
        // own userid
        userId: undefined,
    
        registered: false,
        activityStream: null,
        
        // follow
        onlyFollowing: false,
        followInstalled: false,
        
        // handle view
        currentView: undefined,
        userprofileId: undefined,
        initUserprofile: false,
        
        // block requests if there are any others running
        runningRequest: false
    };
    
    this.settings = {
		moderatable: false
    };
    
    // animations
    this.animation = {
        speedDown: 400,
        speedUp: 200,
        removeHighlight: 1500
    };
    
    // selectors
    this.selector = {
        wrapper: '#activity-stream',
        getMore: '.get-more-activities',
        activityList: '#activity-stream-list',
        commentList: '.activity-comment-list',
        followContainer: '#astream-tabs'
    };
    
    // templates
    this.template = {
        activity: '#activity-stream-template',
        comment: '#comment-stream-template'
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
    
    
    // initialize activity stream
    this.init();
}



// ActivityStream extends Utilities
ActivityStream.prototype = new Utilities();

// ActivityStream implements ClientTimezone
ActivityStream.prototype.TimeConverter = new ClientTimezone();

ActivityStream.prototype.Clipboard = new Clipboard();


/**
 * initialise astream
 *
 * return void
 */
ActivityStream.prototype.init = function() {
    this.setCache('userId', $('#ESI_DATA').data('ityou-uid'));

    if($(this.getOption('followContainer', 'selector')).length > 0) {
        this.setCache('followInstalled', true);
    }
    
    // define in which template we are
    this.defineView();
    
    // get latest activities
    if(this.isActivityStream('astream')) {
        this.initEventHandler();
    
        //this.getActivities('get_latest_activities', true);
        this.getActivities('get_more_activities');
    } else if(this.isActivityStream('userprofile')) {
        this.initEventHandler();
    }
};


/**
 * define which page is currently viewed
 *
 * @return void
 */
ActivityStream.prototype.defineView = function() {
    var pathname = document.location.pathname,
        matchAgainst = /author\/(\w.+)/i;
    
    if(matchAgainst.exec(pathname)) {
        this.setCache('currentView', 'userprofile');
        this.setCache('userprofileId', RegExp.$1);
    
        return ;
    }
    
    if($('#activity-stream').length > 0) {
        this.setCache('currentView', 'astream');
        this.setCache('userprofileId', undefined);
        
        return ;
    }
    
    this.setCache('currentView', undefined);
    this.setCache('userprofileId', undefined);
};


/**
 * simple helper to ask if we can build an astream
 *
 * @return boolean
 */
ActivityStream.prototype.isActivityStream = function(state) {
    if(state && this.getCache('currentView') === state) {
        return true;
    } else if(state && this.getCache('currentView') !== state) {
        return false;
    } else if(this.getCache('currentView') === 'astream' || this.getCache('currentView') === 'userprofile') {
        return true;
    }
    
    return false;
};


ActivityStream.prototype.getContentUid = function() {
	return $('#ESI_DATA').data('ityou-content-uid') === undefined ? "" : $('#ESI_DATA').data('ityou-content-uid'); 
};


/**
 * function to call ajax request
 * 
 * @param string state
 * @param mixed initial
 * @return void
 */
ActivityStream.prototype.getActivities = function(state, initial) {
    var timestamp,
        $wrapper = $(this.getOption('wrapper', 'selector')),
        $activityList = $wrapper.find(this.getOption('activityList', 'selector'));

    if(state === 'get_latest_activities') {
        timestamp = $activityList.find('li.activity').first().data('timestamp');
    } else if(state === 'get_more_activities') {
        timestamp = $activityList.find('li.activity').last().data('timestamp');
        
        // if there's no timestamp set, go with current time
        if(!timestamp) {
        	//timestamp = (new Date()).toISOString();
        }
        
        this.showSpinner();
    } else {
        return ;
    }
    
    $wrapper.find(this.getOption('getMore', 'selector')).hide();
    
    if(this.cache.runningRequest == false) {
	    this.cache.runningRequest = true;
	    
	    $.ajax({
	        url: '@@ajax-activities',
	        data: {
	            action: state,
	            timestamp: timestamp,
	            uid: this.getCache('userprofileId'),
	            content_uid: this.getContentUid()
	        },
	        dataType: 'json',
	        // event handler success
	        success: $.proxy(function(response) {
	            if(response.length > 0) {
	            	response = this.sort(response, 'desc');
	            
	            	// replace \n with <br>
	                $.each(response, $.proxy(function(i, val) {
	                	// need to change response[i][timestr]
	                	response[i]['timestr'] = this.TimeConverter.convertTime(val.timestamp);
	                	
	                	if(typeof response[i]['revision'] !== 'number') {
	                		response[i]['revision'] = 0;
	                	}
	                	
	                    $.each(val.comments, $.proxy(function(j, com) {
	                        response[i].comments[j].comment = response[i].comments[j].comment.replace(/\n/g, '<br>');
	                        
	                        // need to change response[i]['comments'][j]['timestr']
	                        response[i]['comments'][j]['timestr'] = this.TimeConverter.convertTime(com.timestamp);
	                        
	                        if(typeof response[i]['comments'][j]['revision'] !== 'number') {
	                        	response[i]['comments'][j]['revision'] = 0;
	                        }
	                        
	                        // moderation
	                        if(this.getOption('moderatable', 'settings') && response[i]['content_creator'] === this.getCache('userId')) {
	                        	response[i]['comments'][j]['can_delete'] = true;
	                    		response[i]['comments'][j]['can_moderate'] = true;
	                        }
	                        
	                    	response[i]['comments'][j]['revision_old'] = response[i]['revision'] > response[i]['comments'][j]['revision'];
	                    }, this));
	                }, this));
	                
	                // render
	                this.renderActivities(response, state, initial);
	            } else {
	                // remove get more activities trigger if there is no more to load
	                $(this.getOption('wrapper', 'selector')).find(this.getOption('getMore', 'selector')).remove();
	                
	                this.hideSpinner();
	            }
	        }, this),
	        complete: $.proxy(function() {
	        	this.cache.runningRequest = false;
	        }, this)
	    });
    }
};


/**
 *
 */
ActivityStream.prototype.getComments = function() {
    var timestamp,
        commentTimestamps = [];
        
    var $wrapper = $(this.getOption('wrapper', 'selector')),
        $commentList = $wrapper.find(this.getOption('commentList', 'selector'));
        
    // collect comment timestamps
    $commentList.each($.proxy(function(i, el) {
        $(el).find('li').each(function() {
            commentTimestamps.push($(this).data('timestamp'));
        });
    }, this));
    
    // sort timestamp and get first = latest
    timestamp = commentTimestamps.sort().reverse()[0];
    // if there is no comment yet, get the timestamp of the latest activity, streaming comments cannot be older then the latest activity
    if(!timestamp) {
        timestamp = $wrapper.find(this.getOption('activityList', 'selector')).find('li.activity').first().data('timestamp');
    }
    
    // ajax call
    $.ajax({
        url: '@@ajax-activities',
        data: {
            action: 'get_latest_comments',
            timestamp: timestamp
        },
        dataType: 'json',
        // event handler success
        success: $.proxy(function(response) {
            if(response.length > 0) {
            	$.each(response, $.proxy(function(i, val) {
            		var $assignedActivity = $('#' + val.activity_id);
            		
            		response[i]['timestr'] = this.TimeConverter.convertTime(val.timestamp);
            		
            		if(typeof response[i]['revision'] !== 'number') {
                    	response[i]['revision'] = 0;
                    }
            		
            		if(this.getOption('moderatable', 'settings') && $assignedActivity.data('content-creator') === this.getCache('userId')) {
            			response[i]['can_delete'] = true;
            			response[i]['can_moderate'] = true;
            		}
            		
            		response[i]['revision_old'] = parseInt($('#' + response[i]['activitiy_id']).data('revision')) > response[i]['revision'];
            	}, this));
            	
                // render
                this.renderComments(response);
            }
        }, this)
    });
};


/**
 * render the data to the activity stream
 *
 * @param array data
 * @param string state
 * @param mixed initial
 * @return void
 */
ActivityStream.prototype.renderActivities = function(data, state, initial) {
    var activityList = this.getOption('activityList', 'selector'),
        $activityTmpl = $(this.getOption('activity', 'template'));
        
    var speedDown = this.getOption('speedDown', 'animation'),
        speedUp = this.getOption('speedUp', 'animation');
    
    $.each(data, $.proxy(function(i, val) {
    	if($('#' + val.id).length > 0) {
    		$('#' + val.id).remove();
    	}
    	
    	$.each(val.comments, $.proxy(function(k, comment) {
    		comment.ownComment = comment.user_id === this.getCache('userId');
    	}, this));
    }, this));

    if(state === 'get_latest_activities') {
        if(initial) {
            // no animations if initial call
            $($activityTmpl.render(data)).prependTo(activityList);
            
            $(activityList).find('li.activity').each($.proxy(function(k, el) {
            	if($(el).find(this.getOption('commentList', 'selector')).find('li.older_revision').length) {
            		$(el).find('.comment-show').removeClass('hidden').show();
            	}
            }, this));
        } else {
            // add animations if live update
            $($activityTmpl.render(data)).prependTo(activityList).hide().addClass('new');
            
            if(this.getCache('followInstalled') && this.getOption('onlyFollowing')) {
                // follow IS installed and i want to show only the items of authors whom i follow
                $(activityList).find('li.activity.following').slideDown(speedDown, this.removeHighlight(this.getOption('removeHighlight', 'animation')));
            } else {
                // follow IS NOT installed, so show all
                $(activityList).find('li.activity').slideDown(speedDown, this.removeHighlight(this.getOption('removeHighlight', 'animation')));
            }
            
            $(activityList).find('li.activity').each($.proxy(function(k, el) {
            	if($(el).find(this.getOption('commentList', 'selector')).find('li.older_revision').length) {
            		$(el).find('.comment-show').removeClass('hidden').show();
            	}
            }, this));
        }
        
        // set latest activity timestamp (localStorage or cookie)
        this.storage.local.set('activitiesTimestamp', $(activityList).find('li.activity').first().data('timestamp'));
    } else {
        // get_more_activities
        $($activityTmpl.render(data)).appendTo(activityList).hide();
        
        if(this.getCache('followInstalled') && this.getOption('onlyFollowing')) {
            // follow IS installed and i want to show only the items of authors whom i follow
            $(activityList).find('li.activity.following').slideDown(speedDown);
        } else {
            // follow IS NOT installed, -> show all
            $(activityList).find('li.activity').slideDown(speedDown);
        }
    }
    
    // make textarea autogrowing
    $('.comment-textarea').autoGrow();
    
    // show 'get more' container
    $(this.getOption('wrapper', 'selector')).find(this.getOption('getMore', 'selector')).show();
    
    // our own comments are right sided, the comments of others are left sided
    /** @deprecated as of 17.06.14, this is now handled directly via tmpl */
    //this.markUsersComments();
    
    // bug fix
    $(this.getOption('wrapper', 'selector')).find(activityList).find('li').each(function() {
        $(this).css('overflow', '');
    });
    
    // Plone build-in function
    this.prepOverlay();
    
    this.hideSpinner();
};


/**
 * render the data to the comment lists
 *
 * @param array data
 * @return void
 */
ActivityStream.prototype.renderComments = function(data) {
    var commentList = this.getOption('commentList', 'selector'),
        $commentTmpl = $(this.getOption('comment', 'template'));
        
    var $wrapper = $(this.getOption('wrapper', 'selector')),
        $activityList = $wrapper.find(this.getOption('activityList', 'selector'));
        
    var speedDown = this.getOption('speedDown', 'animation');
    
    // start rendering
    $.each(data, $.proxy(function(index, value) {
        var $assignedActivity = $activityList.find('#' + value.activity_id);
        
        // render only if the assigned activity exists
        if($assignedActivity.length > 0) {
            var $assignedComment = $assignedActivity.find(commentList).find('#' + value.id);
            
            value.ownComment = value.user_id === this.getCache('userId');
            
            if($assignedComment.length > 0) {
                // comment already exists, just change date and text
                $assignedComment.data('timestamp', value.timestamp);
                $assignedComment.find('p.user-comment').html(value.comment.replace(/\n/g, '<br>'));
                $assignedComment.find('.user-information small').text(value.timestr);
                $assignedComment.addClass('new', this.removeHighlight(this.getOption('removeHighlight', 'animation'), $assignedComment));
            } else {
                var renderedElement = $commentTmpl.render(value),
                    id = $(renderedElement).attr('id');
            
                $(renderedElement)
                    .appendTo(this.getOption('activityList', 'selector') + ' #' + value.activity_id + ' ' + commentList)
                    .hide()
                    .addClass('new')
                    .slideDown(speedDown, this.removeHighlight(this.getOption('removeHighlight', 'animation'), $('#' + value.id)));
            }
            
            if(value.user_id === this.getCache('userId')) {
                //$('#' + value.id).addClass('self');
            }
        }
    }, this));
};


/**
 * simple helper to remove the new class on activities from live stream
 *
 * @return void
 */
ActivityStream.prototype.removeHighlight = function(delay, el) {
	if(undefined === el) {
		el = $(this.getOption('wrapper', 'selector')).find('.new');
	}
	
    setTimeout(function() {
        el.removeClass('new');
    }, delay);
};


/**
 * simple helper function to positioning users own comments
 *
 * @return void
 */
ActivityStream.prototype.markUsersComments = function() {
    $(this.getOption('wrapper', 'selector')).find('.activity-comment').each($.proxy(function(i, el) {
        if($(el).find('a[data-uid]').data('uid') === this.getCache('userId')) {
            //$('#' + $(el).attr('id')).addClass('self');
        	$(el).addClass('self');
        }
    }, this));
};


/**
 * save a new comment
 *
 * @param string comment
 * @param string parentId
 * @return void
 */
ActivityStream.prototype.saveComment = function(comment, parentId) {
    if(!comment || !parentId || $.trim(comment) === '') {
        return ;
    }
    
    var $el = $('#' + parentId),
        $button = $el.find('span.input-group-btn > button.comment-save');
    
    // disable button
    $button.removeClass('comment-save').addClass('disabled').find('i')
        .removeClass('fa-save')
        .addClass('fa-spin fa-spinner');
        
    // save
    $.ajax({
        url: '@@ajax-post-comment',
        data: {
            comment: $.trim(comment),
            id: parentId
        },
        dataType: 'json',
        // event handler success
        success: $.proxy(function(response) {
            if(response instanceof Object) {
                $el.find('.comment-textarea').val('');
                $el.find('.new-comment-container').hide();
                $el.find('.comment-controls').show();
                
                $button.addClass('comment-save').removeClass('disabled').find('i')
                    .addClass('fa-save')
                    .removeClass('fa-spin fa-spinner');
                    
                this.getComments();
            }
        }, this)
    });
};


//
// Event Handler Functions below
// -----------------------------------------------------------------------------

/**
 * event handler for switchting activity control buttons
 *
 * @param string state
 * @return void
 */
ActivityStream.prototype.activityControls = function(state) {
    var $wrapper = $(this.getOption('wrapper', 'selector')),
        controls = '.activity-controls',
        $controls = $wrapper.find(controls).length > 0 ? $wrapper.find(controls) : $(controls),
        $activity = $wrapper.find(this.getOption('activityList', 'selector')),
        $getMore = $wrapper.find(this.getOption('getMore', 'selector'));
        
    switch(state) {
        case 'activity-hide':
            $controls.find('.show-all').removeClass('hidden').show();
            if($activity.find('li.activity:visible').length <= 1) {
                $controls.find('.hide-all').hide();
                $getMore.hide();
            }
            break;
        case 'activity-hide-all':
            $getMore.hide();
            
            $controls.find('.show-all').removeClass('hidden').show();
            $controls.find('.hide-all').hide();
            break;
        case 'activity-show':
            $controls.find('.hide-all').show();
            if($activity.find('li.activity:not(:visible)').length <= 0) {
                $controls.find('.show-all').hide();
            }
            break;
        case 'activity-show-all':
            $getMore.show();
            
            $controls.find('.hide-all').show();
            $controls.find('.show-all').hide();
            break;
    }
};


/**
 * Plone build-in modal dialog and image preview
 *
 * @return void
 */
ActivityStream.prototype.prepOverlay = function() {
    $('.Image .linked-document, .linked-document').prepOverlay({
        subtype: 'ajax',
        width: '500px',
        height: '50px',
        config: {
            onLoad: $.proxy(function(e) {
                this.prepContentViews();
            }, this)
        }
    });
};


/**
 * Event Handler and Content for Plone build-in modal dialog and image preview
 *
 * @return void
 */
ActivityStream.prototype.prepContentViews = function() {
    var $el = $('.show-preview #content-views').children(),
        color = 'text-primary';

    $el.on('click', function(e) {
        var url = $(this).find('a').attr('href');
        
        if(url) {
            window.location = url;
        }
    });
    
    $el.each(function() {
        var menu_context = $(this).find('a').html();
        
        $(this).prepend('<div class="content-view-box"/>');
        $(this).find('.content-view-box').html(menu_context);
        $(this).find('a').html('');
        
        if(!$(this).hasClass('selected')) {
            $(this).find('.content-view-box').addClass(color);
        }
    });
    
    $el.hover(function() {
        if($(this).find('.content-view-box').html().length > 1) {
            var $contentViewBox = $(this).find('.content-view-box');
        
            $contentViewBox
                .removeClass(color)
                .find('.text').show();
        }
    }, function() {
        var $contentViewBox = $(this).find('.content-view-box');
        
        if(!$(this).hasClass('selected')) {
            $contentViewBox.addClass(color);
        }
        
        $contentViewBox.find('.text').hide();
    });
};





//
// Event Handler Functions below
// -----------------------------------------------------------------------------


/**
 * Click, mouse and scroll event handler for activity stream
 */
ActivityStream.prototype.initEventHandler = function() {
    var speedDown = this.getOption('speedDown', 'animation'),
        speedUp = this.getOption('speedUp', 'animation');

    var wrapper = this.getOption('wrapper', 'selector'),
        $activityList = $(wrapper).find(this.getOption('activityList', 'selector'));

    // hide a single activity
    $(wrapper).on('click', 'li.activity .activity-hide', $.proxy(function(e) {
        e.preventDefault();
        
        var $el = $(e.currentTarget);
        
        $activityList.find($el.data('parent-id'))
            .slideUp(speedUp, this.activityControls('activity-hide'));
    }, this));
    
    
    // hide all activities
    $('.activity-controls').on('click', '.hide-all', $.proxy(function(e) {
        e.preventDefault();
        
        $activityList.find('li.activity').slideUp(speedUp);
        
        this.activityControls('activity-hide-all');
    }, this));
    
    
    // show all activities
    $('.activity-controls').on('click', '.show-all', $.proxy(function(e) {
        e.preventDefault();
        
        $activityList.find('li.activity').slideDown(speedDown);
        
        this.activityControls('activity-show-all');
    }, this));
    
    
    // show textarea writing comment
    $(wrapper).on('click', 'li.activity .comment-write', $.proxy(function(e) {
        e.preventDefault();
        
        var $el = $(e.currentTarget),
            $parentEl = $($el.data('parent-id'));
        
        $activityList.find('li.activity').each(function() {
            $(this).find('.comment-input-group').hide();
            $(this).find('.comment-textarea').val('');
            $(this).find('.comment-write').show();
        });
        
        $parentEl.find('.comment-write').hide();
        $parentEl.find('.comment-input-group').removeClass('hidden').show();
        
        this.Clipboard.addPasteControls();
    }, this));
    
    
    // save comment
    $(wrapper).on('click', 'li.activity .comment-save', $.proxy(function(e) {
        e.preventDefault();
        
        var $el = $(e.currentTarget),
            $li = $($el.data('parent-id'));
            
        this.saveComment($li.find('textarea').val(), $el.data('parent-id').split('#')[1]);
    }, this));
    
    
    // hide comment
    $(wrapper).on('click', 'li.activity .comment-hide', $.proxy(function(e) {
        e.preventDefault();
        
        var $el = $(e.currentTarget)
            $li = $($el.data('parent-id')),
            $assignedActivity = $li.parents('li.activity');
            
        $li.slideUp(speedUp);
        
        $assignedActivity.find('.comment-show').removeClass('hidden').show();
    }, this));
    
    
    // show comments
    $(wrapper).on('click', 'li.activity .comment-show', $.proxy(function(e) {
        e.preventDefault();
        
        var $activity = $(e.currentTarget).parents('li.activity');
        
        $activity.find(this.getOption('commentList', 'selector')).find('li').slideDown(speedDown, function() {
        	$(this).css('display', 'list-item'); // TODO: unschoen...
        });
        
        $(e.currentTarget).hide();
    }, this));
    
    $(wrapper).on('click', 'li.activity .comment-delete', $.proxy(function(e) {
    	e.preventDefault();
    	
    	var $el = $(e.currentTarget),
    		$li = $($el.data('parent-id')),
    		$activity = $(e.currentTarget).parents('li.activity'),
    		activity_id = $activity.attr('id'),
    		comment_id = $li.attr('id');
    	
    	$.ajax({
    		url: '@@ajax-activities',
    		data: {
    			action: 'delete_comment',
    			comment_id: comment_id,
    			content_uid: activity_id
    		},
    		dataType: 'json',
    		success: $.proxy(function(response) {
    			$li.slideUp(speedUp, function() {
    				$li.remove();
    			});
    		}, this)
    	});
    }, this));
    
    $(wrapper).on('click', 'li.activity .comment-moderate', $.proxy(function(e) {
    	e.preventDefault();
    	
    	var $el = $(e.currentTarget),
    		$li = $($el.data('parent-id')),
    		$activity = $(e.currentTarget).parents('li.activity'),
    		activity_id = $activity.attr('id'),
    		comment_id = $li.attr('id');
    	
    	var state = $el.hasClass('activate') ? 'activate' : 'deactivate';
    	
    	// add spinner
    	$el.addClass('disabled').find('i').removeClass().addClass('fa fa-spinner fa-spin');
    	
    	$.ajax({
    		url: '@@ajax-activities',
    		data: {
    			action: state + '_comment',
    			comment_id: comment_id,
    			content_uid: activity_id
    		},
    		dataType: 'json',
    		success: $.proxy(function(response) {
				if(response === true) {
					if(state === 'activate') {
						$el.removeClass('activate').addClass('deactivate');
						$li.removeClass('not-activated').addClass('activated');
						
						$el.removeClass('disabled').find('i').removeClass().addClass('fa fa-eye-slash');
					} else {
						$el.removeClass('deactivate').addClass('activate');
						$li.removeClass('activated').addClass('not-activated');
						
						$el.removeClass('disabled').find('i').removeClass().addClass('fa fa-eye');
					}
				} else {
					$el.removeClass('disabled').find('i').removeClass().addClass('fa fa-eye' + (state === 'activate' ? '' : '-slash'));
				}
    		}, this),
    		error: $.proxy(function(a,b,c) {
    			console.log(a,b,c);
    			
    			$el.removeClass('disabled').find('i').removeClass().addClass('fa fa-eye' + (state === 'activate' ? '' : '-slash'));
    		}, this)
    	});
    }, this));
    
    
    
    // Thumbnail preview mouse handler
    //$(wrapper).find('li.activity a.user-message').hoverIntent($.proxy(this.showThumbnailPreview, this), $.proxy(this.hideThumbnailPreview, this));
    $(wrapper).on({
    	mouseenter: $.proxy(function(e) {
    		this.showThumbnailPreview(e);
    	}, this),
    	mouseleave: $.proxy(function(e) {
    		this.hideThumbnailPreview(e);
    	}, this)
    }, 'li.activity a.user-message');
    
    
    // follow -- only when follow is intalled
    if(this.getCache('followInstalled')) {
        var container = this.getOption('followContainer', 'selector');
    
        $(container).on('click', 'a', $.proxy(function(e) {
            e.preventDefault();
        
            var $el = $(e.currentTarget);
            
            $(container).find('li').removeClass('active');
            $el.parents('li').addClass('active');
            
            if($el.hasClass('astream-tab-all')) {
                $('li.activity').slideDown(speedDown);
            } else {
                $('li.activity.not-following').slideUp(speedUp);
                $('li.activity.following').slideDown(speedDown);
                
                if($('li.activity.following').length < 5) {
                    this.getActivities('get_more_activities');
                }
            }
        }, this));
    }
    
    
    // loading on scroll
    $(window).on('scroll', $.proxy(function(e) {
        var $wrapper = $(this.getOption('wrapper', 'selector')),
            $lastActivity = $wrapper.find(this.getOption('activityList', 'selector')).find('li.activity:last'),
            $getMoreActivities = $wrapper.find(this.getOption('getMore', 'selector'));
            
        if($lastActivity.length > 0 && $getMoreActivities.is(':in-viewport') && $getMoreActivities.is(':visible')) {
            $getMoreActivities.hide();
            
            this.getActivities('get_more_activities');
        } else if($getMoreActivities.is(':in-viewport') && $getMoreActivities.is(':visible') && this.getCache('currentView') === 'userprofile' && this.getCache('initUserprofile') === false) {
            this.setCache('initUserprofile', true);
            
            this.getActivities('get_more_activities', true);
        }
    }, this));
};


/**
 * show thumbnail preview on mouseover (link)
 *
 * @param object e
 * @return void
 */
ActivityStream.prototype.showThumbnailPreview = function(e) {
    var $el = $(e.currentTarget);
    
    var $thumbnailPreview = $el.parents('.well').find('.thumbnail-preview'),
        $thumbnail = $thumbnailPreview.find('img.lazy');
        
    if($thumbnail.attr('src') === undefined || $thumbnail.attr('src') !== $thumbnail.data('original')) {
        $thumbnail.attr('src', $thumbnail.data('original'));
    }
    
    $thumbnailPreview.fadeIn(10);
};


/**
 * hide thumbnail preview on mouseleave link or mouseleave thumbnailpreview
 *
 * @param object e
 * @return void
 */
ActivityStream.prototype.hideThumbnailPreview = function(e) {
    var $el = $(e.currentTarget);
    
    var $thumbnailPreview = $el.parents('.well').find('.thumbnail-preview'),
        $thumbnail = $thumbnailPreview.find('img.lazy');

    setTimeout(function() {
        if(!$thumbnailPreview.is(':hover')) {
            $thumbnailPreview.fadeOut(100);
            
            return ;
        }
    
        $thumbnailPreview.mouseleave(function() {
            $thumbnailPreview.fadeOut(100);
        });
    }, 100);
};




ActivityStream.prototype.sort = function(data, direction) {
    var tmp = data.sort(function(a, b) {
        a = (new Date(a['timestamp'])).getTime();
        b = (new Date(b['timestamp'])).getTime();
    
        return a-b;
    });
    
    if('desc' === direction) {
        tmp.reverse();
    }
    
    return tmp;
};