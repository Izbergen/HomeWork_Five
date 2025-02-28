from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView , DeleteView , UpdateView
from .models import Item
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item
from .forms import ItemForm

class ItemListView(ListView):
    model = Item
    template_name = 'items/item_list.html'
    context_object_name = 'items'

class ItemDetailView(DetailView):
    model = Item
    template_name = 'items/item_detail.html'
    context_object_name = 'item'



class ItemCreateView(CreateView):
    model = Item
    template_name = 'items/item_form.html'
    fields = ['title', 'description', 'location', 'category']
    success_url = reverse_lazy('item-list')

    def form_valid(self, form):
        form.instance.status = 'lost'
        return super().form_valid(form)



class ItemUpdateView(UpdateView):
    model = Item
    template_name = 'items/item_form.html'
    fields = ['title', 'description', 'location', 'status', 'category']
    success_url = reverse_lazy('item-list')




class ItemDeleteView(DeleteView):
    model = Item
    template_name = 'items/item_confirm_delete.html'
    success_url = reverse_lazy('item-list')