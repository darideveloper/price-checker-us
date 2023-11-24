const shareButtons = document.querySelectorAll('button.share')
const url = window.location.href
let currentPage = "home"

const mesages = {
  "home": `Hey, take a look at this awesome product price checker tool`,
  "preview": `Hey, take a look at this '${keyword}' price comparison`
}

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

// Share page in whatsapp
function buttonWhatsapp () {
  const message = mesages[currentPage]
  const encodedMessage = encodeURIComponent(message)
  const link = `whatsapp://send?text=${encodedMessage} ${url}`
  window.open(link, '_blank')
}

// Share page in telegram
function buttonTelegram () {
  const message = mesages[currentPage]
  const link = `https://t.me/share/url?url=${url}&text=${message}`
  window.open(link, '_blank')
}

// Share page in twitter
function buttonTwitter () {
  const message = mesages[currentPage]
  const link = ` https://twitter.com/intent/tweet?text=${message} ${url}`
  window.open(link, '_blank')
}

// Share page in facebook
function buttonFacebook () {
  const link = `https://www.facebook.com/sharer/sharer.php?u=${url}`
  window.open(link, '_blank')
}

// Share page in instagram
function buttonInstagram () {
    // Copy url to clipboard
    navigator.clipboard.writeText(url)

    // Show alert
    Swal.fire({
      title: "Link copied to clipboard",
      text: "We'll redirect you to our instagram page",
      confirmButtonText: "Go to Instagram",
    }).then(() => {
      // Redirect to instagram
      window.open("https://www.instagram.com/", '_blank')
    })
}

// Share page in pinterest
function buttonPinterest () {
  // Copy url to clipboard
  navigator.clipboard.writeText(url)

  // Show alert
  Swal.fire({
    title: "Link copied to clipboard",
    text: "We'll redirect you to our pinterest page",
    confirmButtonText: "Go to Pinterest",
  }).then(() => {
    // Redirect to instagram
    window.open("https://pinterest.com/", '_blank')
  })
}

// Add click event to each button
function addListenersButtons() {

  // Relations between button name and function
  const functions = {
    url: buttonUrl,
    default: buttonDefault,
    whatsapp: buttonWhatsapp,
    telegram: buttonTelegram,
    twitter: buttonTwitter,
    facebook: buttonFacebook,
    instagram: buttonInstagram,
    pinterest: buttonPinterest,
  }

  shareButtons.forEach(shareButton => {
    shareButton.addEventListener('click', () => {
      // Get button class
      const dataSocial = shareButton.getAttribute('data-social')

      // Detect is user is in preview page
      if (url.includes("preview")) {
        currentPage = "preview"
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