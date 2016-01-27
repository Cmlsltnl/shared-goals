import dominate
from dominate.tags import *
from dominate.util import text


print '{% load staticfiles %}'

doc = dominate.document(title="Shared Goal")

with doc.head:
    link(
        rel="stylesheet", href="http://maxcdn.bootstrapcdn.com/bootstrap"
        "/3.3.6/css/bootstrap.min.css")
    link(
        rel="stylesheet", href="{% static 'goal/goal.css' %}")
    script(
        type="text/javascript", src="https://ajax.googleapis.com/ajax/"
        "libs/jquery/1.12.0/jquery.min.js")
    script(
        type="text/javascript", src="http://maxcdn.bootstrapcdn.com/"
        "bootstrap/3.3.6/js/bootstrap.min.js")

fair_trade_logo = (
    'http://i27.photobucket.com/albums/c193/sally_anne_/'
    'Fairtrade/mark_colour_vertical.jpg')

with doc:
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

        text("{% for proposal in proposals %}")

        with div(_class="row proposal"):
            div(_class="col-md-2")
            with div(_class="col-md-1"):
                img(src=fair_trade_logo, height="75", width="75")
            with div(_class="col-md-5"):
                h3("{{ proposal.title }}")
            with div(_class="col-md-1"):
                h4("4.2")
            with div(_class="col-md-2"):
                h4("{{ proposal.pub_date|date:'d M Y' }}")

        text("{% endfor %}")

print doc
