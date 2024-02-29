from app01 import models
from django.core.validators import RegexValidator
from django import forms
from app01.utils.bootstrap import BootstrapModelForm


class UserModelForm(BootstrapModelForm):
    name = forms.CharField(min_length=2,
                           label="Username",
                           widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]


class NumModelForm(BootstrapModelForm):
    mobile = forms.CharField(
        label="Phone Number",
        validators=[RegexValidator(r'1[3-9]\d{9}$', 'Phone number must be entered in the format: 1xx-xxxx-xxxx')]
    )

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]

    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise forms.ValidationError("Phone number already exists.")

        return txt_mobile

    ########## 第二种验证方式(钩子函数) ########
    # def clean_mobile(self):
    #     txt_mobile = self.cleaned_data["mobile"]
    #
    #     if len(txt_mobile) != 11:
    #         # 验证不通过
    #         raise forms.ValidationError("Format is wrong")


class NumEditModelForm(BootstrapModelForm):
    # mobile = forms.CharField(disabled=True, label="Phone Number")
    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]

    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise forms.ValidationError("Phone number already exists.")

        return txt_mobile
