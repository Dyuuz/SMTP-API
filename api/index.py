from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import smtplib
import os
from email.message import EmailMessage

class handler(BaseHTTPRequestHandler):
    # `OPTIONS` request handler for CORS preflight
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    # `GET` request handler
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        message = {"status":"success","message": "GET request received"}
        self.wfile.write(json.dumps(message).encode("utf-8"))

    # `POST` request handler
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

        try:
            data = json.loads(post_data.decode("utf-8"))
            SUBJECT = data.get("SUBJECT")
            MESSAGE = data.get("MESSAGE")
            ZOHO_EMAIL = data.get("SENDER_EMAIL")
            ZOHO_PASSWORD = data.get("SENDER_PASSWORD")
            TO_EMAIL = data.get("RECEIVER_EMAIL")
            HTML_MESSAGE = data.get("HTML_MESSAGE")
            
            # Map field names to values
            fields = {
                "SUBJECT": SUBJECT,
                "MESSAGE": MESSAGE,
                "SENDER_EMAIL": ZOHO_EMAIL,
                "SENDER_PASSWORD": ZOHO_PASSWORD,
                "RECEIVER_EMAIL": TO_EMAIL,
                "HTML_MESSAGE": HTML_MESSAGE,
            }

            errors = {
                field: "This field cannot be empty."
                for field, value in fields.items()
                if value in (None, "")
            }

            # Custom Build response
            if errors:
                err_response = {"status": "error", "errors": errors}
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                
                response = err_response
                self.wfile.write(json.dumps(response).encode("utf-8"))
                return
                
            msg = EmailMessage()
            msg["From"] = ZOHO_EMAIL
            msg["To"] = TO_EMAIL
            msg["Subject"] = SUBJECT
            msg.set_content(MESSAGE)
            
            msg.add_alternative(HTML_MESSAGE, subtype="html")

            with smtplib.SMTP_SSL("smtp.zoho.com", 465) as smtp:
                smtp.login(ZOHO_EMAIL, ZOHO_PASSWORD)
                smtp.send_message(msg)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            response = {"success": "Email sent successfully!"}
            self.wfile.write(json.dumps(response).encode("utf-8"))

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            error_response = {"error": str(e)}
            self.wfile.write(json.dumps(error_response).encode("utf-8"))

# Run Server on local machine
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 8000))
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, handler)
    print(f"🚀 Server running on port {PORT}... Press Ctrl+C to stop.")
    httpd.serve_forever()