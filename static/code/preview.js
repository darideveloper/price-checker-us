const checkboxes = document.querySelectorAll('input[type=checkbox]')
const refreshButtons = document.querySelectorAll('button.refresh')
const restartButtons = document.querySelectorAll('button.restart')
const boomButtons = document.querySelectorAll('button.boom')
const priceGapElem = document.querySelector(".price-gap .price")
const tableRows = document.querySelectorAll('tbody tr')

// Url params
const currentUrl = window.location.href
const urlObject = new URL(currentUrl)
const hidden = urlObject.searchParams.get('hidden')
let productsHidden = hidden ? hidden.split('-') : []


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

function activateRestartButton() {

  // Detect url params
  const urlParams = new URLSearchParams(window.location.search)

  // Validate if there is hidden param
  if (urlParams.has('hidden')) {
    // Activate restart button
    restartButtons.forEach(restartButton => {
      restartButton.removeAttribute("disabled")
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
  // Generate filter url adding hidden products
  urlObject.searchParams.set('hidden', productsHidden.join('-'))

  // Redirect to url
  window.location.href = urlObject
}

function onClickRestartButton() {
  // Generate url without get params
  urlObject.search = ''

  // Redirect to url
  window.location.href = urlObject
}

async function onClickBoomButton() {
  try {
    const response = await fetch(`http://${postBotHost}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(products),
    })
    const result = await response.json()
    console.log("Success:", result)
  } catch (error) {

    // Show alert error
    Swal.fire({
      title: "Post bot not found in your PC",
      showCancelButton: true,
      confirmButtonText: "Read more",
    }).then((result) => {
      // Open a page in a new tab
      if (result.isConfirmed) {
        window.open("/post-bot", "_blank")
      }
    });
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

// Redirect to product page when click on table row
function onClickTableRow(event) {

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

// Hide products from url params
function hiddeUrlProducts() {

  // Get inactive checboxes
  const selector = productsHidden.map(product => `[data-product-id="product-${product}"]`).join(', ')
  if (!selector) {
    return null
  }
  const inactiveCheckboxes = document.querySelectorAll(selector)

  // Delete products
  for (const inactiveCheckbox of inactiveCheckboxes) {
    const productWrapper = inactiveCheckbox.parentNode.parentElement
    productWrapper.classList.add('hidden')
  }

  // Delete products from products array
  let productIndexes = productsHidden.map(product => parseInt(product) - 1)
  productIndexes.sort(function (a, b) {
    return b - a
  })
  for (let productIndex of productIndexes) {
    products.splice(productIndex, 1)
  }
}

function updateHiddenProduct(checkbox) {
  // Get data-product-id
  const dataProductId = checkbox.getAttribute('data-product-id')

  // Get prodyc id
  const productId = dataProductId.split('-')[1]

  // Save or remove product id
  if (checkbox.checked) {
    productsHidden = productsHidden.filter(product => product != productId)
  } else {
    productsHidden.push(productId)
  }
}

// Add listener to checkboxes
checkboxes.forEach(checkbox => {
  checkbox.addEventListener('click', () => {
    // Activate or deactivate refresh button
    toggleRefreshButton()

    // Add or remove product id from hidden products
    updateHiddenProduct(checkbox)
  })
})

// Add listener to refresh button
refreshButtons.forEach(refreshButton => {
  refreshButton.addEventListener('click', () => { onClickRefreshButton() })
})

// Add listener to restart button
restartButtons.forEach(restartButton => {
  restartButton.addEventListener('click', () => { onClickRestartButton() })
})

// Add listener to restart button
boomButtons.forEach(boomButton => {
  boomButton.addEventListener('click', () => { onClickBoomButton() })
})

// Add on click to each table row
tableRows.forEach(tableRow => {
  tableRow.addEventListener('click', (event) => { onClickTableRow(event) })
})


renderProductImages()
hiddeUrlProducts()
calculatePriceGap()
activateRestartButton()