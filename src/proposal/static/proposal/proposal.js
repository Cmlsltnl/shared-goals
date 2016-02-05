$(window).load(function() {
    $('#rateit-review').bind('rated', function() {
        $('#id_rating').val($(this).rateit('value'));
    });

    $("#top-right-div-inner").prepend($("#btn-edit-proposal"));
});