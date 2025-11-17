import streamlit as st
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import pycountry

# ====== CONFIGURACIÓN INICIAL ======
st.set_page_config(page_title="Moodify", page_icon="🎵", layout="centered")

# ====== CARGA EL MODELO DE EMOCIONES ======
@st.cache_resource
def load_emotion_model():
    model = load_model("app/tm/keras_model.h5", compile=False)
    labels = [line.strip() for line in open("app/tm/labels.txt", "r")]
    return model, labels

model, class_names = load_emotion_model()

# DICCIONARIO DE CANCIONES ======
songs_dict = {
    "Feliz": ["Happy – Pharrell Williams", "Can't Stop the Feeling – Justin Timberlake", "Uptown Funk – Bruno Mars", "Good as Hell – Lizzo"],
    "Triste": ["Someone Like You – Adele", "Fix You – Coldplay", "Let Her Go – Passenger", "Skinny Love – Bon Iver"],
    "Enfadado": ["Smells Like Teen Spirit – Nirvana", "Killing In The Name – Rage Against The Machine", "Papercut – Linkin Park", "Stronger – Kanye West"],
    "Neutral": ["Sunflower – Post Malone", "Dreams – Fleetwood Mac", "Ocean Eyes – Billie Eilish", "Electric Feel – MGMT"]
}

# INTERFAZ 
st.title("🎧 MOODIFY – Tu estado de ánimo hecho música")

with st.form("user_form"):
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre")
        apellidos = st.text_input("Apellidos")
    with col2:
        fecha_nacimiento = st.date_input("Fecha de nacimiento")
        paises = [country.name for country in pycountry.countries]
        pais = st.selectbox("País", sorted(paises))
    enviar = st.form_submit_button("Continuar")

if enviar:
    st.success(f"¡Hola {nombre}! Ahora detectaremos tu estado de ánimo. 🌈")

    # ====== CAPTURA O SUBIDA DE IMAGEN ======
    st.write("Puedes subir una imagen o usar tu cámara:")
    col1, col2 = st.columns(2)

    with col1:
        imagen_subida = st.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])
    with col2:
        foto = st.camera_input("O toma una foto")

    imagen_final = imagen_subida or foto

    if imagen_final is not None:
        image = Image.open(imagen_final).convert("RGB")
        st.image(image, caption="Tu imagen analizada", use_column_width=True)

        # ====== PREPROCESAMIENTO ======
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        img_array = np.asarray(image)
        normalized_img_array = (img_array.astype(np.float32) / 255.0)
        data = np.expand_dims(normalized_img_array, axis=0)

        # ====== PREDICCIÓN ======
        prediction = model.predict(data)
        index = np.argmax(prediction)
        emotion = class_names[index].strip()
        confidence = prediction[0][index]

        st.subheader(f"🧠 Emoción detectada: **{emotion}** ({confidence*100:.2f}% confianza)")

        # ====== RECOMENDACIONES ======
        st.subheader("🎶 Canciones recomendadas:")
        if emotion in songs_dict:
            for s in songs_dict[emotion]:
                st.write(f"• {s}")
        else:
            st.write("No se encontraron canciones para esta emoción 😅")

        st.info(f"Gracias por usar Moodify, {nombre} de {pais} 🌍")
