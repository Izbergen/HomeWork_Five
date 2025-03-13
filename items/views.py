from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Item
from .forms import CommentForm, ItemForm

class ItemListView(ListView):
    model = Item
    template_name = 'items/item_list.html'
    context_object_name = 'items'

class ItemDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Item
    template_name = 'items/item_detail.html'
    context_object_name = 'item'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('item-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['form'] = self.get_form()

        item_id = str(self.object.id)

        viewed_items = self.request.session.get('viewed_items', [])

        if item_id not in viewed_items:
            viewed_items.append(item_id)
            self.request.session['viewed_items'] = viewed_items  # Записываем в сессию

        context['viewed_items'] = Item.objects.filter(id__in=viewed_items)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.item = self.object
            comment.author = request.user
            comment.save()
            return super().form_valid(form)
        messages.error(request, "Ошибка валидации комментария!")
        return self.render_to_response(self.get_context_data(form=form))


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'items/item_form.html'
    success_url = reverse_lazy('item-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 'lost'
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка валидации! Проверьте данные.")
        return self.render_to_response(self.get_context_data(form=form))


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'items/item_form.html'
    success_url = reverse_lazy('item-list')

    def test_func(self):
        item = self.get_object()
        return item.author == self.request.user or self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав на изменение этого объекта.")
        return super().handle_no_permission()


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    template_name = 'items/item_confirm_delete.html'
    success_url = reverse_lazy('item-list')

    def test_func(self):
        item = self.get_object()
        return item.author == self.request.user or self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав на удаление этого объекта.")
        return super().handle_no_permission()

