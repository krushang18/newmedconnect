from django.urls import path
from . import views

urlpatterns = [
    path('doc-home/',views.DOChome,name='home'),

    path('generate-bill/<id>/',views.genbill, name = 'generate-bill'),
    path('history/',views.history, name="work_history"),
    path('generate-precription/<id>/',views.genpres, name="generate_prescription"),
    path('received-request/',views.receivedreq, name="received_requests"),
    path('requestresp/<id>/',views.requpdate, name="request_update"),

    path('schedule/',views.docschedule, name="doctors_schedule"),
    path('generate-slot/',views.generateslot, name="generate_slot"),
    path('viewtimeslot/',views.viewtimeslot, name="view_time"),
    path('updateslot/<id>/',views.updateslot, name="updateslot"),


    path('doctors-profile/',views.docprof, name="doctors_profile"),
    path('doctors-profile-update/<id>/',views.docprof_update, name="doctors_profile"),
    path('completed/<id>/',views.app_complete, name="doctors_profile"),
    path('viewbill/<id>/',views.viewbill, name="viewbill"),
    path('viewprescription/<id>/',views.viewprescription, name="viewprescription"),



    path('appointments/',views.appoint_diplay, name="doctors_profile"),



]