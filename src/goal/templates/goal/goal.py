from dominate.tags import *
from django_tags import *


fair_trade_logo = (
    'http://i27.photobucket.com/albums/c193/sally_anne_/'
    'Fairtrade/mark_colour_vertical.jpg')

with django_block("content") as content:
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

    with django_for("proposal in proposals"):
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

print("{% extends 'base.html' %}\n")
print(content)
