(function($, window, document, _, undefined) {
	'use strict';
	
	window.ityouXXX = {
		name: 'ityou.XXX',
		version: '0.1.1',
		settings: {},
		cache: {},
		
		init: function() {
			var self = this;
			
			if(self.cache.registered == undefined || self.cache.registered == false) {
				// Event Handler
			}
			
			
			
			// register plugin
			self.cache.registered = true;
		}
	};
	
	$.fn.ityouXXX = function(opts) {
		var _self = ityouXXX;
		
		if(opts instanceof Object) {
			$.extend(_self.settings, opts);
		}
		
		_self.init();
	}
}(jQuery, this, this.document, this.ityou));
