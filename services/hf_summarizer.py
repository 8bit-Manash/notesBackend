from transformers import pipeline

# 🔹 Global variable (initially empty)
_summarizer = None

def get_summarizer():
    global _summarizer
    if _summarizer is None:
        print("⏳ Loading summarization model...")
        _summarizer = pipeline(
            "summarization",
            model="google/flan-t5-small"
        )
        print("✅ Model loaded")
    return _summarizer


def summarize_text_hf(text: str) -> str:
    summarizer = get_summarizer()

    summary = summarizer(
        "summarize: " + text,
        max_length=120,
        min_length=50,
        do_sample=True,
        temperature=0.7
    )


    return summary[0]["summary_text"]
