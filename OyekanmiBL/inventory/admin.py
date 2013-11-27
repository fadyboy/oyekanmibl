from django.contrib import admin

# import model classes from the inventory application
from inventory.models import Product, Category, ReceiveProduct, IssueProduct
# Add django.template import RequestContext to take care of csrf message
# from django.template import RequestContext

# register both model classes so they are displayed in admin
admin.site.register(Product)
admin.site.register(Category)
# admin.site.register(ReceiveProducts)
# admin.site.register(IssueProducts)


# create admin class to re-arrange field in IssueProducts and ReceiveProducts class

class AdminClass(admin.ModelAdmin):
	fields = ['date_issued', 'name', 'quantity']
	

class AdminClass2(admin.ModelAdmin):
	fields = [ 'date_received', 'name', 'quantity']
	
# Register classes again to implement changes

admin.site.register(IssueProduct, AdminClass)
admin.site.register(ReceiveProduct, AdminClass2)
