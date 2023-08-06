// ROI widgets
// Leon Avery, 18=Sep-2014

define(["widgets/js/widget",
        "widgets/js/widget_selection"],
function(WidgetManager) {

    // widgets/widget_selection doesn't export SelectView, so we find
    // it this way. This is almost certainly a very bad idea.
    //
    var SelectView = WidgetManager._view_types.SelectView;

    // Class definition
    //
    var ClickSelectView = SelectView.extend({

        render: function() {
	    ClickSelectView.__super__.render.apply(this, arguments);
	    this.$el.on('dblclick', '', this, onDoubleClick);
        },

    });

    WidgetManager.register_widget_view('ClickSelectView',
				       ClickSelectView);

    var onDoubleClick = function(event) {
	var w = event.data;
        w.send({event: 'submit'});
	return false;
    }

    return ClickSelectView;
});
