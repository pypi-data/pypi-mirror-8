(function($, window, document, _, undefined) {
	'use strict';
	
	window.ityouBackToTop = {
		name: 'ityou.backtotop',
		version: '0.1.2',
		settings: {
			button: '#back-to-top',
			text: 'Back to Top',
			min: 200,
			fadeIn: 400,
			fadeOut: 400,
			scrollSpeed: 800,
			easingType: 'easeInOut'
		},
		oldiOS: false,
		oldAndroid: false,
		cache: {},
		_constructor: function() {
			var self = this;
			
			$('body').append('<a href="#" id="'+self.settings.button.substring(1)+'" title="'+self.settings.text+'">'+self.settings.text+'</a>');
			
			$(document).on('click', self.settings.button, function(e) {
				e.preventDefault();
				$('html, body').animate({scrollTop: 0}, self.settings.scrollSpeed);
			});
			
			$(window).scroll(function() {
				var position = $(window).scrollTop();
				
				if(self.oldiOS || self.oldAndroid) {
					$(self.settings.button).css({
						position: 'absolute',
						top: position + $(window).height()
					});
				}
				
				if(position > self.settings.min) {
					$(self.settings.button).fadeIn(self.settings.fadeIn);
				} else {
					$(self.settings.button).fadeOut(self.settings.fadeOut);
				}
			});
		},
		_detectOS: function() {
			if(/(iPhone|iPod|iPad)\sOS\s[0-4][_\d]+/i.test(navigator.userAgent)) {
				this.oldiOS = true;
			}
			
			if(/Android\s+([0-2][\.\d]+)/i.test(navigator.userAgent)) {
				this.oldAndroid = true;
			}
		},
		init: function() {
			var self = this;
			
			if(self.cache.registered == undefined || self.cache.registered == false) {
				// Event Handler
			}
			
			self._detectOS();
			self._constructor();
			
			// register plugin
			self.cache.registered = true;
		}
	};
	
	$.fn.ityouBackToTop = function(opts) {
		var _self = ityouBackToTop;
		
		if(opts instanceof Object) {
			$.extend(_self.settings, opts);
		}
		
		_self.init();
	}
}(jQuery, this, this.document, this.ityou));
