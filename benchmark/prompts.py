TEST_PROMPTS = [
    # ---------------------------------------------------------
    # Coding
    # ---------------------------------------------------------
    {
        "id": 1,
        "category": "coding",
        "prompt": "Write a Python function that checks whether a string is a palindrome."
    },
    {
        "id": 2,
        "category": "coding",
        "prompt": "Implement binary search in Python and explain its time complexity."
    },
    {
        "id": 3,
        "category": "coding",
        "prompt": "Write a Django REST Framework serializer for a User model with name and email fields."
    },

    # ---------------------------------------------------------
    # Explanation
    # ---------------------------------------------------------
    {
        "id": 4,
        "category": "explanation",
        "prompt": "Explain how database indexing works and when an index should be used."
    },
    {
        "id": 5,
        "category": "explanation",
        "prompt": "Explain the difference between authentication and authorization with an example."
    },
    {
        "id": 6,
        "category": "explanation",
        "prompt": "Explain how HTTP requests and responses work between a browser and a server."
    },

    # ---------------------------------------------------------
    # Reasoning
    # ---------------------------------------------------------
    {
        "id": 7,
        "category": "reasoning",
        "prompt": "A service has a 2% failure rate per request. If 100 independent requests are made, what is the expected number of failures?"
    },
    {
        "id": 8,
        "category": "reasoning",
        "prompt": "A system processes 500 requests per second and each request requires 200 milliseconds of processing time. Estimate the number of concurrently processing requests using Little's Law."
    },
    {
        "id": 9,
        "category": "reasoning",
        "prompt": "Compare a monolithic architecture with microservices for a small startup and explain the main trade-offs."
    },

    # ---------------------------------------------------------
    # Debugging
    # ---------------------------------------------------------
    {
        "id": 10,
        "category": "debugging",
        "prompt": "Why would an async Python program become slow if it uses time.sleep() inside an async function?"
    },
    {
        "id": 11,
        "category": "debugging",
        "prompt": "A Django API returns 405 Method Not Allowed for an OPTIONS request from the frontend. What could cause this?"
    },

    # ---------------------------------------------------------
    # Summarization
    # ---------------------------------------------------------
    {
        "id": 12,
        "category": "summarization",
        "prompt": "Summarize the purpose of REST APIs in three concise points."
    },
    {
        "id": 13,
        "category": "summarization",
        "prompt": "Summarize the main benefits and drawbacks of using PostgreSQL in a web application."
    },

    # ---------------------------------------------------------
    # Mathematics
    # ---------------------------------------------------------
    {
        "id": 14,
        "category": "math",
        "prompt": "Calculate the HCF and LCM of 24 and 36 and explain the method."
    },
    {
        "id": 15,
        "category": "math",
        "prompt": "If an API costs $0.50 per million input tokens, how much would 250,000 input tokens cost?"
    },

    # ---------------------------------------------------------
    # Technical architecture
    # ---------------------------------------------------------
    {
        "id": 16,
        "category": "architecture",
        "prompt": "Design a basic architecture for a real-time chat application using React, Django, PostgreSQL, and WebSockets."
    },
    {
        "id": 17,
        "category": "architecture",
        "prompt": "Explain how Redis could be used in a web application and give three practical use cases."
    },

    # ---------------------------------------------------------
    # AI / LLM
    # ---------------------------------------------------------
    {
        "id": 18,
        "category": "ai",
        "prompt": "Explain what Retrieval-Augmented Generation is and why vector databases are commonly used with it."
    },
    {
        "id": 19,
        "category": "ai",
        "prompt": "Explain the difference between a traditional chatbot and an AI agent."
    },

    # ---------------------------------------------------------
    # Complex reasoning
    # ---------------------------------------------------------
    {
        "id": 20,
        "category": "complex_reasoning",
        "prompt": (
            "Design a cost-aware LLM routing strategy that decides between "
            "cheap, medium, and powerful models based on query complexity. "
            "Explain the routing signals, fallback strategy, quality verification, "
            "and how you would evaluate whether the system actually reduces cost "
            "without significantly reducing response quality."
        )
    },
]


def get_test_prompts() -> list[dict]:
    """Return the benchmark evaluation prompts."""
    return TEST_PROMPTS.copy()