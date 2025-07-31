from collections import defaultdict
import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Load the sentiment model once
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, truncation=True)

# Global cache to avoid reloading files
loaded_data = {}

def load_data_once(base_path, cuisine, dish_file):
    if "biz_id_dict" not in loaded_data:
        # Load all datasets once
        with open(f"{base_path}/yelp_preprocessed_data/yelp_cuisine_biz_id_dict.json", 'r') as f:
            loaded_data["cuisine_biz_id"] = json.load(f)

        with open(f"{base_path}/yelp_src_dataset/yelp_academic_dataset_business.json", 'r') as f:
            loaded_data["biz_metadata"] = [json.loads(line) for line in f]

        with open(f"{base_path}/yelp_preprocessed_data/sampled_restaurant_reviews.json", 'r') as f:
            loaded_data["res_reviews"] = [json.loads(line) for line in f]

    with open(f"{base_path}/Task7_Application_system_development/{dish_file}", 'r') as f:
        loaded_data["dish_list"] = [line.strip().lower() for line in f]

    # Cache biz_id to name/city
    biz_id_name_dict = {}
    for record in loaded_data["biz_metadata"]:
        if record["business_id"] in loaded_data["cuisine_biz_id"].get(cuisine, []):
            biz_id_name_dict[record["business_id"]] = (record["name"], record["city"])
    loaded_data["biz_id_name_dict"] = biz_id_name_dict


def get_top_restaurants(cuisine, dish_name, base_path, dish_file, top_n=10):
    dish_name = dish_name.lower()

    # Load once if not loaded
    load_data_once(base_path, cuisine, dish_file)

    # Filter reviews for the cuisine and dish
    biz_ids = loaded_data["cuisine_biz_id"].get(cuisine, [])
    dish_list = loaded_data["dish_list"]
    res_reviews = loaded_data["res_reviews"]
    biz_id_name_dict = loaded_data["biz_id_name_dict"]

    # Match reviews with dishes
    res_dish_reviews = defaultdict(lambda: defaultdict(set))
    for review in res_reviews:
        if review["business_id"] in biz_ids:
            text = review["text"].lower()
            for dish in dish_list:
                if dish in text:
                    res_dish_reviews[review["business_id"]][dish].add(text)

    # Sentiment score aggregation
    biz_id_positive_review_counts = {}
    for biz_id, dish_reviews in res_dish_reviews.items():
        if dish_name in dish_reviews:
            positive_count = 0
            for review_text in dish_reviews[dish_name]:
                result = sentiment_pipeline(review_text)[0]
                if result['label'] == "POSITIVE" and result['score'] > 0.80:
                    positive_count += 1
            biz_id_positive_review_counts[biz_id] = positive_count

    # Sort and prepare output
    sorted_biz_ids = sorted(biz_id_positive_review_counts.items(), key=lambda x: x[1], reverse=True)
    output = []
    for biz_id, count in sorted_biz_ids[:top_n]:
        name, city = biz_id_name_dict.get(biz_id, ("Unknown", "Unknown"))
        output.append({"Restaurant": name, "City": city, "Positive_review_count": count})

    return output
