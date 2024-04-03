from django.contrib import admin
from django.urls import path,include
from accounts.views import *
from doctor.views import *

from django.conf.urls.static import static 
from django.conf import settings 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('',home,name='home'),
    # path('pat/',pathome,name='pathome'),

    path('register-doc/',registration_doc,name='Register'),
    path('patient/register/',registration_pat,name='Register'),

    path('login/',loginpage,name="login"),
    path('logout/',logout_page,name="Logout"),

    path('patient/', include('patient.urls'),),
    path('doctor/', include('doctor.urls'),),



    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
