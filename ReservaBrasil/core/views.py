from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from unidecode import unidecode
from .models import *
import random


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'login':
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '')

            if not username or not password:
                messages.error(request, 'Todos os campos são obrigatórios para login.')
                return redirect('login')

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
    return render(request, 'login.html')


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


@login_required
def homeReservation(request):
    return render(request, 'homeReservation.html')


@login_required
def reservation(request):
    return render(request, 'reservation.html')


def Invoice(request):
    return render(request, 'Invoice.html')


def Businesses(request):
    return render(request, 'Businesses.html')


@login_required
def addImage(request):
    return render(request, 'addImage.html')
