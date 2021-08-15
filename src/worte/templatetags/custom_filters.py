from django import template
register = template.Library()


@register.filter('startswith')
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False


@register.filter(name='user_in_the_group')
def user_in_the_group(user, group):
    if user:
        return user.groups.filter(name=group).count() > 0
    return False

