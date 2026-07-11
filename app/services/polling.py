import asyncio
from app.services.gmail import get_gmail_service, get_unread_emails, send_email, mark_as_read
from app.agent.graph import agent

async def poll_gmail(professor_email: str, user_id: str, poll_interval: int = 600):
    service = get_gmail_service()

    while True:
        try:
            emails = get_unread_emails(service, professor_email)

            for email in emails:
                result = agent.invoke({
                    "email_subject": email["subject"],
                    "email_body": email["body"],
                    "user_id": user_id,
                    "email_category": "",
                    "retrieved_context": "",
                    "decision": "",
                    "draft_reply": ""
                })

                if result["draft_reply"] != "":
                    send_email (
                        service=service,
                        to=email["sender"],
                        subject=f"Re: {email['subject']}",
                        body=result["draft_reply"]
                    )
                    send_email (
                        service=service,
                        to=professor_email,
                        subject=f"[Auto-replied] {email['subject']}",
                        body=f"Auto-replied to:\nFrom: {email['sender']}\nSubject: {email['subject']}\n\nReply:\n{result['draft_reply']}"
                    )
                else:
                    send_email (
                        service=service,
                        to=professor_email,
                        subject=f"[Needs attention] {email['subject']}",
                        body=f"This email needs your response:\n\nFrom: {email['sender']}\nSubject: {email['subject']}\n\nBody:\n{email['body']}"
                    )
                mark_as_read(service, email["id"])
                
        except Exception as e:
            print(f"polling error: {e}")

        await asyncio.sleep(poll_interval)
                