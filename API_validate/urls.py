from django.conf.urls import url
from . import views

# url's for comm_info and get_default_reasons for filing

urlpatterns = [

    url(r'^f99/validate_f99$', views.validate_f99, name='validate_f99'),

]
