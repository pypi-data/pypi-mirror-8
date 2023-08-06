// ROI widgets
// Leon Avery, 18=Sep-2014

define(["widgets/js/widget",
	"widgets/js/widget_roi",
	"components/raphael/raphael"],
function(WidgetManager, ROIMultiPointWidgetView, Raphael) {

    // Class definition
    //
    var ROILineWidgetView = ROIMultiPointWidgetView.extend({

	path: function() {
	    if (_.size(this.handles) != 2) {
		return null;
	    }
	    var ids = _.keys(this.handles);
	    var x0 = this.handles[ids[0]][0],
		y0 = this.handles[ids[0]][1],
		x1 = this.handles[ids[1]][0],
		y1 = this.handles[ids[1]][1];
	    var path = 'M' + x0.toString() + ',' + y0.toString() +
		       'L' + x1.toString() + ',' + y1.toString();
	    return path;
	},

	// check if OK to add handle
	addOK: function(r) {
	    return _.size(this.handles) < 2;
	},

	// check if OK to delete
	deleteOK: function(id) {
	    return true;
	},

	addHandle: function(r, id) {
	    id = ROILineWidgetView.__super__.addHandle.apply(this, arguments);
	    // if there were none, add 2 at same location
	    if (_.size(this.handles) == 1) {
		var id2 = ROILineWidgetView.__super__.addHandle.apply(
		    this, arguments);
	    }
	    return id;
	},

    });
    WidgetManager.register_widget_view('ROILineWidgetView',
				       ROILineWidgetView);

    return ROILineWidgetView;
});
