from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'OyekanmiBL.views.home', name='home'),
    # url(r'^OyekanmiBL/', include('OyekanmiBL.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'inventory.views.home', name='home'), # Create a view for the home page
    url(r'^home/', 'inventory.views.home', name='home'),
    url(r'^login/$', 'inventory.views.mylogin', name='login'),
    url(r'^addproduct/', 'inventory.views.addproduct', name='addproduct'), # Create a view for the addProduct page
	url(r'^addcategory/', 'inventory.views.addcategory', name='addcategory'),
	url(r'^receiveproduct/', 'inventory.views.receiveproduct', name='receiveproduct'),
	url(r'^issueproduct/', 'inventory.views.issueproduct', name='issueproduct'),
	url(r'^mylogout/', 'inventory.views.mylogout', name='mylogout'),
)
