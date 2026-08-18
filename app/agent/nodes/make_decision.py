from state import EmailState
from chains.decision_maker import decision_maker

def make_decision(state: EmailState) -> EmailState:
    decision = decision_maker.invoke({"subject": state["subject"], "body": state["body"], })
    return {**state, "decision": decision.}