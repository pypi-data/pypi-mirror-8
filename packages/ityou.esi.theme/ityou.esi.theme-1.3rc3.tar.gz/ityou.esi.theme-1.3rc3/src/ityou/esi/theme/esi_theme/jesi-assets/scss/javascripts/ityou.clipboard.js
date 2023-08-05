/**
 * A module representing a clipboard
 * 
 * @module clipboard
 */

/**
 * @constructor
 * @alias module:clipboard
 * @augments Utilities
 */
function Clipboard() {
	/** How to identify the stored value */
	this.identifier = 'ityouClipboard';
	
	/** event register */
	this.eventsRegistered = 'ityou-clipboard-events-registered';
	
	/** element selectors here */
	this.selector = {
		/** which element can store its value to the clipboard */
		copyToClipboard: '.can-copy-to-clipboard',
		/** Where the stored value can be pasted in to */
		pasteFromClipboard: '.can-paste-from-clipboard',
		/** What is the name of the button to copy something to the clipboard */
		copyButton: '.copy-to-clipboard',
		/** What is the name of the button to paste something from the clipboard */
		pasteButton: '.paste-from-clipboard'
	};
	
	/** important data which is used later on */
	this.cache = {
		/** user id of current user */
		userId: null
	};
	
	this.eventHandler();
}
Clipboard.prototype = new Utilities();

/**
 * @constructs
 */
Clipboard.prototype.init = function() {
	/** set user id */
	this.cache.userId = this.storage.session.get('userId');
};

/**
 * copy a value to our clipboard
 * 
 * @returns {void}
 */
Clipboard.prototype.copyToClipboard = function(parentId) {
	/** pointer to the element */
	var $el = $(parentId).find(this.selector.copyToClipboard);
	/** the value to store */
	var value = "";
	
	if($el.length > 0) {
		/** try to extract the value */ 
		if($el.val().length > 0) {
			value = $el.val();
		} else if($el.text().length > 0) {
			value = $el.text();
		}

		/** store the value */
		this.storage.session.set(this.identifier, value);
		
		$.growl({
			message: 'Text in die Zwischenablage kopiert.',
			icon: 'fa fa-check'
		}, {
			delay: 1500
		});
	}
	
	this.addPasteControls();
};

/**
 * paste the stored value from our clipboard
 *
 * @returns {void}
 */
Clipboard.prototype.pasteFromClipboard = function($btn) {
	/** get element where we wanna change the value */
	var $el = $btn.parents('.input-group').find(this.selector.pasteFromClipboard);
	
	/** append the stored value */
	$el.val($el.val() + this.getStoredValue());
};

/**
 * get the stored value
 * 
 * @returns {String}
 */
Clipboard.prototype.getStoredValue = function() {
	return this.storage.session.get(this.identifier);
};

/**
 * @TODO perhaps not needed
 */
Clipboard.prototype.addCopyControls = function() {
	/** not implemented */
};

/**
 * create controls to paste the stored value
 * 
 * @returns {void}
 */
Clipboard.prototype.addPasteControls = function() {
	if(this.getStoredValue() != null) {
		$(this.selector.pasteFromClipboard).each($.proxy(function(i, el) {
			$btn = $('<button type="button" class="btn btn-default ' + this.selector.pasteButton.substring(1) + '"><i class="fa fa-paste"></i></button>');
			$p = $(el).parents('.input-group');
			
			if($p.length > 0 && $p.find(this.selector.pasteButton).length == 0) {
				$p.prepend($btn);
			}
		}, this));
	}
};

/**
 * initiate some event handler
 * 
 * @returns {void}
 */
Clipboard.prototype.eventHandler = function() {
	if(!$('body').hasClass(this.eventsRegistered)) {
		$('body').addClass(this.eventsRegistered);
	
		/** @events */
		$(document).on('click', this.selector.copyButton, $.proxy(function(event) {
			var parentId = $(event.target).parents('button' + this.selector.copyButton).length > 0 ? $(event.target).parents('button' + this.selector.copyButton).data('parent-id') : $(event.target).data('parent-id');
			
			this.copyToClipboard(parentId);
		}, this));
		
		/** @events */
		$(document).on('click', this.selector.pasteButton, $.proxy(function(event) {
			var parent = $(event.target).parents('button' + this.selector.pasteButton).length > 0 ? $(event.target).parents('button' + this.selector.pasteButton) : $(event.target);
			this.pasteFromClipboard(parent);
		}, this));
	}
};