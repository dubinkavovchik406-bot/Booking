from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from my_auth.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email")