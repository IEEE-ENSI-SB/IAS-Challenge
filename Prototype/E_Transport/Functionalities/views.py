from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.gis.geos import Point
from .models import User
from .block import *

def Get_access(request):
    return render(request, 'Functionalities/Form.html',{})

def Login(request):
    if request.user.is_authenticated:
        return redirect('Dashboard')
    page = 'LOGIN'
    if request.method == 'POST':
        Email = request.POST.get('Email').lower()
        password = request.POST.get('password')
        user = authenticate(request , email = Email, password = password)
        if user is not None:
            login(request, user)
            return redirect('Dashboard')
    return render(request, 'Functionalities/Authentication.html', {'page' : page})

def Register(request):
    if request.user.is_authenticated:
        return redirect('Dashboard')
    if request.method == 'POST':
        image = request.FILES['image']
        file_name = default_storage.save(image.name, image)
        username = request.POST.get('username')
        name = username
        password =make_password(request.POST.get('password1'))
        email = request.POST.get('Email').lower()
        phone = request.POST.get('phone')
        Vehicle_Type = request.POST.get('Vehicle_Type')
        Charger_Type = request.POST.get('Charger_Type')
        user = User.objects.create(image=file_name, name=name, username=username, password=password, email=email, phone=phone, Vehicle_Type=Vehicle_Type, Charger_Type=Charger_Type)
        user.save()
        return redirect('login')
    return render(request, 'Functionalities/Authentication.html', {})

def user_logout(request):
    logout(request)
    return redirect('Home')

def Home(request):
    return render(request, 'Functionalities/Home.html', {})

@login_required(login_url='login')
def Dashboard_User(request):
    scam = False
    error = False
    user = request.user
    chargers = User.objects.filter(role__iexact='charger')
    User_Transactions = []
    Charger_Transactions = []
    for block in BT.chain[::-1]:
        if block['transaction']['User_email'] == user.email:
            User_Transactions.append(block)
        if str(block['transaction']['chargerId']) == str(user.id):
            Charger_Transactions.append(block)
    if request.method == 'POST':
        chargingFees = request.POST.get('chargingFees')
        Energy_Delivered = request.POST.get('Energy_Delivered')
        IDcharger = request.POST.get('IDcharger')
        try:
            charger = User.objects.get(id=IDcharger)
        except User.DoesNotExist:
            charger = None
        if( charger != None  and charger.role.lower() == 'charger'):
            transaction = {
                    'User_ID' : user.id,
                    'User_username': user.username,
                    'User_email': user.email,
                    'User_phone': user.phone,
                    'UserImageUrl': user.image.url,

                    'Charger_username': charger.username,
                    'Charger_email': charger.email,
                    'Charger_phone': charger.phone,
                    'chargerId': IDcharger,
                    'chargerImageUrl': charger.image.url,


                    'charging_fees': chargingFees,
                    'Energy_Delivered': Energy_Delivered,

                    'Vehicle_Type': user.Vehicle_Type,

                    'Charger_Type': charger.Charger_Type,

                    'charger_position': (charger.position.x, charger.position.y),

                    'Transaction_date': timezone.now().strftime('%Y-%m-%d %H:%M'),
                }

            if(float(chargingFees) / float(Energy_Delivered) > float(settings.UNIT_COST)):
                mine_block(BT_scam,transaction)
                scam = True
            else:
                mine_block(BT, transaction)
                return redirect('Dashboard')
        else:
            error = True
    return render(request, 'Functionalities/Dashboard.html', { 'chargers':chargers, 'BT_Charger':Charger_Transactions , 'BT': User_Transactions, 'scam': scam, 'error': error, 'user': user})

