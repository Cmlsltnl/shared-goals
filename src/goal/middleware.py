import re
from goal.models import GlobalUser, Goal


class ExtractGoalMiddleware:
    def process_request(self, request):
        setattr(
            request,
            "global_user",
            GlobalUser.objects.filter(user_id=request.user.id).first()
        )
        if not request.global_user and not request.user.is_anonymous():
            setattr(
                request,
                "global_user",
                GlobalUser.objects.create(user=request.user)
            )

        setattr(request, "goal", None)
        setattr(request, "member", None)

        p = re.compile(r'^/(to/(?P<slug>[\w-]+))/')
        m = re.search(p, request.path_info)
        if m:
            goal_slug = m.group("slug")
            goal = Goal.objects.filter(slug=goal_slug).first()
            if goal:
                setattr(request, "goal", goal)

                member = goal.members.filter(
                    global_user__user_id=request.user.id).first()
                setattr(request, "member", member)
