from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from mptt.forms import TreeNodeChoiceField
from .models import Comment
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']



class CreateCommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['parent'].widget.attrs.update({'class':'d-none'})
        self.fields['post'].widget.attrs.update({'class':'d-none'})
        self.fields['parent'].label = ''
        self.fields['post'].label = ''
        self.fields['parent'].required = False
        self.fields['post'].required = False


    class Meta:
        model = Comment
        fields = ('parent','content','post')
        widgets = {
            'content':forms.Textarea(attrs={'class':'form-control','rows':5,'style':'width:50%'}),
        }

