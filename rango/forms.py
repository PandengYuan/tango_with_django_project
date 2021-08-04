from django import forms
from django.contrib.auth.models import User
from rango.models import Category, Page, UserProfile, Product

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)

class ProductForm(forms.ModelForm):
    # id = models.CharField(max_length=CHAR_MAX_LENGTH, primary_key=True)
    img = forms.ImageField()
    # category = forms.CharField(max_length=Product.CHAR_MAX_LENGTH, help_text="Please enter the category of the product.")
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True, empty_label=None, initial="--", help_text="Please enter the category of the product.")
    name = forms.CharField(max_length=Product.CHAR_MAX_LENGTH, help_text="Please enter the name of the product.")
    description = forms.CharField(max_length=Product.DESCRIPTION_MAX_LENGTH, help_text="Please enter the description of the product.")
    price = forms.FloatField(help_text="Please enter the price of the product.")
    sales = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Product

        fields = ('img','category', 'name', 'description', 'price')
        # or specify the fields to include (don't include the category field).
        #fields = ('title', 'url', 'views')


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=Page.URL_MAX_LENGTH, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
        return cleaned_data

    class Meta:
        model = Page

        exclude = ('category',)
        # or specify the fields to include (don't include the category field).
        #fields = ('title', 'url', 'views')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('address','picture', 'usertype',)
