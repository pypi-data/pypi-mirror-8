(function($, window, document, _, undefined) {
	
	'use strict';
	
	_.libs.mapping = {
		name: 'ityou.mapping',
		version: '0.1.1',
		
		cache: {},
		settings: {
			routes: {
				
			},
			currentView: null,    // what is the current view --> name of the template which has to be loaded
			container: $('body'), // the dom object where we append the html from the template
			tmplPath: 'tmpl/',    // location of templates
			
			// define which templates should be loaded
			templates: []
		},
		
		/**
		 * load template
		 *
		 * @use settings.tmplPath
		 * @use settings.currentView
		 */
		getTemplate: function() {
			var _this = this;
			
			$.ajax({
				type: 'GET',
				dataType: 'html',
				url: _this.settings.tmplPath + _this.settings.currentView + '.html',
				success: function(html) {
					_this.renderTemplate(html);
				},
				error: function(e) {
					_.helper.log('error loading template');
				}
			});
		},
		
		/**
		 * appending the html from loaded template to a defined container
		 *
		 * @use settings.container
		 */
		renderTemplate: function(html) {
			this.settings.container.append(html);
		},
		
		/*
		 * Naming convention:
		 * 
		 * data-ityou-view value has to be the same as the template name (without .html)
		 */
		init: function() {
			this.settings.currentView = $(document).find('[data-ityou-view]').data('ityou-view');
			//_.helper.log('Mapping', this.settings.currentView, '---'); // debugging
			
			if(undefined !== this.settings.currentView && null !== this.settings.currentView && $.inArray(this.settings.currentView, this.settings.templates) > -1) {
				this.getTemplate();
			}
		}
		
		
	};
	
}(jQuery, this, this.document, this.ITYOU));
