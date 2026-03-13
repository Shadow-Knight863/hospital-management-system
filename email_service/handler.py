import json

def send_email(event, context):

    body = json.loads(event["body"])

    email = body.get("email")
    action = body.get("action")

    if action == "SIGNUP_WELCOME":
        message = f"Welcome {email}! Thanks for signing up."

    elif action == "BOOKING_CONFIRMATION":
        message = f"Appointment confirmed for {email}"

    else:
        message = "Unknown email action"

    print("EMAIL SENT:", message)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": message
        })
    }