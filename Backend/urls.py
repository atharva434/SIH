import imp
from django.contrib import admin
from django.urls import path
from qrscan import views
from django.urls import path
from django.views.generic import TemplateView
from rest_framework import routers
from django.contrib.auth.views import LogoutView  
from django.conf.urls.static import static
from django.conf import settings
from qrscan import payment
from qrscan import Qrscanner, graphs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('book/', payment.book,name="homepage"),
    path('', views.homepage,name="home"),
    path('Call_Scan/',Qrscanner.Call_Scan, name='Call_Scan'),
    path('scan',Qrscanner.ScanQR, name='scan'),
    path('payment-status', payment.payment_status, name='payment-status'),
    path("login/",views.login_page,name="login"),
    path("logout/",LogoutView.as_view(next_page="react_app"),name="logout"),
    path("Counter/", views.Counter, name="Counter"),
    path("adminpage/", views.Admin, name="AdminPage"),
    path('Ticket/',views.Ticket_display,name='ticket'),
    path('customerscanner/',Qrscanner.customscanner,name='okk'),
    path('display/<monuments>/',views.display,name='display'),
    path("react", views.MyReactView.as_view(), name='react_app'),  
    # this route catches any url below the main one, so the path can be passed to the front end
    path(r'react/<path:path>', views.MyReactView.as_view(), name='react_app_with_path'),
   

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
