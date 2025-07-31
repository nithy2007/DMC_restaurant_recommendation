# 🍽️ Restaurant Recommendation Web App

This Flask-based web application recommends top restaurants based on a selected **cuisine** and **dish**. 
The system uses review data from Yelp and applies **sentiment analysis** to rank restaurants that serve a particular dish positively.

## 🚀 Features

- Upload your own **dish list file** or use a **default dish list**
- Select a **cuisine** from the dropdown
- Select a **dish** dynamically loaded from the dish list
- Get top recommended restaurants for the selected dish using sentiment-based ranking
- Simple and intuitive **web interface**
- Deployable on **AWS EC2**

---

## 📂 File Structure
restaurant-recommendation-app/
│
├── restau_recommendation_app.py # Main Flask app
├── get_restaurant_recommendations.py # Logic to compute top restaurants
├── cuisine_only_list.txt # List of cuisines to populate cuisine dropdown
├── default_dish_list.txt # Used if user doesn't have their own dish list(Works for Indian cuisine)
├── requirements.txt # Python dependencies
│
├── templates/
│ ├── rest_comm.html # Home page with form
│ └── recommendation_result.html # Results page
│
├── static/
│ └── background.jpg # Background image (optional)
│
└── README.md # This file

##  How It Works

1. **User selects a cuisine**
2. **Uploads a dish list** or uses the default one
3. The app loads dish names into a dropdown
4. User selects a dish and clicks **Get Recommendations**
5. The backend:
   - Filters Yelp reviews for that dish in restaurants offering the selected cuisine
   - Uses a fine-tuned BERT sentiment model to find **positive reviews**
   - Ranks restaurants based on the number of positive reviews
6. Results are displayed on a new page

---

##  Run Locally

### 1. Clone the repo
git clone https://github.com/your-username/restaurant-recommendation-app.git
cd restaurant-recommendation-app

2. Create a virtual environment (optional)
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

4. Install dependencies
pip install -r requirements.txt

4. Run the app
python restau_recommendation_app.py

Then open http://localhost:5000 in your browser.

This project is part of the Data Mining Capstone Project and is intended for educational/demo purposes only.

