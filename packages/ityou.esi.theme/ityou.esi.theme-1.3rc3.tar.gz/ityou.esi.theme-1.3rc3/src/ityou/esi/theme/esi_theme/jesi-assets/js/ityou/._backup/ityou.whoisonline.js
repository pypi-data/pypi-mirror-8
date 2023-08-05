function WhoIsOnline() {
    this.cache = {
        
    };
    
    
    this.settings = {
        timeout: 0,
        delta: 0,
        
        refreshState: 1000
    };
    
    
    this.selector = {
        list: '#who-is-online ul',
        portlet: '.portletWhoIsOnline',
        profileBox: '.userprofile-box',
        profile: '.who-is-online-box',
        
        counter: '#whoisonline-counter'
    };
    
    
    this.template = {
        whoisonline: '#whoisonline-tmpl',
        profile: '#whoisonline-profile-tmpl'
    };
    
    
    
    this.getSelector = function(key) {
        return this.get(key, 'selector');
    };
    
    
    this.getTemplate = function(key) {
        return this.get(key, 'template');
    };
    
    
    this.getCache = function(key) {
        return this.get(key, 'cache');
    };
    
    this.getSettings = function(key) {
        return this.get(key, 'settings');
    };
    
    
    this.setCache = function(key, value) {
        return this.set(key, value, 'cache');
    };
    
    
    
    this.get = function(key, property) {
        if(this.hasOwnProperty(property) && this[property].hasOwnProperty(key)) {
            return this[property][key];
        }
        
        return undefined;
    };
    
    this.set = function(key, value, property) {
        this[property][key] = value;
        return this;
    };
    
    this.setSettings = function(settings) {
    	if(settings) {
    		this.settings = $.extend(this.settings, settings);
    	}
    };
    
    
    this.attachEventHandler();
};


WhoIsOnline.prototype = new Utilities();



WhoIsOnline.prototype.hasPortlet = function() {
    if($(this.getSelector('portlet')).length > 0) {
        return true;
    }
    
    return false;
};



WhoIsOnline.prototype.counter = function(data) {
	$(this.getSelector('counter')).text(data.length);

	if(data.length === 0) {
		$(this.getSelector('counter')).addClass('hidden');
	} else {
		$(this.getSelector('counter')).removeClass('hidden');
	}
};



WhoIsOnline.prototype.onPortrait = function(data) {
	var run = true;
	
	if(false === data) {
		run = false;
		data = this.getCache('online');
	}
	
	data.push({id:$('#ESI_DATA').data('ityou-uid')});
	
	$.each(data, $.proxy(function(i, val) {
		$('body').find('.user-portrait[data-uid="' + val.id + '"]').each($.proxy(function(k, el) {
			if($(el).find('.online-status').length === 0) {
				$(el).append('<div class="online-status online"></div>');
			}
		}, this));
	}, this));
	
	if(run) {
		var x = 0, y = 0;
		var t = setInterval($.proxy(function() {
			y++;
			
			if((y > 10 && x === 0)) {
				clearInterval(t);
			} else {
				x = 0;
				$.each(data, $.proxy(function(i, val) {
					$('body').find('.user-portrait[data-uid="' + val.id + '"]').each($.proxy(function(k, el) {
						if($(el).find('.online-status').length === 0) { x++;
							$(el).append('<div class="online-status online"></div>');
						}
					}, this));
				}, this));
			}
		}, this), 350);
	}
};



WhoIsOnline.prototype.getAll = function() {
    clearInterval(this.getCache('opacity'));

    $.ajax({
        url: '@@ajax-whoisonline',
        data: {
            time_client: (new Date()).getTime() / 1000
        },
        dataType: 'json',
        timeout: 30000,
        // event handler success
        success: $.proxy(function(response) {
        	this.setCache('online', response);
        	
        	if(this.hasPortlet()) {
	            if(response.length > 0) {
	                this.render(response);
	                // show portlet
	                $(this.getSelector('portlet')).show();
	            } else {
	                // clear box
	                $(this.getSelector('list')).empty();
	                // hide portlet
	                $(this.getSelector('portlet')).hide();
	            }
        	}
        	
    		this.onPortrait(response);
    		this.counter(response);
        }, this),
        // event handler error
        error: $.proxy(function(XMLHttpRequest, textStatus, errorThrown) {
            
        }, this)
    });
};



WhoIsOnline.prototype.render = function(data) {
    // profile
    // portrait
    // bar
    // id
    // recent_time
    // timeout_online
    // time_delta
    
    var tmp = this.getCache('userlist');
    this.setCache('userlist', data);
    
    var $tmpl = $(this.getTemplate('whoisonline')),
        $list = $(this.getSelector('list'));
        
    if(data.length > 0) {
        this.set('timeout', data[0].timeout_online, 'settings');
        this.set('delta', data[0].time_delta, 'settings');
    }
    
    $.each(data, $.proxy(function(key, value) {
        var $li = $list.find('li[data-id="' + value.id + '"]');
    
        if($li.length === 0) {
            $li = $($tmpl.render(value));
            $li.appendTo(this.getSelector('list'));
        }
        
        $li.find('img').css('opacity', value.bar);
        
        this.renderTooltip(value, $li);
    }, this));
    
    var opacity = setInterval($.proxy(function() {
        this.renderOpacity();
    }, this), this.getSettings('refreshState'));
    
    this.setCache('opacity', opacity);
};



WhoIsOnline.prototype.renderOpacity = function() {
    var savedUserlist = this.getCache('userlist'),
        $liPortletUserlist = $(this.getSelector('list')).find('li');
        
    var timeout = this.getSettings('timeout'),
        delta = this.getSettings('delta'),
        splitter = timeout / 10,
        bigSplitter = timeout / 100,
        now = Math.round((new Date()).getTime() / 1000);
        
    var $list = $(this.getSelector('list'));
    
    $.each(savedUserlist, $.proxy(function(key, val) {
    
        var $li = $list.find('li[data-id="' + val.id + '"]');
    
        if($li.length > 0) {
            var logout = val.recent_time - delta + timeout,
                logout_delta = logout - now;
            
            if(logout_delta <= 0) {
                $li.remove();
            } else {
                // opacity image
                $li.find('img.img-icon').css('opacity', (Math.round(logout_delta / splitter) / 10));
                // bar width
                $li.find(this.getSelector('profile')).find('.bar').width(Math.round(logout_delta / bigSplitter) + '%');
            }
        }
    
    }, this));
};






WhoIsOnline.prototype.renderTooltip = function(data, element) {
    if(element.find(this.getSelector('profile')).length <= 0) {
        var tmpl = $(this.getTemplate('profile'));
        
        element.find(this.getSelector('profileBox')).append(tmpl.render(data));
    }
};




// attach event handler
// -----------------------------------------------------------------------------

WhoIsOnline.prototype.attachEventHandler = function() {

    // mouse
    $(this.getSelector('list')).on({
    
        mouseenter: $.proxy(function(e) {
            var $li = $(e.currentTarget).parents('li');
            
            if($li.find(this.getSelector('profile')).length > 0) {
                $li.find(this.getSelector('profileBox')).find('> div').each(function() {
                    $(this).show();
                });
            }
        }, this),
        
        mouseleave: $.proxy(function(e) {
            var $li = $(e.currentTarget).parents('li');
            
            $li.find(this.getSelector('profileBox')).find('> div').each(function() {
                $(this).hide();
            });
        }, this)
    
    }, '.portrait');

};

