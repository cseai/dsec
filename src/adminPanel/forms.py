from django import forms
from vendors.models import Store

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = '__all__'
        exclude=('height_field','width_field','parent')
        labels={
            'is_verified':'Is Verified'
        }
        widgets = {
            'is_verified': forms.CheckboxInput(attrs={'class':'form-control'}),
            'title':forms.TextInput(attrs={'class':'form-control'})
        }

    # is_verified=forms.BooleanField()
    
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        # self.fields['is_verified'].widget.atrs['class']='mt-4'
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['style'] = 'margin:10px 0px; '
        
    
