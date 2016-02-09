$(window).load(function() {
    $('#rateit-review').bind('rated', function() {
        $('#id_rating').val($(this).rateit('value'));
    });
    $("#id_image").change( function(){
        $('#upload-submit').trigger('click');
    });
});
