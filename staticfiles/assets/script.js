document.addEventListener('DOMContentLoaded', function () {

  console.log('DOM SIAP');

  /* =========================
     NAV
  ========================= */

  const navItems = document.querySelectorAll('.nav-item');

  navItems.forEach(item => {
    item.addEventListener('click', function () {
      navItems.forEach(i => i.classList.remove('active'));
      this.classList.add('active');
      console.log('CLICK NAV:', this.innerText.trim());
    });
  });


  /* =========================
     SEARCH
  ========================= */

  const openSearch = document.getElementById('openSearch');
  const searchBar  = document.getElementById('searchBar');

  if (openSearch && searchBar) {

    openSearch.addEventListener('click', function (e) {
      e.stopPropagation();
      searchBar.classList.toggle('active');

      const input = searchBar.querySelector('input');
      if (input) input.focus();
    });

    document.addEventListener('click', function (e) {
      if (!searchBar.contains(e.target) && e.target !== openSearch) {
        searchBar.classList.remove('active');
      }
    });

  }


  /* =========================
     HEART
  ========================= */

  const hearts = document.querySelectorAll('.heart-btn');

  console.log('HEART DITEMUKAN:', hearts.length);

  hearts.forEach(heart => {

    heart.addEventListener('click', function (e) {

      e.preventDefault();
      e.stopPropagation();

      const menuId = this.dataset.id;

      if (!menuId) return; // user belum login (dummy)

      fetch(`/toggle-love/${menuId}/`)
        .then(response => response.json())
        .then(data => {

          if (data.status === "ok") {

            this.classList.toggle('active');

            const icon = this.querySelector('i');

            if (icon) {
              icon.classList.toggle('bi-heart');
              icon.classList.toggle('bi-heart-fill');
            }

            if (data.loved) {
              console.log('sudah ditambahkan ke cintaaah');
            } else {
              console.log('dihapus dari cintaaah');
            }

          }

        });

    });

  });

});

