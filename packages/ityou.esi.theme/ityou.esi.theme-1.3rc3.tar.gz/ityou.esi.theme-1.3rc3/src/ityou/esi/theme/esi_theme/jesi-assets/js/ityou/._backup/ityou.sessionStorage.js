(function($, window, document, _, undefined) {
	
	'use strict';
	
	_.libs.sessionStorage = {
		name: 'ityou.sessionStorage',
		version: '0.1.1',
		
		cache: {},
		settings: {
    		/**
    		 * @var integer storageMethod Default value is 1... 0 means using sessionStorage, 1 means using cookies
    		 */
		    storageMethod: 1
		},
		
		get: function(key, object) {
		    if(object === undefined) {
		        object = false;
	        }
		
			if(this.settings.storageMethod === 0) {
    			if(object) {
    			    return JSON.parse(window.sessionStorage.getItem(key));
			    }
				return window.sessionStorage.getItem(key);
			} else {
    			if($.isFunction($.fn.cookie)) {
    			    return $.cookie(key);
    			} else {
                    // read cookie
                    var nameEQ = key + '=',
                        ca = document.cookie.split(';'),
                        i,
                        c;
                        
                    for(i = 0; i < ca.length; i++) {
                        c = ca[i];
                        while(c.charAt(0) === ' ') {
                            c = c.substring(1, c.length);
                        }
                        
                        if(c.indexOf(nameEQ) === 0) {
                            return unescape(c.substring(nameEQ.length, c.length));
                        }
                    }
                    
                    return null;
                }
			}
		},
		
		set: function(key, value, object) {
		    if(object === undefined) {
		        object = false;
		    }
		
			if(this.settings.storageMethod === 0) {
    			if(object) {
    			    window.sessionStorage.setItem(key, JSON.stringify(value));
    			} else {
    				window.sessionStorage.setItem(key, value);
				}
			} else {
			    if($.isFunction($.fn.cookie)) {
			        $.cookie(key, value, {expires: 365, path: '/'});
			    } else {
				    // write cookie
				    var date,
				        expires;
			        
		            date = new Date();
	                date.setTime(date.getTime()+(365*24*60*60*1000));
	                expires = "; expires="+data.toGMTString();
	                
	                document.cookie = key+"="+escape(value)+expires+"; path=/";
                }
			}
		},
		
		remove: function(key) {
			if(this.settings.storageMethod === 0) {
				window.sessionStorage.removeItem(key);
			} else {
			    if($.isFunction($.fn.cookie)) {
			        $.removeCookie(key, {path: '/'});
			    } else {
    				document.cookie = key+'=; expires=-1; path=/';
				}
			}
		},
		
		init: function() {
			if(this.caniuse()) {
				this.settings.storageMethod = 0;
			} else {
				this.settings.storageMethod = 1;
			}
		},
		
		caniuse: function() {
		    try {
		        return 'sessionStorage' in window && window['sessionStorage'] !== null;
	        } catch(e) {
	            return false;
	        }
		}
			
	};
	
}(jQuery, this, this.document, this.ITYOU));
