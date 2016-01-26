import dominate
from dominate.tags import *
# from dominate.util import text

doc = dominate.document(title='Shared Goal')
fair_trade_logo = (
    "http://i27.photobucket.com/albums/c193/sally_anne_/"
    "Fairtrade/mark_colour_vertical.jpg")

with doc:
    with div(_class='container'):
        with div(_class='row'):
            div(_class='col-md-10')
            with div(_class="btn-group btn-new-proposal col-md-2"):
                button("New Proposal", _class="btn")

        with div(_class='row'):
            with div(_class='text-center'):
                with div(_class='proposal-header'):
                    img(
                        _class="proposal-img",
                        src=fair_trade_logo,
                        height=75,
                        width=75)
                    h3(
                        "Buy Fair Trade products",
                        _class="proposal-title")

# <div class="container">
#   <div class="row">
#     <div class="col-md-10">
#     </div>
#     <div class="btn-group btn-new-proposal col-md-2">
#       <button class="btn">
#         New Proposal
#       </button>
#     </div>
#   </div>
#   <div class="row">
#     <div class="text-center">
#       <div class="proposal-header">
#         <img class="proposal-img" src="http://i27.photobucket.com/albums/c193/sally_anne_/Fairtrade/mark_colour_vertical.jpg" height="75" width="75">

#         <h3 class="proposal-title">
#           Buy Fair Trade products
#         </h3>
#       </div>
#       <hr>
#       <div class="btn-group">
#         <button class="btn btn-default" contenteditable="false">
#           Top Proposals
#         </button>
#         <button class="btn btn-default" contenteditable="false">
#           Members
#         </button>
#         <button class="btn btn-default" contenteditable="false">
#           My Profile
#         </button>
#       </div>
#     </div>
#   </div>
#   <hr class="">
#   <hr class="">
# </div>
# <!-- /.container -->

    # with div(id='header').add(ol()):
    #     for i in ['home', 'about', 'contact']:
    #         li(a(i.title(), href='/%s.html' % i))

    # with div():
    #     attr(cls='body')
    #     p('Lorem ipsum..')

print doc
