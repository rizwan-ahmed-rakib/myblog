from django.urls import path
from login_app import views

app_name='Login_App'
urlpatterns=[
   path('signup/',views.sign_up,name='signup'),
   path('login/',views.login_page,name='login'),
   path('logout/',views.logout_user,name='logout'),
   path('profile/',views.profile,name='profile'),
   path('change-profile/',views.profile_change,name='change_profile'),
   path('password/', views.password_change, name='change_password'),
   path('add-profile-picture/', views.add_profile_pic, name='add_profile_pic'),
   path('change-profile-picture/', views.change_profile_pic, name='change_profile_pic'),
   path('user/<str:username>/', views.user_profile, name='user_profile'),

]