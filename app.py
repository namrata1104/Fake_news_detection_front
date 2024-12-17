import streamlit as st
import requests
import pandas as pd  # Importiere pandas für DataFrame

# Titel der App
st.title("Fake News Detector")

# Textarea für Benutzereingabe
news_text = st.text_area("Paste your news text here:")

# Checkboxen in einer Reihe anordnen
col1, col2, col3 = st.columns(3)
with col1:
    baseline = st.checkbox("baseline")
with col2:
    rnn = st.checkbox("rnn")
with col3:
    lstm = st.checkbox("lstm")

# Button für Vorhersage
if st.button("Check"):
    if not news_text.strip():
        st.warning("Please enter some text.")
    elif not (baseline or rnn or lstm):
        st.warning("Please select at least one model.")
    else:
        # Build the list of selected models
        selected_models = []
        if baseline:
            selected_models.append("baseline")
        if rnn:
            selected_models.append("rnn")
        if lstm:
            selected_models.append("lstm")

        # Anfrage an FastAPI senden
        try:
            response = requests.post(
                "http://127.0.0.1:8000/predict",
                json={
                    "text": news_text,
                    "models": selected_models  # Pass the selected models as a list
                }
            )
            response.raise_for_status()
            results = response.json()

            # Prepare the results for the table
            prediction_data = []
            for model, result in results.items():
                prediction = "FAKE" if result["prediction"] else "REAL"
                probability = result["probability"] * 100
                prediction_data.append([model.upper(), prediction, f"{probability:.2f}%"])

            # If multiple models are selected, show the results in a table
            if len(prediction_data) > 1:
                df = pd.DataFrame(prediction_data, columns=["Model", "Prediction", "Probability"])
                st.write("### Predictions Table:")
                st.dataframe(df)  # Display the results as a table

            else:
                # If only one model is selected, display the results as text
                for model, result in results.items():
                    prediction = "FAKE" if result["prediction"] else "REAL"
                    probability = result["probability"] * 100
                    st.write(f"- **{model.upper()}**: {prediction} (Probability: {probability:.2f}%)")

        except Exception as e:
            st.error(f"Error: {e}")
