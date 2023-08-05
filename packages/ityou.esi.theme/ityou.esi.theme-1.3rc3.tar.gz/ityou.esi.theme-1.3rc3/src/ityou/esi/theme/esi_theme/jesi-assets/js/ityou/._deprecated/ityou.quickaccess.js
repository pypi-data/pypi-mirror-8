(function($, window, document, _, undefined) {
	'use strict';
	
	window.ityouQuickAccess = {
		name: 'ityou.quickaccess',
		version: '0.1.1',
		settings: {
			imessage: {
				selector: '.qa-imessage'
			},
			activities: {
				selector: '.qa-activities'
			}
		},
		cache: {},
		_notify: function(state, timestamp) {
			var self = this;
			
			$.getJSON(_.settings.remote + '@@ajax-notify' + _.settings.callback, {action: state, timestamp: timestamp}, function(response) {
				self._notify_render(state, response);
			});
		},
		_notify_render: function(state, numbr) {
			if(state == 'count_latest_messages') {
				if(numbr != undefined && numbr > 0) {
					$(this.cache.current_page).find(this.settings.imessage.selector).find('span.badge').text(numbr);
				} else {
					$(this.cache.current_page).find(this.settings.imessage.selector).find('span.badge').text('');
				}
			} else if(state == 'count_latest_activities') {
				if(numbr != undefined && numbr > 0) {
					$(this.cache.current_page).find(this.settings.activities.selector).find('span.badge').text(numbr);
				} else {
					$(this.cache.current_page).find(this.settings.activities.selector).find('span.badge').text('');
				}
			}
		},
		_notify_activities: function() {
			this.cache.current_date = new Date();
			this.cache.current_timestamp =
				this.cache.current_date.getFullYear() + '-' + 
				((this.cache.current_date.getMonth()+1) < 10 ? '0' : '') + (this.cache.current_date.getMonth()+1) + '-' +
				(this.cache.current_date.getDate() < 10 ? '0' : '') + this.cache.current_date.getDate() + ' ' +
				(this.cache.current_date.getHours() < 10 ? '0' : '') + this.cache.current_date.getHours() + ':' +
				(this.cache.current_date.getMinutes() < 10 ? '0' : '') + this.cache.current_date.getMinutes() + ':' +
				(this.cache.current_date.getSeconds() < 10 ? '0' : '') + this.cache.current_date.getSeconds() + '.' +
				this.cache.current_date.getMilliseconds();
			
			var timestamp = _.cache.activities_timestamp == undefined || _.cache.activities_timestamp == null || _.cache.activities_timestamp == '' ? this.cache.current_timestamp : _.cache.activities_timestamp;
			
			this._notify('count_latest_activities', timestamp)
		},
		_notify_imessage: function() {
			this._notify('count_latest_messages');
		},
		_run_interval: function() {
			var self = this;
			
			this.cache.current_page = window.location.hash;
			
			this.cache.interval = setInterval(function() {
				self._stop_interval();
				
				if(self.cache.interval != null) {
					self._notify_activities();
					self._notify_imessage();
				}
			}, 2500);
		},
		_stop_interval: function() {
			var self = this;
			
			if(this.cache.interval != undefined || this.cache.interval != null) {
				if($(this.cache.current_page).find(self.settings.activities.selector).length == 0 || $(this.cache.current_page).find(self.settings.imessage.selector).length == 0) {
					clearInterval(this.cache.interval);
					
					this.cache.interval == null;
				}
			}
		},
		init: function() {
			var self = this;
			
			if(self.cache.registered == undefined || self.cache.registered == false) {
				// Event Handler
			}
			
			if($.fn.ityouActivityStream instanceof Function) {
				_.cache.activities_timestamp = window.localStorage.getItem('activities_timestamp');
			}
			
			this.cache.current_page = window.location.hash;
			
			// initial call and then interval
			self._notify_activities();
			self._notify_imessage();
			self._run_interval();
			
			// register plugin
			self.cache.registered = true;
		}
	};
	
	$.fn.ityouQuickAccess = function(opts) {
		var _self = ityouQuickAccess;
		
		if(opts instanceof Object) {
			$.extend(_self.settings, opts);
		}
		
		_self.init();
	}
}(jQuery, this, this.document, this.ityou));
