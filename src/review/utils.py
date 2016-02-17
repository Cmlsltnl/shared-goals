from .models import Review


def update_rating_and_save(suggestion):
    reviews = Review.objects.filter(revision__suggestion_id=suggestion.pk)
    if reviews.count():
        suggestion.avg_rating = (
            sum([r.rating for r in reviews]) / reviews.count()
        )
        suggestion.save()
