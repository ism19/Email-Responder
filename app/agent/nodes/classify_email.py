from state import EmailState
from chains.email_classifier import email_classifier

def classify_email(state: EmailState) -> EmailState:
    classification = email_classifier.invoke({"subject": state["subject"], "body": state["body"]})
    return {**state, "category": classification.category.value}
