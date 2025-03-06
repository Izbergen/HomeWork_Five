from django import forms
from .models import Item, Comment

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'location', 'category']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Заголовок должен содержать не менее 5 символов.")
        return title

    def clean_location(self):
        location = self.cleaned_data.get('location')
        if len(location) <= 0:
            raise forms.ValidationError("Локация должна быть заполнена.")
        return location

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError("Категория должна быть выбрана.")
        return category


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['status'] = forms.ChoiceField(choices=Item._meta.get_field('status').choices)
            self.fields['location'].required = True
            self.fields['category'].required = True
            self.fields['title'].required = True




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']