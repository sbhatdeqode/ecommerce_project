from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    dob = forms.DateField(label='Date Of Birth',)

    gender=forms.CharField(
        label=("Gender"),
        widget=forms.TextInput(
            attrs={ "placeholder":("Gender")})
    )
    adress=forms.CharField(
        label=("Adress"),
        widget=forms.TextInput(
            attrs={ "placeholder":("Adress")})
    )

    

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.dob = self.cleaned_data['dob']
        user.gender=self.cleaned_data['gender']
        user.save()
        return user
