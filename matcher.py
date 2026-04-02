from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def compute_similarity(resume_text, jd_text):
    embeddings1 = model.encode(resume_text, convert_to_tensor=True)
    embeddings2 = model.encode(jd_text, convert_to_tensor=True)

    similarity = util.cos_sim(embeddings1, embeddings2)
    return float(similarity[0][0])

def rank_resumes(resumes, jd_text):
    results = []
    
    for resume in resumes:
        score = compute_similarity(resume["text"], jd_text)
        results.append((resume["name"], score))
    
    return sorted(results, key=lambda x: x[1], reverse=True)