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
# CUSTOM STYLE
# ============================================================

st.markdown(
    """
    <style>
    .stButton > button,
div[data-testid="stButton"] > button,
button[kind="primary"] {
    background-color: #1E6FB9 !important;
    border-color: #1E6FB9 !important;
    color: white !important;
    font-weight: 600 !important;
    }

    .stButton > button:hover,
div[data-testid="stButton"] > button:hover,
button[kind="primary"]:hover {
    background-color: #165A96 !important;
    border-color: #165A96 !important;
    color: white !important;
    }

/* Mobile layout */
@media (max-width: 600px) {
     h3 {
    font-size: 24px !important;
     }
    .block-container {
        padding-left: 18px !important;
        padding-right: 18px !important;
        max-width: 100% !important;
        overflow-x: hidden !important;
    }

    html, body {
        overflow-x: hidden !important;
    }
    div[data-testid="stImage"] img {
    width: 160px !important;
    max-width: 160px !important;
    height: auto !important;
    }
}
    </style>
    """,
    unsafe_allow_html=True
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

        st.subheader("🎈 Your Exact Age")

        st.markdown(
            f"""
<div style="display:grid; grid-template-columns:repeat(3, minmax(0, 1fr)); gap:6px; width:100%; box-sizing:border-box; margin-bottom:20px;">
    <div style="flex:1; min-width:0; text-align:center; border:1px solid #D9E5F1; border-radius:12px; padding:12px 4px;">
        <div style="font-size:30px; font-weight:700; color:#123A67;">{age.years}</div>
        <div style="font-size:13px; color:#536273;">Years</div>
    </div>
    <div style="flex:1; min-width:0; text-align:center; border:1px solid #D9E5F1; border-radius:12px; padding:12px 4px;">
        <div style="font-size:30px; font-weight:700; color:#123A67;">{age.months}</div>
        <div style="font-size:13px; color:#536273;">Months</div>
    </div>
    <div style="flex:1; min-width:0; text-align:center; border:1px solid #D9E5F1; border-radius:12px; padding:12px 4px;">
        <div style="font-size:30px; font-weight:700; color:#123A67;">{age.days}</div>
        <div style="font-size:13px; color:#536273;">Days</div>
    </div>
</div>
""",
            unsafe_allow_html=True
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
                width="content"
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

        # ====================================================
        # BIRTHDAY PROGRESS
        # ====================================================

        previous_birthday = next_birthday.replace(
            year=next_birthday.year - 1
        )

        total_days = (
            next_birthday - previous_birthday
        ).days

        days_passed = (
            today - previous_birthday
        ).days

        progress = days_passed / total_days

        st.subheader("🥳 Journey to Your Next Birthday")

        st.progress(progress)

        percentage = round(progress * 100)

        st.write(
            f"{percentage}% of the journey to your next birthday completed"
        )

    except ValueError:

        st.error(
            "Please enter the birth date in DD/MM/YYYY format."
        )