(function($) {
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
                form.closest(".sg-comment-list").sg_comment_list();
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

    $.fn.sg_comment_reply_link = function() {
        return this.each(function(dummy_index, reply_link) {
            $(reply_link).click(on_click_reply_link);
        });
    };
}(jQuery));


(function($) {
    function init_comment_list() {
        // connect all reply-links within $(this) comment list
        $(this).find(".comment-reply-link").sg_comment_reply_link();
    }

    $.fn.sg_comment_list = function() {
        return this.each(function(dummy_index, comment_list) {

            // load comments into this comment list
            url_get_comment_list = $(comment_list).data("ajax-url");
            $(comment_list).load(url_get_comment_list, init_comment_list);
        });
    };
}(jQuery));
