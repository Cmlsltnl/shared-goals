(function($) {
    $.fn.djangoJcrop = function() {
        return this.each(function(dummy_index, imgElement) {
            var img_elm = $(imgElement)

            function updateCropping(c) {
                c.natural_height = img_elm.prop('naturalHeight');
                c.natural_width = img_elm.prop('naturalWidth')
                c.display_height = img_elm.height();
                c.display_width = img_elm.width();
                var data = JSON.stringify(c);
                $("#" + img_elm.data("output-id")).val(data);
            }

            var rawData = img_elm.data("jcrop").replace(/'/g, '"');
            var options = JSON.parse(rawData);
            options.onSelect = updateCropping;
            options.onChange = updateCropping;
            img_elm.Jcrop(options);
        });
    };
}(jQuery));
