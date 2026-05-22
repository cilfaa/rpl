from decimal import Decimal
from .service import Bahan as ServiceBahan, PemakaianBahan, Resep
from .models import Nutrisi


def hitung_dan_simpan_nutrisi_menu(menu):
    if not menu.bahan.exists():
        Nutrisi.objects.filter(menu=menu).delete()
        return None

    resep = Resep(nama_resep=menu.nama_menu,porsi=1)

    for b in menu.bahan.select_related("master_nutrisi"):
        if not b.master_nutrisi:
            continue

        master = b.master_nutrisi

        if not master.berat_persajian or master.berat_persajian == 0:
            continue

        service_bahan = ServiceBahan(
            nama_bahan=master.nama_bahan,
            kalori=float(master.kalori),
            protein=float(master.protein),
            lemak=float(master.lemak),
            serat=float(master.serat),
        )

        faktor = float(b.jumlah) / float(master.berat_persajian)

        resep.tambah_bahan(
            PemakaianBahan(
                bahan=service_bahan,
                faktor=faktor
            )
        )

    hasil = resep.nutrisi_per_porsi()
    nutrisi, _ = Nutrisi.objects.update_or_create(
        menu=menu,
        defaults={
            "kalori": Decimal(str(hasil.get("kalori", 0))),
            "protein": Decimal(str(hasil.get("protein", 0))),
            "lemak": Decimal(str(hasil.get("lemak", 0))),
            "serat": Decimal(str(hasil.get("serat", 0))),
        }
    )
    return nutrisi