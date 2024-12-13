import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import date
import pdfkit
from streamlit_login_auth_ui.widgets import __login__

# Authentication setup
__login__obj = __login__(
    auth_token="pk_prod_WK9CBN31SQMZH8HPMD6KD8H5DFD2",
    company_name="grpx",
    width=200,
    height=250,
    logout_button_name='Logout',
    hide_menu_bool=False,
    hide_footer_bool=False,
    lottie_url='https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json',
)

LOGGED_IN = __login__obj.build_login_ui()

if LOGGED_IN:
    st.sidebar.write("# ***Profile***")
    st.sidebar.write("Hi, welcome to the application!")

    # Image classification function
    def import_and_predict(image_data, model):
        image = ImageOps.fit(image_data, (100, 100), Image.ANTIALIAS)
        image = image.convert('RGB')
        image = np.asarray(image)
        st.image(image, channels='RGB')
        image = image.astype(np.float32) / 255.0
        img_reshape = image[np.newaxis, ...]
        prediction = model.predict(img_reshape)
        return prediction

    # Load TensorFlow model
    model_path = 'my_model2.h5'
    try:
        model = tf.keras.models.load_model(model_path)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.stop()

    st.write("# ***Glaucoma Detector***")
    st.write("This is a simple image classification app to predict glaucoma through a fundus image of the eye.")

    file = st.file_uploader("Please upload a .jpg image file", type=["jpg"])

    if file is None:
        st.text("You haven't uploaded an image file.")
    else:
        image = Image.open(file)
        prediction = import_and_predict(image, model)
        pred = prediction[0][0]

        # Diagnosis based on prediction
        if pred > 0.5:
            st.write("# **Prediction:** Your eye is Healthy. Severity: Normal")
            prii = "Negative"
            course = "Normal"
        elif pred < 0.3:
            st.write("## **Prediction:** You are severely affected by Glaucoma.")
            prii = "Positive"
            course = "Severely Affected"
        else:
            st.write("## **Prediction:** You are affected by Glaucoma. Please consult an ophthalmologist.")
            prii = "Positive"
            course = "Mildly Affected"

        # PDF generation
        env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
        try:
            template = env.get_template("temp.html")
        except Exception as e:
            st.error(f"Error loading template: {e}")
            st.stop()

        html = template.render(
            course=course,
            prii=prii,
            date=date.today().strftime("%B %d, %Y"),
        )

        form = st.form("template_form")
        submit = form.form_submit_button("Generate PDF")

        if submit:
            try:
                pdf = pdfkit.from_string(html, False)
                st.balloons()
                st.success("Your medical report has been generated!")
                st.download_button(
                    "⬇️ Download PDF",
                    data=pdf,
                    file_name="Med_report.pdf",
                    mime="application/pdf",
                )
            except Exception as e:
                st.error(f"Error generating PDF: {e}")
