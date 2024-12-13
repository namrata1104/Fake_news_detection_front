import streamlit as st
import requests

# Titel der App
st.title("Fake News Detector")

# Textarea für Benutzereingabe
news_text = st.text_area("Paste your news text here:")

if st.button("Check"):
    if not news_text.strip():
        st.warning("Please enter some text.")
    else:
        # Sende Anfrage an FastAPI-Backend
        try:
            response = requests.post(
                "http://127.0.0.1:8000/predict",
                json={"text": news_text}
            )
            response.raise_for_status()
            data = response.json()

            # Ergebnis anzeigen
            prediction = data.get("prediction")
            accuracy = data.get("accuracy", 0) * 100

            if prediction:
                st.error(f"⚠️ This is likely FAKE news! (Accuracy: {accuracy:.2f}%)")
            else:
                st.success(f"✅ This appears to be REAL news! (Accuracy: {accuracy:.2f}%)")

        except Exception as e:
            st.error(f"Error: {e}")
