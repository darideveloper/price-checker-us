// Elements
const form = document.querySelector("#search-form")
const inputSearch = document.querySelector("#input-search")
const loading = document.querySelector(".loading")

// Api data
var headers = new Headers()
headers.append("Content-Type", "application/json")

// Control variables
let isLoading = false
let requestId = 0

function alertError(error) {
  // Debug error
  console.log({ error })

  // Show alert
  Swal.fire({
    title: 'Service error!',
    text: 'The service is not available right now. Please try again later!'
  })
}

async function apiSendkeyword(keyword) {

  // Query data
  var raw = JSON.stringify({
    "keyword": keyword,
    "api-key": apiKey
  })

  try {

    // Send data to api
    const response = await fetch("./keyword/", {
      method: 'POST',
      headers: headers,
      body: raw,
      redirect: 'follow'
    })

    // Get json from api
    const result = await response.json()

    // Get request id
    requestId = result.data["request-id"]
    console.log({ requestId })

  } catch (error) {
    alertError(error)
  }


}

async function apiWaitDoneStatus() {

  // Query data
  var raw = JSON.stringify({
    "request-id": requestId,
    "api-key": apiKey
  })

  try {

    // Get data from api
    const response = await fetch("./status/", {
      method: 'POST',
      headers: headers,
      body: raw,
      redirect: 'follow'
    })
  
    // Get json from api
    const result = await response.json()
  
    // Get status
    const status = result.data["status"]

  } catch (error) {
    alertError(error)
  }

}

async function handleSubmitForm(event) {

  // Don't submit form
  event.preventDefault()

  // Only form if is not loading
  if (isLoading) {
    Swal.fire({
      title: 'You already have a request in progress!',
      text: 'Please wait until the process is finished!',
    })
    return
  }

  // Update loading status
  isLoading = true

  // Get search keyword
  const keyword = inputSearch.value

  // Show loading spinner
  loading.classList.remove("transparent")

  // Show alert
  Swal.fire({
    title: 'Hold on...',
    text: 'We are obtaining the real-time prices for you right now. The process might take around 2 minutes!',
  })

  // Send keyword to API
  await apiSendkeyword(keyword)
  console.log ("keyword sent")
  await apiWaitDoneStatus()
  console.log ("status checked")
}

form.addEventListener("submit", (event) => { handleSubmitForm(event) })