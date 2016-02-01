from dominate.tags import *
from dominate.util import text
from django_dominate.django_tags import *
from goal.templates.dominate_tags import *


print("{% extends 'base.html' %}\n")
print("{% load markdown_deux_tags %}")

with django_block("content") as content:
    goal_header()
    h1("{{ proposal.title }}")
    text("{{ proposal.description|markdown }}")

print(content)
