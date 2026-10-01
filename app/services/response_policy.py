def build_generation_prompt(prompt: str, complexity: str) -> str:
    if complexity == "low":
        instruction = (
            "Answer the user's question directly and concisely. "
            "Keep the response short and easy to understand. "
            "Do not add unnecessary sections, background information, "
            "or extended examples unless they are needed to answer the question."
        )

    elif complexity == "medium":
        instruction = (
            "Give a clear and moderately detailed answer. "
            "Explain the important points needed to understand the topic. "
            "Use examples when they improve clarity, but avoid unnecessary detail."
        )

    else:
        instruction = (
            "Provide a detailed and structured answer. "
            "Explain the important concepts, reasoning, examples, "
            "and relevant considerations needed to answer the question thoroughly."
        )

    return f"""You are answering a user's question.

Response style:
{instruction}

User's question:
{prompt}
"""