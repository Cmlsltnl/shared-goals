import dominate
import re
from dominate.tags import *
from dominate.util import text


doc = dominate.document(title="Shared Goal")

fair_trade_logo = (
    'http://i27.photobucket.com/albums/c193/sally_anne_/'
    'Fairtrade/mark_colour_vertical.jpg')

with doc:
    text("\n{% extends 'base.html' %}\n")
    text("\n{% block content %}\n")

    with div(_class="container"):
        with div(_class="row"):
            div(_class="col-md-10")
            with div(_class="btn-group btn-new-proposal col-md-2"):
                button("New Proposal", _class="btn")

        with div(_class="row main-menu"):
            with div(_class="text-center"):
                h1("{{ goal.title }}")
                with div(_class="button-grp"):
                    button("Top Proposals", _class="btn btn-default")
                    button("Members", _class="btn btn-default")
                    button("My Profile", _class="btn btn-default")

        with div(_class="row"):
            div(_class="col-md-8")
            with div(_class="col-md-1"):
                h4("Rating")
            with div(_class="col-md-2"):
                h4("Published")

        text("\n{% for proposal in proposals %}\n")

        with div(_class="row proposal"):
            div(_class="col-md-2")
            with div(_class="col-md-1"):
                img(src=fair_trade_logo, height="75", width="75")
            with div(_class="col-md-5"):
                h3("{{ proposal.title }}")
            with div(_class="col-md-1"):
                h4("{{ proposal.rating }}")
            with div(_class="col-md-2"):
                h4("{{ proposal.pub_date|date:'d M Y' }}")

        text("\n{% endfor %}\n")

    text("\n{% endblock %}\n")


def strip(s):
    def strip_leading(s):
        return re.sub(r'<body>\s+', '', str(s))
    return re.sub(r'\s+</body>', '', strip_leading(s))

print(strip(doc.body))
