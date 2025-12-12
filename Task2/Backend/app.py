from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from ai_engine import get_ai_outputs

app = Flask(__name__)
# -------------------- Database configuration --------------------

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///feedback.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
class Feedback(db.Model):
    """Table to store user feedback and AI-generated fields."""
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)               
    review = db.Column(db.Text, nullable=False)                 
    ai_response = db.Column(db.Text, nullable=False)             
    ai_summary = db.Column(db.Text, nullable=False)              
    ai_actions = db.Column(db.Text, nullable=False)              
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 

    def __repr__(self):
        return f"<Feedback id={self.id} rating={self.rating}>"

# Create the tables 
with app.app_context():
    db.create_all()
    
    
# -------------------- Routes --------------------

@app.route('/')
def hello_world():
    """Returns a simple greeting message for the home page."""
    return 'Flask is installed and working! Hello, World!'

# -------------------- API: GET for admin --------------------

@app.route("/api/feedback", methods=["GET"])
def list_feedback():
    feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()

    result = []
    for f in feedbacks:
        result.append({
            "id": f.id,
            "rating": f.rating,
            "review": f.review,
            "ai_response": f.ai_response,
            "ai_summary": f.ai_summary,
            "ai_actions": f.ai_actions,
            "created_at": f.created_at.isoformat(),
        })

    return jsonify(result), 200

# -------------------- API: POST for users --------------------

@app.route("/api/feedback", methods=["POST"])
def create_feedback():
   
    data = request.get_json() or {}

    # Basic validation
    rating = data.get("rating")
    review = (data.get("review") or "").strip()

    if rating is None:
        return jsonify({"error": "rating is required"}), 400
    try:
        rating = int(rating)
    except ValueError:
        return jsonify({"error": "rating must be an integer"}), 400

    if rating < 1 or rating > 5:
        return jsonify({"error": "rating must be between 1 and 5"}), 400

    if not review:
        return jsonify({"error": "review is required"}), 400

    # Get AI-generated fields
    ai = get_ai_outputs(rating, review)

    # Save to DB
    fb = Feedback(
        rating=rating,
        review=review,
        ai_response=ai["user_response"],
        ai_summary=ai["summary"],
        ai_actions=ai["actions"],
    )
    db.session.add(fb)
    db.session.commit()

    return jsonify({
        "ai_response": fb.ai_response
    }), 201



if __name__ == '__main__':
    app.run(debug=True)