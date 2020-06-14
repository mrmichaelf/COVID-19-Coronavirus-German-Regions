import os

SENDMAIL = "/usr/lib/sendmail"


def sendmail(to: str, body: str, subject: str = "[COVID-19 Newsletter]", sender: str = 'no-reply@entorb.net'):
    mail = f"To: {to}\nSubject: {subject}\nFrom: {sender}\nContent-Type: text/plain; charset=\"utf-8\"\n\n{body}"
    p = os.popen(f"{SENDMAIL} -t -i", "w")
    p.write(mail)
    # status = p.close()


sendmail(to="test@entorb.net", body="Hier steht der Text Test ÄÖÜß",
         subject="Test ÄÖÜß")
