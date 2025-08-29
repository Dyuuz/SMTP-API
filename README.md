# 📧 Serverless Email API (Zoho SMTP)

This project provides a lightweight HTTP API for sending emails using Zoho Mail SMTP.
It supports CORS, JSON requests, input validation, and both plain text + HTML messages.

# 🚀 Features

✅ Accepts GET, POST, and OPTIONS requests

✅ Validates required fields before sending

✅ Supports plain text + HTML email bodies

✅ CORS enabled (can be called from frontend apps directly)

✅ Runs on serverless platforms (Vercel, Netlify, AWS Lambda, etc.)

✅ Secure authentication with Zoho Mail

# 📂 Project Structure
.

├── handler.py      # Main API handler

├── template.py     # (Optional) HTML template helper

└── README.md       # Documentation

# ⚙️ Requirements
Python 3.9+

A valid Zoho Mail account (with SMTP access enabled)

Install dependencies (if not included in your serverless runtime):

*pip install secure-smtplib*

# 📡 API Endpoints

1. Health Check (GET)
 
GET /

Response:
```
{
  "status": "success",
  "message": "GET request received"
}
```

2. Send Email (POST)

POST /

Content-Type: application/json

Request Body (JSON)

```
{
  "SUBJECT": "Hello from API",
  
  "MESSAGE": "This is the plain text version.",
  
  "SENDER_EMAIL": "youraccount@zoho.com",
  
  "SENDER_PASSWORD": "your_zoho_app_password",
  
  "RECEIVER_EMAIL": "recipient@example.com",
  
  "HTML_MESSAGE": "<h1>Hello</h1><p>This is an <b>HTML</b> email.</p>"
  
}
```

Success Response
```
{
  "success": "Email sent successfully!"
}
```

Error Response (validation failure)
```
{
  "status": "error",
  "errors": {
    "MESSAGE": "This field cannot be empty.",
    "RECEIVER_EMAIL": "This field cannot be empty."
  }
}
```

Error Response (server error)
```
{
  "error": "An error occurred while processing your request."
}
```

# 🔐 Security Notes

Always use a Zoho App Password, not your main Zoho account password.

Store sensitive values like SENDER_EMAIL and SENDER_PASSWORD in environment variables on your serverless platform.

Do not hardcode credentials in your code.


🛠️ Deploying

1. Vercel

Put handler.py inside api/ directory.

Add Zoho credentials as environment variables in Vercel dashboard.

Deploy — your endpoint will be available at:

https://yourproject.vercel.app/api/handler


2. Netlify Functions

Place the file under netlify/functions/handler.py.

Configure Netlify to handle Python functions.

Deploy — endpoint will be at:

https://yourproject.netlify.app/.netlify/functions/handler

# 📌 Example Usage (JavaScript Fetch)
```
fetch("https://yourproject.vercel.app/api/handler", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(
  {
    SUBJECT: "Hello",
    MESSAGE: "Plain text version",
    SENDER_EMAIL: "your@zoho.com",
    SENDER_PASSWORD: "zoho_app_password",
    RECEIVER_EMAIL: "user@example.com",
    HTML_MESSAGE: "<h1>Hello</h1><p>This is HTML</p>"
  })
})
.then(res => res.json())
.then(console.log)
.catch(console.error);
```

# 📝 License
MIT License – feel free to use and modify.

