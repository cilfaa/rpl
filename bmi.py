tinggi = float(input('masukkan tinggi badan (cm) : '))
berat = float(input('masukkan berat badan (kg) : '))

tinggibadan = tinggi / 100
bmi = berat / (tinggibadan**2)

if bmi < 18.5:
	kategori = "Underweight"
	rekomendasi = "Makan yang banyak cooy"
	
elif 18.5 <= bmi < 25:
	kategori = "Normal"
	rekomendasi = "udah jangan banyak makan seblak"
	
elif 25 <= bmi < 30:
	kategori = "Pre-obesitas"
	rekomendasi = "Diet gih..."
else:
	kategori = "Obesitas banget cuuy..."
	rekomendasi = "Diet ketat pake meal plan MbGrey..."
	
print("Hasil bmi")
print("BMI : ", round(bmi, 2))
print("Kategori : ", kategori)
print("Rekomendasi : ", rekomendasi)
