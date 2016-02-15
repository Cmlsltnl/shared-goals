from django_dominate.django_tags import *

from dominate.tags import *

from goal.templates.dominate_tags import *

from suggestion.templates.dominate_tags import *


def result():
    with django_block("content") as content:
        h1("Shared Goals")

    return (
        "{% extends 'base.html' %}\n",
        content
    )
