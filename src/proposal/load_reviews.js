sgreviews = function() {
    $('div.rateit, span.rateit').rateit();

    // load all comments
    $(".review-comments").each(function(index, element) {
        review_id = /-(\d+)$/g.exec(element.id)[1];
        url = "{% url 'comments' request.goal.slug 12345 %}".replace("12345", review_id);
        $(element).load(url);
    });
}

$(document).ready(function() {
    $("#reviews").load(
        "{% url 'reviews' request.goal.slug proposal.slug %}",
        sgreviews
    );
});
