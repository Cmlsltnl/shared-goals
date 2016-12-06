import { browserHistory } from 'react-router'

var SuggestionPageMixin = {
  uploadImage: function(file) {
    var fd = new FormData();
    fd.append("image", file);

    $.ajax({
      type: "POST",
      url: this.getImageUploadUrl(),
      data: fd,
      processData: false,
      contentType: false,
      success: function(data) {
        this.props.setImageUrl(data.image_url);
      }.bind(this),
      error: function(jqXHR, textStatus, errorMessage) {
         console.log(errorMessage); // Optional
      }.bind(this)
    });
  },

  postSuggestion: function(form_data, get_next_url) {
    $.ajax({
      type: "POST",
      url: this.getSuggestionUrl(),
      data: form_data,
      success: function(data)
      {
        this.props.receivePostedSuggestion(data);
        if (data.success) {
          browserHistory.push(get_next_url(data))
        }
      }.bind(this)
    });
  },
};

export default SuggestionPageMixin;
