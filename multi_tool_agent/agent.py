from zoneinfo import ZoneInfo
from google.adk.agents import Agent
import requests


def suggest_meal(preferences: str) -> dict:
    """Suggests a meal based on user preferences using TheMealDB API."""
    try:
        if "vegetarian" in preferences.lower():
            url = "https://www.themealdb.com/api/json/v1/1/filter.php?c=Vegetarian"
        elif "chicken" in preferences.lower() or "high protein" in preferences.lower():
            url = "https://www.themealdb.com/api/json/v1/1/filter.php?i=Chicken"
        else:
            url = "https://www.themealdb.com/api/json/v1/1/random.php"

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "meals" in data and data["meals"]:
            meal = data["meals"][0]
            return {
                "status": "success",
                "meal": meal.get("strMeal"),
                "image": meal.get("strMealThumb"),
                "id": meal.get("idMeal")
            }
        else:
            return {"status": "error", "error_message": "No meals found matching your preferences."}

    except Exception as e:
        return {"status": "error", "error_message": str(e)}


def generate_grocery_list(meal_plan: list[str]) -> dict:
    """Generates a grocery list based on the selected meal plan."""
    grocery_db = {
        "Grilled vegetable quinoa salad with lemon dressing.": ["Quinoa", "Bell peppers", "Zucchini", "Lemon", "Olive oil"],
        "Grilled chicken breast with steamed broccoli and brown rice.": ["Chicken breast", "Broccoli", "Brown rice"],
        "Avocado toast with boiled eggs.": ["Bread", "Avocado", "Eggs"],
        "Pasta with tomato sauce and side salad.": ["Pasta", "Tomato sauce", "Lettuce", "Cucumber"]
    }

    grocery_list = []
    for meal in meal_plan:
        grocery_list.extend(grocery_db.get(meal, []))

    if not grocery_list:
        return {"status": "error", "error_message": "No grocery items found for the selected meals."}

    return {"status": "success", "grocery_list": list(set(grocery_list))}


root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash",
    description="Agent to suggest meals and generate grocery lists based on preferences.",
    instruction="You help users plan meals based on their preferences and create efficient grocery lists.",
    tools=[suggest_meal, generate_grocery_list],
)
