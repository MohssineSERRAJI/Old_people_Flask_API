import smtplib
    
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def alert(subject, body, to,client):
    # me == my email address
    # you == recipient's email address
    me = "giromohssine98@gmail.com"
    
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = me
    
    # Create the body of the message (a plain-text and an HTML version).
    text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
    html = """\
    <html>
      <head></head>
      <body>
        <p>Hi!<br>
           How are you?<br>
           <br>
           Here is a new client Ms -- <a href="https://firebase.google.com/">{}</a> -- go to <a href="https://firebase.google.com/">DataBase</a> for more informations.
        </p>
      </body>
    </html>
    """.format(client)
    
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    
    mail.ehlo()
    
    mail.starttls()
    user = "giromohssine98@gmail.com"
    password = "0615167315"
    mail.login(user, password)
    for x in to:
        msg['To'] = x
        mail.sendmail(me, x, msg.as_string())
    mail.quit()
    
if __name__ ==  "__main__":
    alert("New client *-*", "new client *-*", "sera.mohssine@gmail.com","mohssine")
    
    