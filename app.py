import streamlit as st
import pandas as pd
import random
import pdfkit
import base64

# Path to the logo image
logo_path = "Logo.png"

# Define the categories, types, and questions
categories = {
    # ... (categories definition)
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
    for category in scores_data["Category"].unique():
        st.markdown(f"### {category}", unsafe_allow_html=True)
        category_data = scores_data[scores_data["Category"] == category]
        bar_html = '<div style="width: 100%; background-color: #e0e0e0; border-radius: 5px; display: flex; align-items: center;">'
        for _, row in category_data.iterrows():
            percentage = row["Percentage"]
            bar_html += f'<div style="width: {percentage}%; background-color: #377bff; padding: 5px; color: white; text-align: center; border-radius: 5px;">{row["Type"]} ({percentage:.2f}%)</div>'
        bar_html += '</div>'
        st.markdown(bar_html, unsafe_allow_html=True)

# Function to generate PDF
def generate_pdf(html_content, output_path):
    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
    }
    pdfkit.from_string(html_content, output_path, options=options)

# Function to get base64 encoded string for PDF
def get_pdf_download_link(pdf_path, download_name):
    with open(pdf_path, "rb") as f:
        pdf_data = f.read()
    b64 = base64.b64encode(pdf_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{download_name}">Download PDF</a>'
    return href

# Main function to display the self-assessment form
def main():
    st.image(logo_path, width=200)  # Add your logo at the top
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
        custom_stacked_bar_chart(scores_data)

        # Generate HTML content for the results
        html_content = f"""
        <html>
        <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .progress-bar {{
                width: 100%; background-color: #e0e0e0; border-radius: 5px;
            }}
            .progress {{
                width: {{}}%; background-color: #377bff; padding: 5px; color: white; text-align: center; border-radius: 5px;
            }}
            .category-title {{ font-weight: bold; }}
        </style>
        </head>
        <body>
        <h1>Assessment Results</h1>
        <p>Here are your self-assessment results:</p>
        """

        for category_name, score in total_scores_per_category.items():
            max_score = max_scores_per_category[category_name]
            progress = int((score / max_score) * 100)
            html_content += f"""
            <div class="category-title">{category_name}: {score} out of {max_score}</div>
            <div class="progress-bar">
                <div class="progress" style="width: {progress}%;"></div>
            </div>
            <br/>
            """

        html_content += "</body></html>"

        # Generate PDF
        pdf_path = "/tmp/assessment_results.pdf"
        generate_pdf(html_content, pdf_path)

        # Provide download link
        st.markdown(get_pdf_download_link(pdf_path, "Assessment_Results.pdf"), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
