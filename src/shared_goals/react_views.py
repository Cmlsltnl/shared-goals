"""React views."""

from django.shortcuts import render
from django.views.generic import View


class HomeView(View):  # noqa
    def get(self, request):  # noqa
        return render(request, 'shared_goals/react_base.html', {})
