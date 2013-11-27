
# import the models library from django.db
from django.db import models
# add import to add validation for max_length for the text area
from django.core.validators import MaxLengthValidator
# Add import to create forms from class models
# from django.forms import ModelForm
# import admindatewidget from django admin
# from django.contrib.admin.widgets import AdminDateWidget


# Create Product class to represent the Products table

class Product(models.Model):
    name = models.CharField(max_length=100) #name field in the Products table
    #description = models.CharField(max_length=255)
    description = models.TextField(validators=[MaxLengthValidator(350)])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('inventory.Category') # relate the category field to Category table

    def current_quantity(self):
        """
        Function to calculate the total quantity of each product in system
        by subtracting the the quantity issued from the quantity received

        """
        issued = IssueProduct.objects.filter(name=self)
        issued_quantities = issued.values_list('quantity',flat=True)
        issued_quantities = sum(issued_quantities)
        received = ReceiveProduct.objects.filter(name=self)
        received_quantities = received.values_list('quantity', flat=True)
        received_quantities = sum(received_quantities)

        total_quantity = received_quantities - issued_quantities

        # check to make sure that issued products is not greater than products received
        # if issued_quantities > received_quantities:
        #     # total_quantity = "You cannot issue a quantity more than that received"
        #     total_quantity = -1

        return total_quantity

    def current_quantity_value(self):
        """
        Function to calculate the total price value of a particular product by
        multiplying the quantity * price
        """
        product_qty = self.current_quantity()
        product_price = self.price

        total_quantity_value = product_qty * product_price
        return total_quantity_value


    # Create unicode function to display attributes in UTF-8 format
    def __unicode__(self):
        return self.name

		#self.name
		#self.description
		#self.price
		#self.category





# Create a Category class to create a Category table for the products

class Category(models.Model):
	category = models.CharField(max_length=50)

	# Create unicode function to display attributes in UTF-8 format
	def __unicode__(self):
		return self.category


# Create a model form to add category

'''class CategoryForm(ModelForm):
    class Meta:
        model = Category'''


# Create a model form to add products

'''class ProductForm(ModelForm):
    class Meta:
        model = Product'''


# Create a ReceiveProducts class for receiving products as inventory

class ReceiveProduct(models.Model):
	date_received = models.DateField()
	quantity = models.IntegerField(default=0)
	name = models.ForeignKey('inventory.Product') #relate this field to the product name in Products table




# Create an IssueProducts class for issue out products from the inventory

class IssueProduct(models.Model):
	date_issued = models.DateField()
	quantity = models.IntegerField(default=0)
	name = models.ForeignKey('inventory.Product') #relate this field to the product name in Products table


# Create a class so user can edit product

class EditProduct(models.Model):
    product_name = models.ForeignKey('inventory.Product')




# Create form model for Receiveproduct class

'''class ReceiveProductForm(ModelForm):
    class Meta:
        model = ReceiveProduct
        # Display form fields in particular order
        fields = ['date_received', 'name', 'quantity']




# Create form model for Issueproduct class

class IssueProductForm(ModelForm):
    class Meta:
        model = IssueProduct
        fields = ['date_issued', 'name', 'quantity']'''
	
	
	
