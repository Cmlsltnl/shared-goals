$(document).ready(function() {

    function on_click_notification() {
        $.post($(this).data("notification-read-url"));
        $(this).removeClass('sg-notification-read-0');
        $(this).addClass('sg-notification-read-1');
        // window.location = $(this).data("next-url");
    };

    $(".sg-notification").each(function (dummy_index, notification) {
        $(notification).click(on_click_notification);
    });
});
