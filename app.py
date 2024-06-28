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
        score = st.radio(item["question"], [1, 2, 3, 4, 5], index=2, key=f"{item['category']}_{item['type']}_{item['question']}")
        responses.append({
            "category": item["category"],
            "type": item["type"],
            "question": item["question"],
            "score": score
        })
    return responses

# Function to calculate the total score
def calculate_total_score(responses):
    total_score = sum(response['score'] for response in responses)
    return total_score

# Function to calculate the total score per category
def calculate_total_scores_per_category(total_scores):
    total_scores_per_category = {}
    for category_name, types in total_scores.items():
        total_scores_per_category[category_name] = sum(types.values())
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
    st.write("### Rating Scale: 1 = Never | 2 = Rarely | 3 = Sometimes | 4 = Often | 5 = Consistently all the time")

    # Shuffle questions once per session
    if 'shuffled_questions' not in st.session_state:
        st.session_state['shuffled_questions'] = questions_list.copy()
        random.shuffle(st.session_state['shuffled_questions'])

    # Display the questions and collect responses
    responses = display_questions()

    # Group responses by category and type for analytics
    total_scores = {}
    for response in responses:
        category = response["category"]
        type_ = response["type"]
        score = response["score"]
        if category not in total_scores:
            total_scores[category] = {}
        if type_ not in total_scores[category]:
            total_scores[category][type_] = 0
        total_scores[category][type_] += score

    # Calculate the total score
    total_score = calculate_total_score(responses)

    # Calculate the total scores per category
    total_scores_per_category = calculate_total_scores_per_category(total_scores)

    # Calculate the maximum possible scores per category
    max_scores_per_category = calculate_max_scores_per_category(categories)

    # Display the results and visualizations
    if st.button("Submit"):
        st.write("## Assessment Complete. Here are your results:")

        # Display grouped results
        for category_name, types in total_scores.items():
            for type_name, score in types.items():
                st.write(f"**{category_name} - {type_name}: {score}**")

        # Display total score
        st.write(f"### Total Score: {total_score}")

        # Display total scores per category
        for category_name, score in total_scores_per_category.items():
            st.write(f"**{category_name}: {score} out of {max_scores_per_category[category_name]}**")

        # Prepare data for visualization
        flattened_scores = []
        for category_name, types in total_scores.items():
            for type_name, score in types.items():
                flattened_scores.append({"Category": category_name, "Type": type_name, "Score": score})
        scores_data = pd.DataFrame(flattened_scores)

        # Calculate total scores per category for sorting
        total_scores_list = [{"Category": category_name, "Total Score": score, "Max Score": max_scores_per_category[category_name]} for category_name, score in total_scores_per_category.items()]
        total_scores_df = pd.DataFrame(total_scores_list).sort_values(by="Total Score", ascending=False)

        # Sort the scores_data based on the ordered categories
        ordered_categories = total_scores_df["Category"].tolist()
        scores_data["Category"] = pd.Categorical(scores_data["Category"], categories=ordered_categories, ordered=True)
        scores_data = scores_data.sort_values(by=["Category", "Score"], ascending=[True, False])

        # Create a bar chart
        fig_bar = px.bar(scores_data, x="Category", y="Score", color="Type", title="Self Assessment Scores by Category and Type",
                         color_discrete_sequence=["#377bff", "#15965f", "#fa6868"])
        st.plotly_chart(fig_bar)

        # Create a doughnut chart
        fig_doughnut = px.pie(scores_data, names='Category', values='Score', title='Score Distribution by Category',
                              hole=0.4, color_discrete_sequence=["#377bff", "#15965f", "#fa6868"])
        fig_doughnut.update_traces(textposition='inside', textinfo
