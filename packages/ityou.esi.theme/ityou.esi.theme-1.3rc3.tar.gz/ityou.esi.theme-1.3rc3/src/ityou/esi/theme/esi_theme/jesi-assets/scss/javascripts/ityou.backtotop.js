(function($, window, document, _, undefined) {
	
	'use strict';
	
	_.libs.backtotop = {
		name: 'ityou.backtotop',
		version: '0.1.5',
		
		cache: {},
		
		settings: {
			button: '#back-to-top',
			text: 'Back to Top',
			min: 200,
			minWidth: 480,
			fadeIn: 400,
			fadeOut: 400,
			scrollSpeed: 800,
			easingType: 'easeInOut'
		},
		
		oldiOS: false,
		oldAndroid: false,
		
		_constructor: function() {
			var _this = this;
			
			$('body').append('<a href="#" id="' + this.settings.button.substring(1) + '" title="' + this.settings.text + '">' + this.settings.text + '</a>');
			
			$(document).on('click', this.settings.button, function(e) {
				e.preventDefault();
				$('html, body').animate({scrollTop: 0}, _this.settings.scrollSpeed);
			});
			
			$(window).scroll(function() {
				var position = $(window).scrollTop();
				
				if(_this.oldiOS/* || _this.oldAndroid*/) {
					$(_this.settings.button).css({
						position: 'absolute',
						top: position + $(window).height()
					});
				}
				
				if(position > _this.settings.min && $(window).width() > _this.settings.minWidth) {
					$(_this.settings.button).fadeIn(_this.settings.fadeIn);
				} else {
					$(_this.settings.button).fadeOut(_this.settings.fadeOut);
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
			this._detectOS();
			this._constructor();
		}
	};
	
}(jQuery, this, this.document, this.ITYOU));
