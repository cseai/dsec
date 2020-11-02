from django import forms
from vendors.models import Store
from django.utils.safestring import mark_safe

class ImagePreviewWidget(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        input_html = super().render(name, value, attrs=None, **kwargs)
        img_html = mark_safe(f'<br><br><img src="{value.url}" style="height:200px; width:200px; margin:0 auto; display:flex; "  /><br><br>')
        return f'{img_html}{input_html}'


class StoreFormDisable(forms.ModelForm):
    class Meta:
        model = Store
        fields = (
            'logo',
            'title',
            'username',
            'user',
            'category',
            'tagline',
            'description',
            'address',
            'opening_time',
            'closing_time',
            
        )
        exclude=('height_field','width_field','parent')
        
        widgets = {
            'is_verified': forms.CheckboxInput(attrs={'class':'form-control'}),
            'title':forms.TextInput(attrs={'class':'form-control'}),
        }

    logo = forms.ImageField(widget=ImagePreviewWidget,)
    
    
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        # self.fields['is_verified'].widget.atrs['class']='mt-4'
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control is-valid'
            visible.field.widget.attrs['disabled'] = True
            visible.field.widget.attrs['style'] = 'margin:10px 0px; '
        
    

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = (
            'logo',
            'title',
            'username',
            'user',
            'category',
            'tagline',
            'description',
            'address',
            'opening_time',
            'closing_time',
            
        )
        exclude=('height_field','width_field','parent')
        
        widgets = {
            'is_verified': forms.CheckboxInput(attrs={'class':'form-control'}),
            'title':forms.TextInput(attrs={'class':'form-control'}),
        }

    logo = forms.ImageField(widget=ImagePreviewWidget,)
    
    
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control is-warning'
            # visible.field.widget.attrs['disabled'] = True
            visible.field.widget.attrs['style'] = 'margin:10px 0px; '
        
    def save(self, commit=True):
        # Save the provided information
        store = super(StoreForm, self).save(commit=False)
        if commit:
            store.save()
        return store
