function GuidedTour() {
	this.guideId = false;
	this.tour;
	this.NAMESPACE;
	this.END = '_end';
	this.CURRENT_STEP = '_current_step';
	this.initializer = '#btn-help';
	
	this.lang = {
		previous: 'back',
		next: 'next',
		end: 'end'
	};
	
	var esi_data = $('#ESI_DATA').data(),
		currentView = esi_data != null ? (esi_data.hasOwnProperty('ityouView') ? esi_data.ityouView : false) : false;
		
	this.getGuideId = function() {
		return this.guideId;
	};
	
	this.setNamespace = function() {
		if(this.getGuideId()) {
			this.NAMESPACE = 'esi_' + this.getGuideId() + '_tour';
		}
	};
	
	if(navigator.language || navigator.browserLanguage) {
		var lang = navigator.language ? navigator.language : navigator.browserLanguage;
		
		if(lang.indexOf("de") > -1) {
			this.lang = {
				previous: 'zurück',
				next: 'weiter',
				end: 'Beenden'
			}
		}
	}
	
	if(currentView) {
		if(currentView.match(/messages/i)) {
			if(location.search) {
				this.guideId = 'dialog';
			} else {
				this.guideId = 'message';
			}
		} else if(currentView.match(/message-/i)) {
			this.guideId = 'start';
		} else if(currentView.match(/user/i)) {
			this.guideId = 'member';
		} else if(currentView.match(/author/i)) {
			this.guideId = 'profile';
		} else if(currentView.match(/activities/i)) {
			this.guideId = 'activity';
		} else if(currentView.match(/folder_listing/i)) {
			// ---
		} else if(currentView.match(/asco-documents/i)) {
			this.guideId = 'asco-documents';
		} else if(currentView.match(/asco-abstract-listing/i)) {
			this.guideId = 'asco-abstracts';
		}
		
		this.setNamespace();
	}
	
	this.getGuide = function() {
		if(!this.storage.local.get(this.NAMESPACE + this.END, true) && this.getGuideId()) {
			$.ajax({
				url: '@@guide',
				data: {
					p: this.getGuideId()
				},
				dataType: 'json',
				success: $.proxy(function(response) {
					if(response.length > 0) {
						this.guide(response);
					}
				}, this)
			});
		}
	};
	
	this.guide = function(data) {
		this.storage.local.unset(this.NAMESPACE + this.END);
		this.storage.local.unset(this.NAMESPACE + this.CURRENT_STEP);
		
		this.tour = new Tour({
			name: this.NAMESPACE,
			onStart: $.proxy(function() {
				$('#btn-help').addClass('help-active');
			}, this),
			onEnd: $.proxy(function() {
				$('#btn-help').removeClass('help-active');
			}, this),
			template: '<div class="popover tour">' +
				'<div class="arrow"></div>' +
				'<h3 class="popover-title"></h3>' + 
				'<div class="popover-content"></div>' +
				'<div class="popover-navigation">' +
					'<div class="btn-group">' +
						'<button class="btn btn-default" data-role="prev">&laquo; ' + this.lang.previous + '</button>' +
						'<button class="btn btn-default" data-role="next">' + this.lang.next + ' &raquo;</button>' +
					'</div>' +
					'<button class="btn btn-default" data-role="end">' + this.lang.end + '</button>' +
				'</div>' +
			'</div>'
		});
		
		for(var i in data) {
			this.tour.addStep(data[i]);
		}
		
		this.tour.setCurrentStep(null);
		
		this.tour.init();
		this.tour.start();
	};
	
	$(document).on('click', this.initializer, $.proxy(function(e) {
		e.preventDefault();
		
		this.storage.local.unset(this.NAMESPACE + this.END);
		this.storage.local.unset(this.NAMESPACE + this.CURRENT_STEP);
		
		if(this.tour) {
			this.tour.setCurrentStep(null);
			//this.tour = null;
		}
		
		this.getGuide();
	}, this));
}


GuidedTour.prototype = new Utilities();
GuidedTour.prototype.storage = GuidedTour.prototype.storage;