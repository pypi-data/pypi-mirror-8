(function($, window, document, _, undefined) {
	'use strict';
	
	window.ityouActivityStream = {
		name: 'ityou.activity-stream',
		version: '0.1.6',
		settings: {
			animationSpeedDown: 400,
			animationSpeedUp: 200,
			animationRemoveHighlight: 1500,
			wrapper: '#activity-stream',
			get_more_activities: '.get-more-activities',
			activity_container: 'ul#activity-stream-list',
			comment_container: 'ul.activity-comment-list',
			activity_template: '#activity-stream-template',
			comment_template: '#comment-stream-template'
		},
		cache: {},
		_activity_controls: function(state) {
			var self = this,
				controls = $(self.settings.wrapper).find('.activity-controls'),
				activity = $(self.settings.activity_container);
			
			switch(state) {
				case 'activity-hide':
					controls.find('.show-all').show();
					if(activity.find('li:visible').length <= 0) {
						controls.find('.hide-all').hide();						
					}
					break;
				case 'activity-hide-all':
					$(self.settings.get_more_activities).hide();
					
					controls.find('.show-all').show();
					controls.find('.hide-all').hide();
					break;
				case 'activity-show':
					controls.find('.hide-all').show();
					if(activity.find('li:not(:visible)').length <= 0) {
						controls.find('.show-all').hide();
					}
					break;
				case 'activity-show-all':
					$(self.settings.get_more_activities).show();
					
					controls.find('.hide-all').show();
					controls.find('.show-all').hide();
					break;
			}
		},
		_get_activities: function(state) {
			var self = this,
				timestamp = null;
			
			self._stop_running_interval();
			
			if(state === 'get_more_activities') {
				timestamp = $(self.settings.wrapper).find(self.settings.activity_container).find('li.activity').last().attr('data-timestamp');
				_._show_content_spinner(self.settings.wrapper + ' #content', 32);
			} else if(state === 'get_latest_activities') {
				timestamp = $(self.settings.wrapper).find(self.settings.activity_container).find('li.activity').first().attr('data-timestamp');
				
				// initial
				if(timestamp == undefined) {
					_._show_content_spinner(self.settings.wrapper + ' #content', 64);
				}
			}
			
			$.getJSON(_.settings.remote + '@@ajax-activities' + _.settings.callback, {action: state, timestamp: timestamp}, function(response) {
				if(response.length > 0) {
					response = _._correct_json_urls(response);
					
					// insert new activity
					if(state == 'get_latest_activities') {
						if(timestamp == undefined) {
							$($(self.settings.activity_template).render(response))
								.prependTo(self.settings.activity_container)
								.hide()
								.slideDown(self.settings.animationSpeedDown);
						} else {
							$($(self.settings.activity_template).render(response))
								.prependTo(self.settings.activity_container)
								.hide()
								.addClass('new')
								.slideDown(self.settings.animationSpeedDown, function() {
									self._removeHighlight($(this));
								});
						}
					} else if(state == 'get_more_activities') {
						$($(self.settings.activity_template).render(response))
							.appendTo(self.settings.activity_container)
							.hide()
							.addClass(self.settings.highlightNew)
							.slideDown(self.settings.animationSpeedDown);
					}
					
					$('textarea').autogrow();
					
					//$(self.settings.wrapper).find(self.settings.activity_container).find('li').first().attr('data-timestamp');
					window.localStorage.setItem('activities_timestamp', $(self.settings.wrapper).find(self.settings.activity_container).find('li').first().attr('data-timestamp'));
					_.cache.activities_timestamp = window.localStorage.getItem('activities_timestamp');
				}
				
				// remove spinner
				_._hide_content_spinner();
				
				// show loading more sector ... it's not really visible, but it has 2em space for triggering loading more
				$(self.settings.wrapper).find(self.settings.get_more_activities).show();
			});
		},
		_get_comments: function() {
			var self = this,
				timestamp = null,
				comment_timestamps = [];
			
			self._stop_running_interval();
			
			$(self.settings.comment_container).each(function() {
				$(this).find('li').each(function() {
					comment_timestamps.push($(this).attr('data-timestamp'));
				});
			});
			
			timestamp = comment_timestamps.sort().reverse()[0];
			
			$.getJSON(_.settings.remote + '@@ajax-activities' + _.settings.callback, {action: 'get_latest_comments', timestamp: timestamp}, function(response) {
				if(response.length > 0) {
					response = _._correct_json_urls(response);
					
					$.each(response, function(key, val) {
						// if comment hash exists, remove it from the DOM
						if($(self.settings.activity_container).find('#'+val.activity_hash).find(self.settings.comment_container).find('#'+val.hash).length > 0) {
							$(self.settings.activity_container).find('#'+val.activity_hash).find(self.settings.comment_container).find('#'+val.hash).remove();
						}
						
						// insert a new comment
						$($(self.settings.comment_template).render(val))
							.appendTo(self.settings.activity_container+' #'+val.activity_hash+' '+self.settings.comment_container)
							.hide()
							.addClass('new')
							.slideDown(self.settings.animationSpeedDown, function() {
								self._removeHighlight($(this));
							});
					});
				}
			});
		},
		_removeHighlight: function(el) {
			setTimeout(function() {
				el.removeClass('new');
			}, this.settings.animationRemoveHighlight);
		},
		_saveComment: function(comment, parent_id) {
			var self = this;
			
			if(comment == '' || comment == undefined || parent_id == undefined) {
				return;
			}
			
			$('#'+parent_id).find('textarea + span > .comment-save').removeClass('comment-save icon-save').css('cursor','default').html('<img src="img/spinner64.gif" width="16" />');
			
			$.getJSON(_.settings.remote + '@@ajax-post-comment' + _.settings.callback, {comment: comment, hash: parent_id}, function(response) {
				if(response instanceof Object) {
					$('#'+parent_id).find('textarea').val('');
					$('#'+parent_id).find('.new-comment-container').hide();
					$('#'+parent_id).find('.comment-controls').show();
					
					if(self.cache.comment_stream != undefined) {
						clearInterval(self.cache.comment_stream);
					}
					
					self._get_comments();
					self._run_interval_comment_stream();
				}
			});
		},
		_run_interval_activity_stream: function() {
			var self = this;
			
			if(self.cache.activity_stream != undefined) {
				clearInterval(self.cache.activity_stream);
			}
			
			if(_.settings.ASTREAM_ACTIVITY_DELAY != undefined) {
				self.cache.activity_stream = setInterval(function() {
					self._get_activities('get_latest_activities');
				}, _.settings.ASTREAM_ACTIVITY_DELAY);
			}
		},
		_run_interval_comment_stream: function() {
			var self = this;
			
			if(self.cache.comment_stream != undefined) {
				clearInterval(self.cache.comment_stream);
			}
			
			if(_.settings.ASTREAM_COMMENT_DELAY != undefined) {
				self.cache.comment_stream = setInterval(function() {
					self._get_comments();
				}, _.settings.ASTREAM_COMMENT_DELAY);
			}
		},
		_stop_running_interval: function() {
			var self = this;
			
			if(self.cache.activity_stream != undefined || self.cache.comment_stream != undefined) {
				if($(self.settings.wrapper).offset() != undefined && $(self.settings.wrapper).offset().left != 0) {
					clearInterval(self.cache.activity_stream);
					clearInterval(self.cache.comment_stream);
				} else if($(self.settings.wrapper).offset() == undefined) {
					clearInterval(self.cache.activity_stream);
					clearInterval(self.cache.comment_stream);
				}
			}
		},
		init: function() {
			var self = this;
			
			if(self.cache.registered == undefined || self.cache.registered == false) {
				// Event handler hide single activity
				$(document).on('click', 'li.activity .activity-hide', function(e) {
					e.preventDefault();
					
					$(self.settings.activity_container).find($(this).attr('data-parent-hash')).slideUp(self.settings.animationSpeedUp, function() {
						self._activity_controls('activity-hide');
					});
				});
				
				// Event handler show all activities
				$(document).on('click', 'div.activity-controls .show-all', function(e) {
					e.preventDefault();
					$(self.settings.activity_container).children().each(function() {
						$(this).slideDown(self.settings.animationSpeedDown)
					});
					self._activity_controls('activity-show-all');
				});
				
				// Event handler hide all activities
				$(document).on('click', 'div.activity-controls .hide-all', function(e) {
					e.preventDefault();
					$(self.settings.activity_container).children().each(function() {
						$(this).slideUp(self.settings.animationSpeedUp)
					});
					self._activity_controls('activity-hide-all');
				});
				
				// Event handler show comment box
				$(document).on('click', 'li.activity .comment-write', function(e) {
					e.preventDefault();
					$(self.settings.activity_container).children().each(function() {
						$(this).find('.new-comment-container').hide();
						$(this).find('textarea').val('');
						$(this).find('.comment-controls').show();
					});
					
					$($(this).attr('data-parent-hash')).find('.comment-controls').hide();
					$($(this).attr('data-parent-hash')).find('.new-comment-container').show();
				});
				
				// Event handler save comment
				$(document).on('click', 'li.activity .comment-save', function(e) {
					e.preventDefault();
					self._saveComment($($(this).attr('data-parent-hash')).find('textarea').val(), $(this).attr('data-parent-hash').split('#')[1]);
				});
				
				// Event handler hide comment
				$(document).on('click', 'li.activity .comment-hide', function(e) {
					e.preventDefault();
					$($(this).attr('data-parent-hash')).slideUp(self.settings.animationSpeedUp);
					
					var _this = $(this);
					$(self.settings.activity_container + ' > li').each(function() {
						if($(this).find(_this.attr('data-parent-hash')).length != 0) {
							$(this).find('.comment-show').show();
						}
					});
				});
				
				// Event handler show comments
				$(document).on('click', 'li.activity .comment-show', function(e) {
					e.preventDefault();
					$(self.settings.activity_container).find($(this).attr('data-parent-hash')).find(self.settings.comment_container).find('li').not(':visible').each(function() {
						$(this).slideDown(self.settings.animationSpeedDown);
					});
					
					$(this).hide();
				});
			}
			
			// scroll event
			$(window).on('scroll', function(e) {
				if($(self.settings.wrapper).is(':visible') && $(self.settings.wrapper).offset().left == 0) {
					if($(self.settings.wrapper).find(self.settings.get_more_activities).is(':in-viewport') && $(self.settings.wrapper).find(self.settings.get_more_activities).is(':visible')) {
						$(self.settings.wrapper).find(self.settings.get_more_activities).hide();
						
						self._get_activities('get_more_activities');
					}
				}
        	});
			
			// load Activity Stream and start streaming
			self._get_activities('get_latest_activities');
			self._run_interval_activity_stream();
			self._run_interval_comment_stream();
			
			
			// register plugin
			self.cache.registered = true;
		}
	};
	
	$.fn.ityouActivityStream = function(options) {
		var _self = ityouActivityStream;
		
		if(options instanceof Object) {
			$.extend(_self.settings, options);
		}
		
		_self.init();
	}
}(jQuery, this, this.document, this.ityou));