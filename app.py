import pandas as pd
import numpy as np
import streamlit as st
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import requests
from PIL import Image
from io import BytesIO

# Load and preprocess the data
df = pd.read_json('D:/niv/ai/bbcgoodfood_recipes2.json')
ddf = df.transpose()

def convert_time_to_minutes(time_str):
    if not time_str:
        return 0
    time_parts = time_str.split()
    total_minutes = 0
    for i in range(0, len(time_parts), 2):
        try:
            value = int(time_parts[i])
            unit = time_parts[i+1]
            if 'hr' in unit or 'hrs' in unit:
                total_minutes += value * 60
            elif 'min' in unit or 'mins' in unit:
                total_minutes += value
        except (ValueError, IndexError):
            continue
    return total_minutes

def assign_difficulty(row):
    prep_time_minutes = convert_time_to_minutes(row['Prep Time'])
    cook_time_minutes = convert_time_to_minutes(row['Cook Time'])
    total_time_minutes = prep_time_minutes + cook_time_minutes
    if total_time_minutes <= 20:
        return 'Easy'
    elif 20 < total_time_minutes <= 40:
        return 'Medium'
    else:
        return 'Hard'

ddf['Dif'] = ddf.apply(assign_difficulty, axis=1)

def extract_ingredient_names(ingredients):
    ingredient_names = []
    for ingredient in ingredients:
        parts = ingredient.split(',')[0]
        parts = parts.split(' ')
        parts = [part for part in parts if not any(c.isdigit() for c in part)]
        ingredient_names.append(' '.join(parts))
    return ingredient_names

ddf['Ingredient Names'] = ddf['Ingredients'].apply(extract_ingredient_names)

unique_ingredients = set([ingredient for ingredients_list in ddf['Ingredient Names'] for ingredient in ingredients_list])
ingredient_to_index = {ingredient: i for i, ingredient in enumerate(unique_ingredients)}

def encode_ingredients(recipe):
    encoding = np.zeros(len(unique_ingredients))
    for ingredient in recipe:
        encoding[ingredient_to_index[ingredient]] = 1
    return encoding

ddf['Encoded Ingredients'] = ddf['Ingredient Names'].apply(encode_ingredients)

X_train = np.array(list(ddf['Encoded Ingredients']))

model = Sequential([
    Dense(128, activation='relu', input_shape=(len(unique_ingredients),)),
    Dense(64, activation='relu'),
    Dense(len(ddf), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, np.eye(len(ddf)), epochs=10, batch_size=1, verbose=1)

def recommend_recipes(available_ingredients, ddf, model, difficulty_level):
    available_ingredients_set = set(available_ingredients)
    filtered_ddf = ddf[
        (ddf['Ingredient Names'].apply(lambda x: available_ingredients_set.issubset(set(x)))) &
        (ddf['Dif'].str.lower() == difficulty_level.lower())
    ]
    return filtered_ddf

# Streamlit app
st.set_page_config(page_title="Recipe Generator", page_icon="🍲", layout="wide")

st.title('Recipe Generator')

# Placeholder for loading image
loading_image = st.empty()
loading_image.image('https://cdn.dribbble.com/users/3399824/screenshots/6521075/mascot-2-04.jpg', width=500)

st.sidebar.header('Input Ingredients')
available_ingredients = st.sidebar.text_area("Enter your ingredients (comma separated):").split(',')
available_ingredients = [ingredient.strip() for ingredient in available_ingredients]

st.sidebar.header('Select Difficulty Level')
difficulty_level = st.sidebar.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])

if st.sidebar.button('Generate Recipe'):
    filtered_ddf = recommend_recipes(available_ingredients, ddf, model, difficulty_level)
    if not filtered_ddf.empty:
        loading_image.empty()  # Clear the loading image only if a recipe is found
        for _, row in filtered_ddf.iterrows():
            title = row['Title']
            ingredients = row['Ingredient Names']
            method_steps = row['Method Steps']
            prep_time = row['Prep Time']
            cook_time = row['Cook Time']
            image_url = row['Image']
            st.header(title)
            try:
                response = requests.get(image_url)
                img = Image.open(BytesIO(response.content))
                img_width = 200  # Adjust the width as needed
                img_height = int(img.height * (img_width / float(img.width)))
                img = img.resize((img_width, img_height))
                st.image(img, caption=title, use_column_width=False)
            except Exception as e:
                st.error(f"Could not load image: {e}")
            st.subheader("Prep Time")
            st.write(prep_time)
            st.subheader("Cook Time")
            st.write(cook_time)
            st.subheader("Ingredients")
            st.write(", ".join(ingredients))
            st.subheader("Method Steps")
            for step in method_steps:
                split_steps = step.split(".")
                for sub_step in split_steps:
                    if sub_step.strip():
                        st.write(f"- {sub_step.strip()}")

# Sidebar image
st.sidebar.image('https://www.cookingclassy.com/wp-content/uploads/2022/02/food-pics.jpg', width=200)

# Apply some CSS for better styling
st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://www.cookingclassy.com/wp-content/uploads/2022/02/food-pics.jpg");
        background-size: cover;
    }
    .sidebar .sidebar-content {
        background: url("https://www.cookingclassy.com/wp-content/uploads/2022/02/food-pics.jpg");
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)
