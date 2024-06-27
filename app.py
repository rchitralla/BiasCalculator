import streamlit as st
import plotly.express as px
import numpy as np
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

# Flatten the questions and add category information
questions = []
for category_name, types in categories.items():
    for type_name, qs in types.items():
        for q in qs:
            questions.append((category_name, type_name, q))

# Function to display questions and collect responses
def display_questions(questions):
    st.header("Self Assessment Questions")
    scores = []
    random.shuffle(questions)  # Shuffle the questions for each session
    for i, (category, type_, question) in enumerate(questions):
        score = st.radio(question, [3, 2, 1], index=2, key=f"{i}")
        scores.append((category, type_, score))
    return scores

# Main function to display the self-assessment form
def main():
    st.image(logo_path, width=200)  # Add your logo at the top
    st.title("Self Assessment Tool")
    st.write(
        "This tool enables you to explore your own behaviors related to bias & inclusion in the workplace. "
        "Your results are yours and yours alone -- they will not be submitted or shared in any manner unless you choose to do so."
    )
    st.write(
        "Read each statement and choose a score using the rating scale provided. "
        "Once complete, subtotal the scores by section. Reflect on areas where your scores are lower than others and identify where you can continue to grow. "
        "The assessment should take you no longer than 5 – 10 mins."
    )
    st.write("### Rating Scale: 3 = all of the time, consistent application | 2 = some of the time, inconsistent application | 1 = Not done at all")

    # Display questions and collect responses
    scores = display_questions(questions)

    # Process the results and visualizations
    if st.button("Submit"):
        st.write("## Assessment Complete. Here are your results:")

        # Aggregate scores by category and type
        total_scores = {}
        for category, type_, score in scores:
            if category not in total_scores:
                total_scores[category] = {}
            if type_ not in total_scores[category]:
                total_scores[category][type_] = 0
            total_scores[category][type_] += score

        for category_name, types in total_scores.items():
            st.write(f"**{category_name}:**")
            for type_name, score in types.items():
                st.write(f"  - **{type_name}: {score}**")

        # Prepare data for visualization
        flattened_scores = []
        for category_name, types in total_scores.items():
            for type_name, score in types.items():
                flattened_scores.append({"Category": category_name, "Type": type_name, "Score": score})
        scores_data = pd.DataFrame(flattened_scores)

        # Create a bar chart
        fig = px.bar(scores_data, x="Category", y="Score", color="Type", title="Self Assessment Scores by Category and Type",
                     color_discrete_sequence=["#377bff", "#15965f", "#fa6868"])
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
