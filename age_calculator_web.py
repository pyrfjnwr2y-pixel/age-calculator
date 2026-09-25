from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import streamlit as st
import os


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Age Calculator - Rabih Eid",
    page_icon="📅",
    layout="centered"
)


# ============================================================
# CHARACTER SELECTION
# ============================================================

def get_character(gender, age):

    if age < 3:
        return "baby_male.png" if gender == "Male" else "baby_female.png"

    elif age <= 12:
        return "boy.png" if gender == "Male" else "girl.png"

    elif age <= 19:
        return "teenage_male.png" if gender == "Male" else "teenage_female.png"

    elif age <= 59:
        return "adult_male.png" if gender == "Male" else "adult_female.png"

    else:
        return "senior_male.png" if gender == "Male" else "senior_female.png"


# ============================================================
# TITLE
# ============================================================

st.markdown(
    """
    <h1 style='text-align:center; margin-bottom:0;'>
        📅 AGE CALCULATOR
    </h1>

    <h3 style='text-align:center; margin-top:5px;'>
        by <span style='color:#C62828;'>Rabih Eid</span>
    </h3>
    """,
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# USER INPUT
# ============================================================

name = st.text_input(
    "Name",
    placeholder="Enter your name"
)

gender = st.radio(
    "Gender",
    ["Male", "Female"],
    horizontal=True
)

birth_date_text = st.text_input(
    "Birth Date",
    placeholder="DD/MM/YYYY"
)


# ============================================================
# CALCULATE
# ============================================================

if st.button(
    "Calculate Age",
    type="primary",
    use_container_width=True
):

    try:

        if not name.strip():
            st.warning("Please enter your name.")
            st.stop()

        birth_date = datetime.strptime(
            birth_date_text,
            "%d/%m/%Y"
        ).date()

        today = date.today()

        if birth_date > today:
            st.error("Birth date cannot be in the future.")
            st.stop()

        # Exact age
        age = relativedelta(
            today,
            birth_date
        )

        # Next birthday
        next_birthday = birth_date.replace(
            year=today.year
        )

        if next_birthday < today:
            next_birthday = next_birthday.replace(
                year=today.year + 1
            )

        days_remaining = (
            next_birthday - today
        ).days


        # ====================================================
        # RESULTS
        # ====================================================

        st.success(
            f"Welcome, {name}!"
        )

        st.subheader("Your Exact Age")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Years",
            age.years
        )

        col2.metric(
            "Months",
            age.months
        )

        col3.metric(
            "Days",
            age.days
        )


        # ====================================================
        # CHARACTER IMAGE
        # ====================================================

        character_file = get_character(
            gender,
            age.years
        )

        image_path = os.path.join(
            "images",
            character_file
        )

        if os.path.exists(image_path):

            st.image(
                image_path,
                width=210
            )


        # ====================================================
        # NEXT BIRTHDAY
        # ====================================================

        st.subheader("🎂 Next Birthday")

        st.write(
            next_birthday.strftime(
                "%d %B %Y"
            )
        )

        if days_remaining == 0:

            st.success(
                "🎉 Happy Birthday!"
            )

        elif days_remaining == 1:

            st.info(
                "Your birthday is tomorrow!"
            )

        else:

            st.info(
                f"{days_remaining} days remaining until your next birthday."
            )


    except ValueError:

        st.error(
            "Please enter the birth date in DD/MM/YYYY format."
        )