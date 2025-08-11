import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv
load_dotenv()

def send(recepientEmail, capsuleID):
    host = os.environ.get("EMAIL_HOST")
    port = int(os.environ.get("EMAIL_PORT", 587))
    user = os.environ.get("EMAIL_HOST_USER")
    password = os.environ.get("EMAIL_HOST_PASSWORD")
    useTLS = os.environ.get("EMAIL_USE_TLS", "True").lower() == "true"
    domain = os.environ.get("DOMAIN", "https://example.com/")

    if not all([host, port, user, password]):
        return

    msg = EmailMessage()
    msg["From"] = user
    msg["To"] = recepientEmail
    msg["Subject"] = "Time Capsule Is Ready"
    msg.set_content(f"Your time capsule is ready! View it at {domain}/capsule/{capsuleID}")

    # Adjust these colors to match your site's theme if needed
    button_color = "#ffd036"  # Example: indigo-600 from Tailwind
    text_color = "#FFFFFF"
    background_color = "#F3F4F6"  # Example: gray-100
    border_radius = "8px"

    html_content = f"""
    <html>
      <body style="background: {background_color}; font-family: Arial, sans-serif; padding: 2em;">
        <div style="max-width: 480px; margin: auto; background: #fff; border-radius: 12px; box-shadow: 0 2px 8px #0001; padding: 2em;">
          <h1 style="color: {button_color}; text-align: center;">Your Time Capsule is Ready!</h1>
          <p style="font-size: 1.1em; color: #333; text-align: center;">
            Click the button below to view your capsule.
          </p>
          <div style="text-align: center; margin: 2em 0;">
            <a href="{domain}capsule/{capsuleID}" 
               style="background: {button_color}; color: {text_color}; padding: 1em 2em; text-decoration: none; border-radius: {border_radius}; font-weight: bold; font-size: 1.1em; display: inline-block;">
              View Capsule
            </a>
          </div>
          <p style="color: #888; font-size: 0.9em; text-align: center;">
            Or copy and paste this link into your browser:<br>
            <span style="color: #4B5563;">{domain}/capsule/{capsuleID}</span>
          </p>
        </div>
      </body>
    </html>
    """
    msg.add_alternative(html_content, subtype="html")

    with smtplib.SMTP(host, port) as server:
        if useTLS:
            server.starttls()
        server.login(user, password)
        server.send_message(msg)