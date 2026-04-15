# Restaurant Recommendation System (Based on Dish-Level Sentiment Analytics)

## Project Overview

This project is a full-stack **data-driven restaurant recommendation system** that goes beyond traditional rating-based suggestions. Instead of recommending restaurants in general, the system provides **dish-specific recommendations** by analyzing **real Yelp customer reviews** using sentiment analysis.

The application allows users to select a cuisine and a dish and dynamically explore the **best-rated restaurants for a specific dish**, based on the volume of **positive sentiment mentions in reviews**.

This project demonstrates an end-to-end pipeline combining:
- Large-scale text processing
- Sentiment analysis
- Data filtering & ranking
- Web application development
- Cloud deployment (AWS EC2)

---

## Key Features

-  **Dish-level recommendation engine** (fine-grained insights beyond restaurant ratings)
-  **Sentiment-driven ranking** using Yelp review text
-  Supports **user-uploaded dish lists** for dynamic input processing
-  Optimized using **precomputed sentiment data** (handles large datasets efficiently)
-  Fully deployed as a **Flask web application on AWS EC2**
-  Real-time ranking of restaurants based on **positive review frequency per dish**
-  Supports both **default and user-defined inputs**

---

## System Highlights (What Makes This Project Strong)

- Designed a **custom recommendation pipeline** combining NLP + structured filtering
- Built a **cuisine → restaurant → review → sentiment → ranking pipeline**
- Solved scalability issues by moving to **preprocessed sentiment storage**
- Handled real-world constraints such as:
  - Large dataset processing limitations
  - Cloud deployment constraints (EC2 memory/compute limits)
- Implemented **user-driven data ingestion** through file upload interface

---

## Architecture Overview

**User → Flask Web App → Data Processing Layer → Sentiment Filter → Ranking Engine → UI Output**

- Frontend: HTML + JavaScript
- Backend: Flask (Python)
- Data Processing: Pandas / JSON parsing / NLP sentiment labels
- Deployment: AWS EC2 (t2.medium)
- Storage: Local + optional AWS S3 integration

---

## How It Works

1. User selects a **cuisine**
2. User provides a **dish list (upload or default option)**
3. System filters Yelp reviews for:
   - Matching cuisine
   - Matching dish mentions
4. Sentiment-labeled reviews are used to:
   - Count **positive mentions per restaurant**
5. Restaurants are ranked and top results are displayed

---

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Flask (Python)
- **NLP:** Sentiment Analysis (VADER / precomputed labels)
- **Data Processing:** JSON, Pandas
- **Cloud:** AWS EC2
- **Storage (optional):** AWS S3

---

## Project Structure
project/
│
├── app.py
├── get_restaurant_recommendations.py
│
├── templates/
│ ├── rest_recomm.html
│ └── recommendation_result.html
│
├── static/
│ └── bg.jpg
│
├── data/
│ ├── yelp_cuisine_biz_id_dict.json
│ ├── yelp_academic_dataset_business.json
│ └── sampled_restaurant_reviews_with_sentiment.json
│
├── uploaded_files/
│ └── uploaded_dish_list.txt
## Deployment Details

- Hosted on: **AWS EC2 (t2.medium)**
- Flask server runs on port `5000`
- Public access via EC2 IP:

http://<EC2-PUBLIC-IP>:5000
Input Format (User Upload)

Users can upload a `.txt` file containing dish names:


butter chicken
biryani
naan
fried rice
tacos


Each line represents a dish used for recommendation queries.

---

## Engineering Challenges Solved

- Handled large-scale Yelp dataset processing
- Reduced runtime bottlenecks using **precomputed sentiment data**
- Designed a scalable workflow suitable for constrained cloud environments
- Integrated real-time user input with offline data mining outputs

---

## Future Improvements

- Replace keyword matching with **semantic search (BERT embeddings)**
- Add **personalized recommendations**
- Integrate **Google Maps/Yelp links for restaurants**
- Deploy using **AWS Lambda + API Gateway (serverless architecture)**
- Improve UI with React-based frontend

  
