from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView, DetailView
from .forms import UserRegisterForm, AddBalanceForm, NewInvoiceForm, NewInvoiceWebsiteForm, NewInvoiceCredentialsForm, \
    NewInvoiceFileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Invoice, User


def index(request):
    return render(request, 'index.html', context={
        'insert_me': 'Hello world!'
    })


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            form.instance.invoice_user.user_class = form.cleaned_data.get('user_class')
            form.instance.invoice_user.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm(initial={'user_class': User.CLIENT})
    return render(request, 'register.html', {'form': form})


class AddBalance(View):
    @method_decorator(login_required)
    def post(self, request):
        form = AddBalanceForm(request.POST)
        if form.is_valid():
            to_add = form.cleaned_data.get('to_add')
            request.user.invoice_user.add_to_balance(to_add)
            messages.success(request, f'Your balance is increased by {to_add}. Now your balance is ' +
                                      f'{request.user.invoice_user.balance}')
            return redirect('index')
        return render(request, 'balance.html', {'form': form})

    @method_decorator(login_required)
    def get(self, request):
        form = AddBalanceForm()
        return render(request, 'balance.html', {'form': form})


class NewInvoice(View):
    @method_decorator(login_required)
    def get(self, request):
        form = NewInvoiceForm()
        return render(request, 'new_invoice.html', {'form': form, 'title': 'Add your new invoice', 'step': 1})

    @method_decorator(login_required)
    def post(self, request):
        #print('step', request.POST.get('step'))
        if int(request.POST.get('step')) == 1:  # step 1
            form = NewInvoiceForm(request.POST)
            if form.is_valid():
                invoice = form.instance
                if invoice.invoice_type == Invoice.WEBSITE:
                    form = NewInvoiceWebsiteForm(instance=invoice)
                elif invoice.invoice_type == Invoice.CREDENTIALS:
                    form = NewInvoiceCredentialsForm(instance=invoice)
                else:  # invoice.invoice_type == Invoice.FILE:
                    form = NewInvoiceFileForm(instance=invoice)
                return render(request, 'new_invoice.html', {'form': form, 'title': 'Add your new invoice', 'step': 2})
            return render(request, 'new_invoice.html', {'form': form, 'title': 'Add your new invoice', 'step': 1})
        else:
            if request.POST.get('website'):
                form = NewInvoiceWebsiteForm(request.POST)
            elif request.POST.get('iban'):
                form = NewInvoiceCredentialsForm(request.POST)
            else:  # request.POST.get('file'):
                form = NewInvoiceFileForm(request.POST)
            if form.is_valid():
                form.instance.client = request.user.invoice_user
                #print(form.instance)
                form.save()
                messages.success(request, f'You have new invoice {form.instance}')
                return redirect('index')
            return render(request, 'new_invoice.html', {'form': form, 'title': 'Add your new invoice', 'step': 2})


class ClientsList(ListView):
    model = User
    template_name = 'clients_list.html'
    context_object_name = 'clients'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        print('ClientsList', request.user.invoice_user)
        self.object_list = request.user.invoice_user.clients.all()
        context = self.get_context_data()
        return self.render_to_response(context)


class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'invoice_detail.html'
    context_object_name = 'invoice'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        invoice = Invoice.objects.get(pk=int(request.POST.get('invoice_id')))
        try:
            invoice.pay(request.user.invoice_user)
        except ValueError as e:
            messages.error(request, e, extra_tags='danger')
            return self.render_to_response(context)
        messages.success(request, f'Invoice is paid')
        return redirect('index')


class InvoicesList(ListView):
    model = Invoice
    template_name = 'invoices_list.html'
    context_object_name = 'invoices'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        self.object_list = request.user.invoice_user.unpaid_invoices.all()
        context = self.get_context_data()
        return self.render_to_response(context)
