from .models import Message, Notification, CatalogItem


def messages(request):
    unread_messages = Message.objects.filter(read_status=False).order_by('-id')
    context = {
        'unread_messages': unread_messages,
        'unread_messages_count': unread_messages.count(),
    }
    return context


def catalog(request):
    _catalog = CatalogItem.objects.filter(site_preview=True)
    context = {
        'catalog': _catalog.order_by('-id'),
        'catalog_count': _catalog.count(),
    }
    return context



def notifications(request):
    unread_notifications = Notification.objects.filter(read_status=False).order_by('-id')
    context = {
        'unread_notifications': unread_notifications,
        'unread_notifications_count': unread_notifications.count(),
    }
    return context



