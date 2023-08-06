// ROI widgets
// Leon Avery, 18=Sep-2014

define(["widgets/js/widget",
	"widgets/js/widget_roi",
	"components/raphael/raphael"],
function(WidgetManager, ROIMultiPointWidgetView, Raphael) {

    // Class definition
    //
    var ROIRectWidgetView = ROIMultiPointWidgetView.extend({

	path: function() {
	    if (_.size(this.handles) != 2) {
		return null;
	    }
	    var ids = _.keys(this.handles);
	    var x0 = this.handles[ids[0]][0],
		y0 = this.handles[ids[0]][1],
		x1 = this.handles[ids[1]][0],
		y1 = this.handles[ids[1]][1];
	    var xmin = Math.min(x0, x1),
		xmax = Math.max(x0, x1),
		ymin = Math.min(y0, y1),
		ymax = Math.max(y0, y1);
	    var path = 'M' + xmin.toString() + ',' + ymin.toString() +
		       'L' + xmin.toString() + ',' + ymax.toString() +
		       'L' + xmax.toString() + ',' + ymax.toString() +
		       'L' + xmax.toString() + ',' + ymin.toString() +
		       'z';
	    return path;
	},

	// check if OK to add handle
	addOK: function(r) {
	    return _.size(this.handles) < 2;
	},

	addHandle: function(r, id) {
	    id = ROIRectWidgetView.__super__.addHandle.apply(this, arguments);
	    // if there were none, add 2 at same location
	    if (_.size(this.handles) == 1) {
		var id2 = ROIRectWidgetView.__super__.addHandle.apply(
		    this, arguments);
	    }
	    return id;
	},

    });

    WidgetManager.register_widget_view('ROIRectWidgetView',
				       ROIRectWidgetView);

    // Class definition
    //
    var ROIMultiRectWidgetView = ROIMultiPointWidgetView.extend({

        initialize: function() {
	    ROIMultiRectWidgetView.__super__.initialize.apply(this, arguments);
	    this.handleOrder = _.clone(this.model.get('handleOrder'));
	},

	path: function() {
	    var n = this.handleOrder.length;
	    var path = '';
	    for(var i = 0; i < n-1; i += 2) {
		var x0 = this.handles[this.handleOrder[i]][0],
		    y0 = this.handles[this.handleOrder[i]][1],
		    x1 = this.handles[this.handleOrder[i+1]][0],
		    y1 = this.handles[this.handleOrder[i+1]][1];
		var xmin = Math.min(x0, x1),
		    xmax = Math.max(x0, x1),
		    ymin = Math.min(y0, y1),
		    ymax = Math.max(y0, y1);
		path += 'M' + xmin.toString() + ',' + ymin.toString() +
		        'L' + xmin.toString() + ',' + ymax.toString() +
		        'L' + xmax.toString() + ',' + ymax.toString() +
		        'L' + xmax.toString() + ',' + ymin.toString() +
		        'z';
	    }
	    return path;
	},

	// add and delete handles in pairs
	//
	addHandle: function(r, id) {
	    id = ROIRectWidgetView.__super__.addHandle.call(this, r, id);
	    this.handleOrder.push(id);
	    if (this.handleOrder.length & 1 == 0) return id;
	    id = ROIRectWidgetView.__super__.addHandle.call(this, r);
	    this.handleOrder.push(id);
	    this.model.set('handleOrder', _.clone(this.handleOrder));
	    this.touch();
	    this.pathDraw();
	    return id;
	},

	deleteHandle: function(id) {
	    if (this.handleOrder.length & 1 == 1) {
		// shouldn't happen. If it does, just delete the one handle
		this.handleOrder = _.without(this.handleOrder, id);
		this.model.set('handleOrder', _.clone(this.handleOrder));
		this.touch();
		ROIMultiRectWidgetView.__super__.deleteHandle.apply(
		    this, arguments);
		return this;
	    }
	    var i = _.indexOf(this.handleOrder, id);
	    if (i < 0) {	// shouldn't happen
		ROIMultiRectWidgetView.__super__.deleteHandle.call(this, id);
		return this;
	    }
	    var i1 = i | 1,
		i0 = i1 - 1;
	    var id0 = this.handleOrder[i0],
		id1 = this.handleOrder[i1];
	    this.handleOrder.splice(i0, 2);
	    this.model.set('handleOrder', _.clone(this.handleOrder));
	    this.touch();
	    ROIMultiRectWidgetView.__super__.deleteHandle.call(this, id0);
	    ROIMultiRectWidgetView.__super__.deleteHandle.call(this, id1);
	    return this;
	},

    });

    WidgetManager.register_widget_view('ROIMultiRectWidgetView',
				       ROIMultiRectWidgetView);

    return [ROIRectWidgetView, ROIMultiRectWidgetView];
});
