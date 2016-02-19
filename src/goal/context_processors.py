from django.core.urlresolvers import reverse


def profile_url(request):
    return dict(
        profile_url=(
            ''  # reverse('global-profile')
            if not (request.goal and request.global_user) else
            reverse(
                'profile',
                args=(request.goal.slug, request.global_user.user.username)
            )
        )
    )
