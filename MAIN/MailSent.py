import smtplib

def SendMail(recipient, message):
	# creates SMTP session
	s = smtplib.SMTP('smtp.gmail.com', 587)
	# start TLS for security
	s.starttls()
	# Authentication
	s.login("sample1@gmail.com", "password_here")
	# sending the mail
	s.sendmail("sample1@gmail.com", recipient, message)
	# terminating the session
	s.quit()


recipient = "sample1@gmail.com"
message = "Your child might be in stress!"

