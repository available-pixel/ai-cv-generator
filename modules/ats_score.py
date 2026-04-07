# modules/ats_score.py

def calculate_ats_score(data):
    score = 0

    if data.get("name"): score += 10
    if data.get("email"): score += 10
    if data.get("skills"): score += 20
    if data.get("profile"): score += 15

    if any(e.get("job") for e in data.get("experience", [])):
        score += 15

    if any(p.get("name") for p in data.get("projects", [])):
        score += 15

    if any(e.get("degree") for e in data.get("education", [])):
        score += 15

    return min(score, 100)