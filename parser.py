import spacy
import re

nlp = spacy.load("en_core_web_sm")

def extract_text(text):
    return text

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return "Not Found"

def extract_email(text):
    match = re.search(r'\S+@\S+', text)
    return match.group() if match else "Not Found"

def extract_skills(text):
    skills_list = ["python", "java", "machine learning", "data science",
                   "sql", "tensorflow", "nlp", "excel"]
    
    text = text.lower()
    found_skills = [skill for skill in skills_list if skill in text]
    
    return list(set(found_skills))

def parse_resume(text):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "skills": extract_skills(text)
    }