from django import template
from review.models import Review


register = template.Library()


@register.filter
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


@register.filter
def suggestions_owned_by(goal, global_user):
    return [
        x for x in goal.suggestions.filter(owner=global_user, is_draft=False)
    ]


@register.filter
def reviews_by(goal, global_user):
    reviews = Review.objects.filter(owner=global_user, is_draft=False)
    return [r for r in reviews if r.revision.suggestion.goal == goal]
