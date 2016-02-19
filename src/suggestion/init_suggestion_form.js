$(document).ready(function() {
    function updateCropping(c) {
        var data = JSON.stringify(c);
        $("#cropping").val(data)
    }

    $("#suggestion-image").Jcrop({
        aspectRatio: 360 / 200,
        setSelect: [ 0, 0, 180, 100 ],
        onSelect: updateCropping,
        onChange: updateCropping,
    });
});
