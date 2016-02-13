(function($) {
    $.fn.sg_review_list = function() {
        return this.each(function(dummy_index, review_list_div) {

            $(review_list_div).find('div.rateit, span.rateit').rateit();
            $(review_list_div).find('.sg-comment-list').sg_comment_list();

            // connect link for replying to the review
            $(review_list_div).find('.comment-reply-link').sg_comment_reply_link();
        });
    };
}(jQuery));
