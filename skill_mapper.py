# skill_mapper.py

import re
import pandas as pd
import spacy
from rapidfuzz import process, fuzz

nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[\W_]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


class SkillMapper:
    def __init__(self, csv_path="skills_master.csv", threshold=80):
        self.df = pd.read_csv(csv_path)
        self.threshold = threshold

        self.lookup = {}
        self.candidates = []

        for _, row in self.df.iterrows():
            skill_id = row["skill_id"]
            name = normalize(row["skill_name"])
            self.lookup[name] = skill_id
            self.candidates.append(name)

            if isinstance(row["aliases"], str):
                for alias in row["aliases"].split(","):
                    alias = normalize(alias)
                    self.lookup[alias] = skill_id
                    self.candidates.append(alias)

    def map_phrase(self, phrase):
        phrase = normalize(phrase)

        if phrase in self.lookup:
            return self.lookup[phrase], 100

        match = process.extractOne(
            phrase, self.candidates, scorer=fuzz.token_sort_ratio
        )

        if match and match[1] >= self.threshold:
            return self.lookup[match[0]], match[1]

        return None, 0


def extract_phrases(text: str):
    doc = nlp(text)
    phrases = set()

    tokens = [
        token.text.lower()
        for token in doc
        if token.is_alpha and len(token.text) > 2
    ]

    # unigrams
    for t in tokens:
        phrases.add(t)

    # bigrams (e.g. "power bi", "data analysis")
    for i in range(len(tokens) - 1):
        phrases.add(tokens[i] + " " + tokens[i + 1])

    return phrases
