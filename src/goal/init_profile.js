$(document).ready(function() {

    function on_click_notification() {
    };

    $(".sg-notification").each(function (dummy_index, notification) {
        $(notification).click(on_click_notification);
    });
});
