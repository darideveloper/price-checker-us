const checkboxes = document.querySelectorAll('input[type=checkbox]')
const refreshButtons = document.querySelectorAll('button.refresh')
const priceGapElem = document.querySelector(".price-gap .price")
const tableRows = document.querySelectorAll('tr')


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

// Calculate price gap and update in page
function calculatePriceGap() {

  // Get prices
  const visbleTableRow = document.querySelectorAll('tr:not(.hidden) .price')
  const prices = Array.from(visbleTableRow).map(price => parseFloat(price.innerText.replace('$', '')))

  // Get max, min and gap price
  const maxPrice = Math.max(...prices)
  const minPrice = Math.min(...prices)
  const gapPrice = maxPrice - minPrice

  // Update price
  priceGapElem.innerHTML = gapPrice.toFixed(2)
}

function onClickRefreshButton() {

  // Get inactive checboxes
  const activeCheckboxes = Array.from(document.querySelectorAll('input[type=checkbox]:checked'))
  const inactiveCheckboxes = Array.from(checkboxes).filter(checkbox => !activeCheckboxes.includes(checkbox))
  
  // Delete products
  for (const inactiveCheckbox of inactiveCheckboxes) {
    
    // get products based in the product id
    dataProductId = inactiveCheckbox.getAttribute('data-product-id')
    document.querySelectorAll(`[data-product-id="${dataProductId}"]`).forEach(product => {
      const productWrapper = product.parentNode.parentElement
      productWrapper.classList.add('hidden')
    })

  }

  calculatePriceGap ()
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

// Rdirect to product page when click on table row
function onClickTableRow (event) {

  // Ignore when click checkbox
  if (event.target.type == 'checkbox') {
    return
  }

  
  // Get link
  const row = event.target.parentNode
  const link = row.getAttribute('data-link')

  // Open link in new tab
  window.open(link, '_blank')

}

// Add listener to checkboxes
checkboxes.forEach(checkbox => { 
  checkbox.addEventListener('click', () => { toggleRefreshButton() })
})

// Add listener to refresh button
refreshButtons.forEach(refreshButton => {
  refreshButton.addEventListener('click', () => { onClickRefreshButton() })
})

// Add on click to each table row
tableRows.forEach(tableRow => {
  tableRow.addEventListener('click', (event) => { onClickTableRow(event) })
})


renderProductImages ()
calculatePriceGap()