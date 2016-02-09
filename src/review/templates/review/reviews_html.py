from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text, raw

from goal.templates.dominate_tags import *

from proposal.templates.dominate_tags import *


#
@form(
    method="post",
    id="review-form",
    enctype="multipart/form-data",
    _class="big-gap-above"
)
def review_form():
    django_csrf_token()
    with p():
        with label(
            _for="{{ form.rating.id_for_label }}",
            _class="form-label"
        ):
            text("{{ post_button_header }}")
        text("{{ form.rating.errors }}")
        input_(
            id="id_rating",
            type="hidden",
            name="rating",
            value="{{ form.rating.value }}",
            _class="form-field"
        )
        div(
            id="rateit-review",
            _class="rateit",
            data_rateit_resetable="false",
            data_rateit_value="{{ form.rating.value }}"
        )

    with p():
        text("{{ form.description.errors }}")
        with textarea(
            name="description",
            form="review-form",
            rows="10",
            _class="form-field"
        ):
            text("{{ form.description.value }}")

    with div():
        button(
            "{{ post_button_label }}",
            id="save-submit",
            name="submit",
            value="save"
        )
        button(
            "{{ cancel_button_label }}",
            id="cancel-submit",
            name="submit",
            value="cancel"
        )


@form(
    method="post",
    id="comment-form",
    enctype="multipart/form-data",
    _class="big-gap-above"
)
def comment_form():
    django_csrf_token()

    with p():
        text("{{ comment_form.body.errors }}")
        with label(
            _for="{{ comment_form.body.id_for_label }}",
            _class="form-label"
        ):
            text("Comment on this review")
        with textarea(
            name="body",
            form="comment-form",
            _class="form-field"
        ):
            text("{{ comment_form.body.value }}")

    with div():
        button(
            "Submit",
            id="comment-submit",
            name="submit",
            value="save"
        )
        button("Cancel", id="cancel-submit", name="submit", value="cancel")


@span(_class="small-gap-below")
def comment():
    with div(_class="row"):
        column(4)
        with column(4):
            text("{{ comment.owner.name }}, ")
            text("{{ comment.pub_date|naturaltime }}")

    with div(_class="row"):
        column(4)
        with column(4):
            with p():
                text("{{ comment.body }}")


revision_href = (
    "{% url 'revision' request.goal.slug "
    "published_review.revision.proposal.slug published_review.revision.pk %}"
)


@div(_class="row")
def published_review():
    with div(_class="row"):
        column(2)
        with column(2):
            readonly_rateit("{{ published_review.rating }}")
        with column(6):
            with django_if(
                "published_review.revision.pk == latest_revision.pk"
            ):
                text("{{ published_review.header }}")
                with django_else():
                    text("A ")
                    with a(href=revision_href):
                        text("previous version")
                    text(" was {{ published_review.header|lowerfirst }}")

    with div(_class="row"):
        column(2)
        with column(8):
            with p():
                text("{{ published_review.description }}")

    with django_for("comment in published_review.published_comments"):
        comment()


# // Get some values from elements on the page:
# var $form = $( this ),
#   term = $form.find( "input[name='s']" ).val(),
#   url = $form.attr( "action" );

# // Send the data using post
# var posting = $.post( url, { s: term } );

post_review_js = """

$(document).ready(function() {
    $( "#review-form" ).submit(function( event ) {

      // Stop form from submitting normally
      event.preventDefault();

      // Send the data using post
      var posting = $.post(
        "{% url 'reviews' request.goal.slug latest_revision.proposal.slug %}",
        $(this).serialize()
      );

      // Put the results in a div
      posting.done(function(data) {
        $("#reviews").html(data);
      });
    });
});

"""


def result():
    with django_block("content") as content:

        with div(_class="row small-gap-below"):
            column(2)
            with column(8):
                review_form()

                with django_if("review.published_comments|length"):
                    h5(
                        "Note: updating will remove any comments that "
                        "were made on your existing review"
                    )

        with django_for("published_review in published_reviews"):
            published_review()

        with django_if("comment_form"):
            with div(_class="row"):
                column(2)
                with column(8):
                    comment_form()

        with script():
            raw(post_review_js)

    return (
        "{% load humanize %}",
        "{% load case_utils %}",
        content,
    )

# done123
