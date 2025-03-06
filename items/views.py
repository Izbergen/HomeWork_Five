from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView , DeleteView , UpdateView
from django.urls import reverse_lazy, reverse
from .models import Item
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from .forms import CommentForm

class ItemListView(ListView):
    model = Item
    template_name = 'items/item_list.html'
    context_object_name = 'items'

class ItemDetailView(FormMixin, DetailView):
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
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.item = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)



class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    template_name = 'items/item_form.html'
    fields = ['title', 'description', 'location', 'category']
    success_url = reverse_lazy('item-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 'lost'
        return super().form_valid(form)


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    template_name = 'items/item_form.html'
    fields = ['title', 'description', 'location', 'status', 'category']
    success_url = reverse_lazy('item-list')

    def dispatch(self, request, *args, **kwargs):
        item = self.get_object()
        if item.author != request.user and not request.user.is_staff:
            raise PermissionDenied("У вас нет прав на внесений изменений")
        return super().dispatch(request, *args, **kwargs)


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = 'items/item_confirm_delete.html'
    success_url = reverse_lazy('item-list')

    def dispatch(self, request, *args, **kwargs):
        item = self.get_object()
        if item.author != request.user and not request.user.is_staff:
            raise PermissionDenied("У вас нет прав на удаления этого поста")
        return super().dispatch(request, *args, **kwargs)