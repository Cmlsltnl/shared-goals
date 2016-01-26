import dominate
from dominate.tags import *

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

        with div(_class="row"):
            with div(_class="text-center"):
                h1("Improve the world")
                with div(_class="button-grp"):
                    button("Top Proposals", _class="btn btn-default")
                    button("Members", _class="btn btn-default")
                    button("My Profile", _class="btn btn-default")

        hr()
        hr()

        with div(_class="row"):
            div(_class="col-md-8")
            with div(_class="col-md-1"):
                h4("Rating")
            with div(_class="col-md-2"):
                h4("Published")

        with div(_class="row proposal"):
            div(_class="col-md-2")
            with div(_class="col-md-1"):
                img(src=fair_trade_logo, height="75", width="75")
            with div(_class="col-md-5"):
                h3("Buy Fair Trade products")
            with div(_class="col-md-1"):
                h4("4.2")
            with div(_class="col-md-2"):
                h4("10 Jan 2016")

        with div(_class="row proposal"):
            div(_class="col-md-2")
            with div(_class="col-md-1"):
                img(src=fair_trade_logo, height="75", width="75")
            with div(_class="col-md-5"):
                h3("Buy Fair Trade products")
            with div(_class="col-md-1"):
                h4("4.2")
            with div(_class="col-md-2"):
                h4("10 Jan 2016")

print doc
