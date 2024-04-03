from django.shortcuts import render,redirect
from .models import *
from accounts.models import *
from django.contrib.auth.models import User
from django.contrib import messages
from  django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

# Create your views here.

@login_required(login_url='/login/')
def DOChome(request):
    context = {'page':'Home'}
    return render(request, 'doctor/dochome.html',context)

@login_required(login_url='/login/')
def history(request):
    disp = appointment.objects.filter(appointment_state = 'complete' , doctor_id_id = request.user.id)

    context = {'page':'History' , 'disp':disp}
    return render(request, 'doctor/history.html',context)

@login_required(login_url='/login/')
def viewprescription(request,id):
    appoint = appointment.objects.get(id = id)
    pres = prescription.objects.get(appointment_id_id = id)
    presmed = prescribedMedicine.objects.filter(prescription_id_id = pres.id)
    context = {'page':'view prescription','disp':appoint,'pres':pres,'presmed':presmed}
    return render(request, 'doctor/prescriptionview.html',context)

@login_required(login_url='/login/')
def viewbill(request,id):
    appoint = appointment.objects.get(id = id)
    billl = bill.objects.get(appointment_id_id = id)
    billmeds = billmed.objects.filter(bill_id_id = billl.id)
    context = {'page':'view bill','disp':appoint,'billob':billl,'billmedob':billmeds}
    return render(request, 'doctor/billview.html',context)


@login_required(login_url='/login/')
def genbill(request,id):
    if prescription.objects.filter(appointment_id_id=id).exists():
        print('ok')
    else:
        return redirect('/doctor/appointments')
    
    pres = prescription.objects.get(appointment_id_id=id)
    presmed = prescribedMedicine.objects.filter(prescription_id_id=pres.id)

    if request.method == 'POST':
        data = request.POST 
        date = data.get('date')
        med_name = data.getlist('med_name')
        qty = data.getlist('qty')
        rate = data.getlist('rate')
        # price = data.getlist('price')
        discount = data.get('discount')
        amount =0
        price = [0]*len(med_name)
        for i in range(len(med_name)):
            price[i] = float(qty[i]) * float(rate[i])
            amount +=price[i]

        discountamt = (float(discount)/100)*amount
        final_price = amount - discountamt
        print(final_price)
        appoint = appointment.objects.get(id = id)
        billcreate = bill.objects.create(
            appointment_id = appoint,
            date = date,
            final_amount = final_price
        )
        billcreate.save()
        for i in range(len(med_name)):
            if medicine.objects.filter(medicine_name = med_name[i]).exists():
                priceup = medicine.objects.get(medicine_name = med_name[i])
                priceup.price = rate[i]
                priceup.save()
            else:
                newmed = medicine.objects.create(
                    medicine_name = med_name[i],
                    price = rate[i]
                )
                newmed.save()

        for i in range(len(med_name)):
            billmedicines = billmed.objects.create(
                bill_id = billcreate,
                medicine_id = medicine.objects.get(medicine_name = med_name[i])
            )
            billmedicines.save()


    if bill.objects.filter(appointment_id_id = id).exists():
        context = {'page':'View Bill' ,}
        return render(request, 'doctor/billupdate.html',context)
    
    context = {'page':'Generate Bill' , 'pres':pres,'presmed':presmed}
    return render(request, 'doctor/bill.html',context)


@login_required(login_url='/login/')
def genpres(request,id):
    queryset = appointment.objects.get(id = id)

    if request.method == 'POST':
        data = request.POST
        age = data.get('age')
        gender = data.get('gender')  
        date = data.get('date')
        duration = data.get('duration')    
        med_name = data.getlist('med_name')
        dose = data.getlist('dose')
        qty = data.getlist('qty')

        presc = prescription.objects.create(
            appointment_id = queryset,
            date = date,
            age = age,
            gender = gender,
            duration = duration
        )
        presc.save()

        no_of_med = len(med_name)
        for i in range(no_of_med):
            if not medicine.objects.filter(medicine_name = med_name[i]).exists():
                medi = medicine.objects.create(
                    medicine_name = med_name[i]
                )
                medi.save()

            
        for i in range(no_of_med):
            presmed = prescribedMedicine.objects.create(
                prescription_id = presc,
                medicine_id = medicine.objects.get(medicine_name = med_name[i]),
                dosage = dose[i],
                quantity = qty[i]
            )
            presmed.save()

    if prescription.objects.filter(appointment_id_id = id).exists():
        context = {'page':'view Prescription' , 'data' : queryset}
        return render(request, 'doctor/prescriptionupdate.html',context)

    context = {'page':'Prescription' , 'data' : queryset}
    return render(request, 'doctor/prescription.html',context)

@login_required(login_url='/login/')
def app_complete(request , id):
    q = appointment.objects.get(id = id)
    q.appointment_state = 'complete'
    q.save()
    return redirect('/doctor/appointments/')



