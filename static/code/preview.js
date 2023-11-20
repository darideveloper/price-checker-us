const checkboxes = document.querySelectorAll('input[type=checkbox]')
const refreshButtons = document.querySelectorAll('button.refresh')
const priceGapElem = document.querySelector(".price-gap .price")


function toggleRefreshButton() {
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
}

function onClickRefreshButton() {
  console.log ("Refresh button clicked")

  // Get inactive checboxes
  const activeCheckboxes = Array.from(document.querySelectorAll('input[type=checkbox]:checked'))
  const inactiveCheckboxes = Array.from(checkboxes).filter(checkbox => !activeCheckboxes.includes(checkbox))
  
  // Delete products
  for (const inactiveCheckbox of inactiveCheckboxes) {
    const product = inactiveCheckbox.parentNode.parentNode
    product.classList.add("hidden")
  }
}

function renderProductImages() {
  // Place products images
  document.addEventListener('DOMContentLoaded', function () {
    const productImages = document.querySelectorAll('.product-image')
    productImages.forEach(productImage => {
      const imageUrl = productImage.getAttribute('data-image')
      productImage.style.backgroundImage = 'url(' + imageUrl + ')'
    })
  })
}

// Calculate price gap and update in page
function calculatePriceGap() {

  // Get prices
  const visbleTableRow = document.querySelectorAll('tr:not(.hidden) .price')
  const prices = Array.from(visbleTableRow).map(price => parseFloat(price.innerText.replace('$', '')))

  // Get max, min and gap price
  const maxPrice = Math.max(...prices)
  const minPrice = Math.min(...prices)
  const gapPrice = maxPrice - minPrice
  console.log({ maxPrice, minPrice, gapPrice, prices })

  // Update price
  priceGapElem.innerHTML = gapPrice.toFixed(2)
}

// Add listener to checkboxes
checkboxes.forEach(checkbox => { 
  checkbox.addEventListener('click', () => { toggleRefreshButton() })
})

// Add listener to refresh button
console.log (refreshButtons)
refreshButtons.forEach(refreshButton => {
  refreshButton.addEventListener('click', () => { onClickRefreshButton() })
})

renderProductImages ()

calculatePriceGap()