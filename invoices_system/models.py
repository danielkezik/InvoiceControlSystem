from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User as DjangoUser
from dateutil.relativedelta import relativedelta
from datetime import datetime
from django_iban.fields import IBANField


class User(models.Model):
    user = models.OneToOneField(DjangoUser,
                                on_delete=models.CASCADE,
                                related_name='invoice_user')

    MODERATOR = 'MR'
    MANAGER = 'MG'
    CLIENT = 'CL'
    USER_CLASS_CHOICES = [
        (MODERATOR, 'Moderator'),
        (MANAGER, 'Manager'),
        (CLIENT, 'Client'),
    ]

    user_class = models.CharField(max_length=2,
                                  choices=USER_CLASS_CHOICES,
                                  default=CLIENT)
    is_approved = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    balance = models.DecimalField(decimal_places=2, default=0,
                                  max_digits=9)

    managed_by = models.ForeignKey('self', related_name='clients', blank=True,
                                   null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"[{self.user_class}] {self.user.username}"

    def add_to_balance(self, money):
        if self.balance+money < 0:
            raise ValueError('Balance should not be less than 0')
        self.balance += money
        self.save()

    @property
    def unpaid_invoices(self):
        return self.invoices.filter(is_paid=False)

    @property
    def full_name(self):
        if self.user.first_name and self.user.last_name:
            return self.user.get_full_name()
        return self.user.username


class Invoice(models.Model):
    client = models.ForeignKey(User, related_name='invoices',
                               null=True, on_delete=models.SET_NULL)

    name = models.CharField(max_length=100, default='My invoice')

    YEARLY = 'Y'
    MONTHLY = 'M'
    WEEKLY = 'W'
    DAILY = 'D'
    REGULARITY_CHOICES = [
        (YEARLY, 'Yearly'),
        (MONTHLY, 'Monthly'),
        (WEEKLY, 'Weekly'),
        (DAILY, 'Daily'),
    ]
    regularity = models.CharField(max_length=1,
                                  choices=REGULARITY_CHOICES,
                                  default=MONTHLY)
    is_regular = models.BooleanField()
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)

    WEBSITE = 'WEB'
    FILE = 'FIL'
    CREDENTIALS = 'CRD'
    INVOICE_TYPE_CHOICES = [
        (WEBSITE, 'Website'),
        (FILE, 'File'),
        (CREDENTIALS, 'Credentials'),
    ]
    invoice_type = models.CharField(max_length=3,
                                    choices=INVOICE_TYPE_CHOICES)

    website = models.URLField(blank=True)
    login = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100, blank=True)

    file = models.FileField(upload_to='user_files', blank=True)

    iban = IBANField(blank=True)
    full_name = models.CharField(max_length=100, blank=True)

    total = models.DecimalField(decimal_places=2, blank=True,
                                max_digits=9)
    comments = models.TextField()

    def get_regular_delta(self) -> relativedelta:
        if self.regularity == self.DAILY:
            return relativedelta(days=1)
        if self.regularity == self.WEEKLY:
            return relativedelta(weeks=1)
        if self.regularity == self.MONTHLY:
            return relativedelta(months=1)
        if self.regularity == self.YEARLY:
            return relativedelta(years=1)

    def pay(self, author: User):
        # todo validation
        self.client.add_to_balance(-self.total)
        if self.is_regular:
            self.due_date += self.get_regular_delta()
        else:
            self.is_paid = True
        self.invoice_logs.create(paid_by=author)
        self.save()

    def __str__(self):
        return f"Invoice {self.name} till {self.due_date}"


class InvoiceLog(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='invoice_logs',
                                null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(default=datetime.now)
    paid_by = models.ForeignKey(User, related_name='paid_invoices',
                                null=True, on_delete=models.SET_NULL)


admin.site.register(User)
admin.site.register(Invoice)
admin.site.register(InvoiceLog)
