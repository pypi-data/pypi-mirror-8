$.windowActive = true;

$.isWindowActive = function () {
    return $.windowActive;
};

$(window).focus(function() {
    $.windowActive = true;
});

$(window).blur(function() {
    $.windowActive = false;
});



/**
 * A module representing common methods
 * 
 * @module utilities
 * @author mreichenbecher
 */

/**
 * @constructor
 * @alias module:utilities
 */
function Utilities() {
	/** Is the current tab the active tab */
    this.windowActive = true;
}

/**
 * Convert a JS Date Object into an unix timestamp
 * 
 * @param {Number} timestamp 
 * @returns {Number} the unix timestamp
 */
Utilities.prototype.convertToUNIXTimestamp = function(timestamp) {
    timestamp = timestamp.replace(/ /g, 'T');
    
    return Math.floor(Date.parse(timestamp) / 1000);
};

/**
 * Sort a numeric Array
 * 
 * @param {Array} data
 * @param {String} direction asc or desc
 * @returns {Array} the sorted array
 */
Utilities.prototype.sortNumeric = function(data, direction) {
    var tmp = data.sort(function(a, b) {
        return a-b;
    });
    
    if('desc' === direction) {
        tmp.reverse();
    }
    
    return tmp;
};

/**
 * Sort a 2D array by a numeric value
 * 
 * @param {Array} data
 * @param {String} direction asc or desc
 * @returns {Array} the sorted array
 */
Utilities.prototype.sortNumericArray = function(data, direction) {
    var tmp = data.sort(function(a, b) {
        a = a[1];
        b = b[1];
    
        return a-b;
    });
    
    if('desc' === direction) {
        tmp.reverse();
    }
    
    return tmp;
};

/**
 * Sort a 2D array by an alphabetic value 
 * 
 * @param {Array} data
 * @param {String} direction asc or desc
 * @returns {Array} the sorted array
 */
Utilities.prototype.sortAlphabetic = function(data, direction) {
    var tmp = data.sort(function(a, b) {
        var a = a[1].toLowerCase(),
            b = b[1].toLowerCase();
        
        return a.localeCompare(b);
    });
    
    if('desc' === direction) {
        tmp.reverse();
    }
    
    return tmp;
};

/**
 * Sort an HTML table
 * 
 * @param {Object} table
 * @param {Array} rows
 * @returns {void}
 */
Utilities.prototype.tableSort = function(table, rows) {
    table.empty();
    
    $.each(rows, $.proxy(function(k, row) {
        table.append(row);
    }, this));
};

/**
 * convert a given value to a boolean
 * 
 * @param {Mixed} value
 * @returns {Boolean}
 */
Utilities.prototype.toBoolean = function(value) {
    if((typeof value === 'string' && value.toLowerCase() === 'true') || (typeof value === 'boolean' && value === true)) {
        return true;
    } else if((typeof value === 'string' && value.toLowerCase() === 'false') || (typeof value === 'boolean' && value === false)) {
        return false;
    }
    
    return true;
};

/**
 * show a self-defined spinner
 * 
 * @returns {void}
 */
Utilities.prototype.showSpinner = function() {
    //$('#ajax-spinner').css('opacity', 1).show().find('img').css('opacity', 1);
    
    if($('.jesi-spinner').length > 0) {
        $('.jesi-spinner').removeClass('hidden');
    } else {
        $('<div class="jesi-spinner"><div class="inner"><i class="fa fa-spinner fa-spin"></i></div>').appendTo('body');
    }
};

/**
 * hide a self-defined spinner
 * 
 * @returns {void}
 */
Utilities.prototype.hideSpinner = function() {
    //$('#ajax-spinner').css('opacity', 0).show().find('img').css('opacity', 0);
    $('.jesi-spinner').addClass('hidden');
};

/**
 * check wether the window is active or not
 * 
 * @returns {Boolean}
 */
Utilities.prototype.isWindowActive = function() {
    return $.isWindowActive();
};

/**
 * a lightweight log function
 * 
 * @returns {void}
 */
Utilities.prototype.log = function() {
    this.log.history = this.log.history || []; // store logs to an array for reference
    this.log.history.push(arguments);
    
    if(window.console) {
        console.log(Array.prototype.slice.call(arguments));
    }
};

/**
 * remove some html tags from a given value
 *
 * @param {String} str
 * @param {String} allowed_tag
 * @return {String}
 */
