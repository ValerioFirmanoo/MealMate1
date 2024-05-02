import streamlit as st
import openai
import os

def main():
    #st.title("MeatMeal: Your Personalized Meal Planner")
    st.markdown("<h1 style='text-align: center; font-size: 48px;'>MealMate</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; opacity: 0.8;'>Your Personalized Meal Planner</h2>", unsafe_allow_html=True)


    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        st.error("OpenAI API key not found. Please set it as an environment variable.")
        return
    
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
            
        allergies = st.text_area("List any food allergies or ingredients you dislike:",
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
        # Button to generate meal plan
            if st.button("Generate Meal Plan"):
                response = generate_meal_plan(openai_api_key, sex, weight, height, purpose, location, 
                                            cuisine_preference, dietary_preferences, allergies_dislikes, 
                                            variety, complexity, budget, food_habits)
                st.write(response)
            else:
                st.success("Fill out the above details to generate your meal plan.")

def generate_meal_plan(api_key, sex, weight, height, purpose, location, cuisine_preference, dietary_preferences, allergies_dislikes, variety, complexity, budget, food_habits):
    prompt = f"Create a personalized meal plan for a {sex}, {weight} kg, {height} cm tall, aiming for {purpose}. " \
             f"Location: {location}, prefers {cuisine_preference} of local cuisine. Dietary preferences: {', '.join(dietary_preferences)}. " \
             f"Allergies/dislikes: {allergies_dislikes}. Wants {variety} meals, {complexity} complexity, " \
             f"and a {budget} budget for groceries. Additional habits: {food_habits}."
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=150,
        api_key=api_key
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    main()