(function($, window, document, _, _r, undefined) {
	'use strict';
	
	window.ityouUser = {
		name: 'ityou.User',
		version: '0.1.1',
		settings: {
			wrapper_user_list: '#user',
			wrapper_user_profile: '#user-profile',
			input_search_user: 'input[name="search_user"]',
			keyTimeout: 500,
			container: {
				user_list_view: '.table-user-list-view > tbody',
				user_profile: '.user-profile-container'
			},
			template: {
				user_list_view: '#user-table-list-view-template',
				user_profile: '#user-profile-template'
			}
		},
		cache: {},
		_search_user: function(string) {
			var self = this,
				spinner_position = $.trim(self.settings.container.user_list_view.split('>')[0]);
			
			this.cache.resetView = true;
			
			// clear result list
			$(self.settings.container.user_list_view).empty();
			
			// show spinner
			_._show_content_spinner(self.settings.wrapper_user_list + ' ' + spinner_position + ' tfoot td', 64);
			
			$.getJSON(_.settings.remote + '@@ajax-users' + _.settings.callback, {action: 'query', q: string, l: 20}, function(response) {
				if(response.length > 0) {
					response = _._correct_json_urls(response);
					
					// insert new results
					self.cache.userdata = [];
					
					$.each(response, function(k, val) {
						var singledata = {
							portrait: val.portrait,
							fullname: val.name,
							position: val.position,
							phone_number: val.phone,
							location: val.location,
							last_login: val.last_login,
							last_login_timestamp: val.last_login_timestamp,
							id: val.id
						};
						
						self.cache.userdata.push(singledata);
					});
					
					$.each(self.cache.userdata, function(k, val) {
						$($(self.settings.template.user_list_view).render(val)).appendTo(self.settings.container.user_list_view);
					});
				} else {
					$(self.settings.container.user_list_view).html('<tr><td colspan="6">0</td></tr>')
				}
				
				// hide spinner
				_._hide_content_spinner();
			});
		},
		_load_user_list: function() {
			var self = this,
				spinner_position = $.trim(self.settings.container.user_list_view.split('>')[0]);
			
			this.cache.resetView = false;
			
			_._show_content_spinner(self.settings.wrapper_user_list + ' ' + spinner_position + ' tfoot td', 64);
			
			$.getJSON(_.settings.remote + '@@ajax-users-datatable' + _.settings.callback, {raw: true}, function(response) {
				self.cache.userdata = [];
				
				$.each(response.aaData, function(k, val) {
					var singledata = {
						portrait: val[0],
						fullname: val[1],
						position: val[2],
						phone_number: val[3],
						location: val[4],
						last_login: val[5][1],
						last_login_timestamp: val[5][0],
						id: val[6]
					};
					
					self.cache.userdata.push(singledata);
				});
				
				self.cache.userdata = _._correct_json_urls(self.cache.userdata);
				
				$.each(self.cache.userdata, function(k, val) {
					$($(self.settings.template.user_list_view).render(val)).appendTo(self.settings.container.user_list_view);
				});
				
				// hide spinner
				_._hide_content_spinner();
			});
		},
		_load_user_profile: function(uid) {
			var self = this;
			
			// show spinner
			_._show_content_spinner(self.settings.wrapper_user_profile + ' #content', 64);
			
			$.getJSON(_.settings.remote + '@@ajax-personal-profile' + _.settings.callback, {action: 'userprofile', uid: uid}, function(response) {
				response = _._correct_json_urls(response);
				response.description = _._n_to_br(response.description);
				
				if(_.cache.user_id != null && _.cache.user_id == uid) {
					$.extend(response, {own_profile:true});
				}
				
				// pagechange
				window.location.hash = _r.routes.user_profile;
				
				self.cache.untilPageChange = setInterval(function() {
					if($(self.settings.template.user_profile).length > 0) {
						clearInterval(self.cache.untilPageChange);
						
						setTimeout(function() {
							$($(self.settings.template.user_profile).render(response)).appendTo(self.settings.container.user_profile);
							
							setTimeout(function() {
								$(_r.routes.user_profile).find('.page-header').find('small').text(response.fullname);
								
								// remove spinner
								_._hide_content_spinner();
								
								$(self.settings.container.user_profile).find('img').each(function() {
									$(this).addClass('img-responsive');
								});
								
								if(_.cache.user_id == uid) {
									$(self.settings.container.user_profile).find('td:not(:first-child)').each(function() {
										$(this).addClass('editable');
									});
								}
							},1);
						},1);
					}
				},100);
			});
		},
		_editable_standard_view: function() {
			var self = this;
			
			$(self.settings.container.user_profile).find('td.editable').each(function() {
				$(this).removeClass('active').find('.input-group').remove();
				$(this).find('span').not('.input-group-addon').show();
				$(this).find('i[class*="icon-"]').show();
			});
		},
		_editable: function(el, tag, type, value) {
			var self = this;
			
			// reset each cell
			this._editable_standard_view();
			
			el.find('span').not('[class*="input-group"]').hide();
			el.find('i[class*="icon-"]').hide();
			
			if(type == 'textarea') {
				el
					.addClass('active')
					.prepend('<div class="input-group">' +
								'<textarea name="'+tag+'" id="'+tag+'" class="form-control">'+_._br_to_n(value)+'</textarea>' +
								'<span class="input-group-btn">' +
									'<button type="button" data-id="'+tag+'" class="btn btn-default icon-save save-edit"></button>' +
									'<button type="button" data-id="'+tag+'" class="btn btn-default icon-remove cancel-edit"></button>' +
								'</span>' +
							'</div>');
				
				$('textarea').autogrow();
			} else if(type.split('-')[0] == 'input') {
				el
					.addClass('active')
					.prepend('<div class="input-group">' +
							  	'<input type="'+(type.split('-')[1])+'" name="'+tag+'" id="'+tag+'" value="'+value+'" class="form-control" />' +
							  	'<span class="input-group-btn">' +
							  		'<button type="button" data-id="'+tag+'" class="btn btn-default icon-save save-edit"></button>' +
							  		'<button type="button" data-id="'+tag+'" class="btn btn-default icon-remove cancel-edit"></button>' +
						  		'</span>' +
						  	'</div>');
			}
			
			el.find('input, textarea').focus();
		},
		_editable_save_attr: function(el, tag, value) {
			var self = this;
			
			el.removeClass('save-edit icon-save').css('cursor','default').html('<img src="img/spinner64.gif" width="16" />');
			
			$.getJSON(_.settings.remote + '@@ajax-user-property' + _.settings.callback, {action: 'set-property', id: tag, value: value}, function(response) {
				if(response == value) {
					$(self.settings.container.user_profile).find('[data-tag="'+tag+'"]').find('span').not('.input-group-addon').html(_._n_to_br(response));
				}
				
				self._editable_standard_view();
			});
		},
		init: function() {
			var self = this;
			
			if(self.cache.registered == undefined || self.cache.registered == false) {
				// Event handler keyboard input
				$(document).on('keyup', self.settings.input_search_user, function(e) {
					if($(this).val().length >= 2) {
						var _input = $(this);
						
						if(self.cache.keyTimeout) {
							clearTimeout(self.cache.keyTimeout);
						}
						
						self.cache.keyTimeout = setTimeout(function() {
							if(_input.val().length >= 2) {
								self._search_user(_input.val());
							} else {
								self._load_user_list();
							}
						}, self.settings.keyTimeout);
					} else {
						if(self.cache.resetView == true) {
							$(self.settings.container.user_list_view).empty();
							self._load_user_list();
						}
					}
				});
				
				// Event handler clear input
				$(document).on('click', '.search-user .close', function(e) {
					e.preventDefault();
					
					$(self.settings.input_search_user).val('').trigger('keyup');
				});
				
				// Event handler user-profile
				$(document).on('click', '.go-to.user-profile', function(e) {
					e.preventDefault();
					
					self.cache.current_uid = $(this).attr('data-uid');
					
					self._load_user_profile($(this).attr('data-uid'));
				});
				
				// event handler editable
				$(document).on('click', self.settings.container.user_profile + ' .editable:not(.active)', function() {
					if($(this).attr('data-type') == 'textarea') {
						self._editable($(this), $(this).attr('data-tag'), $(this).attr('data-type'), $(this).find('span').html());
					} else {
						self._editable($(this), $(this).attr('data-tag'), $(this).attr('data-type'), $(this).find('span').text());
					}
				});
				
				// event handler cancel edit
				$(document).on('click', self.settings.container.user_profile + ' .cancel-edit', function() {
					self._editable_standard_view();
				});
				
				// event handler save edit
				$(document).on('click', self.settings.container.user_profile + ' .save-edit', function() {
					var value = $.trim($('#'+$(this).attr('data-id')).val());
					
					if(value == $.trim($(self.settings.container.user_profile).find($('[data-tag="'+$(this).attr('data-id')+'"]')).find('span').not('.input-group-addon').text())) {
						self._editable_standard_view();
					} else {
						self._editable_save_attr($(this), $(this).attr('data-id'), value);
					}
				});
			}
			
			self._load_user_list();
			
			// register plugin
			self.cache.registered = true;
		}
	};
	
	$.fn.ityouUser = function(opts) {
		var _self = ityouUser;
		
		if(opts instanceof Object) {
			$.extend(_self.settings, opts);
		}
		
		_self.init();
	}
}(jQuery, this, this.document, this.ityou, this.ityouRouter));
