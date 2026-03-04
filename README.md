# Meal Plan & Diet Planner

Project ini adalah *aplikasi perencanaan makan dan diet* yang bertujuan membantu pengguna mengatur pola makan harian dengan lebih terstruktur, realistis, dan mudah dipahami.

Aplikasi ini tidak hanya menghitung kalori, tetapi membantu pengguna *merencanakan apa yang dimakan setiap hari*, lengkap dengan resep dan informasi gizi dasar.

---

## Konsep Project

Aplikasi ini membantu pengguna untuk:

- Merencanakan makan harian (sarapan, makan siang, makan malam, snack)
- Melihat dan mengikuti resep harian
- Memahami estimasi nilai gizi dari setiap resep
- Membantu pembentukan kebiasaan makan yang lebih sehat

Setiap resep akan menampilkan:
- Daftar bahan
- Cara memasak
- Estimasi total gizi:
  - Protein (gram)
  - Kalori
  - Serat (gram)
  - Lemak (gram)

> Data gizi bersifat *perkiraan*, digunakan untuk membantu perencanaan diet, bukan sebagai acuan medis.

---

## Rencana Arsitektur

### Tahap Saat Ini (UI / UX & Frontend)

Pada tahap ini, project berfokus pada:

- Desain UI/UX menggunakan *Figma*
- Implementasi frontend statis menggunakan:
  - HTML
  - CSS
  - JavaScript
  - Bootstrap Icons
- Pendekatan *mobile-first*
- Konversi desain Figma menjadi *HTML theme* (landing page & halaman aplikasi)

Tahap ini berfungsi sebagai *prototype tampilan dan interaksi* sebelum masuk ke backend.

---

### Tahap Selanjutnya (Backend)

Backend akan dibangun menggunakan:

- *Django (monolithic / SSR)*
- Django Template
- Django Admin untuk pengelolaan konten
- Django Models untuk:
  - Resep
  - Data gizi
  - User
  - Meal plan

Project ini *tidak menggunakan headless backend* dan *tidak menggunakan React*.  
Rendering dilakukan sepenuhnya di server menggunakan Django Template.

---

## Strategi Data Gizi

- Resep diinput bebas oleh admin melalui *RichTextField* di Django Admin
- Nilai gizi *tidak dihitung otomatis dari teks resep*
- Setiap resep memiliki input khusus untuk:
  - Protein
  - Kalori
  - Serat
  - Lemak

Pendekatan ini dipilih karena:
- Nama bahan bisa sangat bebas (ayam, sapi, ikan, dll)
- Sulit dan tidak akurat jika parsing otomatis dari teks
- Lebih stabil, jelas, dan mudah dikontrol

Dengan cara ini, sistem tetap fleksibel tanpa menghasilkan data gizi yang menyesatkan.

---

## Prinsip Desain

- Mobile-first (maksimal lebar 414px)
- Tampilan seperti aplikasi mobile
- Navigasi sederhana
- Fokus ke keterbacaan dan pengalaman pengguna
- Dibuat agar mudah dikembangkan ke Django Template

---

## Status Project

- [x] Desain UI/UX (Figma)
- [x] Frontend HTML/CSS/JS
- [ ] Landing page
- [ ] Integrasi Django
- [ ] Sistem login
- [ ] Meal plan logic
- [ ] Manajemen data gizi

---

## Tech Stack (Saat Ini)

- HTML5
- CSS3
- JavaScript (Vanilla)
- Bootstrap Icons

---

## Tech Stack (Rencana Backend)

- Python
- Django
- Django Template
- SQLite / PostgreSQL

---

## Disclaimer

Aplikasi ini dibuat untuk *perencanaan diet dan edukasi*, bukan alat diagnosis medis atau nutrisi profesional.

---

## Catatan

Project ini dikembangkan bertahap, dimulai dari desain dan frontend, kemudian dilanjutkan ke backend Django secara penuh.

Struktur dibuat agar mudah dikembangkan menjadi aplikasi diet yang utuh.