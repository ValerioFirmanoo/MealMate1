import streamlit as st
import openai
import os
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

def main():
    #st.title("MeatMeal: Your Personalized Meal Planner")
    st.markdown("<h1 style='text-align: center; font-size: 48px;'>MealMate</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; opacity: 0.8;'>Your Personalized Meal Planner</h2>", unsafe_allow_html=True)

    pages = {
        "Iformation about yourself": page_survey,
        "Meal Plan": page_meal_plan
    }

    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()))

    page = pages[selection]
    page()

    
def page_survey():
    # Collecting user inputs
    with st.form("user_info"):
        st.header("Please tell us about yourself")
        sex = st.radio("Select your sex:", options=["Female", "Male", "Other"])
        weight = st.number_input("Enter your weight (in kg):", min_value=10)
        height = st.number_input("Enter your height (in cm):", min_value=50)
        purpose = st.selectbox("What is the purpose of your diet?", 
                               options=["Weight Loss", "Muscle Gain", "Maintaining Health", "Sportive Performance"])
        
        st.header("Dietary preferences")
        location = st.text_input("Where are you from?")
        cuisine_preference = st.selectbox("How much of your diet should consist of cuisine from your country?", 
                                          options=["Few", "Half", "More than half", "Total"])
        
        other_cuisine = st.text_area("List any other cuisines you particularly like:",
                                     placeholder="Chinese, Indian, Italian, etc. Leave blank if none.")

        dietary_preferences = st.selectbox("Do you have any dietary preferences?",
                           options=["Omnivore", "Vegan", "Vegetarian", "No Meat", "No Fish"])
            
        allergies_dislikes = st.text_area("List any food allergies or ingredients you dislike:",
                                 placeholder="Allergic to Wallnuts, Tuna, etc. I don't like asparagus or Indian food. Leave blank if none.")

        food_likes = st.text_area("List any food you particularly like:",
                                  placeholder="Pizza, Lasagne, Hamburger, Pasta Carbonara! Feel free to express yourself. Leave blank if you are a sad person.")

        food_habits = st.text_area("If you want to add some additional information about your food habits:",
                                   placeholder="E.g., 'I eat pasta every lunch', 'I eat the same breakfast every day', 'I like to eat pizza on Fridays'")

        st.header("Meal preferences")
        variety = st.radio("Would you prefer a variety of dishes day-to-day or similar things during the week?",
                           options=["Variety", "Similar"])
        complexity = st.selectbox("How do you prefer your dishes in terms of complexity?",
                                  options=["Simple", "Medium", "Elaborate"])
        budget = st.select_slider("What's your budget level for groceries?",
                                  options=["Low", "Medium", "High"])
        
        # Form submission button
        submitted = st.form_submit_button("Submit")
        if submitted:
             # Save form data to session state
            st.session_state['form_data'] = {
                "sex": sex, "weight": weight, "height": height, "purpose": purpose,
                "location": location, "cuisine_preference": cuisine_preference,
                "other_cuisine": other_cuisine, "food_likes": food_likes, "variety": variety,
                "dietary_preferences": dietary_preferences, "allergies_dislikes": allergies_dislikes,
                "complexity": complexity, "budget": budget, "food_habits": food_habits
            }
            st.session_state['submitted'] = True
            st.experimental_rerun()

def page_meal_plan():
    if 'submitted' not in st.session_state:
        st.warning("Please fill out the survey first.")
        st.stop()
    
    if st.button("Generate Meal Plan"):
        meal_plan = generate_meal_plan(st.session_state['form_data'])
        df = pd.DataFrame(meal_plan, columns=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        st.table(df)

def generate_meal_plan(form_data):

    load_dotenv()

    # Construct prompt based on user inputs
    prompt = (f"This is an assistant that should help people to improve their nutrition, by providing a personalized meal plan for one week."
                f" You have to generate the meal plan for one week considering breakfast, lunch and dinner (with also a snack during the morning) "
                f"with the right balance of macronutrient (in each meal except for the snack there should be carbs , proteins and vegetables)."
                f" The meal plan should be balanced appropriately following this details:"
                f" Sex: {form_data['sex']}, Weight: {form_data['weight']} kg, Height: {form_data['height']} cm, "
                f"if {form_data['purpose']} is weight loss, gaining muscles or sportive performance limit the quantity of sugars and sweets and allow max 1/2 cheat meal per week,"
                f" if it is maintaining health, allow max 2/3 cheat meal per week, if it is sportive performance or gaining muscles Favor protein over other macronutrients."
                f" Take dishes from the cuisine of {form_data['location']}, if {form_data['cuisine_preference']} is not total take the dishes outside local cuisine from"
                f" {form_data['other_cuisine']}, "
                f"strictly respect the dietary preferences of {form_data['dietary_preferences']} and avoid the allergens {form_data['allergies_dislikes']}, "
                f"make sure to include {form_data['food_likes']}, if the food_likes are cheat meals allow only some of them in an adequate number for the purpose of the diet."
                f" Consider the habits of {form_data['food_habits']}, the preferences on variety: {form_data['variety']}, Complexity: {form_data['complexity']}, Budget: {form_data['budget']}. "

                f"I'll do some examples of how a balanced diet should be composed:"
                f"breakfast: yogurt with cereals/fruit/walnuts or rusks with proteic cream or marmalade,"
                f"lunch/dinner: pasta with vegetables and fish or a protein as second dish,"
                f"rice with a protein (fish/meat or legumes) and vegetables, "
                f"salad with  a protein (chicken, tuna, fish, eggs,....) and bread or something to accompany the salad with carbs, "
                f"protein (meat,fish,eggs) with vegetables and potatoes, "
                f"dishes with legumes such as hummus, puree and vegetables and carbs"
                f"oriental dishes like noodles with tofu (or other protein) and vegetables "
                f"cheese (both in dishes like pasta and ricotta) or also alone with sides of vegeables and carbs"

            f"Please format the plan as follows: Day of the week, Meal type (Breakfast, Lunch, Dinner), and the meal. "
              "Example output:\n"
              "Monday: Breakfast - Oatmeal, Lunch - Chicken Salad, Dinner - Grilled Salmon\n"
              "Tuesday: Breakfast - Greek Yogurt, Lunch - Turkey Wrap, Dinner - Stir Fry Tofu\n"
              "Wednesday: Breakfast - Smoothie, Lunch - Vegetable Soup, Dinner - Beef Steak\n"
              "And so on for the entire week.")

    # response = openai.Completion.create(
    #     engine="gpt-3.5-turbo",
    #     prompt=prompt,
    #     max_tokens=500,
    #     api_key=api_key
    # )

#     response = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[{"role": "system", "content": prompt},
#               ],
#     max_tokens=500,
#     api_key=api_key
# )

    client = OpenAI()
    # Ensure your OpenAI API key is correctly set in your environment variables
    
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": prompt}
    ]
    )

    text = response.choices[0].text.strip()
    lines = text.split('\n')
    meal_plan = {}
    for line in lines:
        day_part, meals = line.split(':')
        meal_plan[day_part.strip()] = [meal.strip().split(' - ')[1] for meal in meals.split(',')]
    
    # Convert the dictionary into a DataFrame
    df = pd.DataFrame.from_dict(meal_plan, orient='index', columns=['Breakfast', 'Lunch', 'Dinner'])

    return df

if __name__ == "__main__":
    main()