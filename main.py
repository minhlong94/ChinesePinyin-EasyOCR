import cv2
import easyocr
import pandas as pd
import streamlit as st
import numpy as np
import pinyin
import googletrans

st.title("Image Character Translator")
st.info("This is a small project I made to translate "
        "Chinese character to its Pinyin, though later "
        "I decided to do translator as well.")
languages_df = pd.read_csv("languages.csv")
list_languages = languages_df["Language"] + "-" + languages_df["CodeName"]
OPTIONS = ["Chinese to Pinyin", "Translator"]

option = st.selectbox("Choose your options", OPTIONS)
if option == "Chinese to Pinyin":
    upload_file = st.file_uploader("Upload an image")
    if upload_file is not None:
        image = cv2.imdecode(np.asarray(bytearray(upload_file.read()), dtype=np.uint8), 1)
        version = st.selectbox("Simplified or Traditional?", ["Simplified", "Traditional"])
        if version == "Simplified":
            reader = easyocr.Reader(["ch_sim"])
            result = reader.readtext(image)
        else:
            reader = easyocr.Reader(["ch_tra"])
            result = reader.readtext(image)

        texts = []
        confidences = []
        for (bounding_box, text, confidence) in result:
            (tl, tr, br, bl) = bounding_box
            tl = (int(tl[0]), int(tl[1]))
            tr = (int(tr[0]), int(tr[1]))
            br = (int(br[0]), int(br[1]))
            bl = (int(bl[0]), int(bl[1]))
            cv2.rectangle(image, tl, br, (0, 255, 0), 2)
            cv2.putText(image, pinyin.get(text, format="numerical"), (tl[0], tl[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
            texts.append(text)
            confidences.append(confidence)
        st.image(image)
        st.write(pinyin.get(texts, format="numerical"))
        st.write(confidences)
    else:
        st.exception("Invalid file")
elif option == "Translator":
    upload_file = st.file_uploader("Upload an image")
    if upload_file is not None:
        cv2.imread(upload_file)
        orig_languages = st.multiselect("Please select original language", list_languages)
        dest_languages = st.multiselect("Please select destination language", list_languages)
        reader = easyocr.Reader([orig_languages])
    else:
        st.exception("Invalid file")
