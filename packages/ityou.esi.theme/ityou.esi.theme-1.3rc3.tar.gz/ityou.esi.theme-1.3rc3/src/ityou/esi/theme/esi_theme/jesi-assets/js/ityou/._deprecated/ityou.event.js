(function($, window, document, _, undefined) {
	'use strict';
	
	window.ityouEvent = {
		name: 'ityou.event',
		version: '0.1.5',
		settings: {
			wrapper: '#event',
			yearOffset: 2,
			animationSpeed: 400,
			template: {
				list_view_year: '#event-list-view-year-template',
				list_view_month: '#event-list-view-month-template',
				list_view: '#event-list-view-template'
			},
			container: {
				list_view_year: '.list-view-year',
				list_view_month: '.list-view-month',
				list_view: '.event-list'
			},
			css_class: {
				active: 'state-active',
				has_event: 'state-has-event',
				hover: 'state-hover'
			}
		},
		cache: {
			dict_year: [],
			dict_month_column_1: [{month: 'Januar'}, {month: 'Februar'}, {month: 'M&auml;rz'}, {month: 'April'}, {month: 'Mai'}, {month: 'Juni'}],
			dict_month_column_2: [{month: 'Juli'}, {month: 'August'}, {month: 'September'}, {month: 'Oktober'}, {month: 'November'}, {month: 'Dezember'}],
			dict_year_events: new Array(12)
		},
		_build_list_view: function() {
			var self = this,
				i;
			
			self.cache.current_date = new Date();
			self.cache.current_year = self.cache.current_date.getFullYear();
			self.cache.current_month = self.cache.current_date.getMonth()+1;
			
			self.cache.dict_year = [];
			for(i = self.cache.current_year-self.settings.yearOffset; i <= self.cache.current_year+self.settings.yearOffset; i++) {
				self.cache.dict_year.push({year: i});
			}
			
			// List View YEAR
			$($(self.settings.template.list_view_year).render(self.cache.dict_year)).appendTo(self.settings.container.list_view_year);
			$(self.settings.container.list_view_year).find('li').each(function() {
				$(this).css({
					marginLeft: (5 / $(self.settings.container.list_view_year).find('li').length) + '%',
					width: ((95+(5 / $(self.settings.container.list_view_year).find('li').length)) / $(self.settings.container.list_view_year).find('li').length) + '%' 
				});
				
				if($(this).index() == 0) {
					$(this).css({
						marginLeft: '0'
					});
				}
			});
			// List View MONTH
			$($(self.settings.template.list_view_month).render(self.cache.dict_month_column_1)).appendTo(self.settings.container.list_view_month+'.column-1');
			$($(self.settings.template.list_view_month).render(self.cache.dict_month_column_2)).appendTo(self.settings.container.list_view_month+'.column-2');
			
			setTimeout(function() {
				$(self.settings.container.list_view_year).find('li').each(function() {
					self._get_n_set_selection('year', $(this).text());
				});
			},1);
			
			self._get_event_list(self.cache.current_year);
		},
		_get_n_set_selection: function(state, arg) {
			var self = this;
			
			if(state == 'year') {
				$.getJSON(_.settings.remote + '@@ajax-content' + _.settings.callback, {action: 'query_length', portal_type: 'Event', year: $.trim(arg)}, function(response) {
					if(response > 0) {
						$(self.settings.container.list_view_year)
							.find('li[data-year="'+$.trim(arg)+'"]')
							.addClass(self.settings.css_class.has_event);
					}
					
					if(arg == self.cache.current_year) {
						$(self.settings.container.list_view_year)
							.find('li[data-year="'+self.cache.current_year+'"]')
							.addClass(self.settings.css_class.active);
					}
				});
			} else if(state == 'month') {
				if(arg <= 6) {
					$(self.settings.container.list_view_month+'.column-1')
						.find('li:eq('+(arg-1)+')')
						.addClass(self.settings.css_class.has_event);
					
					if(arg == self.cache.current_month) {
						$(self.settings.container.list_view_month+'.column-1')
							.find('td:eq('+(arg-1)+')')
							.addClass(self.settings.css_class.active);
					}
				} else {
					$(self.settings.container.list_view_month+'.column-2')
						.find('li:eq('+(arg-1-6)+')')
						.addClass(self.settings.css_class.has_event);
					
					if(arg == self.cache.current_month) {
						$(self.settings.container.list_view_month+'.column-2')
							.find('li:eq('+(arg-1)+')')
							.addClass(self.settings.css_class.active);
					}
				}
			}
		},
		_get_event_list: function(arg) {
			var self = this,
				i;
			
			// clear event list
			$(self.settings.container.list_view).empty();
			
			// show spinner
			_._show_content_spinner(self.settings.wrapper + ' #content', 64);
			
			// reset array
			self.cache.dict_year_events = _._new_array2d(12);
			
			// remove css
			$(self.settings.container.list_view_month).find('li').each(function() {
				$(this)
					.removeClass(self.settings.css_class.active)
					.removeClass(self.settings.css_class.has_event);
			});
			
			// get data
			$.getJSON(_.settings.remote + '@@ajax-content' + _.settings.callback, {action: 'query', portal_type: 'Event', year: arg}, function(response) {
				$.each(response, function(k, val) {
					var m = parseInt((val.start_date.split('.')[1]/1));
					
					self.cache.dict_year_events[m-1].push(val);
					
					// style month table
					self._get_n_set_selection('month', m);
				});
				
				// print events
				for(i = 0; i < 12; i++) {
					$($(self.settings.template.list_view).render(self.cache.dict_year_events[i])).appendTo(self.settings.container.list_view).hide().slideDown(self.settings.animationSpeed);
				}
				
				// remove spinner
				_._hide_content_spinner();
			});
		},
		_get_selection_event_list: function(arg) {
			var self = this;
			
			$(self.settings.container.list_view).empty();
			$($(self.settings.template.list_view).render(self.cache.dict_year_events[arg])).appendTo(self.settings.container.list_view).hide().slideDown(self.settings.animationSpeed);
		},
		init: function() {
			var self = this;
			
			if(self.cache.registered == undefined || self.cache.registered == false) {
				// event handler for changing year
				$(document).on('click', self.settings.container.list_view_year+ ' li.'+self.settings.css_class.has_event, function(e) {
					e.preventDefault();
					
					// remove active class on year table
					$(self.settings.container.list_view_year).find('li').each(function() {
						$(this).removeClass(self.settings.css_class.active);
					});
					// remove active/has_event class on month table
					$(self.settings.container.list_view_month).find('li').each(function() {
						$(this)
							.removeClass(self.settings.css_class.active)
							.removeClass(self.settings.css_class.has_event);
					});
					
					// add active class to selection
					$(this).addClass(self.settings.css_class.active);
					
					// get events of selection
					self._get_event_list($(this).text());
				});
				
				// event handler for changing month
				$(document).on('click', self.settings.container.list_view_month+' li.'+self.settings.css_class.has_event, function(e) {
					e.preventDefault();
					
					// remove active class on month table
					$(self.settings.container.list_view_month).find('li').each(function() {
						$(this).removeClass(self.settings.css_class.active);
					});
					
					$(this).addClass(self.settings.css_class.active);
					
					self._get_selection_event_list(($(this).index() + $(this).parent().index() * 6));
				});
				
				// event handler open event
				$(document).on('click', '.open-in-document-view', function(e) {
					e.preventDefault();
					
					// open content
					if(ityouDocument != undefined) {
						ityouDocument._get_document_content($(this).attr('data-uid'));
					}
				});
			}
			
			
			// initialize
			self._build_list_view();
			
			
			// register plugin
			self.cache.registered = true;
		}
	};
	
	$.fn.ityouEvent = function(opts) {
		var _self = ityouEvent;
		
		if(opts instanceof Object) {
			$.extend(_self.settings, opts);
		}
		
		_self.init();
	}
}(jQuery, this, this.document, this.ityou));
