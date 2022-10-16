from django import forms


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class UploadFileForm(forms.Form):
    csv_file = forms.FileField(label="CSV File:", widget=forms.FileInput(attrs={'accept': 'text/csv', 'class': 'form-control'}))
    xml_file = forms.FileField(label="XML File:", widget=forms.FileInput(attrs={'accept': 'application/xml', 'class': 'form-control'}))
