(function($, window, document, _, routing, undefined) {
	'use strict';
	
	window.ityouLogin = {
		name: 'ityou.login',
		version: '0.1.1',
		settings: {
			form: 'form[name="login"]',
			username: 'input#username',
			password: 'input#password'
		},
		cache: {},
		_login: function() {
			var self = this;
			$.getJSON(_.settings.remote + '@@ajax-login' + _.settings.callback, {username: $(self.settings.username).val(), password: $(self.settings.password).val()}, function(response) {
				if(response.login_success == 1) {
					_.cache.user_id = $(self.settings.username).val();
					
					$(self.settings.username + ', ' + self.settings.password).val('');
					
					$.getJSON(_.settings.remote + '@@ajax-personal-profile' + _.settings.callback, {action: 'whoami'}, function(response) {
						response = _._correct_json_urls(response);
						
						routing._set_user_id(response.user_id);
						routing._set_user_name(response.name);
						routing._set_user_portrait(response.portrait);
						
						window.location.hash = routing.routes.login_succeed;
					});
				} else {
					window.location.hash = routing.routes.login_failed;
				}
			});
		},
		init: function() {
			var self = this;
			
			$(document).on('submit', self.settings.form, function(e) {
				e.preventDefault();
				
				self._login();
				
				return false;
			});
		}
	};
	
	$.fn.ityouLogin = function(opts) {
		var _self = ityouLogin;
		
		if(opts instanceof Object) {
			$.extend(_self.settings, opts);
		}

		_self.init();
	}
}(jQuery, this, this.document, this.ityou, this.ityouRouter));
