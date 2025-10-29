import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from tqdm import tqdm

# File paths
input_file = "sampled_restaurant_reviews.json"
output_file = "sampled_restaurant_reviews_with_sentiment.json"

# Initialize VADER
analyzer = SentimentIntensityAnalyzer()

# Load input reviews
with open(input_file, "r", encoding="utf-8") as f:
    reviews = [json.loads(line) for line in f]

# Add sentiment field
for review in tqdm(reviews):
    text = review.get("text", "")
    score = analyzer.polarity_scores(text)
    compound = score["compound"]
    if compound >= 0.5:
        sentiment = "POSITIVE"
    elif compound <= -0.5:
        sentiment = "NEGATIVE"
    else:
        sentiment = "NEUTRAL"
    review["sentiment"] = sentiment

# Save updated reviews
with open(output_file, "w", encoding="utf-8") as f:
    for review in reviews:
        f.write(json.dumps(review) + "\n")

print(f"✅ Done. Saved {len(reviews)} reviews with sentiment to '{output_file}'")