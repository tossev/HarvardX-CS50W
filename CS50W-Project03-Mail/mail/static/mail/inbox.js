document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  $('#inbox').addEventListener('click', () => load_mailbox('inbox'))
  $('#sent').addEventListener('click', () => load_mailbox('sent'))
  $('#archived').addEventListener('click', () => load_mailbox('archive'))
  $('#compose').addEventListener('click', compose_email)

  // By default, load the inbox
  load_mailbox('inbox')

  // Send an email
  $('#compose-form').addEventListener('submit', e => {
    e.preventDefault()
    send_mail($('#compose-recipients').value, $('#compose-subject').value, $('#compose-body').value)
  })

}) // DOMContentLoaded

function compose_email() {

  // Show compose view and hide other views
  $('#emails-view').style.display = 'none'
  $('#display-email').style.display = 'none'
  $('#compose-view').style.display = 'block'

  // Clear out composition fields
  $('#compose-recipients').value = ''
  $('#compose-subject').value = ''
  $('#compose-body').value = ''

  // Clear out error messages
  if ($('#recipients-alert')) $('#recipients-alert').outerHTML = ''
}

function load_mailbox(mailbox) {
  // Keep track of the current mailbox
  sessionStorage.setItem('currentMailbox', mailbox)

  // Show the mailbox and hide other views
  $('#emails-view').style.display = 'block'
  $('#compose-view').style.display = 'none'
  $('#display-email').style.display = 'none'

  // Show the mailbox name
  $('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`

  // Load the emails
  get_mailbox_content(mailbox)
}

/** Sends GET request to the API to load the emails */
function get_mailbox_content(mailbox) {
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      if (emails.length === 0) {
        $('#emails-view').append(document.createElement('p').innerHTML = 'The box is empty.')
      }
      emails.forEach(mail => generate_mail_card_HTML(mail.sender, mail.timestamp, mail.subject, mail.read, mail.id))
    })
}

/** Generates the HTML for mail card */
function generate_mail_card_HTML(sender, timestamp, subject, read, id) {
  const mailCard = create_HTML_elmnt_innerHTML_setAttribute('div', '', 'id', 'mail-card')
  mailCard.style.background = read ? '#D3D3D3' : 'white'
  mailCard.append(create_HTML_elmnt_innerHTML_setAttribute('span', sender, 'id', 'mail-card-sender'))
  mailCard.append(create_HTML_elmnt_innerHTML_setAttribute('span', subject, 'id', 'mail-card-subject'))
  mailCard.append(create_HTML_elmnt_innerHTML_setAttribute('span', timestamp, 'id', 'mail-card-timestamp'))
  // Mark email as read when it is open
  mailCard.onclick = e => {
    e.preventDefault
    if (sessionStorage.getItem('currentMailbox') === 'inbox') {
      email_read(id, true)
    }
    display_email(id)
  }
  $('#emails-view').append(mailCard)
}

/** Displays the email as HTML */
function display_email(id) {
  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      genrate_email_HTML(email.sender, email.recipients, email.subject, email.timestamp, email.body, id, email.archived)
    })
}

/** Sends POST request to the API. Loads 'sent' mailbox on success. */
function send_mail(recipients, subject, body) {
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
    .then(response => {
      // Load 'sent' mailbox if no errors
      if (response.status !== 400) load_mailbox('sent')
      return response.json()
    })
    .then(result => {
      // Handle recipient field errors 
      recipients_error(result.error)
    })
}

/** Adds 'p' element after 'recipients' field with error message */
function recipients_error(error) {
  // Update inner HTML if the element exists 
  if ($('#recipients-alert')) {
    $('#recipients-alert').innerHTML = error
  }
  else { // Create new element
    $('#compose-recipients').after(create_HTML_elmnt_innerHTML_setAttribute('p', error, 'id', 'recipients-alert'))
  }
}

/** Sends PUT request to the API to update 'read' state*/
function email_read(id, stateValue) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: stateValue
    })
  })
}

/** Creates an HTML element with text and attribute. */
function create_HTML_elmnt_innerHTML_setAttribute(element, innerHTML, attribute, attributeValue) {
  const el = document.createElement(element)
  el.innerHTML = innerHTML
  el.setAttribute(attribute, attributeValue)
  return el
}

/** Generates the HTML for the email */
function genrate_email_HTML(sender, recipients, subject, timestamp, body, id, archived) {
  const emailContainer = $('#display-email')
  emailContainer.style.display = 'block'
  emailContainer.innerHTML = ''
  $('#emails-view').style.display = 'none'
  $('#compose-view').style.display = 'none'

  const html = `
    <p><b>From: </b><span>${sender}</span></p>
    <p><b>To: </b>${recipients}</p>
    <p><b>Subject: </b>${subject}</p>
    <p><b>Timestamp: </b>${timestamp}</p>
    <hr>
    <textarea id="text-display" disabled>${body}</textarea>
    `

  const replyBtn = create_HTML_elmnt_innerHTML_setAttribute('button', 'Reply', 'class', 'btn btn-sm btn-primary')
  const archiveBtn = create_HTML_elmnt_innerHTML_setAttribute('button', `${archived ? 'Unarchive' : 'Archive'}`, 'class', 'btn btn-sm btn-secondary')
  replyBtn.onclick = (e) => {
    e.preventDefault()
    email_reply(id)
  }
  archiveBtn.onclick = (e) => {
    e.preventDefault()
    email_archived(id, archived)
  }
  emailContainer.insertAdjacentHTML('beforeend', html)
  sessionStorage.getItem('currentMailbox') === 'sent' ? emailContainer.append(replyBtn) : emailContainer.append(replyBtn, archiveBtn)
}

/** Sends PUT request to the API to update 'archived' state. Loads 'inbox' on success. */
function email_archived(id, archived) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      // Toggle state
      archived: archived ? false : true
    })
  })
    .then(response => {
      if (response.status === 204) load_mailbox('inbox')
    })
}
/** Loads `composition form`. Pre-fill the `composition form`. */
function email_reply(id) {
  compose_email()
  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      $('#compose-recipients').value = sessionStorage.getItem('currentMailbox') === 'sent' ? email.recipients : email.sender
      $('#compose-subject').value = email.subject.startsWith('Re: ') ? email.subject : `Re: ${email.subject}`
      $('#compose-body').value = `${email.body}\nfrom: ${email.sender} ${email.timestamp}\n-----\n`
    })
  $('#compose-body').focus()

}

/** querySelector, jQuery style */
function $(selector) {
  return document.querySelector(selector)
}