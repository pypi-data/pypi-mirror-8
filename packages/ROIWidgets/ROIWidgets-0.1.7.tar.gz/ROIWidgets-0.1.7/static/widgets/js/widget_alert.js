// ROI widgets
// Leon Avery, 18=Sep-2014

define(["widgets/js/widget"],
function(WidgetManager) {

    // Class definition
    //
    var AlertWidgetView = IPython.DOMWidgetView.extend({

        render: function() {
	    AlertWidgetView.__super__.render.apply(this, arguments);
	    this.doAlert();
        },

        update: function() {
	    AlertWidgetView.__super__.update.apply(this, arguments);
	    this.doAlert();
        },

	doAlert: function(event) {
	    this.value = this.model.get('value')
	    if (this.value) {
		window.alert(this.value);
	    }
	    this.value = '';
	    this.model.set('value', this.value);
	    this.touch();
	},

    });

    WidgetManager.register_widget_view('AlertWidgetView',
				       AlertWidgetView);

    return AlertWidgetView;
});
