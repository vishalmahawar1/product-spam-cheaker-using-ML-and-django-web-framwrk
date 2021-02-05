from django.urls import path

                               
from django.contrib.auth import views as auth_views
from .import views

app_name = 'spm_ck'

urlpatterns=[
    
    path('', views.product_list, name='product_list'),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),  
    path('logout/', views.logoutUser, name="logout"),
    path('<int:id>/create_order/', views.createOrder, name="create_order"),
    path('velidate1/' ,views.velidate ,name="velidate1"),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="spm_ck/password_reset.html"), name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="spm_ck/password_reset_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="spm_ck/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="spm_ck/password_reset_done.html"),name="password_reset_complete"),

   
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail,name='product_detail'),

    

]
