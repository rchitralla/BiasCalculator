import streamlit as st
import plotly.express as px
import pandas as pd
import random

# Path to the logo image
logo_path = "Logo.png"

# Define the categories, types, and questions
categories = {
    "Culture & Engagement": {
        "Individual Actions": [
            "I use language carefully to avoid terms that may be degrading or hurtful."
        ],
        "Institution Actions": [
            "I support reviewing policies across all functions to ensure they are inclusive and free from bias."
        ]
    },
    "Development": {
        "Individual Actions": [
            "I sponsor and mentor employees from historically marginalized groups.",
            "I create individual development plans for every team member.",
            "I hold my team accountable for mentoring and sponsoring marginalized employees, including in performance reviews."
        ],
        "Industry Actions": [
            "I mentor and sponsor people from marginalized groups within and outside my organization."
        ],
        "Institution Actions": [
            "I mentor and sponsor people from marginalized groups within and outside my organization.",
            "I monitor training participation to ensure inclusion of all backgrounds.",
            "I support formal mentoring and sponsorship programs in my organization.",
            "I support ongoing inclusion/unconscious bias training for all employees."
        ]
    },
    "Exit & Retain": {
        "Individual Actions": [
            "I personally speak to critical employees from all backgrounds to understand their exit and stay reasons."
        ],
        "Institution Actions": [
            "My function conducts regular exit interviews.",
            "My function takes actions to improve retention of people from all backgrounds."
        ]
    },
    "General": {
        "Individual Actions": [
            "I speak up when team members say things based on stereotypes or assumptions.",
            "I build strong partnerships with communities and organizations supporting historically marginalized groups.",
            "I give equal attention to people from all backgrounds.",
            "I value dissenting opinions, even when they make me uncomfortable.",
            "I examine my connections and diversify the perspectives and experiences around me.",
            "I consider multiple data sources and avoid relying on 'gut reaction' for decisions."
        ],
        "Institution Actions": [
            "I review the team for diversity when starting a project and take action if it's not diverse.",
            "I encourage my team to speak up against stereotypes or assumptions.",
            "I promote the sharing of dissenting opinions across the team.",
            "I seek insights from Employee Resource Groups to improve my function/team/department."
        ],
        "Industry Actions": [
            "I build strong partnerships with communities supporting historically marginalized groups."
        ]
    },
    "Performance & Reward": {
        "Individual Actions": [
            "I regularly review and address bias/equity in pay decisions.",
            "During performance reviews, I check ratings distributions by demographic for potential bias."
        ],
        "Institution Actions": [
            "I support the systemic review of pay equity and performance ratings by demographic annually."
        ],
        "Industry Actions": [
            "I support publicly sharing pay equity results and plans to address gaps."
        ]
    },
    "Recruiting & Hiring": {
        "Individual Actions": [
            "I wait to decide on hiring until there is a balanced slate of candidates.",
            "I use structured interview guides and consistent criteria for all candidates.",
            "I use structured guides and consistent criteria for all interviews.",
            "Every new team member takes inclusion/unconscious bias training when starting."
        ],
        "Institution Actions": [
            "My function has a balanced slate policy.",
            "My function requires structured interviews or diverse panels for all roles.",
            "My function includes inclusion/unconscious bias training in new hire onboarding."
        ]
    }
}

# Flattened list of questions to display without headers
questions_list = []
for category_name, types in categories.items():
    for type_name, questions in types.items():
        for question in questions:
            questions_list.append({
                "category": category_name,
                "type": type_name,
                "question": question
            })

# Function to display questions and collect responses
def display_questions():
    responses = []
    for item in st.session_state['shuffled_questions']:
        st.write(item["question"])
        options = [0, 1, 2, 3, 4, 5]  # Add None as the default option
        key = f"{item['category']}_{item['type']}_{item['question']}"

        if key not in st.session_state:
            st.session_state[key] = 0

        selected_option = st.selectbox(
            "Select your response:", options, index=options.index(st.session_state[key]) if st.session_state[key] in options else 0,
            key=key
        )

        try:
            selected_option = int(selected_option)
            if selected_option not in options:
                raise ValueError("Invalid option selected")
        except ValueError:
            st.error("Invalid selection. Please choose a valid response.")
            continue

        responses.append({
            "category": item["category"],
            "type": item["type"],
            "question": item["question"],
            "score": selected_option
        })
    return responses

# Function to calculate the total score
def calculate_total_score(responses):
    total_score = sum(response['score'] for response in responses if response['score'] is not None)
    return total_score

# Function to calculate the total score per category
def calculate_total_scores_per_category(responses):
    total_scores_per_category = {}
    for response in responses:
        if response["score"] is None:
            continue
        category = response["category"]
        score = response["score"]
        if category not in total_scores_per_category:
            total_scores_per_category[category] = 0
        total_scores_per_category[category] += score
    return total_scores_per_category

# Function to calculate the maximum possible score per category
def calculate_max_scores_per_category(categories):
    max_scores_per_category = {}
    for category_name, types in categories.items():
        total_questions = sum(len(questions) for questions in types.values())
        max_scores_per_category[category_name] = total_questions * 5  # Maximum score is 5 per question
    return max_scores_per_category

# Main function to display the self-assessment form
def main():
    st.image(logo_path, width=200)  # Add your logo at the top
    st.title("Anti-Bias Self Assessment Tool")
    st.write(
        "This tool enables you to explore your own behaviors related to bias & inclusion in the workplace. "
        "Your results are yours and yours alone -- they will not be submitted or shared in any
