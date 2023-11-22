const shareButtons = document.querySelectorAll('button.share')

// Opcy current url
function buttonUrl() {
  // Get current url
  const url = window.location.href

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

// Add click event to each button
function addListenersButtons() {
  shareButtons.forEach(shareButton => {
    shareButton.addEventListener('click', () => {
      // Get button class
      const dataSocial = shareButton.getAttribute('data-social')

      // Object functions
      const functions = {
        url: buttonUrl,
        default: buttonDefault
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