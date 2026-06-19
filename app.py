from src.classifier import classify_persona
from src.rag_pipeline import RAGPipeline
from src.generator import generate_response
from src.escalator import should_escalate, generate_handoff

rag = RAGPipeline()
rag.create_chunks()

print("\nPersona Adaptive Support Agent")
print("-" * 40)

while True:

    query = input("\nEnter Query (or exit): ")

    if query.lower() == "exit":
        break

    persona_result = classify_persona(query)

    if isinstance(persona_result, dict):
        persona = persona_result.get("persona", "Unknown")
    else:
        persona = str(persona_result)

    retrieved = rag.retrieve(query)

    print("\nDetected Persona:")
    print(persona)

    print("\nRetrieved Sources:")

    docs = []

    for item in retrieved:
        print(item["source"])
        docs.append(item["source"])

    if should_escalate(query, retrieved):

        print("\nESCALATION REQUIRED")

        summary = generate_handoff(
            persona,
            query,
            docs
        )

        print(summary)

    else:

        context = "\n".join(
            [chunk["text"] for chunk in retrieved]
        )

        answer = generate_response(
            query,
            persona,
            context
        )

        print("\nResponse:")
        print(answer)