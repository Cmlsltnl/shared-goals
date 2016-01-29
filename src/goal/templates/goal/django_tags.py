from dominate.tags import html_tag


class django_tag(html_tag):
    closing_tag = ""

    def get_opening_tag(self, tag_inner):
        raise

    def _render(self, rendered, indent=1, inline=False):
        from_index = len(rendered)
        tag_inner = self.children[0]
        del self.children[0]

        super(html_tag, self)._render(rendered, indent, inline)
        for i in range(2):
            rendered.pop()
            del rendered[from_index]
        rendered[from_index] = self.get_opening_tag(tag_inner)
        rendered[-1] = self.closing_tag
        return rendered


class django_block(django_tag):
    closing_tag = "{% endblock %}"

    def get_opening_tag(self, tag_inner):
        return "{%% block %s %%}" % tag_inner


class django_for(django_tag):
    closing_tag = "{% endfor %}"

    def get_opening_tag(self, tag_inner):
        return "{%% for %s %%}" % tag_inner


class django_if(django_tag):
    closing_tag = "{% endif %}"

    def get_opening_tag(self, tag_inner):
        return "{%% if %s %%}" % tag_inner


class django_else(django_tag):
    closing_tag = ""

    def get_opening_tag(self, tag_inner):
        return "{%% else %%}"
