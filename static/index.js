// Elements
const form = document.querySelector("#search-form")
const inputSearch = document.querySelector("#input-search")
const loading = document.querySelector(".loading")
const iframe = document.querySelector("iframe")
const footer = document.querySelector("footer")

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

  while (true) {

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
      console.log ({ status })
  
      if (status == "done") {
        break
      }
  
    } catch (error) {
      alertError(error)
    }

    // Wait 5 seconds
    await new Promise(r => setTimeout(r, 5000))
  }


}

function apiGetPreviewPage () {
  return `./preview/?request-id=${requestId}`
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
  // await apiSendkeyword(keyword)
  // await apiWaitDoneStatus()
  // previewPage = apiGetPreviewPage()
  // console.log ({previewPage})


  // Wait 5 seconds
  await new Promise(r => setTimeout(r, 2000))
  const previewPage = "./preview/?request-id=235"

  // Invisible spinner
  loading.classList.add("transparent")

  setTimeout (() => {

    // Hide spinner
    loading.classList.add("hidden")

    // Move footer
    footer.classList.remove("absolute")

    // Show iframe
    iframe.classList.remove("hidden")

  }, 1000)

  setTimeout(() => {
    // Visible iframe
    iframe.classList.remove("transparent")
  }, 1200)


}


form.addEventListener("submit", (event) => { handleSubmitForm(event) })