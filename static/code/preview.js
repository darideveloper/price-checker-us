const checkboxes = document.querySelectorAll('input[type=checkbox]')
const refreshButtons = document.querySelectorAll('button.refresh')

// Detech when click checkbox products
checkboxes.forEach(checkbox => {
  checkbox.addEventListener('change', () => {

    // Get all the checked status
    const activeCheckbox = document.querySelectorAll('input[type=checkbox]:checked').length

    // Validate if there are checkbox unchecked
    if (activeCheckbox != checkboxes.length) {

      // Activate refresh button
      refreshButtons.forEach(refreshButton => {
        refreshButton.removeAttribute("disabled")
      })

    } else {
      // Disable refresh button
      refreshButtons.forEach(refreshButton => {
        refreshButton.setAttribute("disabled", "disabled")
      })
    }

  })
})

// Hide products when click refresh button
refreshButtons.forEach(refreshButton => {
  refreshButton.addEventListener('click', () => {

    // Get inactive checboxes
    const activeCheckboxes = Array.from(document.querySelectorAll('input[type=checkbox]:checked'))
    const inactiveCheckboxes = Array.from(checkboxes).filter(checkbox => !activeCheckboxes.includes(checkbox))

    // Delete products
    for (const inactiveCheckbox of inactiveCheckboxes) {
      const product = inactiveCheckbox.parentNode.parentNode
      product.classList.add("hidden")
    }

  })
})

// Place products images
document.addEventListener('DOMContentLoaded', function () {
  const productImages = document.querySelectorAll('.product-image')
  productImages.forEach(productImage => {
    const imageUrl = productImage.getAttribute('data-image')
    productImage.style.backgroundImage = 'url(' + imageUrl + ')'
  })
})