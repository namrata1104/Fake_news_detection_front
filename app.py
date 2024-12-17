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
        # Liste der ausgewählten Modelle erstellen
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

            # Ergebnisse für die Tabelle vorbereiten
            prediction_data = []
            for model, result in results.items():
                prediction = result["label"]  # "Fake News" oder "Real News" von der API
                probability = result["probability"] * 100  # Umwandlung in Prozent
                prediction_data.append([model.upper(), prediction, f"{probability:.2f}%"])

            # Wenn mehrere Modelle ausgewählt sind, Ergebnisse in einer Tabelle anzeigen
            if len(prediction_data) > 0:
                df = pd.DataFrame(prediction_data, columns=["Model", "Prediction", "Probability"])

                # Index von der DataFrame bei 1 oder 0 beginnen lassen
                df.index = df.index + 1  # Indizes bei 1 beginnen lassen
                st.write("### Predictions Table:")
                st.dataframe(df)  # Zeige die Tabelle ohne leere Zeilen

            else:
                # Wenn nur ein Modell ausgewählt wurde, Ergebnisse als Text anzeigen
                for model, result in results.items():
                    prediction = result["label"]  # "Fake News" oder "Real News" von der API
                    probability = result["probability"] * 100
                    st.write(f"- **{model.upper()}**: {prediction} (Probability: {probability:.2f}%)")

        except Exception as e:
            st.error(f"Error: {e}")
