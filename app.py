import pandas as pd
import json
import streamlit as st
from langchain_groq import ChatGroq
from langchain_experimental.agents import create_pandas_dataframe_agent
from chat import chat_display
from plotter import generalized_plotter

# Initialize the ChatGroq model (LLM)
llm = ChatGroq(
    model="llama3-70b-8192", # you can use an of the suited models
    temperature=0.1,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    groq_api_key='groq_api_key' # Replace with your Groq API key
)

def main():
    st.title("📊 Analytica")  
    st.header("✨ Advanced Multimodal LLM based Data Interpretation tool") 
    st.write("Upload a CSV file to analyze and visualize data.")

    # Sidebar for file upload
    st.sidebar.header("Upload Data")
    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if uploaded_file is not None:
        # Load CSV file
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview:")
        st.dataframe(df)

        # User input
        user_input = st.chat_input("Ask your question about the data:")

        if user_input:
            # Save user input to chat history
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Create a DataFrame agent
            agent = create_pandas_dataframe_agent(llm, df, verbose=False, allow_dangerous_code=True)

            # Define the prompt for the query
            prompt = """
            You are an assistant that can analyze data and generate plots and answers based on queries related to a CSV dataset. Given the query, please return a dictionary structured in a specific format for plotting. The output must strictly adhere to the following formats and should not contain any extra characters, ellipses, or placeholders.
            The output should include one of the following keys based on the query:
            1. "line" - for line plots with data formatted as:
               {"line": {"columns": ["x1", "x2", ...], "data": [value1, value2, ...]}}

            2. "scatter" - for scatter plots with data formatted as:
               {"scatter": {"x": [x1, x2, ...], "y": [y1, y2, ...]}}

            3. "bar" - for bar charts with data formatted as:
               {"bar": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

            4. "histogram" - for histograms with data formatted as:
               {"histogram": {"data": [data1, data2, ...], "bins": number_of_bins}}

            5. "pie" - for pie charts with data formatted as:
               {"pie": {"labels": ["label1", "label2", ...], "data": [value1, value2, ...]}}

            6. "table" - for displaying data in table format with data structured as:
               {"table": {"columns": ["column1", "column2", ...], "data": [[row1_value1, row1_value2, ...], [row2_value1, row2_value2, ...]]}}

            7. "answer" - for displaying a response to a question in a structured format:
               {"answer": "your answer here"}

               The output must strictly adhere to the following formats and should not contain any extra characters, ellipses, or placeholders.
            """

            # Combine user input and prompt
            final = user_input + prompt

            # Invoke the agent with the final prompt
            response = agent.invoke(final)

            # Extract and convert the output to a dictionary
            output_str = response["output"]

            # Normalize and prepare the output string for JSON parsing
            output_str = output_str.replace("“", '"').replace("”", '"')  # Fix fancy quotes if any
            output_str = output_str.replace("'", '"')  # Replace single quotes with double quotes

            # Clean up the output string if it has trailing commas or other issues
            output_str = output_str.strip()  # Remove leading/trailing whitespace

            # Attempt to load the output string as JSON
            try:
                data = json.loads(output_str)  # Convert string to dictionary

                # Check if the output string contains any of the plot keywords
                if any(keyword in output_str.lower() for keyword in ["table", "pie", "bar", "scatter", "line", "histogram"]):
                    st.session_state.messages.append({"role": "assistant", "content": "Here goes your output:"})
                    generalized_plotter(data)  # Generate the relevant plot
                else:
                    # Append the answer from the response if available
                    answer_content = data.get("answer", "No output to display.")
                    st.session_state.messages.append({"role": "assistant", "content": answer_content})
            except json.JSONDecodeError as e:
                st.error(f"Failed to decode JSON: {e}")
                st.write(f"Raw output was: {output_str}")

        # Display chat history and scroll to the bottom
        chat_display(st.session_state.messages)

        # Scroll down the chat display
        if st.session_state.messages:
            st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
