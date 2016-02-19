import hashlib

from django import template
# from django.template import defaultfilters as filters

from dominate.tags import span, img, script
from dominate.tags import input as input_tag
from dominate.util import raw

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


crop_script = """
$(document).ready(function() {{
    function updateCropping_{img_id}(c) {{
        var data = JSON.stringify(c);
        $("#{output_elm_id}").val(data)
    }}

    $("#{img_id}").Jcrop({{
        aspectRatio: 360 / 200,
        setSelect: [ 0, 0, 180, 100 ],
        onSelect: updateCropping_{img_id},
        onChange: updateCropping_{img_id},
    }});
}});
"""


@register.filter
def crop(image, output_elm_id):
    img_id = hashlib.md5(output_elm_id.encode()).hexdigest()

    with span() as result:
        img(
            id=img_id,
            alt=image.url,
            src=image.url,
        )
        input_tag(
            id="%s" % output_elm_id,
            name="%s" % output_elm_id,
            value="",
            type="hidden"
        )

        with script():
            script_contents = crop_script.format(
                img_id=img_id, output_elm_id=output_elm_id)
            raw(script_contents)

    return str(result)
