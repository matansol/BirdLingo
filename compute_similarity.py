"""Compute bird similarity based on English name word overlap.

Birds with similar names are the most confusing distractors.
E.g. "House Sparrow" vs "House Finch", "Great Blue Heron" vs "Great Egret"

Similarity score = number of shared words + partial word bonus.
Top 20 similar birds saved per bird, shuffled each time in the app.
"""
import json
import re

birds_data_path = 'BirdLingo/assets/birds_data.json'
output_path = 'BirdLingo/assets/bird_similarity.json'

bd = json.load(open(birds_data_path, 'r', encoding='utf-8'))
print(f"Loaded {len(bd)} birds")

def tokenize(name):
    """Split name into lowercase words, removing punctuation."""
    return set(re.findall(r"[a-z]+", name.lower()))

def word_similarity(name_a, name_b):
    """Compute similarity based on shared words and partial matches."""
    words_a = tokenize(name_a)
    words_b = tokenize(name_b)
    
    if not words_a or not words_b:
        return 0.0
    
    score = 0.0
    
    # Exact word matches (strongest signal)
    shared = words_a & words_b
    score += len(shared) * 3.0
    
    # Partial matches: words that share a common root (>= 4 chars)
    for wa in words_a - shared:
        for wb in words_b - shared:
            # Check if one word starts with the other (e.g. "eagle" / "eagles")
            if len(wa) >= 4 and len(wb) >= 4:
                if wa.startswith(wb[:4]) or wb.startswith(wa[:4]):
                    score += 1.5
                    break
    
    return score

# Compute similarity
similarity = {}

for i, bird_a in enumerate(bd):
    name_a = bird_a['names']['en']
    scores = []
    
    for j, bird_b in enumerate(bd):
        if i == j:
            continue
        name_b = bird_b['names']['en']
        s = word_similarity(name_a, name_b)
        if s > 0:
            scores.append((bird_b['id'], s))
    
    # Sort by score descending, take top 20
    scores.sort(key=lambda x: -x[1])
    top_20 = [bird_id for bird_id, _ in scores[:20]]
    similarity[bird_a['id']] = top_20

# Save
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(similarity, f)

print(f"Generated similarity map for {len(similarity)} birds")

# Show examples
for ex in bd[:5]:
    sim_ids = similarity.get(ex['id'], [])[:5]
    sim_names = []
    for sid in sim_ids:
        sb = next((b for b in bd if b['id'] == sid), None)
        if sb:
            sim_names.append(sb['names']['en'])
    print(f"\n{ex['names']['en']}:")
    if sim_names:
        print(f"  Similar: {', '.join(sim_names)}")
    else:
        print(f"  (no similar names)")

# Show some interesting matches
print("\n--- Birds with most similar options ---")
for bird in bd:
    sim_ids = similarity.get(bird['id'], [])
    if sim_ids:
        first_sim = next((b for b in bd if b['id'] == sim_ids[0]), None)
        if first_sim:
            s = word_similarity(bird['names']['en'], first_sim['names']['en'])
            if s >= 6:
                print(f"  {bird['names']['en']} <-> {first_sim['names']['en']} (score={s})")
