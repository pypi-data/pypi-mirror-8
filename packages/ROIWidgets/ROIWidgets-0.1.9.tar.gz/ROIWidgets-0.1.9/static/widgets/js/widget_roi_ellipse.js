// ROI widgets
// Leon Avery, 18=Sep-2014

define(["widgets/js/widget",
	"widgets/js/widget_roi",
	"components/raphael/raphael"],
function(WidgetManager, ROIMultiPointWidgetView, Raphael) {

    var circlePath = function(p0, p1) {
	var x0 = p0[0],
	    y0 = p0[1],
	    x1 = p1[0],
	    y1 = p1[1];
	var xmin = Math.min(x0, x1),
	    xmax = Math.max(x0, x1),
	    ymin = Math.min(y0, y1),
	    ymax = Math.max(y0, y1);
	var left = xmin * (1 + Math.sqrt(2.0)) / 2 +
	    xmax * (1 - Math.sqrt(2.0)) / 2,
	    right = xmin * (1 - Math.sqrt(2.0)) / 2 +
	    xmax * (1 + Math.sqrt(2.0)) / 2,
	    mid = (ymin + ymax) / 2.0,
	    rx = (xmax - xmin) / Math.sqrt(2.0),
	    ry = (ymax - ymin) / Math.sqrt(2.0);
	var path =
	    'M' + left.toString() + ',' + mid.toString() +
	    'A' + rx.toString() + ',' + ry.toString() +
	    ',0,1,0,' + 
	    right.toString() + ',' + mid.toString() +
	    'A' + rx.toString() + ',' + ry.toString() +
	    ',0,1,0,' + 
	    left.toString() + ',' + mid.toString() +
	    'z';
	return path;
    };

    // Class definition
    //
    var ROIEllipseWidgetView = ROIMultiPointWidgetView.extend({

	path: function() {
	    if (_.size(this.handles) != 2) {
		return null;
	    }
	    var ids = _.keys(this.handles);
	    return circlePath(this.handles[ids[0]], this.handles[ids[1]]);
	},

	// check if OK to add handle
	addOK: function(r) {
	    return _.size(this.handles) < 2;
	},

	addHandle: function(r, id) {
	    id = ROIEllipseWidgetView.__super__.addHandle.apply(
		this, arguments);
	    // if there were none, add 2 at same location
	    if (_.size(this.handles) == 1) {
		var id2 = ROIEllipseWidgetView.__super__.addHandle.apply(
		    this, arguments);
	    }
	    return id;
	},

    });

    WidgetManager.register_widget_view('ROIEllipseWidgetView',
				       ROIEllipseWidgetView);

    // Class definition
    //
    var ROIMultiEllipseWidgetView = ROIMultiPointWidgetView.extend({

        initialize: function() {
	    ROIMultiEllipseWidgetView.__super__.initialize.apply(
		this, arguments);
	    this.handleOrder = _.clone(this.model.get('handleOrder'));
	},

	path: function() {
	    var n = this.handleOrder.length;
	    var path = '';
	    for(var i = 0; i < n-1; i += 2) {
		path += circlePath(this.handles[this.handleOrder[i]],
				   this.handles[this.handleOrder[i+1]]);
	    }
	    return path;
	},

	// add and delete handles in pairs
	//
	addHandle: function(r, id) {
	    id = ROIEllipseWidgetView.__super__.addHandle.call(this, r, id);
	    this.handleOrder.push(id);
	    if (this.handleOrder.length & 1 == 0) return id;
	    id = ROIEllipseWidgetView.__super__.addHandle.call(this, r);
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
		ROIMultiEllipseWidgetView.__super__.deleteHandle.apply(
		    this, arguments);
		return this;
	    }
	    var i = _.indexOf(this.handleOrder, id);
	    if (i < 0) {	// shouldn't happen
		ROIMultiEllipseWidgetView.__super__.deleteHandle.call(
		    this, id);
		return this;
	    }
	    var i1 = i | 1,
		i0 = i1 - 1;
	    var id0 = this.handleOrder[i0],
		id1 = this.handleOrder[i1];
	    this.handleOrder.splice(i0, 2);
	    this.model.set('handleOrder', _.clone(this.handleOrder));
	    this.touch();
	    ROIMultiEllipseWidgetView.__super__.deleteHandle.call(
		this, id0);
	    ROIMultiEllipseWidgetView.__super__.deleteHandle.call(
		this, id1);
	    return this;
	},

    });

    WidgetManager.register_widget_view('ROIMultiEllipseWidgetView',
				       ROIMultiEllipseWidgetView);

    return [ROIEllipseWidgetView, ROIMultiEllipseWidgetView];
});
