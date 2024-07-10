import streamlit as st
import pandas as pd
import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
import matplotlib.pyplot as plt

# Path to the logo image
logo_path = "Logo.png"

# Define the categories, types, and questions
categories = {
    "General": {
        "Individual Actions": [
            "I speak up when members of my team say things that are rooted in stereotype or assumption",
            "I get involved with and build strong, meaningful partnerships with communities of/organizations that support historically marginalized groups",
            "I intentionally give equal attention to people from all backgrounds",
            "I value dissenting opinions, even when it makes me uncomfortable",
            "I regularly examine my most frequent connections and consider how I can further diversify the perspectives and experiences of those around me",
            "I consider multiple sources of data when making decisions and I don’t rely too often on 'gut reaction'"
        ],
        "Institution Actions": [
            "I encourage everyone in my team to speak up when they hear things that are rooted in stereotype or assumption",
            "When I launch a new project or piece of work, I review the team assigned to ensure it's fully diverse, and take action if it’s not",
            "I encourage dissenting opinions to be shared across the team",
            "I encourage my team members to get involved Employee Resource Groups",
            "I proactively seek insights from various Employee Resource Groups to make my function/team/department better"
        ]
    },
    "Recruiting & Hiring": {
        "Individual Actions": [
            "When hiring a member of my direct team, I hold off on making a selection decision until there is a balanced slate of candidates",
            "When interviewing for a new team member, I use structured interview guides and rate all candidates according to consistent criteria and job requirements",
            "Every new member of my direct team takes inclusion/unconscious bias training when they start in a new role"
        ],
        "Institution Actions": [
            "My function has institutionalized a balanced slate policy",
            "My function requires structured interviews or diverse interview panels for all open roles",
            "My function has embedded inclusion/unconscious bias training into new hire onboarding"
        ]
    },
    "Culture & Engagement": {
        "Individual Actions": [
            "I evaluate my use of language and avoid terms/phrases that may unintentionally be degrading or hurtful to people different than me"
        ],
        "Institution Actions": [
            "I participate in and support the review or policies & practices across all functions (not just HR) and to ensure these are inclusive and free from bias"
        ]
    },
    "Development": {
        "Individual Actions": [
            "I actively sponsor and mentor employees from historically marginalized groups",
            "I regularly mentor and sponsor women/people from historically marginalized groups outside of my organization and across my industry",
            "I hold the members of my team accountable for mentoring and sponsoring employees from historically marginalized groups (and incorporate this into annual performance reviews)",
            "I create detailed individual development plans for every member of my team"
        ],
        "Institution Actions": [
            "I visibly support the formal mentoring and sponsorship programs my organization implements",
            "I monitor my team’s participation in training programs to ensure employees from all different backgrounds are included",
            "I outwardly support ongoing inclusion/unconscious bias training for all employees"
        ]
    },
    "Performance & Reward": {
        "Individual Actions": [
            "I regularly review and address bias/equity in pay decisions",
            "When conducting performance reviews, I review performance ratings distributions by demographic to identify potential bias"
        ],
        "Institution Actions": [
            "I visibly support the systemic review of pay equity and performance rating distributions by demographic group annually"
        ],
        "Industry Actions": [
            "I visibly support the public publication of pay equity results and our plans to mitigate any gaps"
        ]
    },
    "Exit & Retain": {
        "Individual Actions": [
            "I personally and intentionally speak to critical employees from all different backgrounds to explore exit and stay reasons"
        ],
        "Institution Actions": [
            "My function regularly conducts exit interviews",
            "My function takes necessary actions to improve the retention of people from all backgrounds"
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
        options = [1, 2, 3, 4, 5]
        key = f"{item['category']}_{item['type']}_{item['question']}"

        if key not in st.session_state:
            st.session_state[key] = 1

        selected_option = st.selectbox(
            "Select your response:", options, index=options.index(st.session_state[key]) if st.session_state[key] in options else 0,
            key=key
        )

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

# Function to create custom progress bar
def custom_progress_bar(percentage, color="#377bff"):
    st.markdown(
        f"""
        <div style="width: 100%; background-color: #e0e0e0; border-radius: 5px;">
            <div style="width: {percentage}%; background-color: {color}; padding: 5px; color: white; text-align: center; border-radius: 5px;">
                {percentage}%
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Function to create custom stacked bar chart
def custom_stacked_bar_chart(scores_data):
    st.markdown("<h3>Self Assessment Scores by Category and Type (Stacked)</h3>", unsafe_allow_html=True)
    chart_images = []
    for category in scores_data["Category"].unique():
        st.markdown(f"### {category}", unsafe_allow_html=True)
        category_data = scores_data[scores_data["Category"] == category]
        
        fig, ax = plt.subplots(figsize=(8, 1))
        ax.barh(category_data["Type"], category_data["Percentage"], color='#377bff')
        ax.set_xlim(0, 100)
        ax.set_xlabel('Percentage')
        ax.set_title(category)
        plt.tight_layout()
        
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        chart_images.append(buf)
        st.image(buf)
    return chart_images

# Function to generate PDF
def generate_pdf(total_scores_per_category, max_scores_per_category, chart_images):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.drawString(100, height - 40, "Anti-Bias Self Assessment Tool")
    c.drawString(100, height - 60, "Your results:")

    y = height - 80
    for category_name, score in total_scores_per_category.items():
        max_score = max_scores_per_category[category_name]
        progress = int((score / max_score) * 100)
        c.drawString(100, y, f"{category_name}: {score} out of {max_score} ({progress}%)")
        y -= 20

    # Add explanations
    explanations = [
        "How to interpret the results",
        "The questions answered fall under the individual, company, and industry related actions and choices you make every day at work.",
        "They address key areas from hiring through developing and retaining talent that we as company leaders make in relation to our peers, team members, superiors, and creating a broader impact on the industry.",
        "Take a look at the scores below and see:",
        "- Where do you score highest?",
        "- Which area has the highest potential to improve?",
        "- Is there anything that surprised you?",
        "- What are some of the actions that you can take to reduce bias and drive inclusion?",
        "Capture your reflection for a later conversation.",
        "Development: Spans actions in the area of developing talent/your team",
        "General: Covers general work related attitudes and actions",
        "Recruiting & Hiring: Highlights potential bias in recruiting and hiring talent",
        "Performance & Reward: Looks at equity in relation to this area of rewarding the team",
        "Culture & Engagement: Your actions and attitudes related to organisational culture",
        "Exit & Retention: Actions related to retaining and understanding the reasons for talent drain"
    ]
    for explanation in explanations:
        y -= 20
        c.drawString(100, y, explanation)
    
    c.showPage()

    # Embed charts into the PDF
    for img in chart_images:
        c.drawImage(ImageReader(img), 100, height - 200, width=400, height=200)
        c.showPage()

    c.save()
    buffer.seek(0)

    return buffer

# Main function to display the self-assessment form
def main():
    try:
        st.image(logo_path, width=200)  # Add your logo at the top
    except Exception as e:
        st.error("Logo image not found. Please check the path to the logo image.")
        st.write(e)
        
    st.title("Anti-Bias Self Assessment Tool")
    st.write(
        "This tool enables you to explore your own behaviors related to bias & inclusion in the workplace. "
        "Your results are yours and yours alone -- they will not be submitted or shared in any manner unless you choose to do so."
    )
    st.write(
        "Read each statement and choose a score using the rating scale provided. "
        "Once complete, the tool subtotals the scores by section. Reflect on areas where your scores are lower than others and identify where you can continue to grow. "
        "The assessment should take you no longer than 5 – 10 mins."
    )
    st.write("### Rating Scale: 1 = Never | 2 = Rarely | 3 = Sometimes | 4 = Often | 5 = Consistently all the time")

    # Shuffle questions once per session
    if 'shuffled_questions' not in st.session_state:
        st.session_state['shuffled_questions'] = questions_list.copy()
        random.shuffle(st.session_state['shuffled_questions'])

    # Display the questions and collect responses
    responses = display_questions()

    # Calculate the total score
    total_score = calculate_total_score(responses)

    # Calculate the total scores per category
    total_scores_per_category = calculate_total_scores_per_category(responses)

    # Calculate the maximum possible scores per category
    max_scores_per_category = calculate_max_scores_per_category(categories)

    # Display the results and visualizations
    if st.button("Submit"):
        st.write("## Assessment Complete. Here are your results:")

        st.write("### How to interpret the results")
        st.write(
            "The questions answered fall under the individual, company, and industry related actions and choices you make every day at work. "
            "They address key areas from hiring through developing and retaining talent that we as company leaders make in relation to our peers, team members, superiors, and creating a broader impact on the industry."
        )
        st.write(
            "Take a look at the scores below and see:\n"
            "- Where do you score highest?\n"
            "- Which area has the highest potential to improve?\n"
            "- Is there anything that surprised you?\n"
            "- What are some of the actions that you can take to reduce bias and drive inclusion?\n"
            "Capture your reflection for a later conversation."
        )
        st.write("#### Development")
        st.write("Spans actions in the area of developing talent/your team")
        st.write("#### General")
        st.write("Covers general work related attitudes and actions")
        st.write("#### Recruiting & Hiring")
        st.write("Highlights potential bias in recruiting and hiring talent")
        st.write("#### Performance & Reward")
        st.write("Looks at equity in relation to this area of rewarding the team")
        st.write("#### Culture & Engagement")
        st.write("Your actions and attitudes related to organisational culture")
        st.write("#### Exit & Retention")
        st.write("Actions related to retaining and understanding the reasons for talent drain")

        # Display total scores per category
        for category_name, score in total_scores_per_category.items():
            max_score = max_scores_per_category[category_name]
            st.write(f"**{category_name}: {score} out of {max_score}**")

            # Calculate and display custom progress bar
            progress = int((score / max_score) * 100)
            custom_progress_bar(progress)

        # Prepare data for visualization
        flattened_scores = []
        for category_name, types in categories.items():
            for type_name, questions in types.items():
                response_scores = [response['score'] for response in responses if (response['category'] == category_name) and (response['type'] == type_name) and (type(response['score']) == int)]
                score = sum(response_scores)
                max_score = len(questions) * 5
                percentage = (score / max_score) * 100
                flattened_scores.append({"Category": category_name, "Type": type_name, "Score": score, "Percentage": percentage})
        scores_data = pd.DataFrame(flattened_scores)

        # Sort the scores_data based on the ordered categories
        ordered_categories = scores_data["Category"].unique()
        scores_data["Category"] = pd.Categorical(scores_data["Category"], categories=ordered_categories, ordered=True)
        scores_data = scores_data.sort_values(by=["Category", "Percentage"], ascending=[True, False])

        # Create a custom horizontal stacked bar chart for scores (percentage)
        chart_images = custom_stacked_bar_chart(scores_data)

        # Generate and provide download link for PDF
        pdf_buffer = generate_pdf(total_scores_per_category, max_scores_per_category, chart_images)
        st.download_button(
            label="Download PDF of Results",
            data=pdf_buffer,
            file_name="assessment_results.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    main()
