# AI Expense Insights using Google Gemini

import os
from dotenv import load_dotenv
from google import genai
from sqlalchemy.orm import Session

# Import our existing CRUD so we reuse the analytics we already built
from app import crud

# Load the GEMINI_API_KEY from .env
load_dotenv()


# Generate natural-language insights for one user's expenses
def get_ai_insights(db: Session, user_id: int):

    # Reuse the analytics functions we already have
    total = crud.get_total_expenses(db, user_id)["total_expenses"]
    by_category = crud.get_expenses_by_category(db, user_id)

    # If the user has no expenses yet, skip calling the AI
    if not by_category:
        return {
            "insights": "No expenses yet. Add some expenses to get AI insights."
        }

    # Turn the category totals into simple text for the prompt
    category_lines = "\n".join(
        f"- {category}: {amount}" for category, amount in by_category
    )

    # Build the prompt we send to Gemini
    prompt = (
        "You are a friendly personal finance assistant. "
        "Here is a user's expense data:\n\n"
        f"Total spending: {total}\n"
        f"Spending by category:\n{category_lines}\n\n"
        "In simple language, give: "
        "1) a short spending summary, "
        "2) the highest spending category, "
        "3) two personalized money-saving recommendations. "
        "Keep it under 120 words."
    )

    # Call Gemini and return the text
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return {
            "insights": response.text
        }

    except Exception as e:
        # Print the real reason in the server console for debugging
        print("AI error:", e)
        return {
            "insights": "AI is temporarily unavailable. Please try again later."
        }
