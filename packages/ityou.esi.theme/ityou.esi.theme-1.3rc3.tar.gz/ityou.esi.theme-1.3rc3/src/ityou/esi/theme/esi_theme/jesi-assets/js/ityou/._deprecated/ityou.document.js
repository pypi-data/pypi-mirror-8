(function($, window, document, _, _r, undefined) {
	'use strict';
	
	window.ityouDocument = {
		name: 'ityou.document',
		version: '0.1.6',
		settings: {
			wrapper_doc_list: '#doc-list',
			wrapper_doc_content: '#doc-content',
			animationSpeed: 200,
			document_link: '.document-link',
			input_search_doc: 'input[name="search_document"]',
			keyTimeout: 500,
			basicView: 'File',
			eventHandler: {
				collapse_information: '.toggle-additional-information',
				document_download: '.document-download',
				document_fullview: '.document-fullview',
				document_preview: '.document-preview',
				keyChangedInput: 'state-changed'
			},
			template: {
				doc_list_result_list: '#doc-list-result-list-template',
				doc_list_dialog_content: '#doc-list-dialog-content-template',
				doc_content: '#doc-content-template'
			},
			container: {
				doc_list_result_list: '.search-document-result-list',
				doc_list_result_count: '.search-document-result-count',
				doc_list_additional_information: '.additional-information',
				doc_list_dialog_content: '#doc-list-dialog',
				doc_content: '.doc-content'
			},
			dialog: {
				overlay: '.dialog-overlay',
				size: 0.8,
				thumbnailSize: 0.9
			}
		},
		cache: {},
		_search_document: function(string) {
			var self = this;
			
			this.cache.resetView = true;
			
			// clear result list
			$(self.settings.container.doc_list_result_list).empty();
			
			// show spinner
			_._show_content_spinner(self.settings.wrapper_doc_list + ' #content', 64);
			
			$.getJSON(_.settings.remote + '@@ajax-content' + _.settings.callback, {action: 'query', search_text: string}, function(response) {
				// set counting
				$(self.settings.container.doc_list_result_count).show().find('span').text(response.length);
				
				if(response.length > 0) {
					response = _._correct_json_urls(response);
					
					// insert new results
					$($(self.settings.template.doc_list_result_list).render(response)).appendTo(self.settings.container.doc_list_result_list);
					
					// replace images
					self._replace_portal_type_images(response);
				}
				
				// remove spinner
				_._hide_content_spinner();
			});
		},
		_load_latest: function(type) {
			var self = this;
			
			this.cache.resetView = false;
			
			// clear result list
			$(self.settings.container.doc_list_result_list).empty();
			
			if(type == undefined) {
				type = self.settings.basicView;
			}
			
			if(_.cache.inputval == undefined || _.cache.inputval.length < 2) {
				// show spinner
				_._show_content_spinner(self.settings.wrapper_doc_list + ' #content', 64);
				
				$.getJSON(_.settings.remote + '@@ajax-content' + _.settings.callback, {action: 'query', portal_type: type}, function(response) {
					if(response.length > 0) {
						// set counting
						$(self.settings.container.doc_list_result_count).show().find('span').text(response.length);
						
						response = _._correct_json_urls(response);
	
						$($(self.settings.template.doc_list_result_list).render(response)).appendTo(self.settings.container.doc_list_result_list);
						
						// replace images
						self._replace_portal_type_images(response);
					}
					
					// remove spinner
					_._hide_content_spinner();
				});
			} else {
				$(self.settings.input_search_doc).val(_.cache.inputval);
				
				self._search_document(_.cache.inputval);
			}
		},
		_replace_portal_type_images: function(obj) {
			$.each(obj, function(k, val) {
				if(val.type == 'Folder') {
					$('#'+val.uid).find('img.icon').attr('src', 'img/icon/folder.png');
				} else if(val.type == 'Document') {
					$('#'+val.uid).find('img.icon').attr('src', 'img/icon/document.png');
				} else if(val.type == 'Event') {
					$('#'+val.uid).find('img.icon').attr('src', 'img/icon/event.png');
				} else if(val.type == 'Link') {
					$('#'+val.uid).find('img.icon').attr('src', 'img/icon/link.png');
				} else if(val.type == 'File' || val.type == 'Image') {
					if($('#'+val.uid).find('img.icon').attr('src').substr(0, 4) != 'http') {
						$('#'+val.uid).find('img.icon').attr('src', _.settings.remote + $('#'+val.uid).find('img').attr('src'));
					}
				}
			});			
		},
		_get_document_preview: function(uid, url, title) {
			var self = this;
			
			$($(self.settings.template.doc_list_dialog_content).render({path: url, title: title})).appendTo(_.settings.container.mainContainer);
			$(self.settings.container.doc_list_dialog_content).modal();
		},
		_get_document_content: function(uid, search_string) {
			var self = this;
			
			// show spinner
			_._show_content_spinner(self.settings.wrapper_doc_content + ' #content', 64);
			
			$.getJSON(_.settings.remote + '@@ajax-content' + _.settings.callback, {action: 'get_object', uid: uid}, function(response) {
				if(response.type == 'Link') {
					self.cache.ref = window.open(response.link, '_blank', 'location=yes');
				} else {
					window.location.hash = _r.routes.doc_content;
					
					self.cache.untilPageChange = setInterval(function() {
						if($(self.settings.template.doc_content).length > 0) {
							clearInterval(self.cache.untilPageChange);
							setTimeout(function() {
								$($(self.settings.template.doc_content).render(response)).appendTo(self.settings.container.doc_content);
								
								// remove spinner
								_._hide_content_spinner();
								
								setTimeout(function() {
									$(self.settings.container.doc_content).find('img').each(function() {
										$(this).addClass('img-responsive');
									});
								},1);
							},1);
						}
					}, 100);
				}
			});
		},
		init: function() {
			var self = this;
			
			if(self.cache.registered == undefined || self.cache.registered == false) {
				// restore last search on back
				/*$(window).on('hashchange', function() {
					setTimeout(function() {
						if(window.location.hash == _r.routes.doc_list && _r.cache.cacheHistory[_r.cache.cacheHistory.length-2] == _r.routes.doc_content && _.cache.inputval != '') {
							$(ityouDocument.settings.input_search_doc).val(_.cache.inputval).trigger('keyup');
						} else if(window.location.hash == _r.routes.doc_content) {
							;
						} else {
							_.cache.inputval = "";
						}
					}, 1);
				});*/
				
				// Event handler keyboard input
				$(document).on('keyup', self.settings.input_search_doc, function(e) {
					if($(this).val().length >= 2) {
						var _input = $(this);
						
						if(self.cache.keyTimeout) {
							clearTimeout(self.cache.keyTimeout);
						}
						
						self.cache.keyTimeout = setTimeout(function() {
							if(_input.val().length >= 2) {
								_.cache.inputval = _input.val();
								self._search_document(_input.val());
							} else {
								self._load_latest();
								$(self.settings.container.doc_list_result_count).hide().find('span').text('0');
							}
						}, self.settings.keyTimeout);
					} else {
						if(self.cache.resetView == true) {
							$(self.settings.container.doc_list_result_count).hide().find('span').text('0');
							$(self.settings.container.doc_list_result_list).empty();
							//load latest documents using standard filetype
							self._load_latest();
						}
					}
				});
				
				// Event handler clear input
				$(document).on('click', '.search-document .close', function(e) {
					e.preventDefault();
					
					$(self.settings.input_search_doc).val('');
					_.cache.inputval = '';
					
					self._load_latest();
				});
				
				// Event handler click on document
				$(document).on('click', self.settings.container.doc_list_result_list+' '+self.settings.eventHandler.collapse_information, function(e) {
					e.preventDefault();
					var el = $('#'+$(this).attr('data-uid'));
					
					if(el.find(self.settings.container.doc_list_additional_information).is(':visible') == false) {
						$(self.settings.container.doc_list_result_list).find(self.settings.container.doc_list_additional_information+':visible').each(function() {
							$(this).slideToggle(self.settings.animationSpeed);
							$(this).parents('li').find('span.toggle-icon').removeClass('icon-angle-up').addClass('icon-angle-down');
						});
					}
					el.find(self.settings.container.doc_list_additional_information).slideToggle(self.settings.animationSpeed, function() {
						if(el.find('span.toggle-icon').hasClass('icon-angle-down')) {
							el.find('span.toggle-icon').removeClass('icon-angle-down').addClass('icon-angle-up');
							
							if(el.find('img.lazy').attr('src') != el.find('img.lazy').attr('data-original')) {
								$('img.lazy').show().lazyload({
									effect: 'fadeIn'
								});
							}
						} else {
							el.find('span.toggle-icon').removeClass('icon-angle-up').addClass('icon-angle-down');
						}
					});
					
					
				});
				
				// Event handler doc preview (open dialog)
				$(document).on('click', self.settings.container.doc_list_result_list+' '+self.settings.eventHandler.document_preview, function(e) {
					e.preventDefault();
					var uid = $(this).attr('data-uid'),
						url = $('#' + uid).attr('data-url'),
						title = $('#' + uid).attr('data-title');
					
					self._get_document_preview(uid, url, title);
				});
				
				// Event handler doc preview modal
				$(document).on('hidden.bs.modal', function() {
					$(self.settings.container.doc_list_dialog_content).remove();
				});
				
				// Event handler orientationchange/resize
				//$(window).on('resize orientationchange', self._rescale_document_preview_modal);
				
				// Event handler get document content
				$(document).on('click', self.settings.container.doc_list_result_list+' '+self.settings.eventHandler.document_fullview, function(e) {
					e.preventDefault();
					self._get_document_content($(this).attr('data-uid'), $(self.settings.input_search_doc).val());
				});
				
				// Event handler download
				$(document).on('click', self.settings.container.doc_list_result_list+' '+self.settings.eventHandler.document_download, function(e) {
					e.preventDefault();
					var el = $(this);
					
					$(this).ityouPhonegapFileTransfer({
						settings: {
							download_dom: self.settings.eventHandler.document_download,
							status_dom: '.download-status',
							parent: $('#'+el.attr('data-uid'))
						},
						cache: {
							path: $('#'+el.attr('data-uid')).attr('data-url')
						}
					});
				});
				
				// detect target
				$(document).on('click', self.settings.container.doc_list_result_list+' a', function(e) {
					if(_._hasAttr($(this), 'target') && self.attr('target') == '_blank') {
						self.cache.ref = window.open($('#'+$(this).attr('data-uid')).attr('data-url'), '_blank', 'location=yes');
					}
				});
			}
			
			
			// load latest view with standard file type
			self._load_latest();
			
			
			// register plugin
			self.cache.registered = true;
		}
	};
	
	$.fn.ityouDocument = function(opts) {
		var _self = ityouDocument;
		
		if(opts instanceof Object) {
			$.extend(_self.settings, opts);
		}
		
		_self.init();
	}
}(jQuery, this, this.document, this.ityou, this.ityouRouter));
