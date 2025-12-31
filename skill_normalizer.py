# skill_normalizer.py

ALIAS_MAP = {
    "machine learning": ["ml"],
    "deep learning": ["dl"],
    "natural language processing": ["nlp"],
    "scikit-learn": ["sklearn", "scikit learn"],
    "javascript": ["js"],
    "node.js": ["node"],
    "kubernetes": ["k8s"],
    "postgresql": ["postgres"],
    "amazon web services": ["aws"],
    "continuous integration": ["ci"],
    "continuous deployment": ["cd"]
}

def normalize_text(text: str) -> str:
    text = text.lower()
    for canonical, aliases in ALIAS_MAP.items():
        for alias in aliases:
            text = text.replace(alias, canonical)
    return text
