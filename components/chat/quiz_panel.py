# EJEMPLO

import streamlit as st

def render_quiz_panel():
    st.subheader("📝 Quiz")
    st.write("Test yourself with generated questions.")

    question = "What is supervised learning?"

    # Le agregamos index=None para que ninguna opción salga seleccionada por defecto
    answer = st.radio(
        question,
        [
            "Learning without labels",
            "Learning using labeled data",
            "Random guessing",
            "None of the above"
        ],
        index=None
    )

    if st.button("Submit Answer"):
        if answer == "Learning using labeled data":
            st.success("Correct!")
        elif answer is not None:
            st.error("Incorrect.")
        else:
            st.warning("Please select an answer first.")