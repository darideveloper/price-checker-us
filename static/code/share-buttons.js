const shareButtons = document.querySelectorAll('button.share')
const url = window.location.href

// Opcy current url
function buttonUrl() {
  // Copy url to clipboard
  navigator.clipboard.writeText(url)

  // Show alert
  Swal.fire("Page copied to clipboard")
}

// DEfgault function: comming soon alert
function buttonDefault() {
  // Show alert
  Swal.fire("Comming soon")
}

// Open share message page in whatsapp
function buttonWhatsapp () {
  // Open link in new tab
  const message = `Hey, take a look at this awesome product price checker tool: ${url}`
  const encodedMessage = encodeURIComponent(message)
  const link = `whatsapp://send?text=${encodedMessage}`
  window.open(link, '_blank')
}

// Add click event to each button
function addListenersButtons() {
  shareButtons.forEach(shareButton => {
    shareButton.addEventListener('click', () => {
      // Get button class
      const dataSocial = shareButton.getAttribute('data-social')

      // Object functions
      const functions = {
        url: buttonUrl,
        default: buttonDefault,
        whatsapp: buttonWhatsapp
      }

      // Run default function if not found
      if (!(dataSocial in functions)) {
        functions["default"]()
        return null
      }

      // Run button function
      functions[dataSocial]()
    })
  })
}

addListenersButtons ()