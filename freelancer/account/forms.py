from django import forms
from django.contrib.auth import get_user_model
from django.contrib.postgres.forms import SimpleArrayField
from django.contrib.auth.validators import UnicodeUsernameValidator


class UserRegisterForm(forms.Form):
    first_name = forms.CharField(
        max_length=70,
        widget=forms.TextInput(
            attrs={"class":"input-text",
                "placeholder":"نام"}))

    last_name = forms.CharField(
        max_length=70,
        widget=forms.TextInput(
            attrs={"class":"input-text",
                "placeholder":"نام خانوادگی"}))
    
    username = forms.RegexField(
        regex=r"^[A-Za-z][A-Za-z0-9_.]*$",
        max_length=70,
        widget=forms.TextInput(
            attrs={"class":"input-text",
                "placeholder":"نام کاربری"}))

    email = forms.CharField(
        max_length=70,
        widget=forms.EmailInput(
            attrs={"class":"input-text",
                "placeholder":"ایمیل"}))

    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"class":"input-text",
                "placeholder":"رمز عبور"}))

    confirm_password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(
            attrs={"class":"input-text",
                "placeholder":"تکرار رمز عبور"}))


    def clean_email(self) -> "email":
        """
        Check whether an email already exists or not. 

        Raises:
            ValidationError: email already exists.

        Returns:
            email: new user email address.
        """
        email = self.cleaned_data.get("email")    
        user = get_user_model().objects.filter(email=email)

        if user.exists():
            raise forms.ValidationError("این ایمیل قبلا در سایت ثبت نام کرده است")
        return email
    
    def clean_username(self) -> "username":
        """ 
        Check whether an username already exists or not. 

        Raises:
            ValidationError: username already exists.

        Returns:
            username: new username.
        """
        username = str(self.cleaned_data.get("username")).lower()
        user = get_user_model().objects.filter(username=username)
        if user.exists():
            raise forms.ValidationError("این یوزرنیم از قبل در سایت وجود دارد")

        return username.lower()


    def clean_password(self) -> "password":
        data = self.cleaned_data
        password = data.get("password")

        if len(password) < 4:
            raise forms.ValidationError("رمز عبور شما کوتاه میباشد، لطفا رمز عبور طولانی تری را وارد نمایید.")


    def clean_confirm_password(self) -> "password":
        """
        Check the first password and confirm password is the same or not.
        
        Returns:
            password: str
        """
        cd = self.cleaned_data
        password = cd.get('password')
        confirm_password = cd.get('confirm_password')
        
        if password and confirm_password and confirm_password != password:
            raise forms.ValidationError("دو پسورد وارد شده با هم مطابقت ندارد.")
        else:
            return confirm_password


class UserLoginForm(forms.Form):
    email = forms.CharField(
        max_length=70,
        error_messages={"required": "لطفا مقدار خواسته شده برای فیلد زیر را وارد نمایید."},
        widget=forms.EmailInput(
            attrs={"placeholder":"ایمیل",
                "class":"input-text"}))

    password = forms.CharField(
        max_length=100,
        error_messages={"required": "لطفا مقدار خواسته شده برای فیلد زیر را وارد نمایید."},
        widget=forms.PasswordInput(
            attrs={"class":"input-text",
                "placeholder":" رمز عبور"}))

    def clean_username(self):
        return str(self.cleaned_data.get("username")).lower()


class EditProfileForm(forms.Form):
    first_name = forms.CharField(
        label="اسم",
        max_length=70,
        required=False,
        widget=forms.TextInput(
            attrs={"class":"input-text",
                "placeholder":"نام"}))

    last_name = forms.CharField(
        label="اسم خانوادگی",
        required=False,
        max_length=70,
        widget=forms.TextInput(
            attrs={"class":"input-text",
                "placeholder":"نام خانوادگی"}))

    bio = forms.CharField(
        label="توضیحات پروفایل",
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={"class":"input-text",
                "placeholder":"بیوگرافی شما، حد اکثر 100 کاراکتر"}))

    skills = SimpleArrayField(
        forms.CharField(max_length=400, required=False),
        required=False,
        label_suffix="مهارت های شما(حد اکثر 10 مورد)")

    avatar = forms.ImageField(
        label="عکس پروفایل",
        required=False,
        allow_empty_file=True,
        widget=forms.FileInput(attrs={
            "class":"uploadProfileInput",
            "style":"opacity: 0;",
            "onchange":"loadImgFile(event)",
            "accept":"image/jpg,image/png,image/jpeg"}))

    def save(self, user_id, profile_model):
        """
        Update the user profile and User model.
        """
        data = self.cleaned_data
        user = get_user_model().objects.get(id=user_id)
        user.first_name=data['first_name']
        user.last_name=data['last_name']
        user.save()

        profile_model(
            user=user,
            bio=data["bio"],
            avatar=data["avatar"]
        ).save()

        user.user_cv.skills = data["skills"]
        user.user_cv.save()


class ConversationForm(forms.Form):
    message = forms.CharField(
        label_suffix="توضیحات",
        max_length=500,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "input-text",
                    "placeholder": "نوشتن پیام..."}))

    file = forms.FileField(
        label="فایل",
        required=False,
        allow_empty_file=True,
        widget=forms.FileInput(attrs={
            "class":"uploadProfileInput"}))