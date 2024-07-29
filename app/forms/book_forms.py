from django import forms

class BookSearchForm(forms.Form):
    title = forms.CharField(
        label='本のタイトル',
        required=True
    )

    author = forms.CharField(
        label='著者名',
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(BookSearchForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control mb-3'
