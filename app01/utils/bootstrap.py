from django import forms


class BootStrap:
    bootstrap_exclude_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            ## 如果字段中原来有值，保留其他的，没有属性，才增加
            if name in self.bootstrap_exclude_fields:
                continue
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {"class": "form-control",
                                      "placeholder": field.label
                                      }


class BootstrapModelForm(BootStrap, forms.ModelForm):
    pass


class BootstrapForm(BootStrap, forms.Form):
    pass
