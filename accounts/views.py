from django.shortcuts import render,redirect
from .models import *
# from django.http import HttpResponse
from django.contrib import messages
from  django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def home(request):
    return redirect('/login/')


def loginpage(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not CustomUser.objects.filter(email=email ).exists():
            messages.error(request, "Invalid Email")
            return redirect('/login/')
        
        user = authenticate(email = email , password = password)
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        else:
            if user.type == 'doctor':
                login(request , user)
                return redirect('/doctor/doc-home/')
            else:
                login(request , user)
                return redirect('/patient/')

    context={'page':'login'}
    return render(request, 'login.html',context)




def registration_doc(request):

    if request.method == "POST":
        first_name= request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        email= request.POST.get('email')
        phone_number= request.POST.get('phoneno')
        street= request.POST.get('street')
        city= request.POST.get('city')
        state= request.POST.get('state')
        # addr= street + city + state
        qualification= request.POST.get('qualification')
        specialization= request.POST.get('specialization')
        certificate_no= request.POST.get('certificate_no')
        fees= request.POST.get('fees')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        profile_img=request.FILES.get('profile')



        user = CustomUser.objects.filter(email=email)
        if user.exists():
            messages.error(request, "Username already exists")
            return redirect('/register-doc/')
        if(password != confirm_password):
            messages.error(request,"Password didnot match")
            return redirect('/register-doc/')

        addrcreate = Address.objects.create(
            city = city,
            state = state,
            street = street,
        )
        addrcreate.save()
        # addrq = Address.objects.get(city = city , state=state , street=street)
        # addrid = addrq.id
        user = CustomUser.objects.create(
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone_number = phone_number,
            type = 'doctor'
            
        )
        user.set_password(password)
        user.save()

        doccreate = Doctor.objects.create(
            user_id = user.id,

            doctor_addr_id = addrcreate.id,
            qualification = qualification,
            specialization = specialization,
            certificate_no = certificate_no,
            fees = fees,
            profile_img=profile_img

        )
        doccreate.save()
        messages.success(request, "User registered")

        return redirect('/register-doc/')

    context={'page':'Register Yourself'}
    return render(request, 'register.html',context)


def registration_pat(request):

    if request.method == "POST":
        first_name= request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        email= request.POST.get('email')
        phone_number= request.POST.get('phoneno')
        street= request.POST.get('street')
        city= request.POST.get('city')
        state= request.POST.get('state')
        # addr= street + city + state
        dob = request.POST.get("dob")
        bloodgroup = request.POST.get('bloodgroup')
        profile_img=request.FILES.get('profile')
        confirm_password = request.POST.get('confirm_password')

        password = request.POST.get('password')

        user = CustomUser.objects.filter(email=email)
        if user.exists():
            messages.error(request, "Username already exists")
            return redirect('/patient/register/')
        if(password != confirm_password):
            messages.error(request,"Password did not match")
            return redirect('/patient/register/')

        addrcreate = Address.objects.create(
            city = city,
            state = state,
            street = street,
        )
        addrcreate.save()
        # addrq = Address.objects.get(city = city , state=state , street=street)
        # addrid = addrq.id
        user = CustomUser.objects.create(
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone_number = phone_number,
        )
        user.set_password(password)
        user.save()

        pat_create = Patient.objects.create(
            user_id = user.id,
            date_of_birth = dob,
            blood_group = bloodgroup,
            patient_addr_id = addrcreate.id,
            profile_img=profile_img
        )
        # print('here')
        pat_create.save()
        messages.success(request, "User registered")

        return redirect('/patient/register/')


    context={'page':'Register Yourself'}
    return render(request, 'patregister.html',context)

def logout_page(request):
    logout(request)
    return redirect('/login/')