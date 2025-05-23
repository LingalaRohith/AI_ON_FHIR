import spacy
import re

nlp = spacy.load("en_core_web_sm")

# Fake dataset
patients_db = [
    {"id": "1", "name": "Alice Johnson", "age": 55, "conditions": ["diabetes"]},
    {"id": "2", "name": "Bob Smith", "age": 45, "conditions": ["covid"]},
    {"id": "3", "name": "Carlos Gomez", "age": 62, "conditions": ["cancer"]},
    {"id": "4", "name": "Diana Patel", "age": 28, "conditions": ["covid"]},
    {"id": "5", "name": "Ethan Lee", "age": 70, "conditions": ["copd", "hypertension"]},
    {"id": "6", "name": "Fiona Zhang", "age": 38, "conditions": ["hypertension"]},
    {"id": "7", "name": "Grace Kim", "age": 50, "conditions": ["covid", "diabetes"]}
]

# Normalize synonyms/adjectives to match dataset terms
condition_map = {
    "diabetic": "diabetes",
    "asthmatic": "asthma",
    "hypertensive": "hypertension"
}

# All known conditions from dataset
KNOWN_CONDITIONS = set(c for p in patients_db for c in p["conditions"])

# Words to ignore as candidate conditions
IGNORE_WORDS = {"show", "list", "find", "give", "get", "all", "patients", "patient", "with", "me"}

def parse_query(query):
    doc = nlp(query.lower())
    age_filter = {}
    conditions = []

    # Extract from noun chunks first
    for chunk in doc.noun_chunks:
        for word in chunk:
            if word.text in IGNORE_WORDS:
                continue
            normalized = condition_map.get(word.lemma_, word.lemma_)
            if normalized in KNOWN_CONDITIONS and normalized not in conditions:
                conditions.append(normalized)

    # Fallback to token loop
    if not conditions:
        for token in doc:
            if token.text not in IGNORE_WORDS and token.pos_ in {"NOUN", "ADJ"}:
                normalized = condition_map.get(token.lemma_, token.lemma_)
                if normalized in KNOWN_CONDITIONS and normalized not in conditions:
                    conditions.append(normalized)

    # Age filter logic
    age_match = re.search(r'\d+', query)
    if age_match:
        age_val = int(age_match.group())
        if "over" in query or "older than" in query:
            age_filter = {"operator": ">", "value": age_val}
        elif "under" in query or "younger than" in query:
            age_filter = {"operator": "<", "value": age_val}
        elif "between" in query:
            numbers = [int(n) for n in re.findall(r'\d+', query)]
            if len(numbers) == 2:
                age_filter = {"operator": "between", "value": numbers}

    return {
        "resourceType": "Patient",
        "conditions": conditions,
        "ageFilter": age_filter
    }

def simulate_fhir_response(parsed_query):
    conditions = parsed_query["conditions"]
    age_filter = parsed_query["ageFilter"]

    results = []
    for p in patients_db:
        if conditions:
            if not any(cond in p["conditions"] for cond in conditions):
                continue

        age = p["age"]
        if age_filter:
            op = age_filter["operator"]
            val = age_filter["value"]
            if op == ">" and not age > val:
                continue
            elif op == "<" and not age < val:
                continue
            elif op == "between" and not (val[0] <= age <= val[1]):
                continue

        results.append({
            "resourceType": "Patient",
            "id": p["id"],
            "name": [{"text": p["name"]}],
            "age": age,
            "condition": p["conditions"]
        })

    return {
        "resourceType": "Bundle",
        "type": "searchset",
        "total": len(results),
        "entry": results
    }

# Example queries
if __name__ == "__main__":
    queries = [
        "Show me all diabetic patients over 50",
        "List covid patients under 20",
        "Find cancer patients between 40 and 60",
        "Patients older than 70 with COPD",
        "Give me all patients with hypertension",
        "Find patients with covid and diabetes"
    ]

    for q in queries:
        print(f"🧠 Query: {q}")
        parsed = parse_query(q)
        print("🔍 Parsed:", parsed)
        simulated = simulate_fhir_response(parsed)
        print("📦 Simulated FHIR Response:", simulated)
        print("=" * 60)
