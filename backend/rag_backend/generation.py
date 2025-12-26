from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()


def generate_answer_with_gemini(context_text, query):
    # Build the prompt exactly like notebook
    prompt_template = (
        "Use the following video context to answer the question.\n\n"
        "CONTEXT:\n"
        f"{context_text}\n\n"
        "QUESTION:\n"
        f"{query}\n\n"
        "Answer in a clear and concise way. Answer the questions if asked other than video context."
    )

    model = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash-lite", temperature = 0)

    # invoke() is the typical LangChain call for chat models
    response = model.invoke(prompt_template)

    # Extract final text
    return response.content


def convert_context_dict_to_text(context_dict):
    
    parts = []
    for key, value in context_dict.items():
        parts.append(f"[{key}]\n{value}\n")
    return "\n".join(parts)
