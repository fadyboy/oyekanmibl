from django import forms
#from django.forms import ModelForm
from inventory.models import ReceiveProduct, IssueProduct, Category, Product, EditProduct
from django.contrib.admin import widgets


# Form to create new Category

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category



# Form to create new Product

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product



# Form to Receive products

class ReceiveProductForm(forms.ModelForm):

    # use admin calendar widget for date_received field
    date_received = forms.DateField(widget=widgets.AdminDateWidget)

    class Meta:
        model = ReceiveProduct
        fields = ['date_received', 'name', 'quantity']
    """
    def __init__(self, *args, **kwargs):
        super(ReceiveProductForm, self).__init__(*args, **kwargs)
        self.fields['date_received'].widget.attrs['class'] = 'datepicker'
    """



# Form to Issue products

class IssueProductForm(forms.ModelForm):

    # use admin calendar widget for date_issued field
    date_issued = forms.DateField(widget=widgets.AdminDateWidget)
    class Meta:
        model = IssueProduct
        fields = ['date_issued', 'name', 'quantity']


# Form to select a product to view its details

# class ViewProductDetails(forms.ModelForm):
#
#     class Meta:
#         model = Product
#         fields = ['name']

class EditProductDetails(forms.ModelForm):

    class Meta:
        model = EditProduct



