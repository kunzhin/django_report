from django import forms
from django.db import models
from django.forms import fields, widgets
from .models import *
from django.core.exceptions import ValidationError


# Форма отправки аудита фотопотока
class PhotostreamInsertForm(forms.ModelForm):
    class Meta:
        model = PhotostreamForm
        fields = (
            'esr',
            'tt',
            'address',
            'category',
            'url_photo',
            'photo',
            'comment',
            'status_worked_out',
            'date_correction'
        )

        widgets = {
            'esr': forms.Select(attrs={'class': 'form-control'}),
            'tt': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'url_photo': forms.URLInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'status_worked_out': forms.CheckboxInput(attrs={'class': 'form-check-label'}),
            'date_correction': forms.DateInput(attrs={'type': 'date'}),
        }

    # Валидатор, проверяем ссылку
    def clean_url_photo(self):
        url = self.cleaned_data['url_photo']
        url_split = url.split('/')
        if 'photo.nestle.ru' not in url_split:
            raise ValidationError('Ссылка на фото должна быть с сайта "photo.nestle.ru"')
        else:
            return url