Utilities.prototype.stripTags = function(str, allowed_tags) {
    var key = '',
        allowed = false;
        
    var matches = [],
        allowed_array = [];
        
    var allowed_tag = '',
        i = 0,
        k = '',
        html = '';
        
    var replacer = function(search, replace, str) {
        return str.split(search).join(replace);
    };
    
    if(allowed_tags) {
        allowed_array = allowed_tags.match(/([a-zA-Z0-9]+)/gi);
    }
    
    str += '';
    
    matches = str.match(/(<\/?[\S][^>]*>)/gi);
    
    for(key in matches) {
        if(isNaN(key)) {
            continue;
        }
        
        html = matches[key].toString();
        allowed = false;
        
        for(k in allowed_array) {
            allowed_tag = allowed_array[k];
            i = -1;
            
            if(i != 0) {
                i = html.toLowerCase().indexOf('<' + allowed_tag + '>');
            }
            
            if(i != 0) {
                i = html.toLowerCase().indexOf('<' + allowed_tag + ' ');
            }
            
            if(i != 0) {
                i = html.toLowerCase().indexOf('</' + allowed_tag);
            }
            
            if(i == 0) {
                allowed = true;
                break;
            }
        }
        
        if(!allowed) {
            str = replacer(html, ' ', str);
        }
    }
    
    return str;
};

/**
 * get the size of an object
 * 
 * @param {Object} object
 * @returns {Number} the size of the object
 */
Utilities.prototype.size = function(object) {
    var count = 0, i;
    
    for(i in object) {
        if(object.hasOwnProperty(i)) {
            count++;
        }
    }
    
    return count;
};

/** create an instance of storage to deploy its methods to all other classes */
Utilities.prototype.storage = {
	session: new Storage('session'),
	local: new Storage('local')
};


/**
 * A module representing the storage
 * 
 * @module storage
 * @author mreichenbecher
 */

/**
 * @constructor
 * @alias module:storage
 * @param {String} type session or local
 */
function Storage(type) {
	/** What storage should be used */
	this.type = type;
	/** a pointer on the used storage */
	this.storage = (type === 'session' ? ('sessionStorage' in window && window['sessionStorage'] !== null ? window.sessionStorage : false) : (type === 'local' ? ('localStorage' in window && window['localStorage'] !== null ? window.localStorage : false) : false));
}

/**
 * @constructs
 * @deprecated
 */
Storage.prototype.initialize = function() {
	console.log(this.type);
	/** define what storage we are using and allocate the pointer */
	if(this.type === 'session' && this.usage()) {
		this.storage = window.sessionStorage;
	} else if(this.type === 'local' && this.usage()) {
		this.storage = window.localStorage;
	}
};

/**
 * check if the browser supports the selected method,
 * if not fall back to cookies
 * 
 * @deprecated
 * @returns {Boolean}
 */
Storage.prototype.usage = function() {
	if(this.type === 'session') {
		return 'sessionStorage' in window && window['sessionStorage'] !== null;
	} else if(this.type === 'local') {
		return 'localStorage' in window && window['localStorage'] !== null;
	} else {
		return false;
	}
};

/**
 * get a stored value
 * 
 * @param {String} key
 * @param {Boolean} noParse optional, use it if you dont want to parse the value
 * @returns {Mixed}
 */
Storage.prototype.get = function(key, noParse) {
	if(this.storage) {
		if(noParse) {
			return this.storage.getItem(key);
		} else {
			return JSON.parse(this.storage.getItem(key));
		}
	} else {
		var name = key + '=',
			ca = document.cookie.split(';');
		
		var erg = '';
		
		$.each(ca, $.proxy(function(i, val) {
			var c = $.trim(val);
			
			if(c.indexOf(name) === 0) {
				if(noParse) {
					erg = c.substring(name.length, c.length);
					return;
				} else {
					erg = JSON.parse(c.substring(name.length, c.length));
					return;
				}
			}
		}, this));
		
		return erg;
	}
}

/**
 * save a value to the storage
 * use noParse if you dont want the value to be parsed
 * 
 * @param {String} key
 * @param {Mixed} value
 * @param {Boolean} noParse
 * @returns {void}
 */
Storage.prototype.set = function(key, value, noParse) {
	if(this.storage) {
		if(noParse) {
			this.storage.setItem(key, value);
		} else {
			this.storage.setItem(key, JSON.stringify(value));
		}
	} else {
		var date = new Date(),
			expires = "";
		
		if(this.type === 'local') {
			data.setTime(date.getTime() + (365 * 24 * 60 * 60 * 1000));
			expires = '; expires=' + date.toGMTString();
		}
		
		if(noParse) {
			document.cookie = key + '=' + value + expires + '; path=/';
		} else {
			document.cookie = key + '=' + JSON.stringify(value) + expires + '; path=/';
		}
	}
};

/**
 * remove an item from the storae
 * 
 * @param {String} key
 * @returns {void}
 */
Storage.prototype.unset = function(key) {
	if(this.storage) {
		this.storage.removeItem(key);
	} else {
		document.cookie = key + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT';
	}
};