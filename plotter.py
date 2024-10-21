import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def generalized_plotter(data_dict):
    """Generalized function to plot various charts using matplotlib."""
    plt.figure(figsize=(8, 4))  # Adjust the width and height as needed
    if "line" in data_dict:
        data = pd.DataFrame({'columns': data_dict["line"]["columns"], 'values': data_dict["line"]["data"]})
        plt.plot(data['columns'], data['values'], marker='o')
        plt.xlabel("Columns")
        plt.ylabel("Values")
        plt.title("Line Plot")
        st.pyplot(plt)

    elif "scatter" in data_dict:
        data = pd.DataFrame({'x': data_dict["scatter"]["x"], 'y': data_dict["scatter"]["y"]})
        plt.scatter(data['x'], data['y'])
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Scatter Plot")
        st.pyplot(plt)

    elif "bar" in data_dict:
        data = pd.DataFrame({'columns': data_dict["bar"]["columns"], 'values': data_dict["bar"]["data"]})
        plt.bar(data['columns'], data['values'])
        plt.xlabel("Columns")
        plt.ylabel("Values")
        plt.title("Bar Chart")
        st.pyplot(plt)

    elif "histogram" in data_dict:
        data = pd.Series(data_dict["histogram"]["data"])
        plt.hist(data, bins=data_dict.get("bins", 10))
        plt.xlabel("Values")
        plt.ylabel("Frequency")
        plt.title("Histogram")
        st.pyplot(plt)

    elif "pie" in data_dict:
        data = pd.Series(data_dict["pie"]["data"], index=data_dict["pie"]["labels"])
        plt.pie(data, labels=data.index, autopct='%1.1f%%')
        plt.title("Pie Chart")
        st.pyplot(plt)

    elif "table" in data_dict:
        df = pd.DataFrame(data_dict["table"]["data"], columns=data_dict["table"]["columns"])
        st.write("Table:")
        st.dataframe(df)

    elif "answer" in data_dict:
        st.write(data_dict["answer"])
    else:
        st.write("Unsupported plot type or missing data.")
    plt.clf() 
