const shareUrlButton = document.querySelector('.share.url')


shareUrlButton.addEventListener('click', () => {
  // Get current url
  const url = window.location.href

  // Copy url to clipboard
  navigator.clipboard.writeText(url)

  // Show alert
  Swal.fire("Page copied to clipboard")
  
})
