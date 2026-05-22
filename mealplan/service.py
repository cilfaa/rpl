class Bahan:
    def __init__(self, nama_bahan, kalori, protein, lemak, serat):
        self.nama_bahan = nama_bahan
        self.kalori = float(kalori)
        self.protein = float(protein)
        self.lemak = float(lemak)
        self.serat = float(serat)


class PemakaianBahan:
    def __init__(self, bahan, faktor):
        self.bahan = bahan
        self.faktor = float(faktor)

    def cek_nutrisi(self):
        return {
            "kalori": self.bahan.kalori * self.faktor,
            "protein": self.bahan.protein * self.faktor,
            "lemak": self.bahan.lemak * self.faktor,
            "serat": self.bahan.serat * self.faktor,  # ditambahkan
        }


class Resep:
    def __init__(self, nama_resep, porsi):
        self.nama_resep = nama_resep
        self.porsi = int(porsi)
        self.pemakaian_bahan = []

    def tambah_bahan(self, pemakaian_bahan):
        self.pemakaian_bahan.append(pemakaian_bahan)

    def total_nutrisi(self):
        total = {
            "kalori": 0.0,
            "protein": 0.0,
            "lemak": 0.0,
            "serat": 0.0,  # ditambahkan
        }

        for pb in self.pemakaian_bahan:
            nutrisi = pb.cek_nutrisi()
            for k in total:
                total[k] += nutrisi[k]

        return total

    def nutrisi_per_porsi(self):
        total = self.total_nutrisi()
        return {k: v / self.porsi for k, v in total.items()}