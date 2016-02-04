from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text

from goal.templates.dominate_tags import *

from proposal.templates.dominate_tags import *


# 123
with django_block("content") as content:
    goal_header()

    with django_for("proposal_list in proposal_lists"):
        with div(_class="row"):
            with django_for("proposal in proposal_list"):
                with col(4):
                    with div(
                        _class="proposal--photo",
                        style="background-image:url({{ proposal.image.url }});"
                    ):
                        div(_class="proposal--gradient")
                        with h3(_class="proposal--title"):
                            text("{{ proposal.get_current_version.title }}")

print("{% extends 'base.html' %}\n")
print(content)