def search_User_transactions(request):
    inside_div = str(request.POST.get('transactions_made_by_user'))
    if (inside_div== ''):
        innerHTML = ''
        for block in BT.chain[::-1]:
            if block['transaction']['User_email'] == request.user.email:
                innerHTML += '''
                <tr>
                    <td>'''+ str(block['transaction']['chargerId']) +'''</td>
                    <td>
                        <div class="client">
                            <img class="client-img bg-img" src="'''+  block['transaction']['chargerImageUrl']  + '''" alt="">
                            <div class="client-info">
                                <h4>'''+ block['transaction']['Charger_username'] + '''</h4>
                                <small>''' + block['transaction']['Charger_email'] + '''</small>
                            </div>
                        </div>
                    </td>
                    <td>''' + block['transaction']['Energy_Delivered'] + '''</td>
                    <td>''' + block['transaction']['Transaction_date'] + '''</td>
                    <td>''' + block['transaction']['charging_fees'] + ''' dt</td>
                    <td>
                        <span class="paid">Valid</span>
                    </td>
                </tr>
                '''

        return HttpResponse(innerHTML)
    else:
        innerHTML = ''
        for block in BT.chain[::-1]:
            if block['transaction']['User_email'] == request.user.email and inside_div in block['transaction']['Charger_username']:
                innerHTML += '''
                <tr>
                    <td>'''+ str(block['transaction']['chargerId']) +'''</td>
                    <td>
                        <div class="client">
                            <img class="client-img bg-img" src="'''+  block['transaction']['chargerImageUrl']  + '''" alt="">
                            <div class="client-info">
                                <h4>'''+ block['transaction']['Charger_username'] + '''</h4>
                                <small>''' + block['transaction']['Charger_email'] + '''</small>
                            </div>
                        </div>
                    </td>
                    <td>''' + block['transaction']['Energy_Delivered'] + '''</td>
                    <td>''' + block['transaction']['Transaction_date'] + '''</td>
                    <td>''' + block['transaction']['charging_fees'] + ''' dt</td>
                    <td>
                        <span class="paid">Valid</span>
                    </td>
                </tr>
                '''
            
        return HttpResponse(innerHTML)
      
def search_Charger_transactions(request):
    inside_div = str(request.POST.get('transactions_made_by_Charger'))
    if (inside_div== ''):
        innerHTML = ''
        for block in BT.chain[::-1]:
            if block['transaction']['Charger_email'] == request.user.email:
                innerHTML += '''
                <tr>
                    <td>'''+ str(block['transaction']['User_ID']) +'''</td>
                    <td>
                        <div class="client">
                            <img class="client-img bg-img" src="'''+  block['transaction']['UserImageUrl']  + '''" alt="">
                            <div class="client-info">
                                <h4>'''+ block['transaction']['User_username'] + '''</h4>
                                <small>''' + block['transaction']['User_email'] + '''</small>
                            </div>
                        </div>
                    </td>
                    <td>''' + block['transaction']['Energy_Delivered'] + '''</td>
                    <td>''' + block['transaction']['Transaction_date'] + '''</td>
                    <td>''' + block['transaction']['charging_fees'] + ''' dt</td>
                    <td>
                        <span class="paid">Valid</span>
                    </td>
                </tr>
                '''

        return HttpResponse(innerHTML)
    else:
        innerHTML = ''
        for block in BT.chain:
            if block['transaction']['Charger_email'] == request.user.email and inside_div in block['transaction']['User_username']:
                innerHTML += '''
                <tr>
                    <td>'''+ str(block['transaction']['User_ID']) +'''</td>
                    <td>
                        <div class="client">
                            <img class="client-img bg-img" src="'''+  block['transaction']['UserImageUrl']  + '''" alt="">
                            <div class="client-info">
                                <h4>'''+ block['transaction']['User_username'] + '''</h4>
                                <small>''' + block['transaction']['User_email'] + '''</small>
                            </div>
                        </div>
                    </td>
                    <td>''' + block['transaction']['Energy_Delivered'] + '''</td>
                    <td>''' + block['transaction']['Transaction_date'] + '''</td>
                    <td>''' + block['transaction']['charging_fees'] + ''' dt</td>
                    <td>
                        <span class="paid">Valid</span>
                    </td>
                </tr>
                '''
            
        return HttpResponse(innerHTML)