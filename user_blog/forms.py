from django import forms
from user_blog.models import Category
from user_page.models import Knowledge
from django.urls import reverse


class ModelFormPostMixin:
    fields, exclude = '__all__', ['user']
    widgets = {
        'knowledge_field': forms.RadioSelect(attrs={'id': 'field_knowledge'}),
        'categories': forms.CheckboxSelectMultiple(attrs={'id': 'categories'}),
        'header': forms.Textarea(attrs={'cols': '100', 'rows': '5', 'class': 'form-control'}),
        'image': forms.FileInput(attrs={'type': 'file', 'class': 'form-control-file'}),
        'title': forms.Textarea(attrs={'cols': '100', 'rows': '1', 'class': 'form-control'}),
        'body': forms.Textarea(attrs={'cols': '1000', 'rows': '10', 'class': 'form-control'})
    }
    labels = {'categories': 'Please equip the category this post'}
    help_texts = {'categories': '(not required)'}

    def get_form(self, **kwargs):
        """Return an instance of the form to be used in this view."""
        form_class = self.get_form_class()
        form = form_class(**self.get_form_kwargs())  # for UpdateView get_form_kewargs return 'instance' Model object PK
        form.fields['knowledge_field'].label_from_instance = lambda obj: "%s" % obj.name
        form.fields['knowledge_field'].queryset = Knowledge.objects.filter(user=self.request.user)
        form.fields['categories'].label_from_instance = lambda obj: "%s" % obj.name
        form.fields['categories'].queryset = Category.objects.filter(user=self.request.user)

        return form

    def get_form_class(self):
        return forms.modelform_factory(
            self.model, fields=self.fields, exclude=self.exclude,
            widgets=self.widgets, labels=self.labels, help_texts=self.help_texts
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.kwargs.get('username')
        return context

    def get_success_url(self):
        return reverse('article_index', args=[self.kwargs.get('username')])


class CommentForm(forms.Form):
    body = forms.CharField(
        label="",
        widget=forms.Textarea,
    )

    parent = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput,
    )
