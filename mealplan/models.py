from django.db import models, transaction
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils.text import slugify

class Pengguna(models.Model):

    PLAN_CHOICES = (
        ('diet', 'Diet'),
        ('bulking', 'Bulking'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    meal_plan = models.CharField(max_length=20, choices=PLAN_CHOICES, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Pengguna'

    def __str__(self):
        return self.user.username

class MasterNutrisiBahan(models.Model):
    nama_bahan = models.CharField(max_length=200, unique=True)

    berat_persajian = models.FloatField(
        help_text="contoh: 100 (gr/ml) atau 1 (butir)"
    )

    satuan = models.CharField(
        max_length=20,
        help_text="gr / ml / butir"
    )

    kalori = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    serat = models.FloatField(default=0) 
    lemak = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = 'Master Nutrisi Bahan'

    def __str__(self):
        return f"{self.nama_bahan} ({self.berat_persajian}{self.satuan})"

class KategoriMenu(models.Model):
    nama_kategori = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Kategori Menu"

    def __str__(self):
        return self.nama_kategori        

class NamaMenu(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="menu_dibuat")
    gambar_menu = models.ImageField(upload_to='gambar/', null=True, blank=True)
    nama_menu = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True) 
    dibaca = models.PositiveIntegerField(default=0)
    lama_perkiraan_masak = models.IntegerField(default=0)
    utama = models.BooleanField(default=False)

    kategori = models.ManyToManyField(KategoriMenu, related_name="menus", blank=True)
    diloved_oleh = models.ManyToManyField(User, blank=True, related_name="menus_dilove") #supaya User bisa ngeliked banyak menu

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nama_menu)
            slug = base_slug
            counter = 1
            while NamaMenu.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        with transaction.atomic():
            super().save(*args, **kwargs) 

            if self.utama:
                NamaMenu.objects.filter(utama=True).exclude(id=self.id).update(utama=False)

    def total_disimpan(self):
        return self.diloved_oleh.count()

    def hitung_nutrisi(self):
        total_kalori = Decimal("0")
        total_protein = Decimal("0")
        total_serat = Decimal("0")

        for b in self.bahan.all():
            if not b.master_nutrisi:
                continue

            faktor = Decimal(str(b.faktor()))

            total_kalori += Decimal(str(b.master_nutrisi.kalori)) * faktor
            total_protein += Decimal(str(b.master_nutrisi.protein)) * faktor
            total_serat += Decimal(str(b.master_nutrisi.serat)) * faktor

        total_lemak = total_kalori / Decimal("9")

        return {
            "kalori": total_kalori,
            "protein": total_protein,
            "lemak": total_lemak,
            "serat": total_serat,
        }

    class Meta:
        verbose_name_plural = 'Nama Menu'

    def __str__(self):
        return self.nama_menu

class Nutrisi(models.Model):
    menu = models.OneToOneField(NamaMenu, on_delete=models.CASCADE, related_name="nutrisi")
    protein = models.DecimalField(max_digits=6, decimal_places=2)
    lemak = models.DecimalField(max_digits=6, decimal_places=2)
    kalori = models.DecimalField(max_digits=8, decimal_places=2)
    serat = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural = 'Nutrisi'

    def __str__(self):
        return f"Nutrisi {self.menu.nama_menu}"


class Bahan(models.Model):
    menu = models.ForeignKey(NamaMenu, on_delete=models.CASCADE, related_name="bahan")

    jumlah = models.FloatField()
    satuan = models.CharField(max_length=50)

    master_nutrisi = models.ForeignKey(MasterNutrisiBahan, on_delete=models.SET_NULL, null=True,
        blank=True,
        related_name="dipakai_di"
    )

    class Meta:
        verbose_name_plural = 'Bahan'

    def faktor(self):
        if not self.master_nutrisi:
            return 0
        return self.jumlah / self.master_nutrisi.berat_persajian

    def __str__(self):
        return f"{self.master_nutrisi.nama_bahan} - {self.menu.nama_menu}"


class CaraMasak(models.Model):
    menu = models.ForeignKey(NamaMenu, on_delete=models.CASCADE, related_name="cara_masak")
    urutan = models.PositiveIntegerField()
    deskripsi = models.TextField()

    class Meta:
        verbose_name_plural = 'Cara Memasak'
        ordering = ["urutan"]

    def __str__(self):
        return f"Step {self.urutan} - {self.menu.nama_menu}"