from django import forms
from .models import Item, Comment

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'location', 'category']

    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Title Placeholder"}))
    description = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Description Placeholder"}))
    location = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Location Placeholder"}))
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        location = cleaned_data.get('location')
        category = cleaned_data.get('category')

        if title and len(title) < 5:
            self.add_error('title', "Заголовок должен содержать не менее 5 символов.")

        if not location:
            self.add_error('location', "Локация должна быть заполнена.")

        if not category:
            self.add_error('category', "Категория должна быть выбрана.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['status'] = forms.ChoiceField(choices=Item._meta.get_field('status').choices)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
