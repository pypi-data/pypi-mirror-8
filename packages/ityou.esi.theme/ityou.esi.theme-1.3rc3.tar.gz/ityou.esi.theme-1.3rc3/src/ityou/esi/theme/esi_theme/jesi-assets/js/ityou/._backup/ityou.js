(function($, window, document, undefined) {
	
	'use strict';
	
	window.ITYOU = {
		name: 'ityou',
		version: '0.2.0',
		
		cache: {
			serverResponse: false,
			userId: null
		},
		
		breakpoints: {
			xs: 480,
			small: 768,
			medium: 1280,
			large: 1440
		},
		
		settings: {
			storageMethod: 0, // 0 = localStorage, 1 = cookie
			backtotop: {},
			ajax: {
				remote: '',
				callback: '?callback=?',
				spinnerClass: 'content-spinner',
				timeout: 5000
			},
			selector: {
			    notifyAstream: '#link-to-astream',
			    notifyImessage: '#link-to-imessage'
		    }
		},
		
		libs: {},
		
		hoverClass: 'state-hover',
		activeClass: 'state-active',
		
		/** ----- STORAGE --------------------------------------------------
		 *
		 * USAGE:
		 * 
		 * window.ITYOU.storage.set(key, value, object = true/false)
		 * window.ITYOU.storage.get(key, object = true/false)
		 * window.ITYOU.storage.unset(key)
		 *
		 */
		storage: {
			ityou: function() {
				return window.ITYOU;
			},
			set: function(key, value, object) {
				if(this.ityou().libs.hasOwnProperty('storage')) {
					if(this.ityou().libs.storage.hasOwnProperty('set')) {
						this.ityou().libs.storage.set(key, value, object);
					} else {
						this.ityou().helper.log('No such property "set" in "storage"!');
					}
				} else {
					this.ityou().helper.log('No such property "storage" in "libs"!');
				}
				
				return;
			},
			get: function(key, object) {
				if(this.ityou().libs.hasOwnProperty('storage')) {
					if(this.ityou().libs.storage.hasOwnProperty('get')) {
						return this.ityou().libs.storage.get(key, object);
					} else {
						this.ityou().helper.log('No such property "get" in "storage"!');
					}
				} else {
					this.ityou().helper.log('No such property "storage" in "libs"!');
				}
				
				return;
			},
			unset: function(key) {
				if(this.ityou().libs.hasOwnProperty('storage')) {
					if(this.ityou().libs.storage.hasOwnProperty('remove')) {
						this.ityou().libs.storage.remove(key);
					} else {
						this.ityou().helper.log('No such property "unset" in "storage"!');
					}
				} else {
					this.ityou().helper.log('No such property "storage" in "libs"!');
				}
				
				return;
			}
		}, // - storage
		
		session: {
		    ityou: function() {
		        return window.ITYOU;
	        },
	        set: function(key, value, object) {
				if(this.ityou().libs.hasOwnProperty('sessionStorage')) {
					if(this.ityou().libs.sessionStorage.hasOwnProperty('set')) {
						this.ityou().libs.sessionStorage.set(key, value, object);
					} else {
						this.ityou().helper.log('No such property "set" in "sessionStorage"!');
					}
				} else {
					this.ityou().helper.log('No such property "sessionStorage" in "libs"!');
				}
				
				return;
			},
			get: function(key, object) {
				if(this.ityou().libs.hasOwnProperty('storage')) {
					if(this.ityou().libs.sessionStorage.hasOwnProperty('get')) {
						return this.ityou().libs.sessionStorage.get(key, object);
					} else {
						this.ityou().helper.log('No such property "get" in "sessionStorage"!');
					}
				} else {
					this.ityou().helper.log('No such property "sessionStorage" in "libs"!');
				}
				
				return;
			},
			unset: function(key) {
				if(this.ityou().libs.hasOwnProperty('storage')) {
					if(this.ityou().libs.sessionStorage.hasOwnProperty('remove')) {
						this.ityou().libs.sessionStorage.remove(key);
					} else {
						this.ityou().helper.log('No such property "unset" in "sessionStorage"!');
					}
				} else {
					this.ityou().helper.log('No such property "sessionStorage" in "libs"!');
				}
				
				return;
			}
		}, // - sessionstorage
		
		helper: {
			// get the real object
			ityou: function() {
				return window.ITYOU;
			},
			// log function, console.log or alert
			log: function() {
				if(window.console) {
					for(var i = 0; i < arguments.length; i++) {
						console.log(arguments[i]);
					}
				} else {
					var output = "";
					for(var i = 0; i < arguments.length; i++) {
						output += arguments[i] + "\n";
					}
					alert(output);
				}
				
				return;
			},
			// correct viewport width
			correctedViewportWidth: function() {
				var mM = window['matchMedia'] || window['msMatchMedia'],
					client = document.body.clientWidth,
					inner = window.innerWidth;
				
				return mM && client < inner && true === mM('(min-width:' + inner + 'px')['matches'] ? inner : client;
			},
			// helper method for replacing wrong urls with right ones
			correctJsonURL: function(object, rootPath, newPath) {
				if(rootPath === undefined) {
					if(this.ityou().settings.ESI_ROOT === undefined) {
						return object;
					} else {
						rootPath = this.ityou().settings.ESI_ROOT;
					}
				}
				
				if(newPath === undefined) {
					if(this.ityou().settings.ajax.remote === undefined) {
						return object;
					} else {
						newPath = this.ityou().settings.ajax.remote;
					}
				}
				
				var _this = this; 
				if(object instanceof Object) {
					$.each(object, function(key, value) {
						if(value instanceof Object) {
							_this.correctJsonURL(value, rootPath, newPath);
						} else {
							object[key] = _this.replace(value, rootPath, newPath, true);
						}
					});
				}
				return object;
			},
			// replace method
			replace: function(value, needle, haystack, url) {
				if(undefined == value || null == value) {
					return;
				}
				
				if(url !== undefined && url) {
					if(needle.match(/\$/) == null && haystack.match(/\/$/) == null) {
						needle += '/';
					} else if(needle.match(/\$/) == null && haystack.match(/\$/) == null) {
						haystack += '/';
					}
				}
				
				var replace = new RegExp(needle, 'gi');
				
				return value.toString().match(needle) ? value.replace(replace, haystack) : value;
			},
			// filter keys
			filtered_keys: function(object, filter) {
				var keys = [];
				
				for(var key in object) {
					this.ityou().log(key); // debugging
					if(object.hasOwnProperty(key) && key.match(filter)) {
						keys.push(key);
					}
				}
				
				return keys;
			},
			// create 2dim array
			new2dArray: function(size) {
				var temp = new Array(size);
				
				for(var i = 0; i < size; i++) {
					temp[i] = newArray();
				}
				
				return temp;
			},
			// check if an element has a given attribute
			hasAttribute: function(element, attribute) {
				if(undefined == element.attr(attribute)) {
					return false;
				} else {
					return true;
				}
			},
			// toggle linebreaks
			newLineToBreak: function(str) {
				return str.replace(/\r?\n/g, '<br>');
			},
			breakToNewLine: function(str) {
				return str.replace(/\<br.*?\>/gi, "\n");
			},
			// show/hide spinner
			showSpinner: function(parent, size) {
			    if(this.ityou().settings.hasOwnProperty('ajax') && this.ityou().settings.ajax.hasOwnProperty('spinner')) {
					if(undefined == size) {
						size = 128;
					}
					
					var spinnerRow = $('<div class="row ' + this.ityou().settings.ajax.spinnerClass + '" />'),
						spinnerColumn = $('<div class="col-xs-12 text-center" />'),
						spinner = $('<img src="' + this.ityou().settings.ajax.imagePath + '/' + this.ityou().settings.ajax.spinner + '" width="' + size + '">');
					
					spinnerRow.append(spinnerColumn);
					spinnerColumn.append(spinner);
					
					// insert into dom
					spinnerRow.appendTo(parent);
				} else {
				    $('#ajax-spinner').css({
				        opacity: 1
			        }).show();
			        $('#ajax-spinner').find('img').css({
			            opacity: 1
		            });
				}
			},
			hideSpinner: function() {
				if(this.ityou().settings.hasOwnProperty('ajax') && this.ityou().settings.ajax.hasOwnProperty('spinner')) {
					$(document).find('.' + this.ityou().settings.ajax.spinnerClass).each(function() {
						$(this).remove();
					});
				} else {
				    $('#ajax-spinner').css({
				        opacity: 0
				    }).hide();
				    $('#ajax-spinner').find('img').css({
				        opacity: 0
				    });
				}
			},
			// check if value is in object
			valueInObject: function(needle, object) {
				var foundKey = -1;
				
				$.each(object, function(key, value) {
					if(needle == value) {
						foundKey = key;
						return; // break each
					}
				});
				
				return foundKey;
			}
		},
		
		/**
		 * options: {
		 *   uid
		 *   portraitDefault
		 *   portraitIcon
		 *   profileUrl
		 *   portalUrl
		 *   homefolderUrl
		 *   imessageUrl
		 * }
		 */
		personalToolbar: function(options) {
		    options.portalUrl += options.portalUrl.charAt(options.portalUrl.length-1) !== '/' ? '/' : '';
		
		    if(options.portraitIcon !== undefined) {
		        $('#personal-tools').find('img.xs').attr('src', options.portraitIcon);
	        }
	        
	        $('#personal-tools').find('img').not('.xs').attr('src', options.portraitDefault);
	                    
            $('#personal-tools').find('ul').find('li').each(function() {
                var $el = $(this).find('a');
                
                if(options.hasOwnProperty($el.data('type'))) {
                    $el.attr('href', options[$el.data('type')]);
                } else {
                    $el.attr('href', options.portalUrl + $el.data('type'));
                }
            });
		},
		
		
		init: function() {
			var _this = this; // because we cannot call this in ajax requests. this in ajax requests is pointing at the ajax object
			
			// setting user dd
		    this.cache.userId = $('#ESI_DATA').data('ityou-uid');
		    
		    // setting esiroot
		    this.settings.ajax.remote = $('#ESI_DATA').data('ityou-portal-url');
            if(this.settings.ajax.remote !== undefined && this.settings.ajax.remote.charAt(this.settings.ajax.remote.length-1) !== '/') {
                this.settings.ajax.remote += '/';
            }
			
			
			
			// setting localStorage or cookie
			this.setStorageMethod; // not working atm
			
			// init loaded libs
			for(var lib in this.libs) {
				if(this.settings.hasOwnProperty(lib)) {
					$.extend(this.libs[lib].settings, this.settings[lib]);
				}
				
				if(this.libs[lib].hasOwnProperty('init')) {
					this.libs[lib].init();
				}
			}
			
			// get params from esi instance
			/*$.getJSON(this.settings.ajax.remote + '@@ajax-esiparams' + this.settings.ajax.callback, {action: 'get_params'}, function(response) {
				$.extend(_this.settings, response);
				
				_this.cache.serverResponse = true;
				
				// TODO do something else
			});*/
			
			$(this.settings.selector.notifyAstream).attr('href', (this.settings.ajax.remote + '@@activities'));
			$(this.settings.selector.notifyImessage).attr('href', (this.settings.ajax.remote + '@@messages'));
			
			
			// ---------------------------------------------------------------
			// ---------------------------------------------------------------
			// ---------------------------------------------------------------
			// PERSONAL TOOLS
			if(_this.session.get('userId') !== null && _this.session.get('portraitDefault') !== null && _this.session.get('portraitIcon') !== null && _this.session.get('profileURI') !== null && _this.session.get('homeFolderURI') !== null && _this.session.get('imessageURI') !== null && _this.session.get('portalUrl')) {
		        _this.personalToolbar({
                    uid: _this.session.get('userId'),
		            portraitDefault: _this.session.get('portraitDefault'),
		            portraitIcon: _this.session.get('portraitIcon'),
		            profileUrl: _this.session.get('profileUrl'),
		            portalUrl: _this.session.get('portalUrl'),
		            homefolderUrl: _this.session.get('homefolderUrl'),
		            //imessageUrl: _this.session.get('imessageUrl')
		            imessageUrl: '@@messages'
		        });
			} else {
			    var esiData = $('#ESI_DATA').data();
			    
			    if(esiData.ityouProfileUrl !== undefined) {
			        _this.session.set('profileUrl', esiData.ityouProfileUrl);
			    }
			    
			    if(esiData.ityouPortalUrl !== undefined) {
			        _this.session.set('portalUrl', esiData.ityouPortalUrl);
			    }
			    
			    if(esiData.ityouHomefolderUrl !== undefined) {
			        _this.session.set('homefolderUrl', esiData.ityouHomefolderUrl);
			    }
			    
			    if(esiData.ityouImessageUrl !== undefined) {
			        //_this.session.set('imessageUrl', esiData.ityouImessageUrl);
			        _this.session.set('imessageUrl', '@@messages');
			    }
			
			    $.getJSON(this.settings.ajax.remote + '@@ajax-personal-profile' + this.settings.ajax.callback, {action: 'whoami'}, function(response) {
			        if(response.user_id != null) {
			            // 128 thumb, 64 tile, 32 icon, 16 micro
			            $.getJSON(_this.settings.ajax.remote + '@@ajax-personal-profile' + _this.settings.ajax.callback, {action: 'whoami', portrait_size: 'icon'}, function(small_portrait) {
	                        $('#personal-tools').find('img.xs').attr('src', small_portrait.portrait);
	                        
	                        // save
	                        _this.session.set('portraitIcon', small_portrait.portrait);
	                    });
	                    
	                    _this.personalToolbar({
	                        uid: response.user_id,
	                        portraitDefault: response.portrait,
		                    portraitIcon: _this.session.get('portraitIcon'),
		                    profileUrl: _this.session.get('profileUrl'),
		                    portalUrl: _this.session.get('portalUrl'),
		                    homefolderUrl: _this.session.get('homefolderUrl'),
        		            imessageUrl: _this.session.get('imessageUrl')
	                    });
                        
                        // save
                        _this.session.set('userId', response.user_id);
                        _this.session.set('portraitDefault', response.portrait);
                    }
			    });
		    }
			// ---------------------------------------------------------------
			// ---------------------------------------------------------------
			// ---------------------------------------------------------------
			
			
			
			
			
			
			this.cache.serverCheck = setInterval(function() {
				if(_this.cache.serverResponse == true) {
					clearInterval(_this.cache.serverCheck);
					clearTimeout(_this.cache.serverCheckTimeout);
					
					$(document).trigger('ityouReady');
				}
			}, 500);
			
			this.cache.serverCheckTimeout = setTimeout(function() {
				if(_this.settings.serverResponse == false) {
					// TODO Loading failed
				}
			}, _this.settings.ajax.timeout);
			
			// self defined event
			window.addEventListener('ityouReady', function(e){});
		}
		
	};
	
	
	$.fn.ITYOU = function() {
		var _this = window.ITYOU;
		
		// add function to get objects size
		Object.size = function(object) {
			var size = 0;
			
			for(var key in object) {
				if(object.hasOwnProperty(key)) {
					size++;
				}
			}
			
			return size;
		};
		
        // Setting options
		if(arguments.length > 0) {
		    for(var i = 0; i < arguments.length; i++) {
			    for(var lib in arguments[i]) {
				    if(_this.settings.hasOwnProperty(lib)) {
					    $.extend(_this.settings[lib], arguments[i][lib]);
				    } else {
					    _this.settings[lib] = arguments[i][lib];
				    }
			    }
		    }
		}
		
		_this.init();
	};
	
	
}(jQuery, this, this.document));
