document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', () => {
      document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'))
      item.classList.add('active')
    })
    
    const navItems = document.querySelectorAll('.nav-item')

    navItems.forEach(item => {
     item.addEventListener('click', () => {

       navItems.forEach(i => i.classList.remove('active'))
       item.classList.add('active')

       console.log('CLICK:', item.innerText)
     })
   })
  })

  const openSearch = document.getElementById('openSearch')
  const searchBar  = document.getElementById('searchBar')


  openSearch.addEventListener('click', (e) => {
    e.stopPropagation()
    searchBar.classList.toggle('active')

    if (searchBar.classList.contains('active')) {
      const input = searchBar.querySelector('input')
      if (input) input.focus()
    }
  })

  document.addEventListener('click', () => {
    searchBar.classList.remove('active')
  })

  searchBar.addEventListener('click', e => {
    e.stopPropagation()
  })
})