from django.urls import path 
from .views import *

app_name = 'mealplan'

urlpatterns = [
    path('', home, name='home'),
    path('api/menu/<int:menu_id>/nutrisi/', nutrisi_menu_view, name='nutrisi-menu'),
    path('masuk/', halaman_login, name='masuk'),
    path('logout/', halaman_logout, name='logout'),
    path('daftar/', halaman_daftar, name='daftar'),
    path('aktivasi/<uidb64>/<token>/', aktivasi_akun, name='aktivasi'),
    path('dashboard/', dashboard, name='dashboard'),
    path('ganti-password/', ganti_password, name='ganti-password'),
    path('meal-plan/', meal_plan, name='meal-plan'),
    path('loved/', halaman_loved, name='loved'),
    path('batal-loved/<int:id>/', batal_loved, name='batal-loved'),
    path('toggle-love/<int:id>/', toggle_love, name='toggle-love'),
    path('detail-resep/<int:id>/', detail_resep, name='detail-resep'),
    path('search/', search, name='search'),
    path('lihat-semua/', lihat_semua, name='lihat-semua'),
]