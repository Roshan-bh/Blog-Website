
from django.contrib import admin
from django.urls import path
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
    path('login/',views.user_login,name="login"),
    path('logout/',views.user_logout,name="logout"),
    path('signup/',views.signup,name="signup"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('addpost/',views.add_post,name="addpost"),
    path('edit/<int:id>/',views.edit_post,name="editpost"),
    path('delete/<int:id>/',views.delete_post,name="deletepost"),
]
