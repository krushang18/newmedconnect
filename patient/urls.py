from django.urls import path
from . import views

urlpatterns = [
    path('',views.pathome,name='home'),
    path('doctors/',views.doctors,name='doctors'),
    path('myaccount/',views.myaccount,name='myaccount'),
    path('aboutus/',views.aboutus,name='aboutus'),
    path('contactus/',views.contactus,name='contactus'),
    path('patient-settings/',views.settings,name='settings'),
    path('patient-change-password/',views.change_password,name='change_password'),
    path('patient-notifications/',views.patient_notifications,name='patient_notifications'),
    path('search/',views.search,name='search'),
    path('delete-account/',views.delete_account,name='delete_account'),
    path('bills/',views.bills,name='bills'),
    path('prescription/',views.pat_prescription,name='pat_prescription'),
    path('doc-details/<int:id>',views.doc_details,name='doc_details'),
    path('view-prescription/<int:id>',views.view_prescription,name='view_prescription'),
    path('view-bill/<int:id>',views.view_bill,name='view_bill'),
    
    path('appointment/<id>/',views.appointmentt,name='appointment'),
    path('appointment/<id>/<date>/',views.apptime,name='appointment_time'),

]