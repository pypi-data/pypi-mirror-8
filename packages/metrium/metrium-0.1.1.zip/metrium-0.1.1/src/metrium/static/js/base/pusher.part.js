(function(jQuery) {
    jQuery.fn.upusher = function(options) {
        var matchedObject = this;
        matchedObject.each(function() {
                    var element = jQuery(this);
                    var key = element.attr("data-key");
                    if (!key) {
                        return;
                    }

                    var pusher = new Pusher(key);
                    element.data("pusher", pusher);
                });
        return matchedObject;
    };
})(jQuery);
