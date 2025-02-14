import os
from postmarker.core import PostmarkClient
from dotenv import load_dotenv

load_dotenv()

def send_thank_you_email(to_email):
    # Initialize the Postmark client
    postmark = PostmarkClient(server_token=os.getenv('POSTMARK_SERVER_TOKEN'))

    # Define the email details
    sender_email = "info@babystopform.co.uk"
    subject = "Thank You for Visiting Baby Stop!"
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
                    <p>If you have any questions, feel free to contact us at <a href="mailto:team@babystop.uk">team@babystop.uk</a></p>
                    <p>&copy; 2024 Baby Stop. All rights reserved.</p>
                </footer>
            </div>
        </body>
    </html>
    """
    text_content = "Thanks for submitting your details to Baby Stop. We appreciate your visit!"

    try:
        # Send the email
        response = postmark.emails.send(
            From=sender_email,
            To=to_email,
            Subject=subject,
            HtmlBody=html_content,
            TextBody=text_content
        )
        print("Email sent successfully:", response)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False