import streamlit as st
import openai
import os
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
import json


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
    
    st.markdown("""
        <style>
            div.stButton > button:first-child {
                display: block;
                margin: 0 auto;
            }
            div.stSpinner > div {
                display: flex;
                justify-content: center;
            }
        </style>""", unsafe_allow_html=True)

    if st.button("Generate Meal Plan"):
        with st.spinner('Generating your meal plan... Please wait'):
            meal_plan_df = generate_meal_plan(st.session_state['form_data'])
            st.success('Meal plan generated successfully!')
            st.table(meal_plan_df)

def generate_meal_plan(form_data):
#def generate_meal_plan():


    load_dotenv()

    
    prompt = (f"you are an assistant that should help people to improve their nutrition, by providing a personalized meal plan for one week."
                f" You have to generate the meal plan for one week considering breakfast, lunch and dinner (with also a snack during the morning) "
                f"with the right balance of macronutrient (in each meal except for the snack there should be carbs , proteins and vegetables)."
                f" The meal plan should be balanced appropriately following this details:"
                f" Sex: {form_data['sex']}, Weight: {form_data['weight']} kg, Height: {form_data['height']} cm, "
                f" purpose:({form_data['purpose']}) "
                f" Take {form_data['cuisine_preference']} of the dishes from the cuisine of {form_data['location']}, the other dishes outside local cuisine from"
                f" {form_data['other_cuisine']}, "

                f"I'll do some examples of how a balanced diet should be composed:"
                f"breakfast: yogurt with cereals/fruit/walnuts or rusks with proteic cream or marmalade,"
                f"Snack: chose some fresh friuts or walnuts "
                f"lunch/dinner: pasta with vegetables and fish or a protein as second dish,"
                f"rice with a protein (fish/meat or legumes) and vegetables, "
                f"salad with  a protein (chicken, tuna, fish, eggs,....) and bread or something to accompany the salad with carbs, "
                f"protein (meat,fish,eggs) with vegetables and potatoes, "
                f"dishes with legumes such as hummus, puree and vegetables and carbs"
                f"oriental dishes like noodles with tofu (or other protein) and vegetables "
                f"cheese (both in dishes like pasta and ricotta) or also alone with sides of vegeables and carbs"

                f"strictly respect the dietary preferences of {form_data['dietary_preferences']} and avoid the allergens {form_data['allergies_dislikes']}, "
                f"follow the preferences on variety: {form_data['variety']}, Complexity: {form_data['complexity']}, Budget: {form_data['budget']}. "
                f"follow the habits: {form_data['food_habits']},  "
                f"give the output in json format keys as days of the weeks and meal types")

    client = OpenAI()
    # Ensure your OpenAI API key is correctly set in your environment variables
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": prompt},
            ],
        temperature=1,
        max_tokens=1000,
        top_p=1,
    )

    text = response.choices[0].message.content
    df = pd.DataFrame(json.loads(text))
    return df

if __name__ == "__main__":
    main()