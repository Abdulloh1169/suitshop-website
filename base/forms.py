from django import forms
from django.conf import settings as st
from django.core.mail import send_mail
from django.utils.translation import gettext as _
from . import models


class ContactForm(forms.ModelForm):
	message = forms.CharField(widget=forms.Textarea(attrs={"rows": 6, 'placeholder': _('message'), 'class': "form-control"}))
	subject = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('subject'), 'class': "form-control"}))
	phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('phone'), 'class': "form-control"}))
	name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('name'), 'class': "form-control"}))
	
	class Meta:
		model=models.Contact
		fields = '__all__'


	def send_message(self):
		send_mail(
    		self.subject, self.message, st.EMAIL_HOST_USER,
    		[st.EMAIL_BOSS_USER], fail_silently=True)
