// ROI widgets
// Leon Avery, 18=Sep-2014

define(["widgets/js/widget",
	"widgets/js/widget_roi",
	"components/raphael/raphael"],
function(WidgetManager, ROIMultiPointWidgetView, Raphael) {

    // Class definition
    //
    var ROIPolygonWidgetView = ROIMultiPointWidgetView.extend({

        initialize: function() {
	    ROIPolygonWidgetView.__super__.initialize.apply(this, arguments);
	    this.handleOrder = _.clone(this.model.get('handleOrder'));
	},

	path: function() {
	    var n = this.handleOrder.length;
	    if (n <= 1) {
		return null;
	    }
	    var x = this.handles[this.handleOrder[0]][0],
		y = this.handles[this.handleOrder[0]][1];
	    var path = 'M' + x.toString() + ',' + y.toString();
	    for(var i = 1; i < n; i++) {
		x = this.handles[this.handleOrder[i]][0],
		y = this.handles[this.handleOrder[i]][1];
		path += 'L' + x.toString() + ',' + y.toString();
	    }
	    path += 'z';
	    return path;
	},

	closestSide: function(p) {
	    var n = this.handleOrder.length;
	    if (n <= 2) {
		return n;
	    }
	    var dmin = point2LineDistance(
		p,
		this.handles[this.handleOrder[n-1]],
		this.handles[this.handleOrder[0]]
	    );
	    var imin = n;
	    for(var i = 0; i < n-1; i++) {
		var d = point2LineDistance(
		    p,
		    this.handles[this.handleOrder[i]],
		    this.handles[this.handleOrder[i+1]]
		);
		if (d < dmin) {
		    dmin = d;
		    imin = i;
		}
	    }
	    return imin;
	},

	addHandle: function(r, id) {
	    id = ROIPolygonWidgetView.__super__.addHandle.apply(
		this, arguments);
	    var i = this.closestSide(this.handles[id]);
	    this.handleOrder.splice(i+1, 0, id);
	    this.model.set('handleOrder', _.clone(this.handleOrder));
	    this.touch();
	    this.pathDraw();
	    return id;
	},

	deleteHandle: function(id) {
	    this.handleOrder = _.without(this.handleOrder, id);
	    this.model.set('handleOrder', _.clone(this.handleOrder));
	    this.touch();
	    ROIPolygonWidgetView.__super__.deleteHandle.apply(
		this, arguments);
	    return this;
	},

    });

    WidgetManager.register_widget_view('ROIPolygonWidgetView',
				       ROIPolygonWidgetView);

    // distance of a point from a line segment
    var point2LineDistance = function(p, e0, e1) {
	var x = p[0], y = p[1],
	    x0 = e0[0], y0 = e0[1],
	    x1 = e1[0], y1 = e1[1];
	var t = (x - x0)*(x1 - x0) + (y - y0)*(y1 - y0);
	if (t <= 0) {
	    // degenerate case or closest point is e0
	    var d0 = (x - x0)*(x - x0) + (y - y0)*(y - y0);
	    return Math.sqrt(d0);
	}
	else if (t >= l2) {
	    // closest point is e1
	    var d1 = (x - x1)*(x - x1) + (y - y1)*(y - y1);
	    return Math.sqrt(d1);
	}
	else {
	    // closest point is in segment
	    var l2 = (x1 - x0)*(x1 - x0) + (y1 - y0)*(y1 - y0);
	    var dl = x*(y1 - y0) + y*(x0 - x1) + x1*y0 - x0*y1;
	    return Math.abs(dl) / Math.sqrt(l2);
	}
    };

    return ROIPolygonWidgetView;
});
