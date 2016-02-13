sgreviews = function() {
    $('div.rateit, span.rateit').rateit();

    function on_comment_form_submit(event) {
        event.preventDefault();

        // Send the data using post
        var form = $(this);
        var posting = $.post(
            form.data("ajax-url"),
            form.serialize() + "&submit=" + $(document.activeElement)[0].value
        );

        // Put the results in a div
        posting.done(function(data) {
            if (data.success) {
                load_comment_block(0, form.closest(".comment-block"));
            }
        });
    }

    function init_reply_div() {
        // connect post button to do an ajax post
        form = $(this).find("form")[0];
        url_get_reply_form = $(this).data("ajax-url");
        $(form).data("ajax-url", url_get_reply_form);
        $(form).submit(on_comment_form_submit);
    }

    function on_click_reply_link() {
        // respond to clicking on $(this) reply link by showing a reply form
        reply_div = $(this).siblings(".comment-reply-div")[0];
        url_get_reply_form = $(this).data("ajax-url");
        $(reply_div).data("ajax-url", url_get_reply_form);
        $(reply_div).load(url_get_reply_form, init_reply_div);
    }

    function init_comment_block() {
        // connect all reply-links within $(this) comment-block
        $(this).find(".comment-reply-link").each(function(index, reply_link) {
            $(reply_link).click(on_click_reply_link);
        });
    }

    function load_comment_block(dummy_index, comment_block) {
        // load comments into this comment-block
        url_get_comment_block = $(comment_block).data("ajax-url");
        $(comment_block).load(url_get_comment_block, init_comment_block);
    }

    (function($) {
        $.fn.load_comment_block = function() {
            return this.each(load_comment_block);
        };
    }(jQuery));

    $(".comment-block").load_comment_block();
}

$(document).ready(function() {
    $("#reviews").load(
        "{% url 'reviews' request.goal.slug suggestion.slug %}",
        sgreviews
    );
});
