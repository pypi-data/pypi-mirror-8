# -*- coding: utf-8 -*-

from django import template
from django.template.loader import get_template
from django.template import Context
register = template.Library()
from coop_bar.bar import CoopBar
from django.conf import settings

class CoopBarNode(template.Node):

    def render(self, context):
        request = context.get("request", None)
        commands = CoopBar().get_commands(request, context)
        if commands: #hide admin-bar if nothing to display
            css_classes = CoopBar().get_css_classes(request, context)
            context_dict = {'commands': commands, 'css_classes': css_classes}
            #for var_name in ('article', 'object'):
            #    var = context.get(var_name, None)
            #    context_dict[var_name] = var
            t = get_template("coop_bar.html")
            return t.render(Context(context_dict))
        return u''

@register.tag
def coop_bar(parser, token):
    return CoopBarNode()


class CoopBarHeaderNode(template.Node):
    def render(self, context):
        request = context.get("request", None)
        STATIC_URL = getattr(settings, 'STATIC_URL', '')
        headers = [u'<link rel="stylesheet" href="{0}css/coop_bar.css" type="text/css" />'.format(STATIC_URL)]
        #headers += [u'<script src="{0}js/jquery-ui-1.8.14.custom.min.js"></script>'.format(STATIC_URL)]
        headers += CoopBar().get_headers(request, context)
        return "\n".join(headers)

@register.tag
def coop_bar_headers(parser, token):
    return CoopBarHeaderNode()

