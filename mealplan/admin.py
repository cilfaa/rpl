from django.contrib import admin
from .models import *

@admin.register(KategoriMenu)
class KategoriMenuAdmin(admin.ModelAdmin):
    list_display = ("nama_kategori", "slug")
    search_fields = ("nama_kategori", "slug")
    prepopulated_fields = {"slug": ("nama_kategori",)}
    ordering = ("nama_kategori",)

@admin.register(MasterNutrisiBahan)
class MasterNutrisiBahanAdmin(admin.ModelAdmin):
    list_display = (
        "nama_bahan",
        "berat_persajian",
        "satuan",
        "kalori",
        "protein",
        "serat",
        "lemak",
    )
    search_fields = ("nama_bahan",)
    list_filter = ("satuan",)
    ordering = ("nama_bahan",)

class BahanInline(admin.TabularInline):
    model = Bahan
    extra = 1
    autocomplete_fields = ("master_nutrisi",)
    fields = (
        "master_nutrisi",
        "jumlah",
        "satuan",
    )


class CaraMasakInline(admin.TabularInline):
    model = CaraMasak
    extra = 1

@admin.register(NamaMenu)
class NamaMenuAdmin(admin.ModelAdmin):
    list_display = (
        "nama_menu",
        "slug",
        "posted_by",
        "utama",
        "created_at",
        "dibaca",
    )

    search_fields = ("nama_menu", "slug",)
    list_filter = ("created_at", "kategori", "utama")
    readonly_fields = ("created_at", "dibaca")
    prepopulated_fields = {"slug": ("nama_menu",)} 
    filter_horizontal = ("kategori",)
    inlines = (BahanInline, CaraMasakInline)

@admin.register(Nutrisi)
class NutrisiAdmin(admin.ModelAdmin):
    list_display = (
        "menu",
        "kalori",
        "protein",
        "lemak",
        "serat",
    )
    readonly_fields = ("menu", "kalori", "protein", "lemak", "serat")

    def has_add_permission(self, request):
        return False

admin.site.register(Bahan)
@admin.register(CaraMasak)
class CaraMasakAdmin(admin.ModelAdmin):
    list_display = ("menu", "urutan")
    search_fields = ("menu__nama_menu",)
    ordering = ("menu", "urutan")