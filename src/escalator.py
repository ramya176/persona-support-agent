def should_escalate(query, retrieved_chunks):

    escalation_keywords = [
        "refund",
        "legal",
        "lawsuit",
        "billing",
        "account deletion"
    ]

    query = query.lower()

    for word in escalation_keywords:
        if word in query:
            return True

    if len(retrieved_chunks) == 0:
        return True

    return False


def generate_handoff(persona, query, docs):

    summary = {
        "persona": persona,
        "issue": query,
        "documents_used": docs,
        "recommendation": "Human support investigation required"
    }

    return summary