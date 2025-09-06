from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''

@register.simple_tag(takes_context=True)
def querystring(context, **kwargs):
    """
    Merge current GET parameters with new ones.
    Pass None to remove a key.
    """
    request = context["request"]
    params = request.GET.copy()
    params.pop("page", None)  # remove page so pagination resets

    for k, v in kwargs.items():
        if v is None:
            params.pop(k, None)
        else:
            params[k] = v

    encoded = params.urlencode()
    return f"?{encoded}" if encoded else ""
