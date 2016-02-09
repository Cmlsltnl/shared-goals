$(window).load(function() {
    $("#id_image").change( function(){
        $('#upload-submit').trigger('click');
    });
});
