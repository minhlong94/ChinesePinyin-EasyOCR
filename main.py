import cv2
import easyocr
import streamlit as st
import numpy as np
import xpinyin
import langid
from PIL import Image
from langid.langid import LanguageIdentifier, model

langid.set_languages(["zh"])
identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
CHART_IMAGE_PATH = "files/chart.png"
CHART_IMAGE = Image.open(CHART_IMAGE_PATH).resize((700, 200))
PINYIN_TRANSLATOR = xpinyin.Pinyin()

st.title("Chinese to Pinyin translator")
markdown = """This is a small project I made to translate Chinese character to its Pinyin.  
        View the source code on GitHub: [GitHub](https://github.com/minhlong94/ChinesePinyin-EasyOCR).  
        The chart of the project is as follows: """
st.markdown(markdown)
st.image(CHART_IMAGE)
st.warning("Due to limited hardware resource, detecting and translation take time.")
upload_file = st.file_uploader("Upload an image")

if upload_file is not None:
    image = cv2.imdecode(np.asarray(bytearray(upload_file.read()), dtype=np.uint8), 1)
    st.image(image, caption="Review your input image")
    version = st.selectbox("Simplified or Traditional?", ["Simplified", "Traditional"])
    THRESHOLD = st.slider("Choose the confidence interval: ", 0.0, 1.0, 0.8, 0.01)
    st.info("Only the characters detected above the confidence threshold will be visualized and translated.")
    button = st.button("Get Pinyin!")
    if button:
        if version == "Simplified":
            reader = easyocr.Reader(["ch_sim"])
            result = reader.readtext(image)
        else:
            reader = easyocr.Reader(["ch_tra"])
            result = reader.readtext(image)

        texts = []
        confidences = []
        numeric_pinyin = []
        for (bounding_box, text, confidence) in result:
            detect_chinese = identifier.classify(text)
            if detect_chinese[1] > THRESHOLD:
                (tl, tr, br, bl) = bounding_box
                tl = (int(tl[0]), int(tl[1]))
                tr = (int(tr[0]), int(tr[1]))
                br = (int(br[0]), int(br[1]))
                bl = (int(bl[0]), int(bl[1]))
                cv2.rectangle(image, tl, br, (0, 255, 0), 2)

                pinyin = PINYIN_TRANSLATOR.get_pinyin(text, tone_marks='numbers', splitter=" ")
                numeric_pinyin.append(pinyin)
                cv2.putText(image, pinyin, (bl[0], bl[1] + 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
                texts.append(text)
                confidences.append(confidence)
            else:
                continue
        st.image(image)
        st.write([x[0] + ": " + x[1] for x in zip(texts, numeric_pinyin)])

