sgreviews = function() {
    $('div.rateit, span.rateit').rateit();

    // load comments into each comment-block
    $(".comment-block").each(function(index, comment_block) {

        // load comments into this comment-block
        url_get_comment_block = $(comment_block).data("ajax-url");
        $(comment_block).load(url_get_comment_block, function() {

            // connect all reply-links within this comment-block
            var reply_links = $(comment_block).find(".comment-reply-link");
            reply_links.each(function(index, reply_link) {

                // connect this reply-link, so that it loads a form into reply-div
                $(reply_link).click(function() {

                    // load a reply form with ajax
                    url_get_comment_form = $(reply_link).data("ajax-url");
                    reply_div = $(reply_link).siblings(".comment-reply-div")[0];
                    $(reply_div).load(url_get_comment_form);
                });
           });
        });
    });
}

$(document).ready(function() {
    $("#reviews").load(
        "{% url 'reviews' request.goal.slug proposal.slug %}",
        sgreviews
    );
});
