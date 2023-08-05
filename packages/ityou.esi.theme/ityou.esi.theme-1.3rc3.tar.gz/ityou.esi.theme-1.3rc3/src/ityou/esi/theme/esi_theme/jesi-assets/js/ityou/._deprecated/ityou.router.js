(function($, window, document, _, undefined) {
	'use strict';
	
	window.ityouRouter = {
		name: 'ityou.router',
		version: '0.1.4',
		routes: {
			login: '#login',
			login_succeed: '#login-succeed',
			login_failed: '#login-failed',
			logout: '#logout'
		},
		settings: {
			firstRoute: '',
			container: $('body'),
			//tmplPath: 'tmpl/'
			tmplPath: '++theme++esi_theme/jesi-tmpl/'
		},
		cache: {
			stateHistory: [],
			currentPage: null,
			cacheHistory: []
		},
		_get_user_data: function() {
			var self = this;
			
			$.getJSON(_.settings.remote + '@@ajax-personal-profile' + _.settings.callback, {action: 'whoami'}, function(response) {
				response = _._correct_json_urls(response);
				
				self._set_user_id(response.user_id);
				self._set_user_name(response.name);
				self._set_user_portrait(response.portrait);
			});
		},
		_set_user_id: function() {
			_.cache.user_id = arguments[0];
		},
		_set_user_name: function() {
			_.cache.user_name = arguments[0];
		},
		_set_user_portrait: function() {
			_.cache.user_portrait = arguments[0];
		},
		valueInObject: function(needle, obj) {
			var foundKey = -1;
			
			$.each(obj, function(key, value) {
				if(needle == value) {
					foundKey = key;
					return;
				}
			});
			
			return foundKey;
		},
		route: function(event) {
			var self = ityouRouter,
				page,
				hash = window.location.hash,
				tmpl = hash == undefined || hash == '' ? 'login' : self.valueInObject(hash, self.routes);
			
			// hash found in routes, proceed
			if(tmpl != -1) {
				$.ajax({
					type: 'GET',
					dataType: 'html',
					url: self.settings.tmplPath + self.routes[tmpl].split('#')[1] + '.html',
					success: function(html) {
						page = html;
						
						// save page to history
						self.cache.cacheHistory.push(self.routes[tmpl]);
						
						// refresh user data
						self._get_user_data();
						
						// Page Transition
						self.slidePage($(page));
					},
					error: function() {
						console.log('failed to load template');
					}
				});
			} else {
				return;
			}
		},
		slidePage: function(page) {
			var l = this.cache.stateHistory.length,
				state = window.location.hash;
		
			if(l === 0) {
				this.cache.stateHistory.push(state);
				this.slidePageFrom(page);
				return;
			}
			
			if(state === this.cache.stateHistory[l-2]) {
				this.cache.stateHistory.pop();
				this.slidePageFrom(page, 'left');
			} else {
				this.cache.stateHistory.push(state);
				this.slidePageFrom(page, 'right');
			}
		},
		slidePageFrom: function(page, from) {
			if($(document).find('#'+page.attr('id')).length > 0) {
				$(document).find('#'+page.attr('id')).remove();
			}
			
			this.settings.container.append(page);
			
			if(!this.cache.currentPage || !from) {
				page.attr('class', 'page center');
				this.cache.currentPage = page;
				return;
			}
			
			page.attr('class', 'page ' + from);
			
			this.cache.currentPage.one('webkitTransitionEnd', function(e) {
				$(e.target).remove();
			});
			
			this.settings.container[0].offsetWidth;
			
			page.attr('class', 'page transition center');
			this.cache.currentPage.attr('class', 'page transition ' + (from === 'left' ? 'right' : 'left'));
			this.cache.currentPage = page;
			
			_._resize_content();
			_._show_login_name();
		}
	};
	
	$.fn.ityouRouter = function(opts) {
		var _self = ityouRouter;
		
		$(window).on('hashchange', _self.route);
		
		$(document).on('click', '.history-back', function(e) {
			e.preventDefault();
			window.history.back();
		});
		
		if(opts instanceof Object) {
			if(opts.routes instanceof Object) {
				$.extend(_self.routes, opts.routes);
			}
			
			if(opts.settings instanceof Object) {
				$.extend(_self.settings, opts.settings);
			}
		}
		
		if(_self.settings.firstRoute == '') {
			_self.settings.firstRoute = _self.routes.login;
		}
		
		$(window).trigger('hashchange');
	}
}(jQuery, this, this.document, this.ityou));
