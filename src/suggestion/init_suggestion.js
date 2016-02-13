$(document).ready(function() {
    $('#rateit-review').bind('rated', function() {
        $('#id_rating').val($(this).rateit('value'));
    });

    $("#review-form").submit(function(event) {

        // Stop form from submitting normally
        event.preventDefault();

        // Send the data using post
        var posting = $.post(
            $("#review-form").data("ajax-url"),
            $(this).serialize() + "&submit=" + $(document.activeElement)[0].value
        );

        // Put the results in a div
        posting.done(function(data) {
            $("#sg-review-list").html(data);
            $("#sg-review-list").sg_review_list();
        });
    });

    $("#sg-review-list").load(
        "{% url 'reviews' request.goal.slug suggestion.slug %}",
        function() {
            $(this).sg_review_list();
        }
    );
});
