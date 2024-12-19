import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

# Custom CSS to enhance the appearance with rainbow colors
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, violet, indigo, blue, green, yellow, orange, red);
        font-family: 'Arial', sans-serif;
    }
    .title {
        color: #FFFFFF;
        text-align: center;
        background-color: rgba(0, 0, 0, 0.5);
        padding: 10px;
        border-radius: 10px;
    }
    .welcome {
        color: #FF0000;  /* Red color for welcome message */
        text-align: center;
        font-size: 24px;
        margin-bottom: 20px;
        animation: rainbow-text 5s infinite;
    }
    @keyframes rainbow-text {
        0%, 100% { color: red; }
        14% { color: orange; }
        28% { color: yellow; }
        42% { color: green; }
        57% { color: blue; }
        71% { color: indigo; }
        85% { color: violet; }
    }
    .stTextInput > label, .stCheckbox > label {
        color: #FFFFFF;
        font-weight: bold;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px;
        transition: background-color 0.3s;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .stAlert {
        background-color: rgba(255, 255, 255, 0.8);
        border: 1px solid #ddd;
    }
    .stDataFrame {
        margin-top: 20px;
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Welcome message
st.markdown("<h2 class='welcome'>Welcome to Fake News Detector</h2>", unsafe_allow_html=True)

# Title of the app
st.markdown("<h1 class='title'>Fake News Detector</h1>", unsafe_allow_html=True)

# Sidebar for model selection
st.sidebar.header("Select Models to Use:")
# baseline = st.sidebar.checkbox("Baseline")
rnn = st.sidebar.checkbox("RNN")
lstm = st.sidebar.checkbox("LSTM")

# Textarea for user input
news_text = st.text_area("Paste your news text here:", height=150)

# Button for prediction
if st.button("Check"):
    if not news_text.strip():
        st.warning("Please enter some text.")
    elif not (rnn or lstm):
        st.warning("Please select at least one model.")
    else:
        # Build the list of selected models
        selected_models = []
        # if baseline:
        #     selected_models.append("baseline")
        if rnn:
            selected_models.append("rnn")
        if lstm:
            selected_models.append("lstm")

        # Send request to FastAPI
        try:
            response = requests.post(
                "https://fake-news-service-876173016892.europe-west1.run.app/predict",
                json={
                    "text": news_text,
                    "models": selected_models
                }
            )
            response.raise_for_status()
            results = response.json()

            # Prepare the results for the table
            prediction_data = []
            model_names = []
            model_probabilities = []
            for model, result in results.items():
                # Use the label from the API response
                prediction = result["label"]
                probability = result["probability"] * 100
                prediction_data.append([model.upper(), prediction, f"{probability:.2f}%"])
                model_names.append(model.upper())
                model_probabilities.append(probability)

            # Calculate the height of the table based on the actual number of rows
            min_table_height = 130  # Minimum table height
            row_height = 58  # Height of one row

            # Dynamic height calculation
            table_height = max(min_table_height, row_height * len(prediction_data))

            # If there are no rows, don't display the table
            if len(prediction_data) > 0:
                # Create DataFrame and set index to start from 1
                df = pd.DataFrame(prediction_data, columns=["Model", "Prediction", "Probability"])
                df.index = range(1, len(df) + 1)  # Set the index to start from 1
                st.markdown("<h4 style='color:white;'>Predictions Table:</h4>", unsafe_allow_html=True)
                st.dataframe(df, height=table_height)

                # Chart for model probabilities
                st.markdown("<h4 style='color:white;'>Model Probability:</h4>", unsafe_allow_html=True)
                fig = go.Figure([go.Bar(x=model_names, y=model_probabilities, marker_color='rgb(26, 118, 255)')])
                fig.update_layout(
                    title='Model Probability Comparison',
                    xaxis_title='Model',
                    yaxis_title='Probability (%)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig)
            else:
                st.warning("No predictions available.")

        except Exception as e:
            st.error(f"Error: {e}")

# Footer or additional info
st.markdown("""
    <hr>
    <footer>
        <p style='text-align: center; color: grey;'>
        Fake News Detector App &copy; 2024
        </p>
    </footer>
    """, unsafe_allow_html=True)
