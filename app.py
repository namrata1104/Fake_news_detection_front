import streamlit as st
import requests

# Streamlit app layout
#st.title("Fake News Detection")
#st.subheader("Input news text to check if it's fake or real")

# Input from the user
#user_input = st.text_area("Enter news text:")

#url = "http://localhost:8000/predict"

# Predict button




# App Title
st.title("Textnachricht an Backend senden")

# Eingabefeld für Textnachricht
message = st.text_area("Gib eine Nachricht ein:")

# Button, der die Nachricht an das Backend sendet
if st.button("Predicat"):
    # Sende die Nachricht an das Backend (URL http://0.0.0.0:8000)
    url = "http://localhost:8000"  # Hier die URL des Backends
    payload = {"message": message}

    try:
        # Sende POST-Anfrage an das Backend
        response = requests.get(url)

        # Überprüfe den Statuscode der Antwort
        if response.status_code == 200:
            st.success("Nachricht erfolgreich gesendet!")
            st.write("Antwort vom Backend:", response.json())
        else:
            st.error(f"Fehler: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Fehler bei der Anfrage: {e}")#
