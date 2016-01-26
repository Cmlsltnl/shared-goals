from django.http import HttpResponse
from django.template import loader


def goal(request):
    template = loader.get_template('goal/goal.html')
    context = {}
    return HttpResponse(template.render(context, request))
