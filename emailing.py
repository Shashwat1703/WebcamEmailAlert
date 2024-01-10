import smtplib
import imghdr
from email.message import EmailMessage
PASSWORD = "ysngrzojadrhfytc"
SENDER = "veruscodex@gmail.com"
RECEIVER = "sharma.shashwat1717@gmail.com"
def send_email(image_path):
    print("Send_Email function has started.")
    email_message = EmailMessage()
    email_message["Subject"] = "Webcam Alert!"
    email_message.set_content("Webcam captured something")

    with open(image_path, "rb") as file:
        content = file.read()

    email_message.add_attachment(content, maintype = "image", subtype = imghdr.what(None, content))
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER,PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()
    print("Email is sent")

if __name__ == "__main__":
    send_email(image_path ="images/20.png")


