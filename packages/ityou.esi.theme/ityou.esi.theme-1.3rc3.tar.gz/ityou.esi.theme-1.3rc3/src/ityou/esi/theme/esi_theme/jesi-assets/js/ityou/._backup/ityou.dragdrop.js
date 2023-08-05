/*

function DragDrop() {
    this.options = {
        templateDnDContainer: '#dragdrop-dragdropcontainer-tmpl',
    };
    
    this.getOption = function(option) {
        if(this.options.hasOwnProperty(option)) {
            return this.options[option];
        }
        
        return null;
    };
}


DragDrop.prototype = new Utilities();


DragDrop.prototype.checkPermission = function(el, state) {
    $.getJSON('@@ajax-dragdrop', {action: state, uid: el.attr('id')}, $.proxy(function(response) {
        if(this.toBoolean(response) === true) {
            el.draggable(); // TODO draggableOptions
            el.removeClass('can-not-move-or-copy');
        } else {
            el.draggable('destroy');
            el.addClass('can-not-move-or-copy');
        }
    }, this));
};


DragDrop.prototype.getObjects = function() {
    $.getJSON('@@ajax-dragdrop', {action: 'get_objects'}, $.proxy(function(response) {
        if(response.length > 0) {
            var portlet = 'dl.portlet-static-drag-drop';
            
            $(portlet).find('#dragdrop-portlet-text').hide();
            
            $.each(response, $.proxy(function(i, val) {
                val.thumbnail_class = (val.portal_type.toLowerCase() === 'folder' ? '' : 'linked-document link-overlay');
                
                $($(this.getOption('templateDnDContainer')).render(val)).appendTo(portlet + ' p#dragdrop-container');
            }, this));
            
            $('.drag-drop-container').each($.proxy(function(k, el) {
                var $el = $(el),
                    state = $(portlet).find('.copy-move-container').find('.action-bar.move').hasClass('state-active') ?  'can_move' : 'can_copy';
                    
                this.checkPermission($el, state);
            }, this));
        }
    }, this));
};



*/



$(function() {
    
    /*dragdrop = new DragDrop();
    
    if($('dl.portlet-static-drag-drop').length > 0) {
        dragdrop.getObjects();
    }
    */
    
});
