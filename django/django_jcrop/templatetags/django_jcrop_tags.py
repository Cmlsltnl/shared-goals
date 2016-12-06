import json

from django import template
from django.template import defaultfilters as filters

register = template.Library()


crop_widget_html = """
<img
    class="djangoJcrop {klass}"
    alt="{url}"
    src="{url}"
    data-output-id="{output_key}"
    data-jcrop="{jcrop}"
></img>
<input id="{output_key}" name="{output_key}" value="" type="hidden"></input>
"""


@register.filter
def django_jcrop_widget(crop_settings):
    updated_crop_settings = dict(crop_settings)
    updated_crop_settings['jcrop'] = json.dumps(
        updated_crop_settings.get('jcrop', '')
    ).replace('"', "'")

    return (
        filters.safe(crop_widget_html.format(**updated_crop_settings))
        if updated_crop_settings.get("url", "") else
        ""
    )


init_django_jcrop_html = """
<script>
$(document).ready(function() {{
    $(".djangoJcrop").djangoJcrop();
}});
</script>
"""


@register.simple_tag
def init_django_jcrop():
    return filters.safe(init_django_jcrop_html)
