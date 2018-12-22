from django import template

register = template.Library()

@register.filter
def cleansify(value):
    result = value.replace(':       makeArticleAd();    ', '')
    result = result.replace(':makeArticleAd();', '')
    result = result.replace(':       ', '')
    result = result.replace(':', '')

    return result

