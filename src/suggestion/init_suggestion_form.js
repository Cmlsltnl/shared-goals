$(document).ready(function() {
    var chkPreviewElm = $("#chkPreview");
    function onChkPreviewChanged() {
        var previewElm = $("#descriptionPreview");
        var descriptionElm = $("#description");
        url_get_preview = previewElm.data("ajax-url");
        var token = $("input[name='csrfmiddlewaretoken']").val();
        previewElm.load(
            url_get_preview,
            {
                csrfmiddlewaretoken: token,
                text: descriptionElm.val()
            }
        );
        if ($("#chkPreview").prop('checked')) {
            previewElm.removeClass("hidden-but-not-gone");
            descriptionElm.addClass("hidden-but-not-gone");
        }
        else {
            previewElm.addClass("hidden-but-not-gone");
            descriptionElm.removeClass("hidden-but-not-gone");
        }
        // previewElm.toggle($("#chkPreview").prop('checked'));
        // descriptionElm.toggle(!$("#chkPreview").prop('checked'));
    }
    chkPreviewElm.change(onChkPreviewChanged);
    onChkPreviewChanged();
});
