import requests
from bs4 import BeautifulSoup
import hashlib
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

URL = "https://www.issrermagoraefortunato.it/index.php/comunicazioni-corsi"

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# ------------------------

def get_content():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(URL, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text()

    start = text.lower().find("studio teologico interdiocesano")

    if start == -1:
        return None

    return text[start:start+2000]

# ------------------------

def send_email(content):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "📢 Aggiornamento ISSR"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_USER

    html = f"""
    <html>
    <body style="font-family: Arial;">
        <h2 style="color:#2c3e50;">📢 Aggiornamento ISSR</h2>
        <p>È stato rilevato un aggiornamento nella sezione:</p>
        <h3>STUDIO TEOLOGICO INTERDIOCESANO</h3>
        <hr>
        <pre style="white-space: pre-wrap;">{content}</pre>
        <hr>
        <p style="font-size:12px;color:gray;">
        {datetime.now().strftime("%Y-%m-%d %H:%M")}
        </p>
    </body>
    </html>
    """

    part = MIMEText(html, "html")
    msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, [EMAIL_USER], msg.as_string())

# ------------------------

def main():
    content = get_content()
    if not content:
        return

    new_hash = hashlib.md5(content.encode()).hexdigest()

    try:
        with open("hash.txt", "r") as f:
            old_hash = f.read()
    except:
        old_hash = ""

    if True:
        send_email(content)

    with open("hash.txt", "w") as f:
        f.write(new_hash)

# ------------------------

if __name__ == "__main__":
    main()
