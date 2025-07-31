from flask import Flask, render_template, request, jsonify
import os
from get_restaurant_recommendations import get_top_restaurants

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Load cuisine list from a file
with open('cuisine_only_list.txt','r') as cuisine_file:
   cuisine_list =[line.strip() for line in cuisine_file]

@app.route("/restaurant_recommendation")
def home():
    return render_template("rest_recom.html", cuisines=cuisine_list)

@app.route("/default_dish_list", methods=["GET"])
def default_dish_list():
    try:
        with open("default_dish_list.txt", "r") as f:
            dishes = [line.strip() for line in f if line.strip()]
        return jsonify({"dishes": dishes})
    except Exception as e:
        print("Error loading default dish list:", e)
        return jsonify({"dishes": []})


@app.route("/upload_dish_file", methods=["POST"])
def upload_dish_file():
    if "dish_file" in request.files:
        dish_file = request.files["dish_file"]
        if dish_file.filename.endswith(".txt"):
            contents = dish_file.read().decode("utf-8")
            dishes = [line.strip() for line in contents.splitlines() if line.strip()]
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], "uploaded_dish_list.txt")
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(contents)
            return jsonify({"dishes": dishes})
    return jsonify({"dishes": []})

@app.route("/get_recommendations", methods=["POST"])
def recommend():
    cuisine = request.form.get("cuisine")
    dish = request.form.get("dish")
    use_default = request.form.get("use_default")

    if use_default:
        dish_file = "default_dish_list.txt"  # place in static folder or app directory
    else:
        dish_file = os.path.join(app.config['UPLOAD_FOLDER'], "uploaded_dish_list.txt")

    
    base_path="/Users/shanmugam/Documents/Nithya_MCS_DS_Illinois/Datamining_capstone/"
    results = get_top_restaurants(cuisine, dish, base_path, dish_file)
    if not results:
        return render_template("recommendation_result.html", recommendations=[],
                                                            selected_dish=dish,
                                                            selected_cuisine=cuisine,
                               message="No results found. Check if the dish file has dishes relevant to the selected cuisine, else use appropriate dish file")
    else:
        return render_template("recommendation_result.html", recommendations=results,
                                                            selected_dish=dish,
                                                            selected_cuisine=cuisine)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)
