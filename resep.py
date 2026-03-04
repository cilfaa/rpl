class Bahan:
	def __init__(self, nama_bahan, kalori, protein, lemak, serat):
		self.nama_bahan = nama_bahan
		self.kalori = kalori 
		self.protein = protein 
		self.lemak = lemak 
		self.serat = serat
		
class PemakaianBahan:
	def __init__(self, bahanmasak, hitungan):
		# 1.0 = 100g, 0.5 = 50g
		self.bahanmasak = bahanmasak
		self.hitungan = hitungan 
		
	def cek_nutrisi(self):
		return{
			"kalori": self.bahanmasak.kalori * self.hitungan,
			"protein": self.bahanmasak.protein * self.hitungan,
			"lemak": self.bahanmasak.lemak * self.hitungan,
			"serat": self.bahanmasak.serat * self.hitungan,
		}
		
class Resep:
	def __init__(self, namaresep, persajian):
		self.namaresep = namaresep
		self.persajian = persajian 
		self.bahanbahan = []
		
	def cek_bahan(self, pemakaianbahan):
		self.bahanbahan.append(pemakaianbahan)
		
	def total_nutrisi(self):
		total = {"kalori":0, "protein":0 , "lemak": 0, "serat":0}
		
		for x in self.bahanbahan:
			nutrisi = x.cek_nutrisi()
			for y in total:
				total[y] += nutrisi[y]
				
		return total 
		
	def nutrisi_per_sajian(self):
		total = self.total_nutrisi()
		return {x: y / self.persajian for x, y in total.items()}
		
	def isian(self):
		per_sajian = self.nutrisi_per_sajian()
		print(f"Resep : {self.namaresep}")
		print(f"Porsi : {self.persajian}")
		print("Nutrisi per porsi : ")
		print(f"Kalori : {per_sajian['kalori']:.1f} kcal")
		print(f"Protein : {per_sajian['protein']:.1f} g")
		print(f"Lemak : {per_sajian['lemak']:.1f} g")
		print(f"Serat : {per_sajian['serat']:.1f} g")
		

kentang = Bahan(
	nama_bahan="Kentang",
	kalori=36,
	protein=20,
	lemak=3.6,
	serat=6,
)		
		
dada_ayam = Bahan(
	nama_bahan="Dada ayam",
	kalori=165,
	protein=18,
	lemak=3.6,
	serat=0,
)

perkedel = Resep("Perkedel kentang ayam", persajian=5)
perkedel.cek_bahan(PemakaianBahan(kentang, 5.0)) # untuk 500g
perkedel.cek_bahan(PemakaianBahan(dada_ayam, 1.0)) #untuk 100g

perkedel.isian()