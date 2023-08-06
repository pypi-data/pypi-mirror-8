// ROI widgets
// Leon Avery, 18=Sep-2014

define(["widgets/js/widget",
	"components/raphael/raphael"],
function(WidgetManager, Raphael) {

    // Class variable: used to generate unique IDs
    //
    var handleID = 1;

    // Class definition
    //
    var ROIMultiPointWidgetView = IPython.DOMWidgetView.extend({

	// Class methods
	//
	initialize: function() {
	    // console.log('initialize');
	    ROIMultiPointWidgetView.__super__.initialize.apply(this, arguments);
	    var w = Math.max(document.documentElement.clientWidth,
			     window.innerWidth || 0);
	    var h = Math.max(document.documentElement.clientHeight,
			     window.innerHeight || 0);
	    this.handles = _.clone(this.model.get('handles'));
	    this.handleSize = this.model.get('handleSize');
	    this.handleAttrs = this.model.get('handleAttrs');
	    this.pathAttrs = this.model.get('pathAttrs');
	    this.pathID = this.newID('path');
	},

        render: function() {
	    // console.log('render');
	    var width = this.model.get('width');
	    var height = this.model.get('height');
	    var imageURL = this.model.get('imageURL');

            this.paper = new Raphael(this.el, width, height);
            this.image = this.paper.image(imageURL, 0, 0, width, height);
	    this.$el.on('click', 'image', this, onClick);
	    _.each(this.handles,
		   function(v, k) { this.addHandle(v, k) },
		   this);
	    var path = this.path();
	    if (path) {
		this.pathDraw();
	    }
        },

	pathDraw: function() {
	    var path = this.path();
	    if (!path) {
		this.pathDelete();
		return null;
	    }
	    var pathNode = document.getElementById(this.pathID);
	    if (pathNode) {
		$(pathNode).attr('d', path);
	    }
	    else {
		pathElement = this.paper.path(path);
		pathNode = pathElement.node;
		pathElement.attr(this.pathAttrs);
		$(pathNode).attr({
		    id: this.pathID,
		    'class': 'ROIWidgetPath'
		});
		pathElement.id = this.pathID;
	    }
	    return pathNode;
	},

	pathDelete: function() {
	    var path = document.getElementById(this.pathID);
	    if (path) {
		path.remove();
	    }
	},

	newID: function(s) {
	    return s + handleID++;
	},

	// check if OK to add handle
	addOK: function(r) {
	    return true;
	},

	// check if OK to delete
	deleteOK: function(id) {
	    return true;
	},

	addHandle: function(r, id) {
	    if (!id) {
		// only check if really adding
		if (!this.addOK(r)) return;
		id = this.newID('handle');
	    }
	    this.handles[id] = r;
	    this.model.set('handles', _.clone(this.handles));
	    this.touch();
	    var handle = this.renderHandle(id);
	    this.$el.on('dblclick', '#'+id, this, onHandleDoubleClick);
	    this.$el.on('mousedown', '#'+id, this, onHandleDown);
	    this.pathDraw();
	    return id;
	},
	
	deleteHandle: function(id) {
	    if (!this.deleteOK(id)) return;
	    this.$el.off('dblclick', '#'+id, onHandleDoubleClick);
	    this.$el.off('mousedown', '#'+id, onHandleDown);
	    var handle = document.getElementById(id);
	    handle.remove();
	    delete(this.handles[id]);
	    this.model.set('handles', _.clone(this.handles));
	    this.touch();
	    this.pathDraw();
	    return this;
	},

	moveHandle: function(handle, x, y, id) {
	    handle.setAttribute('x', x - this.handleSize/2);
	    handle.setAttribute('y', y - this.handleSize/2);
	    this.handles[id] = [x, y];
	    this.pathDraw();
	    return handle;
	},

	renderHandle: function(id) {
	    var r = this.handles[id];
	    var x = r[0] - this.handleSize/2,
		y = r[1] - this.handleSize/2;
	    var handle = document.getElementById(id);
	    if (handle) {
		$(handle).attr({x: x, y: y});
	    }
	    else {
		handleElement = this.paper.rect(x, y, this.handleSize,
						this.handleSize);
		handle = handleElement.node;
		handleElement.attr(this.handleAttrs);
		$(handle).attr({
		    id: id,
		    'class': 'ROIWidgetHandle'
		});
		handleElement.id = id;
	    }
	    return handle;
	},

	// Calculate path to show for current state.
	// To be overridden by subclasses
	path: function() {
	    return null;
	},
    });

    WidgetManager.register_widget_view('ROIMultiPointWidgetView',
				       ROIMultiPointWidgetView);

    // Event handlers
    //
    var onHandleDown = function(event) {
	// console.log('mousedown');
	// console.log(event);
	var w = event.data;
	var origClientX = event.clientX,
	    origClientY = event.clientY;
	var handle = event.currentTarget;
	var id = handle.getAttribute('id');
	var x = w.handles[id][0],
	    y = w.handles[id][1];
	var origX = x, origY = y;

	var onHandleMove = function(event) {
	    // console.log('mousemove');
	    x = origX + event.clientX - origClientX;
	    y = origY + event.clientY - origClientY,
	    w.moveHandle(handle, x, y, id);
	    return false;
	};

	var onHandleUp = function(event) {
	    // console.log('mouseup');
	    w.$el.off('mousemove mouseup');
	    onHandleMove(event);
	    w.model.set('handles', _.clone(w.handles));
	    w.touch();
	    return false;
	};
	w.$el.on('mousemove', '', w, onHandleMove);
	w.$el.on('mouseup', '', w, onHandleUp);
	return false;
    };

    var onHandleDoubleClick = function(event) {
	// console.log('handleDoubleClick');
	// console.log(event);
	var w = event.data;
	var handle = event.currentTarget;
	var id = $(handle).attr('id');
	w.deleteHandle(id);
	return false;
    };

    var onClick = function(event) {
	// console.log('click');
	// console.log(event);
	if (event.which != 1) {	// only handle left button
	    return true;
	};
	var w = event.data;
	var paper = w.paper;
	// console.log(paper);
	var box = event.currentTarget.getBoundingClientRect();
	var r = [
	    event.clientX - box.left,
	    event.clientY - box.top
	];
	// console.log(r);
	var id = w.addHandle(r);
    };

    return ROIMultiPointWidgetView;
});
