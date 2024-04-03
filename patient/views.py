from django.shortcuts import render,redirect
from doctor.models import *
from .models import *
from datetime import datetime
from django.contrib.auth.decorators import login_required
from accounts.models import *
from django.contrib import messages
from django.db.models import Subquery
# from patient.models import *
# from accounts.models import *

# from accounts.models import *



def pathome(request):
    return render(request,'patient/index.html')

def doctors(request):
    doctors=Doctor.objects.all()
    context={
        'doctor':doctors
    }
    return render(request,'patient/doctors.html',context)

@login_required(login_url='/login/')
def myaccount(request):
    current_user=request.user
    id=current_user.id
    patient= Patient.objects.get(user_id=id)
    address=Address.objects.get(id=patient.patient_addr_id)
    appt=appointment.objects.filter(patient_id_id=id)
    context={'cuser':current_user,
    'patient':patient,
    'address':address,
    'appointment':appt,
    }
    print(patient.profile_img)
    return render(request,'patient/myaccount.html',context)


def aboutus(request):
    return render(request,'patient/aboutus.html')

def contactus(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')

        user=CustomUser.objects.filter(email=email)
        if not user.exists():
            messages.error(request,"Register yourself first....")
            return redirect('/patient/register/')
        contact=contact_us.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        contact.save()
        return redirect('/patient/')
    return render(request,'patient/contactus.html')

def appointmentt(request,id):

    if request.method == "POST":
        doc = Doctor.objects.get(user_id = id) # doctors id
        patid = request.user.id
        # print(patid)
        pat = Patient.objects.get(user_id = patid) # patient details

        data = request.POST
        patient_name = data.get('patient_names')
        date = data.get('selectedDate')
        print(date)
        note = data.get('illness')

        app = appointment.objects.create(
            patient_id = pat,
            doctor_id = doc,
            patient_name=patient_name,
            # datetime = date,
            note = note,
            appointment_state = 'pending'
            
        )
        app.save()

        appid = app.id
        context = {'appid' : appid}
        request.session['appid'] = appid


        return redirect('/patient/appointment/'+id+'/'+date , context)#+'/'+appid+'/'

    return render(request,'patient/appointment.html')

def apptime(request,id,date):#,appid
    appid = request.session.get('appid')
    if request.method == 'POST':
        app = appointment.objects.get(id = appid)
        t= request.POST.get('timeslots')
        # timingobj = timeslot.objects.filter(starttime = t , slot_date = date)
        # print(timingobj)
        datein = datetime.strptime(date, '%Y-%m-%d').date()
        time = datetime.strptime(t, '%H:%M').time()
        timeslot.objects.filter(slot_date=datein, starttime=time).update(is_available='booked')
        date_time = datetime.combine(datein,time) 
        app.datetime = date_time
        app.save()
        return redirect('/patient/')

    slotsett = timeslot.objects.filter(doctor_id_id = id , slot_date = date)
    context = {'page':'time slots','slots' : slotsett}
    return render(request,'patient/timeselect.html',context)


@login_required(login_url='/login/')
def settings(request):
    cuser=request.user
    patient=Patient.objects.get(user_id=cuser.id)
    address=Address.objects.get(id=patient.patient_addr_id)
    if request.method=="POST":
        cuser.first_name= request.POST.get('first_name')
        cuser.last_name= request.POST.get('last_name')
        cuser.phone_number= request.POST.get('phone_number')
        address.street= request.POST.get('street')
        address.city= request.POST.get('city')
        address.state= request.POST.get('state')
        if  request.POST.get("dob"):
            patient.date_of_birth = request.POST.get("dob")
        patient.blood_group = request.POST.get('blood_group')
        if request.FILES.get('profile'):
            patient.profile_img=request.FILES.get('profile')
        cuser.save()
        address.save()
        patient.save()
        return redirect('/patient/myaccount/')
    context={
        'user':cuser,
        'patient':patient,
        'address':address
        }
    return render(request,'patient/settings.html',context)

@login_required(login_url='/login/')
def patient_notifications(request):
    cuser=request.user
    if request.method=="POST":
        notification=Notifications.objects.filter(user_id=cuser.id)
        notification.delete()
    patient=Patient.objects.get(user_id=cuser.id)
    address=Address.objects.get(id=patient.patient_addr_id)
    notification=Notifications.objects.filter(user_id=cuser.id)
    context={
        'user':cuser,
        'patient':patient,
        'address':address,
        'notification':notification,
        }
    return render(request,'patient/patient_notifications.html',context)

@login_required(login_url='/login/')
def change_password(request):
    cuser=request.user
    patient=Patient.objects.get(user_id=cuser.id)
    address=Address.objects.get(id=patient.patient_addr_id)
    update_user=CustomUser.objects.get(id=cuser.id)
    if request.method=="POST":
        old_pass = request.POST.get('old_password')
        new_password=request.POST.get('new_password')
        new_password_confirm=request.POST.get('new_password_confirm')
        if not update_user.check_password(old_pass):
            messages.error(request,"Enter correct password")
            return redirect('/patient/patient-change-password/')
        
        if (new_password != new_password_confirm):
            messages.error(request,"Password doesnot match")
            return redirect('/patient/patient-change-password/')
        
        update_user.set_password(new_password)
        update_user.save()
        return redirect('/patient/myaccount/')

    context={
        'user':cuser,
        'patient':patient,
        'address':address
        }
    return render(request,'patient/change_password.html',context)

def search(request):
    if request.method=="POST":
        input=request.POST.get('input')

        # doc_fname=Doctor.objects.filter()
        # doc_lname=Doctor.objects.filter(last_name__icontains=input)
        doc_quali=Doctor.objects.filter(qualification__icontains=input)
        doc_speciality=Doctor.objects.filter(specialization__icontains=input)

        # if  not len(doc_fname)==0:
        #     doctors= doctors.union(doc_fname)
        # if  not len(doc_lname)==0:
        #     doctors=doctors.union(doc_lname)
        if  not len(doc_quali)==0:
            doctors=doctors.union(doc_quali)
        if  not len(doc_speciality)==0:
            doctors=doctors.union(doc_speciality)

        context={'doc':doctors}

        return render(request,"patient/search_doctor.html",context)

@login_required(login_url='/login/')
def delete_account(request):
    cuser=request.user
    patient=Patient.objects.get(user_id=cuser.id)
    address=Address.objects.get(id=patient.patient_addr_id)
    context={
        'user':cuser,
        'patient':patient,
        'address':address
        }
    return render(request,"patient/delete_account.html",context)

@login_required(login_url='/login/')
def bills(request):
    current_user=request.user
    patient=Patient.objects.get(user_id=current_user.id)
    address=Address.objects.get(id=patient.patient_addr_id)
    appt=appointment.objects.filter(patient_id_id=current_user.id).only('id').all()
    bills=bill.objects.filter(appointment_id_id__in=Subquery(appt))
    context={
        'user':current_user,
        'patient':patient,
        'address':address,
        'bill':bills,
        }
    
    return render(request,"patient/bills.html",context)

@login_required(login_url='/login/')
def pat_prescription(request):
    current_user=request.user
    patient=Patient.objects.get(user_id=current_user.id)
    address=Address.objects.get(id=patient.patient_addr_id)
    appt=appointment.objects.filter(patient_id_id=current_user.id).only('id').all()
    presc=prescription.objects.filter(appointment_id_id__in=Subquery(appt))
    context={
        'user':current_user,
        'patient':patient,
        'address':address,
        'presc':presc,
        }
    return render(request,"patient/prescription.html",context)

def doc_details(request,id):
    doctor=Doctor.objects.get(user_id=id)
    context={'doc':doctor}
    return render(request,"patient/doc_details.html",context)

@login_required(login_url='/login/')
def view_prescription(request,id):
    current_user=request.user
    patient=Patient.objects.get(user_id=current_user.id)
    address=Address.objects.get(id=patient.patient_addr_id)
    presc=prescription.objects.get(id=id)
    medicines=prescribedMedicine.objects.filter(prescription_id=presc.id)
    context={'user':current_user,
        'patient':patient,
        'address':address,"presc":presc,
        'med':medicines}
    return render(request,"patient/view_prescription.html",context)

@login_required(login_url='/login/')
def view_bill(request,id):
    current_user=request.user
    patient=Patient.objects.get(user_id=current_user.id)
    address=Address.objects.get(id=patient.patient_addr_id)
    bills=bill.objects.get(id=id)
    context={'user':current_user,
        'patient':patient,
        'address':address,"bill":bills}
    return render(request,"patient/view_bill.html",context)