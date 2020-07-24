from init.models import Info

def add_variable_to_context(request):
    info = Info.objects.all().first()
    return {
        'groupName': info.group_name,
        'cardName': info.card_name
    }