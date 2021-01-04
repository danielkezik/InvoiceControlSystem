from django import forms
from .models import User, Invoice
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)

    class Meta:
        model = DjangoUser
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']


class AddBalanceForm(forms.Form):
    to_add = forms.DecimalField(min_value=0.01, decimal_places=2, max_digits=8)


class NewInvoiceForm(forms.ModelForm):
    # invoice_type = forms.ChoiceField(Invoice.INVOICE_TYPE_CHOICES)
    _step = 1

    step = forms.IntegerField(
        widget=forms.HiddenInput(),
        initial=_step,
        required=False,
    )

    class Meta:
        model = Invoice
        fields = ['step', 'name', 'invoice_type', 'is_regular', 'regularity', 'due_date']


class NewInvoiceWebsiteForm(forms.ModelForm):
    _step = 2

    step = forms.IntegerField(
        widget=forms.HiddenInput(),
        initial=_step,
        required=False,
    )

    class Meta:
        model = Invoice
        fields = ['step', 'website', 'login', 'password', 'total', 'name', 'invoice_type', 'is_regular', 'regularity', 'due_date']
        widgets = {
            'name': forms.HiddenInput(),
            'invoice_type': forms.HiddenInput(),
            'is_regular': forms.HiddenInput(),
            'regularity': forms.HiddenInput(),
            'due_date': forms.HiddenInput()
        }


class NewInvoiceCredentialsForm(forms.ModelForm):
    _step = 2

    step = forms.IntegerField(
        widget=forms.HiddenInput(),
        initial=_step,
        required=False,
    )

    class Meta:
        model = Invoice
        fields = ['step', 'iban', 'full_name', 'total', 'name', 'invoice_type', 'is_regular', 'regularity', 'due_date']
        widgets = {
            'name': forms.HiddenInput(),
            'invoice_type': forms.HiddenInput(),
            'is_regular': forms.HiddenInput(),
            'regularity': forms.HiddenInput(),
            'due_date': forms.HiddenInput()
        }


class NewInvoiceFileForm(forms.ModelForm):
    _step = 2

    step = forms.IntegerField(
        widget=forms.HiddenInput(),
        initial=_step,
        required=False,
    )

    class Meta:
        model = Invoice
        fields = ['step', 'file', 'total', 'name', 'invoice_type', 'is_regular', 'regularity', 'due_date']
        widgets = {
            'name': forms.HiddenInput(),
            'invoice_type': forms.HiddenInput(),
            'is_regular': forms.HiddenInput(),
            'regularity': forms.HiddenInput(),
            'due_date': forms.HiddenInput()
        }
