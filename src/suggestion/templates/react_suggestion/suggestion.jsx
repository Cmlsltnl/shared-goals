{% extends 'react_base.html' %}
{% block react %}

ReactDOM.render(
  <Suggestion.CardGridBox url="/api/suggestions?goal={{ goal.pk }}" pollInterval={100000} />,
  document.getElementById('content')
);

{% endblock %}
