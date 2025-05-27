import resend

resend.api_key = "re_ZNDUY3nh_Fqa2VZnwLEK5At3sRW1Z7AGm"

r = resend.Emails.send({
  "from": "onboarding@resend.dev",
  "to": "oswaldoleon72@gmail.com",
  "subject": "Hello World",
  "html": "<p>Congrats on sending your <strong>first email</strong>!</p>"
})
print(r, "" if r else "No response from Resend API")