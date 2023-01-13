from django import forms


class MLModelForm(forms.Form):
    name = forms.CharField(label="Enter model's name", max_length=200)
    model_file = forms.FileField()
    train_file = forms.FileField()
    test_file = forms.FileField()
