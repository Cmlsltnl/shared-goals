$(document).ready(function() {
    url_suggestion_image = $("#suggestion-image-div").data("ajax-url");

    // load form into div
    var on_image_form_loaded = function() {

        // respond to submitting the form
        $("#image-form").submit(function(event) {
            // Stop form from submitting normally
            event.preventDefault();

            var data = new FormData();
            data.append('csrfmiddlewaretoken', $("#image-form").data('token'));
            data.append('submit', 'upload');
            data.append('image', $("#id_image")[0].files[0]);

            // Send the data using post
            var posting = $.post({
                url: url_suggestion_image,
                data: data,
                cache: false,
                processData: false,
                contentType: false,
            });

            // // Load the result into the image div
            // posting.done(function(data) {
            //     $("#suggestion-image-div").load(url_suggestion_image);
            // });
        });

        // todo reenable automatic upload
        // $("#id_file_input").change(function () {
        //     $('#upload-submit').trigger('click');
        // });
    };

    $("#suggestion-image-div").load(url_suggestion_image, on_image_form_loaded);
});
