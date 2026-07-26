from django.core.mail import EmailMultiAlternatives

def send_activation_email(email,random_code,subject):
            from_email = 'OFFSITE <rz1125.1386@gmail.com>'
            to_email = [email]

            # Plain text version (fallback for email clients that don't support HTML)
            text_content = (
                f"{email}،کاربر گرامی\n"
                f"{random_code}:کد شما\n"
            )

            # HTML version with simple styling
            html_content = f"""
            <html lang="fa" dir="rtl">
            <head>
                <style>
                body {{
                    font-family: 'Tahoma', sans-serif;
                    background-color: #f9f9f9;
                    color: #333;
                    padding: 20px;
                }}
                .container {{
                    background-color: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    max-width: 600px;
                    margin: auto;
                }}
                h1 {{
                    color: #4CAF50;
                }}
                .code {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #e91e63;
                    margin-top: 20px;
                }}
                p {{
                    line-height: 1.6;
                    font-size: 16px;
                }}
                </style>
            </head>
            <body>
                <div class="container">
                <h1>کاربر گرامی، {email}</h1>
                <p>کد شما:</p>
                <p class="code">{random_code}</p>
                </div>
            </body>
            </html>
            """
            email = EmailMultiAlternatives(
                subject,
                text_content,
                from_email,
                to_email,
            )
            email.attach_alternative(html_content, "text/html")
            result = email.send()

            if result == 0:
                raise Exception("Email sending failed")