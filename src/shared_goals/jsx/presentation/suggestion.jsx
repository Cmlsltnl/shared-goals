import Widgets from 'presentation/widgets'
import Goal from 'presentation/goal'
import Review from 'presentation/review'

import React, { PropTypes } from 'react'
import ReactMarkdown from 'react-markdown'
import ReactCrop from 'react-image-crop';

var Suggestion = React.createClass({
  render: function() {}
});

Suggestion.Card = ({ url, suggestion, revision }) => {
  var style = {};
  if (suggestion.image) {
    style.backgroundImage = "url(" + suggestion.image + ")";
  }

  return (
    <a href={url}>
      <div className="suggestion--image" style={style}>
        <div className="suggestion--gradient"></div>
        <span className="suggestion--title">
          <span className="suggestion--title--caption">
            {suggestion.type_display} {suggestion.stars}
          </span>
          <h3>{revision.title}</h3>
        </span>
      </div>
    </a>
  );
}

Suggestion.Card.propTypes = {
  url: PropTypes.string.isRequired,
  suggestion: PropTypes.object.isRequired,
}

let chunks = function(items, chunkSize) {
    var R = [];
    for (var i=0; i<items.length; i+=chunkSize)
        R.push(items.slice(i,i+chunkSize));
    return R;
}

Suggestion.CardGrid = ({ goal_slug, suggestions }) => {
  var suggestionNodes = suggestions.map(function(suggestion) {
    return (
      <div className="col-md-4 suggestion_CardGridBox" key={suggestion.id}>
        <Suggestion.Card
          url={"/to/" + goal_slug + "/by/" + suggestion.slug + "/"}
          suggestion={suggestion}
          revision={suggestion.current_revision}
          key={suggestion.id}
        />
      </div>
    );
  });

  var rows = chunks(suggestionNodes, 3).map(function(chunk, index) {
    return (
      <div className="row gap--small-above" key={index}>
      {chunk}
      </div>
    );
  });

  return (
    <div>
    {rows}
    </div>
  );
}

Suggestion.CardGrid.propTypes = {
  goal_slug: PropTypes.string.isRequired,
  suggestions: PropTypes.array.isRequired
}

Suggestion.PageHeader = ({ url, suggestion }) => {
  if (!suggestion)
  {
    return (<div/>);
  }

  let revision = suggestion.current_revision

  return (
    <span>
      <div className="row gap--small-above">
        <div className="col-md-4 col-md-offset-4">
          <Suggestion.Card
            url={url}
            suggestion={suggestion}
            revision={revision}
            key={suggestion.id}
          />
        </div>
      </div>
      <div className="row gap--small-above">
        <div className="col-md-8 col-md-offset-2">
          <h5>Published by {suggestion.owner.name}, {revision.pub_date_display}</h5>
          <ReactMarkdown skipHtml={true} source={revision.description} />
        </div>
      </div>
    </span>
  )
}

Suggestion.Form = React.createClass({
  getInitialState: function() {
    return {
      descriptionValue: '',
      isPreviewVisible: false,
      cropString: '',
      crop: {
        x: 0,
        y: 0,
        width: 1000,
        height: 1000,
        aspect: 360.0 / 200.0
      }
    };
  },

  doUpload: function(e)
  {
    e.preventDefault();
    this.props.uploadImage($('#id_image')[0].files[0]);
  },

  doPost: function(e)
  {
    e.preventDefault();
    $("#id_is_draft").val(0);
    this.props.postSuggestion($("#id_new_suggestion_form").serialize());
  },

  doCancel: function(e)
  {
    e.preventDefault();
    $("#id_is_draft").val(1);
    this.props.cancelPostSuggestion($("#id_new_suggestion_form").serialize());
  },

  onDescriptionChange: function(e)
  {
    this.setState({descriptionValue: e.target.value});
  },

  onChkPreviewChange: function(e)
  {
    this.setState({isPreviewVisible: !this.state.isPreviewVisible});
  },

  onCropComplete: function(crop, pixelCrop)
  {
    this.setState({
      cropString: JSON.stringify(pixelCrop),
      crop: crop,
    });
  },

  onImageLoaded: function(crop, image, pixelCrop)
  {
    this.onCropComplete(crop, pixelCrop)
  },

  imageSrc: function()
  {
    const suggestion = this.props.suggestion;
    return (suggestion && suggestion.uncropped_image)
      ? suggestion.uncropped_image
      : "";
  },

  revisionTitle: function()
  {
    let revision = this.props.suggestion.current_revision
    return revision.title === "not set" ? "" : revision.title
  },

  revisionDescription: function()
  {
    let revision = this.props.suggestion.current_revision
    return revision.description === "not set" ? "" : revision.description
  },

  render: function() {
    if (!this.props.suggestion) {
      return <div/>;
    }

    let errors = this.props.errors;

    return (
      <form id="id_new_suggestion_form">
        <p>
          <label className="form--label">
          Will you suggest a one-time Action, or a continuous Practice?
          </label>
          <select id="id_type" name="type" defaultValue={0}>
            <option value="0">action</option>
            <option value="1">practice</option>
          </select>
        </p>

        <p>
          <label className="form--label">Title</label>
          <input id="id_title" maxLength="100" name="title" type="text" defaultValue={this.revisionTitle()}/>
          <Widgets.errorLabel errors={errors} fieldName="title" />
        </p>

        <p>
          <Widgets.errorLabel errors={errors} fieldName="description" />
          <label className="form--label">
            Describe your suggestion
            <label className="form--label pull-right">
              <input id="chkPreview" type="checkbox" onChange={this.onChkPreviewChange}/>
              <span>Preview</span>
              <span className="suggestion--form--markdown">
                <a href="http://commonmark.org/help/">Markdown allowed</a>
              </span>
            </label>
          </label>
          <textarea
            id="id_suggestion_description"
            name="description" rows={10}
            className={
              "suggestion--form--text" +
              (this.state.isPreviewVisible ? " hidden" : "")
            }
            defaultValue={this.revisionDescription()}
            onChange={this.onDescriptionChange}
          />
        </p>
        {this.state.isPreviewVisible
          ? (
            <ReactMarkdown
              className="suggestion--form--preview"
              skipHtml={true}
              source={this.state.descriptionValue}
            />)
          : null
        }

        <input
          id="id_crop"
          type="hidden"
          name="crop"
          value={this.state.cropString}
        />
        <ReactCrop
          className="suggestion--form--crop"
          src={this.imageSrc()}
          crop={this.state.crop}
          onImageLoaded={this.onImageLoaded}
          onComplete={this.onCropComplete}
        />

        <div className="sugggestion--form--image">
          <p>
            <label className="form--label">Make your suggestion look good by uploading an image</label>
            <input id="id_image" name="image" type="file"/>
            <button id="upload-submit" name="submit" value="upload" onClick={this.doUpload}>Upload</button>
            <Widgets.errorLabel errors={errors} fieldName="image" />
          </p>
        </div>

        <input
          id="id_is_draft"
          type="hidden"
          name="is_draft"
        />

        <div>
          <div className="gap--small-above gap--small-below">
            <label className="form--label">Press Submit to publish your suggestion</label>
            <button name="submit" value="save" onClick={this.doPost}>Submit</button>
            <button name="submit" value="cancel" onClick={this.doCancel}>Cancel</button>
          </div>
        </div>
      </form>
    );
  }
});

export default Suggestion
