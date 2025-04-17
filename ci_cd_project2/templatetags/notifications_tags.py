from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def new_notifications_count(context):
    request = context.get('request')
    user = request.user if request else None
    if user and user.is_authenticated:
        return user.notifications.filter(status="new").count()
    return 0
