import asyncio
from app.services.gmail import get_gmail_service, get_unread_emails, send_email, mark_as_read
from app.agent.graph import agent
import traceback

async def poll_gmail(professor_email: str, user_id: str, poll_interval: int = 30):
    service = get_gmail_service()

    while True:
        try:
            emails = get_unread_emails(service, professor_email)

            for email in emails:
                if not email.get("sender", ""):
                    continue

                result = agent.invoke({
                    "subject": email.get('subject', ''),
                    "body": email.get("body", ""),
                    "user_id": user_id,
                    "category": "",
                    "retrieved_context": "",
                    "decision": "",
                    "draft_reply": ""
                })

                if result["category"] == "spam":
                    continue
                elif result["draft_reply"] != "":
                    send_email (
                        service=service,
                        to=email.get("sender", ""),
                        subject=f"Re: {email.get('subject', '')}",
                        body=result["draft_reply"]
                    )
                    send_email (
                        service=service,
                        to=professor_email,
                        subject=f"[Auto-replied] {email.get('subject', '')}",
                        body=f"Auto-replied to:\nFrom: {email.get('sender', '')}\nSubject: {email.get('subject', '')}\n\nReply:\n{result['draft_reply']}"
                    )
                else:
                    send_email (
                        service=service,
                        to=professor_email,
                        subject=f"[Needs attention] {email.get('subject', '')}",
                        body=f"This email needs your response:\n\nFrom: {email.get('sender', '')}\nSubject: {email.get('subject', '')}\n\nBody:\n{email.get('body', '')}\n\nView email: https://mail.google.com/mail/u/0/#inbox/{email.get('id', '')}"
                    )
                mark_as_read(service, email.get("id", ""))
                
        except Exception as e:
            print(f"polling error: {e}")
            traceback.print_exc()

        await asyncio.sleep(poll_interval)
                