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
    path('meus-imoveis/', MyPropertyListView.as_view(), name='my-properties'),
    path('meus-imoveis/criar/', PropertyCreateView.as_view(), name='property-create'),
    path('meus-imoveis/<int:pk>/editar/', PropertyUpdateView.as_view(), name='property-update'),
    path('meus-imoveis/<int:pk>/excluir/', PropertyDeleteView.as_view(), name='property-delete'),
    path('meus-imoveis/<int:property_id>/quartos/', RoomListView.as_view(), name='room-list'),
    path('meus-imoveis/<int:property_id>/quartos/criar/', RoomCreateView.as_view(), name='room-create'),
    path('quartos/<int:pk>/editar/', RoomUpdateView.as_view(), name='room-update'),
    path('quartos/<int:pk>/excluir/', RoomDeleteView.as_view(), name='room-delete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

