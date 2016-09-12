'use strict'

var React = require('react')

var Suggestion = React.createClass({
  render: function() {}
});

Suggestion.Card = React.createClass({
  render: function() {
    var style = {};
    if (this.props.suggestion.image) {
      style.backgroundImage = "url(" + this.props.suggestion.image + ")";
    }

    return (
      <div className="col-md-4">
        <a href={this.props.suggestion.get_url}>
          <div className="suggestion--image" style={style}>
            <div className="suggestion--gradient"></div>
            <span className="suggestion--title">
              <span className="suggestion--title--caption">
                {this.props.suggestion.get_type_display} {this.props.suggestion.stars}
              </span>
              <h3>{this.props.suggestion.current_revision.title}</h3>
            </span>
          </div>
        </a>
      </div>
    );
  }
});

Suggestion.CardGrid = React.createClass({
  chunks: function(items, chunkSize) {
      var R = [];
      for (var i=0; i<items.length; i+=chunkSize)
          R.push(items.slice(i,i+chunkSize));
      return R;
  },
  render: function() {
    var suggestionNodes = this.props.data.map(function(suggestion) {
      return (
        <Suggestion.Card suggestion={suggestion} key={suggestion.pk}/>
      );
    });

    var rows = this.chunks(suggestionNodes, 3).map(function(chunk, index) {
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
});

Suggestion.CardGridBox = React.createClass({
  loadSuggestionsFromServer: function() {
    $.ajax({ url: this.props.url, dataType: 'json', cache: false,
      success: function(data) { this.setState({data: data}); }.bind(this),
      error: function(xhr, status, err) { console.error(this.props.url, status, err.toString()); }.bind(this)
    });
  },
  getInitialState: function() { return {data: []}; },
  componentDidMount: function() {
    this.loadSuggestionsFromServer();
    setInterval(this.loadSuggestionsFromServer, this.props.pollInterval);
  },
  render: function() {
    return (
      <div className="suggestion_CardGridBox">
        <h1>Suggestions</h1>
        <Suggestion.CardGrid data={this.state.data} />
      </div>
    );
  }
});

export default Suggestion