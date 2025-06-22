from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', homepage, name='homepage'),
    path('login/', login_view, name='login_view'),
    path('RecoverPassword/', recoverPassword, name='recoverPassword'),
    path('reservation/', reservation, name='reservation'),
    path('searchResults/', searchProperty, name='searchProperty'),
    path('homeReservation/', homeReservation, name='homeReservation'),
    path('users/', users, name='users'),
    path('Invoice/', Invoice, name='Invoice'),
    path('Businesses/', Businesses, name='Businesses'),
    path('addImage/', addImage, name='addImage'),
     path('property/<int:property_id>/', propertyDetail, name='propertyDetail'),  
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
