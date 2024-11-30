import os
from mailersend import emails
from dotenv import load_dotenv

load_dotenv()

def send_thank_you_email(to_email):
    # Initialize the MailerSend client
    mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY'))

    # Define the email from and to details
    mail_from = {
        "name": "Baby Stop",
        "email": "info@babystopform.co.uk",
    }

    recipients = [
        {
            "name": "Recipient",  # You can modify this based on the user
            "email": to_email,
        }
    ]

    # Define email content (plain text and HTML)
    mail_body = {}

    # Set mail details
    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject("Thank You for Visiting Baby Stop!", mail_body)

    # HTML content with logo and professional styling
    html_content = """
    <html>
        <body style="font-family: Arial, sans-serif; margin: 0; padding: 0;">
            <div style="text-align: center; padding: 20px; background-color: #f4f4f4;">
                <img src="https://poetic-narwhal-538917.netlify.app/babystoplogo.png" alt="Baby Stop Logo" style="width: 150px; margin-bottom: 20px;" />
                <h2 style="color: #4CAF50;">Thank You for Submitting Your Details!</h2>
                <p style="font-size: 16px; line-height: 1.6; color: #333;">
                    Thank you for submitting your details to <strong>Baby Stop</strong>. We appreciate your visit and your effort in reusing preloved equipment.
                </p>
                <p style="font-size: 16px; line-height: 1.6; color: #333;">
                    We would like to remind you that by completing the form, you agree to take full responsibility for inspecting the product before use.
                    Baby Stop holds no liability for the product’s safety. Please dispose of any unsuitable items at your local recycling depot.
                </p>
                <footer style="font-size: 12px; color: #777; margin-top: 20px;">
                    <p>If you have any questions, feel free to contact us at <a href="mailto:support@babystop.com">support@babystop.com</a></p>
                    <p>&copy; 2024 Baby Stop. All rights reserved.</p>
                </footer>
            </div>
        </body>
    </html>
    """

    mailer.set_html_content(html_content, mail_body)
    mailer.set_plaintext_content("Thanks for submitting your details to Baby Stop. We appreciate your visit!", mail_body)

    # Send the email and handle the response
    response = mailer.send(mail_body)
    print(response)
    
    if response:
        print("Email sent successfully!")
        return True
    else:
        print(f"Error sending email: {response}")
        return False
