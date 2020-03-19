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
          "Email": "scgoh.2018@sis.smu.edu.sg",
          "Name": "Geralyn"
        }
      ],
      "Subject": "Greetings from Mailjet.",
      "TextPart": "My first Mailjet email",
      "HTMLPart": "<h3>Dear passenger 1, welcome to <a href='https://www.mailjet.com/'>Mailjet</a>!</h3><br />May the delivery force be with you!",
      "CustomID": "AppGettingStartedTest"
    }
  ]
}
result = mailjet.send.create(data=data)
print (result.status_code)
print (result.json())