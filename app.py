# Import statements:
import requests
import streamlit as st

# Save the API endpoint from CocktailDB to a variable:
url = 'https://www.thecocktaildb.com/api/json/v1/1/list.php?i=list'

# Make a GET request to the API to retrieve the ingredients list:
response = requests.get(url)
data = response.json()
ingredients = [d['strIngredient1'] for d in data['drinks']]

# Sort the ingredients alphabetically
ingredients.sort()

# Create a title for the Streamlit app:
st.title('CocktailDB Lookup')

# Create a title for the sidebar:
st.sidebar.title('Find a cocktail!')

# Create a Streamlit selectbox with the sorted ingredients list:
selected_ingredient = st.sidebar.selectbox(
    'Select an ingredient:',
    ingredients
)

# Make a GET request to the API to retrieve the drinks list for the selected
# ingredient:
selected_drinks_url = f'https://www.thecocktaildb.com/api/json/v1/1/filter' \
                      f'.php?i={selected_ingredient}'
selected_drinks_response = requests.get(selected_drinks_url)
selected_drinks_data = selected_drinks_response.json()
selected_drinks = [d['strDrink'] for d in selected_drinks_data['drinks']]

# Create a Streamlit selectbox with the drinks list for the selected ingredient:
selected_drink = st.sidebar.selectbox(
    'Select a drink:',
    selected_drinks
)

# Create a Submit button:
if st.sidebar.button('Submit'):
    # Make a GET request to the API to retrieve the details of the selected
    # drink:
    selected_drink_url = f'https://www.thecocktaildb.com/api/j' \
                         f'son/v1/1/search.php?s={selected_drink}'
    selected_drink_response = requests.get(selected_drink_url)
    selected_drink_data = selected_drink_response.json()
    selected_drink_details = selected_drink_data['drinks'][0]

    # Display the selected drink details in the main Streamlit window with tabs:
    st.header('Cocktail Details')
    tabs = st.tabs(
        ['Image', 'Category', 'Glass', 'Ingredients', 'Instructions'])

    with tabs[0]:
        st.image(selected_drink_details['strDrinkThumb'], width=200)

    with tabs[1]:
        st.write(selected_drink_details['strCategory'])

    with tabs[2]:
        st.write(selected_drink_details['strGlass'])

    with tabs[3]:
        st.markdown('**Ingredients:**')
        for i in range(1, 16):
            ingredient_name = selected_drink_details[f'strIngredient{i}']
            if ingredient_name:
                ingredient_measurement = selected_drink_details[
                    f'strMeasure{i}']
                st.write(f'- **{ingredient_name}** {ingredient_measurement}')

    with tabs[4]:
        st.write(selected_drink_details['strInstructions'])
