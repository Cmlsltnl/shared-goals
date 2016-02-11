sgreviews = function() {
    $('div.rateit, span.rateit').rateit();

    function on_comment_form_submit(event) {
        alert($(document.activeElement)[0].value);
        event.preventDefault();
    }

    function init_reply_div() {
        // connect post button to do an ajax post
        form = $(this).find("form")[0];
        $(form).submit(on_comment_form_submit);
    }

    function on_click_reply_link() {
        // respond to clicking on $(this) reply link by showing a reply form
        reply_div = $(this).siblings(".comment-reply-div")[0];
        url_get_reply_form = $(this).data("ajax-url");
        $(reply_div).load(url_get_reply_form, init_reply_div);
    }

    function init_comment_block() {
        // connect all reply-links within $(this) comment-block
        $(this).find(".comment-reply-link").each(function(index, reply_link) {
            $(reply_link).click(on_click_reply_link);
        });
    }

    function init_reviews() {
        $(".comment-block").each(function(index, comment_block) {
            // load comments into this comment-block
            url_get_comment_block = $(comment_block).data("ajax-url");
            $(comment_block).load(url_get_comment_block, init_comment_block);
        });
    }

    init_reviews();
}

$(document).ready(function() {
    $("#reviews").load(
        "{% url 'reviews' request.goal.slug suggestion.slug %}",
        sgreviews
    );
});
