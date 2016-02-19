import hashlib

from django import template

from review.models import Review


register = template.Library()


@register.filter
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


@register.filter
def suggestions_by(goal, global_user):
    return [
        x for x in goal.suggestions.filter(owner=global_user, is_draft=False)
    ]


@register.filter
def reviews_by(goal, global_user):
    reviews = Review.objects.filter(owner=global_user, is_draft=False)
    return [
        r for r in reviews if
        r.description and r.revision.suggestion.goal == goal
    ]


crop_widget_html = """
<img class="{img_class}" alt="{img_url}" id="{img_id}" src="{img_url}"></img>
<input id="{output_id}" name="{output_id}" value="" type="hidden"></input>

<script>
$(document).ready(function() {{
    img_elm = $("#{img_id}");

    function updateCropping(c) {{
        c.natural_height = img_elm.prop('naturalHeight');
        c.natural_width = img_elm.prop('naturalWidth')
        c.display_height = img_elm.height();
        c.display_width = img_elm.width();
        var data = JSON.stringify(c);
        $("#{output_id}").val(data)
    }}

    img_elm.Jcrop({{
        {aspect_ratio}
        {initial}
        onSelect: updateCropping,
        onChange: updateCropping,
    }});
}});
</script>
"""


@register.filter
def show_crop_widget(crop_settings):
    options = dict(
        img_class=crop_settings.get('klass', ''),
        img_url=crop_settings['url'],
        output_id=crop_settings['output_key'],
        img_id=hashlib.md5(crop_settings['output_key'].encode()).hexdigest(),
    )

    options['aspect_ratio'] = ''
    aspect_ratio = crop_settings.get('aspect_ratio', 0)
    if aspect_ratio:
        options['aspect_ratio'] = (
            "aspectRatio: {aspect_ratio},"
        ).format(
            aspect_ratio=aspect_ratio,
        )

    options['initial'] = ''
    initial = crop_settings.get('initial', [])
    if initial:
        options['initial'] = (
            "setSelect: [ {left}, {top}, {right}, {bottom} ],"
        ).format(
            left=initial[0],
            top=initial[1],
            right=initial[2],
            bottom=initial[3],
        )

    return crop_widget_html.format(**options)
