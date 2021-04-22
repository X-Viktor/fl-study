from django import forms

from .models import Order, Response


class OrderCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)

        for field_name in ['category', 'title', 'description', 'price']:
            self.fields[field_name].widget.attrs['class'] = 'form-control'

        self.fields['description'].widget.attrs['rows'] = '5'

    class Meta:
        model = Order
        fields = ('category', 'title', 'description', 'price')


class ResponseForm(forms.ModelForm):

    class Meta:
        model = Response
        fields = ('message',)
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'})
        }