@login_required(login_url='/login/')
def receivedreq(request):
    queryset = appointment.objects.filter(appointment_state = 'pending' , doctor_id_id =  request.user.id , datetime__isnull = False)
    
    if request.method == 'POST':
        qupdate = appointment.objects.get(id = request.POST.get('reasonid'))
        qupdate.rejection_reason = request.POST.get('reason')
        qupdate.appointment_state = 'Rejected'
        qupdate.save()
        
        # send mail to the user with rejection reason




    context = {'page':'Received Requests' , 'disp' : queryset}
    return render(request, 'doctor/requests.html',context)

@login_required(login_url='/login/')
def requpdate(request , id):
    queryset = appointment.objects.get(id = id)
    queryset.appointment_state = 'Accepted'
    queryset.save()
    return redirect('/doctor/received-request/')

@login_required(login_url='/login/')
def docschedule(request):
    docid = request.user.id
    slotset = timeslot.objects.filter(doctor_id_id = docid , slot_date = date.today())
    context = {'page':'Schedule','slots' : slotset}
    return render(request, 'doctor/schedule.html',context)

@login_required(login_url='/login/')
def generateslot(request):
    docid = request.user.id
    docobj = Doctor.objects.get(user_id=docid)
    if request.method == "POST":
        data = request.POST
        datestr = data.get('date')
        starttime_str = data.get('starttime')
        endtime_str=data.get('endtime')
        duration_str = data.get('duration')

        # print(datestr)
        # print(starttime_str)
        # print(endtime_str)
        # print(duration_str)
        date = datetime.strptime(datestr, '%Y-%m-%d').date()
        starttime = datetime.strptime(starttime_str, '%H:%M').time()
        endtime = datetime.strptime(endtime_str, '%H:%M').time()
        duration = int(duration_str)

        if timeslot.objects.filter(slot_date = date , doctor_id_id = docid).exists():
            return redirect('/doctor/viewtimeslot/')
        else:
            time_slots = []
            current_time = datetime.combine(date, starttime)
            end_datetime = datetime.combine(date, endtime)
    
            while current_time <= end_datetime:
                time_slots.append(current_time)
                current_time += timedelta(minutes=duration)
               
            for i in range(len(time_slots)):
                slotobj = timeslot.objects.create(
                    doctor_id_id = docid,
                    slot_date = date,
                    # is_available = True,
                    starttime = time_slots[i].time(),
                )
                slotobj.save()
            return redirect('/doctor/viewtimeslot/')
            
                      

    



    context = {'page':'Generate Slots'}
    return render(request,'doctor/generateslot.html',context)

@login_required(login_url='/login/')
def viewtimeslot(request):
    id = request.user.id
    qset=[]
    if request.method == 'POST':
        seldate = request.POST.get('selecteddate')
        qset = timeslot.objects.filter(slot_date = seldate , doctor_id_id = id)



    uniquedate = date.today()
    print(uniquedate)
    context = {'page':'slot update' , 'slot':qset , 'uniquedate' : uniquedate} 
    return render(request, 'doctor/viewtimeslot.html',context)

@login_required(login_url='/login/')
def updateslot(request,id):
    slotob = timeslot.objects.get(id =id)
    print(slotob)
    if slotob.is_available == 'available':
        slotob.is_available = 'disabled'
    elif slotob.is_available == 'disabled':
        slotob.is_available = 'available'

    slotob.save()
    return redirect('/doctor/viewtimeslot/')

@login_required(login_url='/login/')
def docprof(request):
    id = request.user.id
    queryset = Doctor.objects.get(user_id = id)
    q = CustomUser.objects.get(id = id)
    print(queryset.fees)
    print(q.first_name)

    print(queryset.doctor_addr.street)

    context = {'page':'Your Profile' , 'doc' : queryset , 'cuser' : q}
    return render(request, 'doctor/profile.html',context)


def docprof_update(request,id):
    doc = Doctor.objects.get(user_id = id)
    cuser = CustomUser.objects.get(id = id)
    # adid = doc.doctor_addr
    # print(adid)
    addr = Address.objects.get(id =doc.doctor_addr_id)
    
    if request.method == "POST":
        data = request.POST
        cuser.first_name= data.get('first_name')
        cuser.last_name= data.get('last_name')
        cuser.email= data.get('email')
        cuser.phone_number= data.get('phoneno')
        addr.street= data.get('street')
        addr.city= data.get('city')
        addr.state= data.get('state')
        doc.qualification= data.get('qualification')
        doc.specialization= data.get('specialization')
        doc.certificate_no= data.get('certificate_no')
        doc.fees= request.POST.get('fees')
 
        profile_img=request.FILES.get('profile')

        if profile_img:
            doc.profile_img = profile_img
        
        cuser.save()
        addr.save()
        doc.save()

        return redirect ('/doctor/doctors-profile/')

    context = {'page':'Your Profile' , 'doc' : doc , 'cuser' : cuser , 'addr' : addr}
    return render(request, 'doctor/update_profile.html',context)



def appoint_diplay(request):
    queryset = appointment.objects.filter(appointment_state = 'Accepted' , doctor_id_id =  request.user.id)


    context = {'page':'appointments' ,'disp' : queryset }
    return render(request, 'doctor/appointments.html',context)

