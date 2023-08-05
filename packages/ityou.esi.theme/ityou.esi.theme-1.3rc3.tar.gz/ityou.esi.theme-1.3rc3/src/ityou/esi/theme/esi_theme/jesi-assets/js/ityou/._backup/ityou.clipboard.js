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
	
	this.eventHandler();
}
Clipboard.prototype = new Utilities();

/**
 * copy a value to our clipboard
 * 
 * @returns {void}
 */
Clipboard.prototype.copyToClipboard = function() {
	/** pointer to the element */
	var $el = $(this.selector.copyToClipboard);
	/** the value to store */
	var value = "";
	
	/** try to extract the value */ 
	if($el.val().length > 0) {
		value = $el.val();
	} else if($el.text().length > 0) {
		value = $el.text();
	}
	
	/** store the value */
	this.storage.session.set(this.identifier, value);
};

/**
 * paste the stored value from our clipboard
 *
 * @returns {void}
 */
Clipboard.prototype.pasteFromClipboard = function() {
	/** paste the stored value */
	$(this.selector.pasteFromClipboard).val(this.getStoredValue());
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
 * create controls to paste the stored value
 * 
 * @returns {void}
 */
Clipboard.prototype.addControls = function() {
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
	/** @events */
	$(document).on('click', this.selector.copyButton, $.proxy(function(event) {
		this.copyToClipboard();
	}, this));
	
	/** @events */
	$(document).on('click', this.selector.pasteButton, $.proxy(function(event) {
		this.pasteFromClipboard();
	}, this));
};