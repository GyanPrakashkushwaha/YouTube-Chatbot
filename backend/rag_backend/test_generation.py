from rag_utils import (
    load_index,
    augment_query_with_context,
    convert_context_dict_to_text,
    generate_answer_with_gemini
)

video_id = "f8dhP521DHI"
query = "What is divide and conquer in simple words?"

print("Loading index...")
vs = load_index(video_id)

print("Retrieving context...")
aug = augment_query_with_context(vs, query, k=3)

context_text = convert_context_dict_to_text(aug["context"])

print("Sending to Gemini model...")
answer = generate_answer_with_gemini(context_text, query)

print("\nFINAL ANSWER:\n", answer)
