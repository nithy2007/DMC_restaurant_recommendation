import json

loaded_data = {}

def load_data_once(base_path, cuisine, dish_file):
    if "cuisine_biz_id" not in loaded_data:
        with open(f"{base_path}/yelp_cuisine_biz_id_dict.json", 'r') as f:
            loaded_data["cuisine_biz_id"] = json.load(f)

    if "biz_metadata" not in loaded_data:
        with open(f"{base_path}/yelp_academic_dataset_business.json", 'r') as f:
            loaded_data["biz_metadata"] = [json.loads(line) for line in f]

    if "res_reviews" not in loaded_data:
        with open(f"{base_path}/sampled_restaurant_reviews_with_sentiment.json", 'r') as f:
            loaded_data["res_reviews"] = [json.loads(line) for line in f if line.strip()]

    with open(dish_file, 'r') as f:
        loaded_data["dish_list"] = [line.strip().lower() for line in f if line.strip()]

    # Build name + city dict
    biz_id_name_dict = {}
    for record in loaded_data["biz_metadata"]:
        if record["business_id"] in loaded_data["cuisine_biz_id"].get(cuisine, []):
            biz_id_name_dict[record["business_id"]] = (record["name"], record["city"])
    loaded_data["biz_id_name_dict"] = biz_id_name_dict

def get_top_restaurants(cuisine, target_dish, base_path, dish_file, top_n=50):
    load_data_once(base_path, cuisine, dish_file)

    biz_id_positive_review_counts = {}

    # Filter by cuisine and presence of dish in review
    for record in loaded_data["res_reviews"]:
        biz_id = record.get("business_id")
        review = record.get("text", "").lower()
        sentiment = record.get("sentiment", "")
        if biz_id in loaded_data["cuisine_biz_id"].get(cuisine, []):
            if target_dish.lower() in review and sentiment == "POSITIVE":
                if biz_id not in biz_id_positive_review_counts:
                    biz_id_positive_review_counts[biz_id] = 0
                biz_id_positive_review_counts[biz_id] += 1

    # Sort and pick top N
    sorted_biz = sorted(biz_id_positive_review_counts.items(), key=lambda x: x[1], reverse=True)
    top_biz_ids = sorted_biz[:top_n]

    # Build readable labels
    results = []
    for biz_id, count in top_biz_ids:
        name, city = loaded_data["biz_id_name_dict"].get(biz_id, ("Unknown", "Unknown"))
        label = f"{name} ({city}) → {count} positive reviews"
        results.append(label)

    return results
