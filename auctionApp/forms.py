from django import forms

from auctionApp.currency import Currency


class LoginForm(forms.Form):
    username = forms.CharField(initial='Username', max_length=20)
    password = forms.CharField(initial='Password', widget=forms.PasswordInput())


class AddNewUserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    email = forms.EmailField(label='E-mail')
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Re-type password')
    currency = forms.CharField(widget=forms.Select(choices=Currency.code_list(type='pairlist')), label='What is your currency?', initial='EUR')


class EditUserForm(forms.Form):
    email = forms.EmailField(label='E-mail', required=False)
    new_password1 = forms.CharField(label = 'New password', widget=forms.PasswordInput(), required=False)
    new_password2 = forms.CharField(label = 'Re-enter new password', widget=forms.PasswordInput(), required=False)
    old_password = forms.CharField(label = 'Current password (required)', widget=forms.PasswordInput())


class AddAuctionForm(forms.Form):
    title = forms.CharField(label="Auction title", max_length=100)
    description = forms.Field(widget=forms.Textarea)
    starting_price = forms.FloatField(initial=0)


class CurrencyPicker(forms.Form):
    currency = forms.CharField(widget=forms.Select(choices=Currency.code_list(type='pairlist')), label='Currency')
