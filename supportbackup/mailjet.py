def sendemail(ticketid, dateOpen, issueTitle, issueDetails, username, email):
  from mailjet_rest import Client
  import os
  api_key = '8a1c7c18d061725a36de6e19d9f4a2f9'
  api_secret = 'fc8a89742489e2d8846eae8f750864d3'
  mailjet = Client(auth=(api_key, api_secret), version='v3.1')
  data = {
    'Messages': [
      {
        "From": {
          "Email": "scgoh.2018@sis.smu.edu.sg",
          "Name": "Geralyn"
        },
        "To": [
          {
            "Email": email,
            "Name": username
          }
        ],
        "Subject": "You opened a ticket.",
        "TextPart": "Here is your ticket",
        "HTMLPart": "Your ticket details are as follows: <br> Title: " + issueTitle + "<br> TicketID: " + str(ticketid) + "<br> Description: " + issueDetails + "<br> Date Opened: " + str(dateOpen),
        "CustomID": "AppGettingStartedTest"
      }
    ]
  }
  result = mailjet.send.create(data=data)
  print (result.status_code)
  print (result.json())