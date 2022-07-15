  # CS50W Project 3 - Mail
  ## Description
  Design a front-end for an email client that makes API calls to send and receive emails.
  
  Video for CS50W-Project03-Mail -> https://youtu.be/psdNiSQieJA
  
  ## Understanding
  In the distribution code is a Django project called project3 that contains a single app called mail.

  First, after making and applying migrations for the project, run python manage.py runserver to start the web server. Open the web server in your browser, and use the “Register” link to register for a new account. The emails you’ll be sending and receiving in this project will be entirely stored in your database (they won’t actually be sent to real email servers), so you’re welcome to choose any email address (e.g. foo@example.com) and password you’d like for this project: credentials need not be valid credentials for actual email addresses.

  Once you’re signed in, you should see yourself taken to the Inbox page of the mail client, though this page is mostly blank (for now). Click the buttons to navigate to your Sent and Archived mailboxes, and notice how those, too, are currently blank. Click the “Compose” button, and you’ll be taken to a form that will let you compose a new email. Each time you click a button, though, you’re not being taken to a new route or making a new web request: instead, this entire application is just a single page, with JavaScript used to control the user interface. Let’s now take a closer look at the distribution code to see how that works.

  Take a look at mail/urls.py and notice that the default route loads an index function in views.py. So let’s up views.py and look at the index function. Notice that, as long as the user is signed in, this function renders the mail/inbox.html template. Let’s look at that template, stored at mail/templates/mail/inbox.html. You’ll notice that in the body of the page, the user’s email address is first displayed in an h2 element. After that, the page has a sequence of buttons for navigating between various pages of the app. Below that, notice that this page has two main sections, each defined by a div element. The first (with an id of emails-view) contains the content of an email mailbox (initially empty). The second (with an id of compose-view) contains a form where the user can compose a new email. The buttons along the top, then, need to selectively show and hide these views: the compose button, for example, should hide the emails-view and show the compose-view; the inbox button, meanwhile, should hide the compose-view and show the emails-view.

  How do they do that? Notice at the bottom of inbox.html, the JavaScript file mail/inbox.js is included. Open that file, stored at mail/static/mail/inbox.js, and take a look. Notice that when the DOM content of the page has been loaded, we attach event listeners to each of the buttons. When the inbox button is clicked, for example, we call the load_mailbox function with the argument 'inbox'; when the compose button is clicked, meanwhile, we call the compose_email function. What do these functions do? The compose_email function first hides the emails-view (by setting its style.display property to none) and shows the compose-view (by setting its style.display property to block). After that, the function takes all of the form input fields (where the user might type in a recipient email address, subject line, and email body) and sets their value to the empty string '' to clear them out. This means that every time you click the “Compose” button, you should be presented with a blank email form: you can test this by typing values into form, switching the view to the Inbox, and then switching back to the Compose view.

  Meanwhile, the load_mailbox function first shows the emails-view and hides the compose-view. The load_mailbox function also takes an argument, which will be the name of the mailbox that the user is trying to view. For this project, you’ll design an email client with three mailboxes: an inbox, a sent mailbox of all sent mail, and an archive of emails that were once in the inbox but have since been archived. The argument to load_mailbox, then, will be one of those three values, and the load_mailbox function displays the name of the selected mailbox by updating the innerHTML of the emails-view (after capitalizing the first character). This is why, when you choose a mailbox name in the browser, you see the name of that mailbox (capitalized) appear in the DOM: the load_mailbox function is updating the emails-view to include the appropriate text.
  ## Specification
  * **Send mail**: When a user submits the email composition form, add Javascipt code to actually send the email.
      * You’ll likely want to make a `POST` request to `/emails`, passing in values for `recipients`, `subject`, and `body`.
      * Once the email has been sent, load the user’s sent mailbox.
  * **Mailbox**: When a user visits their Inbox, Sent mailbox, or Archive, load the appropriate mailbox.
      *  You’ll likely want to make a `GET` request to /emails/<mailbox> to request the emails for a particular mailbox.
      *  When a mailbox is visited, the application should first query the API for the latest emails in that mailbox.
      *  When a mailbox is visited, the name of the mailbox should appear at the top of the page (this part is done for you).
      *  Each email should then be rendered in its own box (e.g. as a `<div>` with a border) that displays who the email is from, what the subject line is, and the timestamp of the email.
      *  If the email is unread, it should appear with a white background. If the email has been read, it should appear with a gray background.
  * **Veiw Email**: When a user clicks on an email, the user should be taken to a view where they see the content of that email.
      * You’ll likely want to make a `GET` request to `/emails/<email_id>` to request the email.
      * Your application should show the email’s sender, recipients, subject, timestamp, and body.
      * You’ll likely want to add an additional `div` to `inbox.html` (in addition to `emails-view` and `compose-view`) for displaying the email. Be sure to update your code to hide and show the right views when navigation options are clicked.
      * See the hint in the Hints section about how to add an event listener to an HTML element that you’ve added to the DOM.
      * Once the email has been clicked on, you should mark the email as read. Recall that you can send a `PUT` request to `/emails/<email_id>` to update whether an email is read or not.
      * Once an email has been archived or unarchived, load the user’s inbox.
* **Reply**: Allow users to reply to an email.
	* When viewing an email, the user should be presented with a “Reply” button that lets them reply to the email.
	* When the user clicks the “Reply” button, they should be taken to the email composition form.
	* Pre-fill the composition form with the `recipient` field set to whoever sent the original email.
	* Pre-fill the subject line. If the original email had a `subject` line of `foo`, the new subject line should be `Re: foo.` (If the subject line already begins with `Re:` , no need to add it again.)
	* Pre-fill the `body` of the email with a line like `"On Jan 1 2020, 12:00 AM foo@example.com wrote:"` followed by the original text of the email.

## Functions
* `compose_email()`
	* Show compose view and hide other views
	* Clear out composition fields
	* Clear out error messages

* `load_mailbox(mailbox)`
	* Keep track of the current mailbox
	* Show the mailbox and hide other views
	* Show the mailbox name
	* Load the emails

* `get_mailbox_content(mailbox)`
	* Sends GET request to the API to load the emails 

* `function generate_mail_card_HTML(sender, timestamp, subject, read, id)`
	* Generates the HTML for mail card
	* Marks email as read when it is open

* `display_email(id)`
	* Displays the email as HTML

* `send_mail(recipients, subject, body)`
	* Sends POST request to the API. Loads 'sent' mailbox on success
	* Load 'sent' mailbox if no errors
	* Handle recipient field errors

* `recipients_error(error)`
	* Adds 'p' element after 'recipients' field with error message

* `email_read(id, stateValue)`
	* Sends PUT request to the API to update 'read' state

* `create_HTML_elmnt_innerHTML_setAttribute(element, innerHTML, attribute, attributeValue)`
	* Creates an HTML element with text and attribute

* `genrate_email_HTML(sender, recipients, subject, timestamp, body, id, archived)`
	* Generates the HTML for the email

* `email_archived(id, archived)`
	* Sends PUT request to the API to update 'archived' state. Loads 'inbox' on success
* `email_reply(id)`
	* Loads `composition form`. Pre-fill the `composition form`

* `$(selector)`
	* querySelector, jQuery style
