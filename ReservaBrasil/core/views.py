from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from unidecode import unidecode
from .models import *
import random
import os

# Create your views here.
class MyPropertyListView(LoginRequiredMixin, ListView):
    model = Property
    template_name = "property_list.html"
    context_object_name = "properties"

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)


class PropertyCreateView(LoginRequiredMixin, CreateView):
    model = Property
    fields = ['image', 'name', 'price', 'rate', 'active', 'category', 'typeProperty', 'description']
    template_name = "property_form.html"
    success_url = reverse_lazy("my-properties")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PropertyUpdateView(LoginRequiredMixin, UpdateView):
    model = Property
    fields = ['image', 'name', 'price', 'rate', 'active', 'category', 'typeProperty', 'description']
    template_name = "property_form.html"
    success_url = reverse_lazy("my-properties")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise Http404("Você não tem permissão para editar este imóvel.")
        return obj


class PropertyDeleteView(LoginRequiredMixin, DeleteView):
    model = Property
    template_name = "property_confirm_delete.html"
    success_url = reverse_lazy("my-properties")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise Http404("Você não tem permissão para excluir este imóvel.")
        return obj


class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = "room_list.html"
    context_object_name = "rooms"

    def get_queryset(self):
        property_id = self.kwargs['property_id']
        property_obj = get_object_or_404(Property, id_property=property_id, owner=self.request.user)
        return property_obj.rooms.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property'] = get_object_or_404(Property, id_property=self.kwargs['property_id'])
        return context


class RoomCreateView(LoginRequiredMixin, CreateView):
    model = Room
    fields = ['name', 'price', 'numberOfPeople', 'beds', 'description']
    template_name = "room_form.html"

    def form_valid(self, form):
        property_obj = get_object_or_404(Property, id_property=self.kwargs['property_id'], owner=self.request.user)
        form.instance.property = property_obj
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('room-list', kwargs={'property_id': self.kwargs['property_id']})


class RoomUpdateView(LoginRequiredMixin, UpdateView):
    model = Room
    fields = ['name', 'price', 'numberOfPeople', 'beds', 'description']
    template_name = "room_form.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.property.owner != self.request.user:
            raise Http404("Você não tem permissão para editar este quarto.")
        return obj

    def get_success_url(self):
        return reverse_lazy('room-list', kwargs={'property_id': self.object.property.id_property})


class RoomDeleteView(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = "room_confirm_delete.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.property.owner != self.request.user:
            raise Http404("Você não tem permissão para excluir este quarto.")
        return obj

    def get_success_url(self):
        return reverse_lazy('room-list', kwargs={'property_id': self.object.property.id_property})


def login_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'login':
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '')

            if not username or not password:
                messages.error(request, 'Todos os campos são obrigatórios para login.')
                return redirect('login_view')

            user = authenticate(request, username=username, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('homepage')
                messages.error(request, 'Esta conta está desativada.')
            else:
                messages.error(request, 'Nome de usuário ou senha inválidos.')
            return redirect('login_view')

        elif action == 'register':
            username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            phoneNumber = request.POST.get('telefone', '').strip()
            password = request.POST.get('password', '')
            confirm_password = request.POST.get('confirm_password', '')

            if not all([username, email, phoneNumber, password, confirm_password]):
                messages.error(request, 'Todos os campos são obrigatórios para registro.')
                return redirect('login_view')

            if password != confirm_password:
                messages.error(request, 'As senhas não coincidem.')
                return redirect('login_view')

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Nome de usuário já está em uso.')
                return redirect('login_view')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'E-mail já está em uso.')
                return redirect('login_view')

            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                UserApp.objects.create(user=user, phoneNumber=phoneNumber)
                messages.success(request, 'Conta criada com sucesso! Faça login.')
            except:
                messages.error(request, 'Erro ao criar a conta. Tente novamente.')
            return redirect('login_view')

    image_list = [
        'img/login_view/fundo1.jpg',
        'img/login_view/fundo2.jpg',
        'img/login_view/fundo3.jpg',
    ]

    selected_image = random.choice(image_list)
    return render(request, 'login.html', {'background_image': selected_image})


def recoverPassword(request): 
    return render(request, 'recoverPassword.html')


def homepage(request):
    properties = list(Property.objects.filter(active=True))  
    random.shuffle(properties)  
    propertyResults = properties[:9]  
    return render(request, 'homepage.html', {'propertyResults': propertyResults})



def normalizeText(text):
    return unidecode(text.lower())


def searchProperty(request):
    searchQuery = normalizeText(request.GET.get('searchQuery', '').strip())
    propertyResults = []

    if searchQuery:
        allProperties = Property.objects.select_related('category', 'typeProperty').all()
        propertyResults = [
            p for p in allProperties
            if searchQuery in normalizeText(p.name)
            or (p.category and searchQuery in normalizeText(p.category.name))
            or (p.typeProperty and searchQuery in normalizeText(p.typeProperty.name))
        ]

    return render(request, 'searchResults.html', {
        'searchQuery': request.GET.get('searchQuery', '').strip(),
        'propertyResults': propertyResults
    })


def propertyDetail(request, property_id):
    property_obj = get_object_or_404(Property, id_property=property_id)
    return render(request, 'propertyDetail.html', {'property': property_obj})


def users(request):
    return render(request, 'users.html')


@login_required(login_url='login_view')
def homeReservation(request):
    return render(request, 'homeReservation.html')


@login_required(login_url='login_view')
def reservation(request):
    return render(request, 'reservation.html')


def Invoice(request):
    return render(request, 'Invoice.html')


def Businesses(request):
    return render(request, 'Businesses.html')
