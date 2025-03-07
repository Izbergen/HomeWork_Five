from django.shortcuts import redirect
from django.contrib import messages
from .models import Item

class ItemPermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/update/') or request.path.startswith('/delete/'):
            item_id = request.resolver_match.kwargs.get('pk')
            if item_id:
                item = Item.objects.get(id=item_id)
                if request.user != item.author and not request.user.is_staff:
                    messages.error(request, "У вас нет разрешения на выполнение этого действия.")
                    return redirect('item-list')
        return self.get_response(request)