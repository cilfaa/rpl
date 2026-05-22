from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator 

from .models import *
from .serializers import *

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings
from django.db.models import Prefetch, F, Q
import random

from django.http import JsonResponse

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password


def halaman_daftar(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        if password != confirm_password:
            messages.error(request, 'Password tidak sama')
            return redirect('mealplan:daftar')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah digunakan')
            return redirect('mealplan:daftar')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email sudah digunakan')
            return redirect('mealplan:daftar')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.is_active = False
        user.save()

        Pengguna.objects.create(
            user=user,
            meal_plan=None
        )

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        domain = get_current_site(request).domain
        link = f"http://{domain}{reverse('mealplan:aktivasi', kwargs={'uidb64': uid, 'token': token})}"

        subject = 'Konfirmasi Pendaftaran MealPlan'
        message = f"""
        Halo {username},

        Terima kasih sudah mendaftar di MealPlan.

        Klik link berikut untuk mengaktifkan akun Anda (berlaku 1x24 jam):

        {link}

        Jika Anda tidak merasa mendaftar, abaikan email ini.
        """
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        messages.success(
            request,
            'Pendaftaran berhasil. Silakan cek email untuk aktivasi akun.'
        )
        return redirect('mealplan:masuk')
    return render(request, 'daftar.html')

def aktivasi_akun(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Akun berhasil diaktifkan. Silakan login.')
        return redirect('mealplan:masuk')
    else:
        messages.error(request, 'Link aktivasi tidak valid atau sudah kadaluarsa.')
        return redirect('mealplan:daftar')


def halaman_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Username tidak ditemukan')
            return redirect('mealplan:masuk')

        if not user_obj.is_active:
            messages.error(request, 'Akun belum diaktivasi. Silakan cek email Anda.')
            return redirect('mealplan:masuk')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login berhasil')
            return redirect('mealplan:home')
        else:
            messages.error(request, 'Password salah')
            return redirect('mealplan:masuk')
    return render(request, 'login.html')

@api_view(["GET"])
@permission_classes([AllowAny])
def nutrisi_menu_view(request, menu_id):
    try:
        nutrisi = Nutrisi.objects.select_related("menu").get(menu_id=menu_id)
    except Nutrisi.DoesNotExist:
        return Response(
            {
                "detail": "Nutrisi untuk menu ini belum tersedia"
            },
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = NutrisiSerializer(nutrisi)
    return Response(serializer.data, status=status.HTTP_200_OK)


def home(request):
    menu_utama = NamaMenu.objects.filter(utama=True).select_related("nutrisi").first()
    recommended_menus = None
    meal_plan = None
    meal_history = None

    if request.user.is_authenticated:
        pengguna = Pengguna.objects.filter(user=request.user).first()

        if pengguna and pengguna.meal_plan in ["diet", "bulking"]:
            meal_plan = pengguna.meal_plan
            recommended_menus = NamaMenu.objects.filter(kategori__nama_kategori__iexact=meal_plan).select_related("nutrisi").distinct()[:2]

        if not recommended_menus:
            all_ids = list(NamaMenu.objects.values_list("id", flat=True))
            random_ids = random.sample(all_ids, min(2, len(all_ids)))
            recommended_menus = NamaMenu.objects.filter(id__in=random_ids).select_related("nutrisi")

        loved_menus = NamaMenu.objects.filter(diloved_oleh=request.user).select_related("nutrisi")

        if loved_menus.count() >= 2:
            meal_history = loved_menus
        else:
            loved_ids = list(loved_menus.values_list("id", flat=True))
            remaining_ids = list(NamaMenu.objects.exclude(id__in=loved_ids).values_list("id", flat=True))
            random_ids = random.sample(remaining_ids, min(2 - len(loved_ids), len(remaining_ids)))
            random_menus = NamaMenu.objects.filter(id__in=random_ids).select_related("nutrisi")
            meal_history = list(loved_menus) + list(random_menus)

    context = {
        "menu_utama": menu_utama,
        "recommended_menus": recommended_menus,
        "meal_plan": meal_plan,
        "meal_history": meal_history
    }
    return render(request, "home.html", context)



@login_required
def dashboard(request):
    pengguna = Pengguna.objects.filter(user=request.user).first()
    current_plan = pengguna.meal_plan if pengguna else None
    context = {
        'current_plan': current_plan
    }
    return render(request, 'halaman/dashboard.html', context)

def halaman_logout(request):
    logout(request)
    messages.success(request, 'Anda berhasil logout')
    return redirect('mealplan:masuk')

@login_required
def ganti_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        if not check_password(current_password, user.password):
            messages.error(request, 'Password sekarang salah')
            return redirect('mealplan:dashboard')

        if new_password != confirm_password:
            messages.error(request, 'Password baru tidak sama')
            return redirect('mealplan:dashboard')

        user.set_password(new_password)
        user.save()

        # Supaya tidak logout setelah ganti password
        update_session_auth_hash(request, user)

        messages.success(request, 'Password berhasil diperbarui')
        return redirect('mealplan:dashboard')
    return redirect('mealplan:dashboard')


@login_required
def meal_plan(request):
    bmi = None
    kategori = None
    rekomendasi = None

    pengguna = Pengguna.objects.filter(user=request.user).first()
    current_plan = pengguna.meal_plan if pengguna else None

    if request.method == 'POST':

        if request.POST.get('selected_plan'):
            selected_plan = request.POST.get('selected_plan')

            if not pengguna:
                pengguna = Pengguna.objects.create(user=request.user)

            pengguna.meal_plan = selected_plan
            pengguna.save()

            messages.success(request, 'Meal plan berhasil diperbarui')
            return redirect('mealplan:meal-plan')

        try:
            tinggi = float(request.POST.get('tinggi'))
            berat = float(request.POST.get('berat'))

            tinggi_meter = tinggi / 100
            bmi = berat / (tinggi_meter ** 2)

            if bmi < 18.5:
                kategori = "Underweight"
                rekomendasi = "Bulking"
            elif 18.5 <= bmi < 25:
                kategori = "Normal"
                rekomendasi = "Pertahankan berat badan"
            else:
                kategori = "Overweight"
                rekomendasi = "Diet"

        except (TypeError, ValueError):
            messages.error(request, 'Input tidak valid')

    context = {
        'bmi': round(bmi, 2) if bmi else None,
        'kategori': kategori,
        'rekomendasi': rekomendasi,
        'current_plan': current_plan
    }
    return render(request, 'halaman/plan.html', context)

@login_required
def halaman_loved(request):
    loved_menus = request.user.menus_dilove.all().order_by('-created_at')
    context = {
        'loved_menus': loved_menus
    }
    return render(request, 'halaman/loved.html', context)

@login_required
def toggle_love(request, id):
    menu = NamaMenu.objects.filter(id=id).first()

    if not menu:
        return JsonResponse({"status": "error"})

    if request.user in menu.diloved_oleh.all():
        menu.diloved_oleh.remove(request.user)
        loved = False
    else:
        menu.diloved_oleh.add(request.user)
        loved = True
    return JsonResponse({"status": "ok", "loved": loved})

@login_required
def batal_loved(request, id):
    menu = NamaMenu.objects.filter(id=id).first()

    if not menu:
        return JsonResponse({"status": "error"}, status=404)

    menu.diloved_oleh.remove(request.user)
    return JsonResponse({ "status": "ok", "message": "removed"})


def detail_resep(request, id):
    menu = NamaMenu.objects.filter(id=id).select_related("posted_by", "nutrisi").prefetch_related("bahan__master_nutrisi", "cara_masak", "kategori").first()

    if not menu:
        return render(request, "halaman/detail-resep.html")

    NamaMenu.objects.filter(id=id).update(dibaca=F("dibaca") + 1)
    menu.refresh_from_db()

    pengguna = None
    recommended = None

    if request.user.is_authenticated:
        pengguna = Pengguna.objects.filter(user=request.user).first()

        if pengguna and pengguna.meal_plan:
            recommended = NamaMenu.objects.filter(
                kategori__nama_kategori__iexact=pengguna.meal_plan
            ).exclude(id=menu.id).distinct()[:5]

    context = {
        "menu": menu,
        "recommended": recommended
    }
    return render(request, "halaman/detail-resep.html", context)



def search(request):
    query = request.GET.get("q", "").strip()

    results = NamaMenu.objects.none()

    if query:
        results = NamaMenu.objects.select_related("nutrisi").filter(
                Q(nama_menu__icontains=query) |
                Q(nutrisi__kalori__icontains=query) |
                Q(nutrisi__protein__icontains=query)
            ).distinct()

    context = {
        "results": results,
        "search_query": query
    }
    return render(request, 'halaman/search.html', context)


def lihat_semua(request):
    meal_plan = None
    menus = NamaMenu.objects.select_related("nutrisi").prefetch_related("kategori").order_by("-created_at")
    
    if request.user.is_authenticated:
        pengguna = Pengguna.objects.filter(user=request.user).first()
        if pengguna and pengguna.meal_plan:
            meal_plan = pengguna.meal_plan
            menus = menus.filter(
                kategori__nama_kategori__iexact=meal_plan
            ).distinct()

    paginator = Paginator(menus, 6) 

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        data = []
        for menu in page_obj:
            data.append({
                "id": menu.id,
                "nama_menu": menu.nama_menu,
                "gambar": menu.gambar_menu.url if menu.gambar_menu else "",
                "kalori": menu.nutrisi.kalori if hasattr(menu, "nutrisi") else "",
                "waktu": menu.lama_perkiraan_masak
            })
        return JsonResponse({
            "menus": data,
            "has_next": page_obj.has_next()
        })

    context = {
        "recommended_menus": page_obj,
        "meal_plan": meal_plan
    }
    return render(request, "halaman/lihat-semua.html", context)