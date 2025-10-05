import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading 'en_core_web_sm' model...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def extract_keywords(text: str) -> set:
    """Extracts significant keywords (nouns, proper nouns, verbs) from text."""
    doc = nlp(text)
    keywords = {
        token.lemma_.lower() for token in doc 
        if not token.is_stop and not token.is_punct and token.pos_ in ["NOUN", "PROPN", "VERB"]
    }
    return keywords

def compute_match_score(rewritten_text: str, job_keywords: set) -> float:
    """Computes the percentage of job keywords found in the rewritten CV."""
    if not job_keywords:
        return 0.0  # Avoid division by zero

    rewritten_keywords = extract_keywords(rewritten_text)
    common_keywords = rewritten_keywords.intersection(job_keywords)
    
    score = (len(common_keywords) / len(job_keywords))
    return min(score, 0.97) # Cap score at 1.0 (100%)
