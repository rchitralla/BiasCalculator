import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd

# Path to the logo image
logo_path = "Logo.png"

# Define the sections and questions
sections = {
    "General": [
        "I speak up when team members say things based on stereotypes or assumptions.",
        "I build strong partnerships with communities and organizations supporting historically marginalized groups.",
        "I give equal attention to people from all backgrounds.",
        "I value dissenting opinions, even when they make me uncomfortable.",
        "I examine my connections and diversify the perspectives and experiences around me.",
        "I consider multiple data sources and avoid relying on 'gut reaction' for decisions.",
        "I encourage my team to speak up against stereotypes or assumptions.",
        "I promote the sharing of dissenting opinions across the team.",
        "I seek insights from Employee Resource Groups to improve my function/team/department.",
        "I support reviewing policies across all functions to ensure they are inclusive and free from bias.",
        "I support formal mentoring and sponsorship programs in my organization.",
        "I hold my team accountable for mentoring and sponsoring marginalized employees, including in performance reviews.",
        "I support ongoing inclusion/unconscious bias training for all employees.",
        "I regularly review and address bias/equity in pay decisions.",
        "I support the systemic review of pay equity and performance ratings by demographic annually.",
        "During performance reviews, I check ratings distributions by demographic for potential bias.",
        "I support publicly sharing pay equity results and plans to address gaps.",
        "I personally speak to critical employees from all backgrounds to understand their exit and stay reasons.",
        "My function conducts regular exit interviews.",
        "My function takes actions to improve retention of people from all backgrounds."
    ],
    "Recruiting & Hiring": [
        "I review the team for diversity when starting a project and take action if it's not diverse.",
        "I wait to decide on hiring until there is a balanced slate of candidates.",
        "I use structured interview guides and consistent criteria for all candidates.",
        "I use structured guides and consistent criteria for all interviews.",
        "My function has a balanced slate policy.",
        "My function requires structured interviews or diverse panels for all roles.",
        "Every new team member takes inclusion/unconscious bias training when starting.",
        "My function includes inclusion/unconscious bias training in new hire onboarding."
    ],
    "Culture & Engagement": [
        "I use language carefully to avoid terms that may be degrading or hurtful.",
        "I sponsor and mentor employees from historically marginalized groups.",
        "I mentor and sponsor people from marginalized groups within and outside my organization.",
        "I monitor training participation to ensure inclusion of all backgrounds.",
        "I create individual development plans for every team member.",
        "I support the systemic review of pay equity and performance ratings by demographic annually.",
        "During performance reviews, I check ratings distributions by demographic for potential bias.",
        "I personally speak to critical employees from all backgrounds to understand their exit and stay reasons.",
        "My function conducts regular exit interviews.",
        "My function takes actions to improve retention of people from all backgrounds."
    ]
}

# Function to display each section and collect responses
def display_section(section_name, questions):
    st.header(section_name)
    scores = []
    for question in questions:
        score = st.radio(question, [3, 2, 1], index=2, key=f"{section_name}_{question}")
        scores.append(score)
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

    # Dictionary to store the total scores for each section
    total_scores = {}

    # Iterate over each section and display the questions
    for section_name, questions in sections.items():
        scores = display_section(section_name, questions)
        total_scores[section_name] = sum(scores)

    # Display the results and visualizations
    if st.button("Submit"):
        st.write("## Assessment Complete. Here are your results:")
        for section_name, score in total_scores.items():
            st.write(f"**{section_name}: {score}**")

        lowest_score_section = min(total_scores, key=total_scores.get)
        st.write(f"### Reflect on areas where your scores are lower than others. Consider focusing on improving the **{lowest_score_section}** section.")

        # Visualization using plotly.express
        st.write("### Visualizations")
        
        # Prepare data for visualization
        scores_data = pd.DataFrame({
            "Section": list(total_scores.keys()),
            "Score": list(total_scores.values())
        })

        # Create a bar chart
        fig = px.bar(scores_data, x="Section", y="Score", title="Self Assessment Scores by Section")
        st.plotly_chart(fig)

        # Create a pie chart
        fig_pie = px.pie(scores_data, names="Section", values="Score", title="Distribution of Scores by Section")
        st.plotly_chart(fig_pie)

if __name__ == "__main__":
    main()
