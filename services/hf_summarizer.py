from transformers import pipeline

# Load once (IMPORTANT)
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

def summarize_text_hf(text: str) -> str:
    # Handle very small notes
    if len(text.split()) < 40:
        return text

    summary = summarizer(
        text,
        max_length=120,
        min_length=60,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.9
    )


    return summary[0]["summary_text"]
