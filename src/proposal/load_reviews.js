sgreviews = function() {
    $('div.rateit, span.rateit').rateit();

    // load comments into each comment-block
    $(".comment-block").each(function(index, comment_block) {
        review_id = /-(\d+)$/g.exec(comment_block.id)[1];

        // load comments into this comment-block
        url_get_comment_block = "{% url 'comments' request.goal.slug 123 %}".replace("123", review_id);
        $(comment_block).load(url_get_comment_block, function() {

            // connect all reply-links within this comment-block
            var reply_links = $(comment_block).find(".comment-reply-link");
            reply_links.each(function(index, reply_link) {

                // connect this reply-link, so that it loads a form into reply-div
                $(reply_link).click(function() {
                    // load a reply form with ajax
                    comment_id = /-(\d+)$/g.exec(reply_link.id)[1];
                    url_get_comment_form = "{% url 'reply_comment' request.goal.slug 123 456 %}".replace("123", review_id).replace("456", comment_id);

                    reply_div = $(reply_link).siblings(".comment-reply-div")[0];
                    // alert(reply_div);
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
