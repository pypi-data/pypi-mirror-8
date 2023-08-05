(function($, window, document, undefined) {
	'use strict';
	
	window.ityou = {
		name: 'ityou',
		version: '0.1.3',
		settings: {
			callback: '?callback=?',
			remote: '',
			router: {},
			serverResponse: false,
			serverTimeout: 5000,
			container: {
				mainContainer: '#container'
			},
			ajax: {
				content_spinner: 'spinner128ccc.gif'
			}
		},
		viewport: {},
		cache: {
			user_id: null,
			user_name: null,
			user_portrait: null
		},
		_correct_json_urls: function(obj, root, path) {
			var self = this;
			
			if(root == undefined) {
				if(self.settings.ESI_ROOT == undefined) {
					return obj;
				} else {
					root = self.settings.ESI_ROOT;
				}
			}
			
			if(path == undefined) {
				if(self.settings.remote == undefined) {
					return obj;
				} else {
					path = self.settings.remote;
				}
			}
			
			if(obj instanceof Object) {
				$.each(obj, function(key, value) {
					if(obj.hasOwnProperty(key)) {
						if(value instanceof Object) {
							self._correct_json_urls(value, root, path);
						} else {
							obj[key] = self._replace(value, root, path);
						}
					}
				});
			}
			
			return obj;
		},
		_filtered_keys: function(obj, filter) {
			var key, keys = [];
			for(key in obj) {
				console.log(key);
				if(obj.hasOwnProperty(key) && key.match(filter)) {
					keys.push(key);
				}
			}
			return keys;
		},
		_new_array2d: function(size) {
			var temp = new Array(size);
			
			for(var i = 0; i < size; i++) {
				temp[i] = new Array();
			}
			
			return temp;
		},
		_replace: function(value, needle, haystack) {
			if(value == undefined || value == null)
				return;
			
			if(needle.match(/\/$/) == null && haystack.match(/\/$/) != null) {
				needle += '/'; 
			} else if(needle.match(/\/$/) != null && haystack.match(/\/$/) == null) {
				haystack += '/';
			}
			
			var replace = new RegExp(needle, 'gi');
			
			return value.toString().match(needle) ? value.replace(replace, haystack) : value;
		},
		__debug: function() {
			var output = '';
			if(typeof console == 'object') {
				for(var i = 0; i < arguments.length; i++) {
					output += arguments[i] + ' ';
				}
				
				console.log(output);
			}
		},
		_hasAttr: function(el, attr) {
			if(el.attr(attr) == undefined) {
				return false;
			} else {
				return true;
			}
		},
		_n_to_br: function(str) {
			return str.replace(/\r?\n/g, '<br />');
		},
		_br_to_n: function(str) {
			return str.replace(/\<br.*?\>/gi, "\n");
		},
		_show_content_spinner: function(parent, size) {
			var self = this;
			
			if(size == undefined) {
				size = 128;
			}
			
			var spinner = $('<div class="row content-spinner"><div class="col-xs-12 text-center"><img src="img/'+self.settings.ajax.content_spinner+'" width="'+size+'" /></div></div>');
			
			spinner.appendTo(parent);
		},
		_hide_content_spinner: function() {
			$(document).find('.content-spinner').each(function() {
				$(this).remove();
			});
		},
		_resize_content: function() {
			var current_page = window.location.hash;
			
			if($(current_page + ' #content').outerHeight() >= $(window).outerHeight()) {
				$('#container').css('height', $(current_page + ' #content').outerHeight() + $(current_page + ' header').outerHeight() + 50);
			} else {
				$('#container').css('height', '100%');
			}
		},
		_show_login_name: function() {
			var current_page = window.location.hash;
			
			if($(current_page + ' .navbar').find('.navbar-text.signed-in-as').length > 0) {
				$(current_page + ' .navbar').find('.navbar-text.signed-in-as').find('span').text(this.cache.user_name);
			}
		},
		init: function(routerOptions) {
			var self = this;
			
			$.getJSON(self.settings.remote + '@@ajax-esiparams' + self.settings.callback, {action: 'get_params'}, function(response) {
				$.extend(self.settings, response);
				
				self.settings.serverResponse = true;
				
				// Setting up Router
				$(document).ityouRouter(routerOptions);
				
				// Setting up LoginForm
//				$(document).ityouLogin();
			});
			
			self.cache.serverCheck = setInterval(function() {
				if(self.settings.serverResponse == true) {
					clearInterval(self.cache.serverCheck);
					clearTimeout(self.cache.serverCheckTimeout);
					
					$(document).trigger('ityouReady');
				}
			}, 1000);
			
			self.cache.serverCheckTimeout = setTimeout(function() {
				if(self.settings.serverResponse == false) {
					$('.page.loading').find('span.loading').text('Loading failed...');
					$('.page.loading').find('img.loading').attr('src', 'img/spinnerstop128.gif');
				}
			}, self.settings.serverTimeout);
			
			self.cache.resizeInterval = setInterval(function() {
				self._resize_content();
			}, 500);
			
			// resize/orientationchange
			window.addEventListener('orientationchange', function(e) {});
			window.addEventListener('resize', function(e) {});
			window.addEventListener('scroll', function(e) {});
			window.addEventListener('touchmove', function(e) {});
			window.addEventListener('ityouReady', function(e) {});
		}
	};
	
	$.fn.ityou = function(options, routerOptions) {
		var _self = ityou;
		
		if(options instanceof Object) {
			$.extend(_self.settings, options);
		}
		
		_self.init(routerOptions);
	}
}(jQuery, this, this.document));
