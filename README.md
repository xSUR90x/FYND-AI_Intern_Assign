#Yelp Rating Prediction Using LLM Prompting:
This project implements LLM-based rating prediction for Yelp reviews using different prompting strategies.
The goal is to classify each review into 1–5 stars and return strict JSON output

##Overview

The objective of Task 1 is to explore how different prompting techniques affect:

 Accuracy

 MAE (Mean Absolute Error)

 JSON validity rate

 Reliability of responses

We evaluate multiple prompt designs on a sample of 200 Yelp reviews and compare performance.

Dataset

Yelp Reviews Dataset:
https://www.kaggle.com/datasets/omkarsabnis/yelp-reviewsdataset

Used fields:

text → Review text

stars → Actual rating

A random sample of 200 reviews is used for efficiency and reproducibility.

LLM Used

Gemini 2.5 Flash (via LangChain)

Temperature kept low for stable results


##Prompting Strategies

We implemented three different prompting approaches to compare their behavior:

1️⃣ Zero-Shot Prompting (template_v1)

Simple instruction-based prompt

No examples

Baseline performance

High JSON validity

2️⃣ Rubric-Based Prompting (template_v2)

The model is given a clear rating rubric

Helps structure reasoning

Better accuracy & MAE

JSON validity slightly lower due to stricter rules

3️⃣ Few-Shot + Internal CoT (template_v3)

Three worked-out examples

Hidden internal chain-of-thought

Very high JSON validity

More stable predictions

 Evaluation Metrics

Each strategy is evaluated on:

Accuracy

Mean Absolute Error (MAE)

JSON Validity Rate

Total samples processed

The evaluation pipeline:

Runs the LLM once per review

Parses output safely

Counts only valid predictions for accuracy/MAE

Measures JSON format compliance separately


##Discussion

Rubric-based prompting improved accuracy and MAE, showing the model benefits from a structured scoring guideline.

Few-shot prompting provided more stable JSON output with strong performance.

Zero-shot produced the highest JSON validity but weaker predictions.

Each method demonstrates different strengths:

Approach	      Strength
Zero-shot	    Simple, reliable formatting
Rubric	        Best rating accuracy
Few-shot CoT	Best JSON stability + consistent reasoning

##How to Run

Install dependencies:

pip install -r requirements.txt


Add your Gemini API key to .env:

GOOGLE_API_KEY=your_key_here


Run the notebook:
Open prompt.ipynb and execute all cells.

#AI Feedback System – User & Admin Dashboards

This project contains the complete implementation of Task 2 for the Fynd AI Intern Assessment.
It includes a user-facing dashboard to collect feedback and an internal admin dashboard to analyze and manage submissions.
The system runs on a Flask backend with an SQLite database and an LLM-powered AI engine using Gemini + LangChain.

## Usage:

Open the User Dashboard from the link below, where anyone can submit feedback:

🔗 User Dashboard:
https://xsur90x-ai-frontend-home-62hkdo.streamlit.app/

Users can provide:

A rating

A written review

Once submitted, the system generates an AI-powered response based on the sentiment and content of the review. This response is produced using Gemini 2.5 Flash via LangChain, and only the final AI response is shown to the user.

All feedback is stored automatically in the backend database.

Admin Dashboard

To access the internal dashboard, use:

🔗 Admin Dashboard:
https://xsur90x-ai-frontend-home-62hkdo.streamlit.app/ADMIN_dashboard

Password: admin123

The admin dashboard shows:

User rating

Review text

AI-generated summary

AI-recommended improvements

Timestamp

It also supports:

Sorting (by time or urgency)

Pagination

Analytics (total reviews, sentiment distribution, average rating)

Rating distribution chart

Because the backend is deployed on a free tier, you may need to wait a few seconds if the server is waking up.
How the System Works

The system uses a Flask API to receive and store feedback.
Every user submission triggers a two-step AI process:

Sentiment Classification
The review (and rating) is passed to an LLM that determines whether it is positive or negative.

Response + Summary Generation
Based on the sentiment, a specific prompt is used to generate:

A user-facing response

A short summary for admins

Actionable recommendations for the business team

This is implemented using LangChain’s RunnableBranch to dynamically route the request to the appropriate prompt.

All generated outputs are saved to the database and used in the admin dashboard.

# Running Locally:

To run the project locally:

Backend
cd Backend
pip install -r requirements.txt
python app.py

Frontend
cd Frontend
pip install -r requirements.txt
streamlit run Home.py


Make sure to set your Gemini API key in a .env file:

GOOGLE_API_KEY=your_key_here

# Deployment Links:

User Dashboard:
https://xsur90x-ai-frontend-home-62hkdo.streamlit.app/

Admin Dashboard:
https://xsur90x-ai-frontend-home-62hkdo.streamlit.app/ADMIN_dashboard

Password: admin123

Both services are fully deployed and connected to the Flask backend.
