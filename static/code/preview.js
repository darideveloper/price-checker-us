const checkboxes = document.querySelectorAll('input[type=checkbox]')
const refreshButtons = document.querySelectorAll('button.refresh')
const boomButtons = document.querySelectorAll('button.boom')
const priceGapElem = document.querySelector(".price-gap .price")
const tableRows = document.querySelectorAll('tbody tr')

// Url params
const currentUrl = window.location.href
const host = window.location.host
const urlObject = new URL(currentUrl)
let productsHidden = []
console.log({host})
console.log(`${host}/filter/`)


// Get request id fom url
const requestId = currentUrl.split('/').pop()


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
  // Generate new page with products filtered

  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  var raw = JSON.stringify({
    "request-id": requestId,
    "products-ids": productsHidden,
    "api-key": apiKey,
  });

  var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: raw,
    redirect: 'follow'
  };

  fetch(`../../filter/`, requestOptions)
    .then(response => response.text())
    .then(result => {
      // Get new request from json data
      const jsonData = JSON.parse(result)
      const newRequestId = jsonData.data['request-id']
      const new_page = `./${newRequestId}`
      
      // Redirect to new page
      window.location.href = new_page
    })
    .catch(error => console.log('error', error));
}

async function onClickBoomButton() {
  
  // Filter only products (ignore ads)
  products = products.filter(product => product.title)
  console.log({products})

  try {
    // Send data to post bot
    const response = await fetch(`http://${postBotHost}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(products),
    })
    response.json()
    
    Swal.fire({
      title: "Boom Post Bot started",
      confirmButtonText: "Ok",
    })

  } catch (error) {

    // Show alert error
    Swal.fire({
      title: "Boom Post Bot not found in your PC",
      showCancelButton: true,
      confirmButtonText: "Read more",
    }).then((result) => {
      // Open a page in a new tab
      if (result.isConfirmed) {
        window.open("/boom-bot-info", "_blank")
      }
    })
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

function updateHiddenProduct(checkbox) {
  // Get data-product-id
  const dataProductId = checkbox.getAttribute('data-product-id')

  // Save or remove product id
  if (checkbox.checked) {
    productsHidden = productsHidden.filter(product => product != dataProductId)
  } else {
    productsHidden.push(parseInt(dataProductId))
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

// Add listener to boom button
boomButtons.forEach(boomButton => {
  boomButton.addEventListener('click', () => { onClickBoomButton() })
})

// Add on click to each table row
tableRows.forEach(tableRow => {
  tableRow.addEventListener('click', (event) => { onClickTableRow(event) })
})


renderProductImages()
calculatePriceGap()