import smtplib

def SendMail(recipient, message):
	# creates SMTP session
	s = smtplib.SMTP('smtp.gmail.com', 587)
	# start TLS for security
	s.starttls()
	# Authentication
	s.login("thetrendz360@gmail.com", "ecjg hojv xonn jzra")
	# sending the mail
	s.sendmail("thetrendz360@gmail.com", recipient, message)
	# terminating the session
	s.quit()


recipient = "thetrendz360@gmail.com"
message = "Your child might be in stress!"

