from django import forms

class add_entry(forms.Form):
    Title = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Title'
    }))
    Content = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Content'
    }))
    Edit = forms.BooleanField(initial=False, required=False)

class NewSearchForm(forms.Form):
    search = forms.CharField(label="Search",required= False,
    widget= forms.TextInput
    (attrs={'placeholder':'Search Encyclopedia'}))

