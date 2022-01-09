from typing import Text
from django import forms
from django.forms.models import ModelChoiceField,ModelMultipleChoiceField
from django.forms.widgets import Select,Input,TextInput
from ..models import Hincatmst,Ckmmst,Ktnmst,Sskmst,DateModel
from django.contrib.auth.forms import (
    AuthenticationForm
)

class SosikiForm(forms.Form):
    name = ModelChoiceField(
        label='店舗',
        queryset=Sskmst.objects.all(),
        empty_label= None, 
        to_field_name='sskcd',
        widget=Select(attrs={'id': 'Select_sskId','name': 'Select_sskName'}),
        required=True
    )
    # 組織セレクトボックス
    class Meta:
        model  = Ckmmst
        fields = ("sskcd", "sskname")


class KyotenForm(forms.Form):

    name = ModelChoiceField(
        label='店舗',
        queryset=Ktnmst.objects.all(),
        empty_label= None, 
        to_field_name='ktncd',
        widget=Select(attrs={'id': 'Select_ktnId','name': 'Select_ktnName'}),
        required=True
    )

    # 店舗セレクトボックス
    class Meta:
        model  = Ckmmst
        fields = ("ktncd", "ktnname")

class KyotenFormDisable(forms.Form):

    name = ModelChoiceField(
        label='店舗',
        queryset=Ktnmst.objects.all(),
        empty_label= None, 
        to_field_name='ktncd',
        widget=Select(attrs={'id': 'Select_ktnId','name': 'Select_ktnName','disabled':'disabled'}),
        required=True
    )
    # disableにする
    name.widget.attrs["disabled"] = ""
    # 店舗セレクトボックス
    class Meta:
        model  = Ckmmst
        fields = ("ktncd", "ktnname")


class HinCategoryForm(forms.Form):
    name = ModelMultipleChoiceField(
        label='カテゴリ',
        queryset=Hincatmst.objects.all(),
        to_field_name='catcd',
        widget=Select(attrs={'id': 'Select_catId','name': 'Select_catName'})
    )
    # カテゴリセレクトボックス
    class Meta:
        model  = Hincatmst
        fields = ("catcd", "catname")

class CookingMethodForm(forms.Form):
    name = ModelChoiceField(
        label='調達方法',
        queryset=Ckmmst.objects.all(),
        empty_label= None, 
        to_field_name='ckmcd',
        widget=Select(attrs={'id': 'Select_ckmId','name': 'Select_ckmName'}),
        required=True
    )
    # 調達方法セレクトボックス
    class Meta:
        model  = Ckmmst
        fields = ("ckmcd", "ckmname")

class CookingMethodFormDisable(forms.Form):
    name = ModelChoiceField(
        label='調達方法',
        queryset=Ckmmst.objects.all(),
        empty_label= None, 
        to_field_name='ckmcd',
        widget=Select(attrs={'id': 'Select_ckmId','name': 'Select_ckmName'}),
        required=True
    )

    # disableにする
    name.widget.attrs["disabled"] = ""
    # 調達方法セレクトボックス
    class Meta:
        model  = Ckmmst
        fields = ("ckmcd", "ckmname")


class AddCalenderForm(forms.ModelForm):

    name = forms.DateField(
        label="",
        widget=Input(attrs={'id': 'Calender_dtId','name': 'Calender_dtName'}),
    )

    class Meta:
        model = DateModel
        fields = ('date_field',)

class AddCalenderForm2(forms.ModelForm):

    name = forms.DateField(
        label="",
        widget=TextInput(attrs={'id': 'sledtlabel','name': 'sledtlabelnm','class':'crdselectinp'}),
    )

    class Meta:
        model = DateModel
        fields = ('date_field',)


class AddCalenderForm3(forms.ModelForm):

    name = forms.DateField(
        label="",
        widget=TextInput(attrs={'id': 'discdtlabel-from','name': 'discdtlabelnm-from','class':'crdselectinp'}),
    )

    class Meta:
        model = DateModel
        fields = ('date_field',)

class AddCalenderForm4(forms.ModelForm):

    name = forms.DateField(
        label="",
        widget=TextInput(attrs={'id': 'discdtlabel-to','name': 'discdtlabelnm-to','class':'crdselectinp'}),
    )

    class Meta:
        model = DateModel
        fields = ('date_field',)

class HinSerchTextform(forms.Form):

    name = forms.CharField(label='商品',
        max_length=100,
        widget=TextInput(attrs={'id': 'Hin_dtId','name': 'Hin_dtName','placeholder':'JANコードまたは商品名'}),
        )


class Kako4ChoiceForm(forms.Form):
    name = forms.fields.ChoiceField(
        choices = (
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4')
        ),
        required=True,
        widget=forms.widgets.Select(attrs={'id': 'kako4_Id','name': 'kako4_Name','class':'d-inline-block form-control-sm'})
    )

class WeekcheckboxForm(forms.Form):
    weekckbx = forms.ChoiceField(
        label="",
        choices=(
            ('0','月'),('1','火'),('2','水'),('3','木'),('4','金'),('5','土'),('6','日')
        ),
        required=True,
        widget=forms.CheckboxSelectMultiple(attrs={'class':'wkrowlyo ulstart0'}), 
    )
    