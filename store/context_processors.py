from .models import (
    Product,
    Customer,
    ShoppingCart,
)

def store_context(request):
    # unread_messages = .objects.filter(read_status=False).order_by('-id')
    context = {
        'products': Product.objects.all(),
        # 'unread_messages_count': unread_messages.count(),
    }
    return context

