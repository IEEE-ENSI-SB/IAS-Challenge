from django.urls import path
from . import views
urlpatterns = [
    path('Login/', views.Login, name= 'login'),
    path('Register/', views.Register, name= 'register'),
    path('Dashboard/', views.Dashboard_User, name= 'Dashboard'),
    path('Get_access/', views.Get_access, name='access'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.Home, name='Home'),

]

htmx_urlpatterns = [
    path('search_User_transactions/',views.search_User_transactions),
    path('search_Charger_transactions/',views.search_Charger_transactions),
]

urlpatterns += htmx_urlpatterns