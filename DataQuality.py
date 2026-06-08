## Import Libraries

import seaborn as sns 
import pandas as pd
from datetime import datetime
from typing import Optional, Any, Dict
import re 
from sklearn.metrics import accuracy_score 
import numpy as np 

## Data Quality Class 

class data_quality_checker: 

    """
    The class serves as a data quality checker to make sure the data follows
    the basic measures for data quality. 

    Quality Checks: Consistency, Accuracy, Timeliness, Uniqueness, Completeness 

    """
    
    def __init__(self, df: pd.DataFrame): 
        self.df = df.copy() 

    def check_data_completeness(self):  # Completeness

        missing_results = pd.DataFrame({"Total_Missing": (self.df.isnull().sum()),
                                        "Percent_Missing": (self.df.isnull().sum()/ len(df)*100)})
        missing_results["Missing_Impact"] = missing_results["Percent_Missing"].apply(lambda x: "High" if x > 15 else ("Medium" if x > 5 else "Low"))
        
        return missing_results

    def check_data_timeliness(self):  # Timeliness 

        current_month = datetime.now().month 
        df["Last_Updated"] = pd.to_datetime(df["Last_Updated"])
        df["Last_Updated_Month"] = datetime.month(df["Last_Updated"])
        df["Month_Difference"] = df["Last_Updated_Month"] - current_month
        df['Timely'] = df["Month_Difference"] <= 1 

        return df 
    
    def check_duplicated_values(self):  # Uniqueness 

        duplicated_values = df.duplicated(keep = False)
        total_dup = duplicated_values.sum() 
        
        if total_dup != 0: 
            df.drop_duplicates(inplace=True)
            total_dup_transform = df.duplicated().sum()

        results = {
            "Total Duplicates": total_dup,
            "Post-Tranform Duplicates": total_dup_transform
        }

        return pd.DataFrame([results])

    # reference_df: pd.DataFrame add to check_accuracy_values when needed
    def check_accuracy_values(self): # Accuracy
        cols = df.columns
        
        scores = {} 
        for col in cols: 

            # y_true = reference_df[col]
            y_pred = df[col]

            # scores[col] = accuracy_score(y_true, y_pred)
        
        outlier_info = {}
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        for col in numeric_cols: 

            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)

            iqr_range = Q3 - Q1

            outliers = df[(df[col] < 1.5*iqr_range) | (df[col] > 1.5*iqr_range)][col]

            if not outliers.empty: 
                outlier_info[col] = len(outliers)
        

        return scores , outlier_info 




# Import Dataset 

df = sns.load_dataset("tips")
data_quality_check = data_quality_checker(df) 

# Interactive Dashboard 

import streamlit as st 

st.title("Data Quality Checker")

read_me = st.sidebar.checkbox("What does this do?")

if read_me: 
    st.write("The purpose of this dashboard is to gain instant insight into data quality through data quality dimensions. The dimensions include: Accuracy, Completeness, Validity, Timeliness, and Uniqueness. Note: Quality Measures duch as Timeliness and Validity can be dataset dependent. This implies that some will not contain a 'Last Updated' column for timeliness or values needed for Regex validation.")
    st.write("The dashboard also contains schema analysis with the Python GX package. This allows for data validation for schemas directly and ensures that specific input schemas are correct.")

    st.write("Documentation:")
    st.page_link("https://docs.greatexpectations.io/docs/core/introduction/try_gx/", label = "GX Package Docs", icon="🌐")


data_st = st.sidebar.checkbox("Check the DataFrame")
    
if data_st: 
    st.write(df)

Rule_Att = ["", "Accuracy", "Timeliness", "Validity", "Completeness", "Uniqueness"]
Rule = st.sidebar.selectbox("Select the Data Quality Rule:", Rule_Att)

## Sidebar Button User Interaction with created functions 
if Rule == "Completeness": 
    complete_values = data_quality_check.check_data_completeness() 
    st.write("Missing Values")
    st.dataframe(complete_values)
elif Rule == "Uniqueness": 
    unique_values = data_quality_check.check_duplicated_values() 
    st.write("Duplicate Values")
    st.dataframe(unique_values)
elif Rule == "Timeliness":
    timely_values = data_quality_check.check_data_timeliness()  
    st.dataframe(timely_values)
elif Rule == "Accuracy": 
    # df_reference = pd.read_csv() ### CHOOSE THE REFERENCE then ADD it to the function below
    accuracy_values = data_quality_check.check_accuracy_values() 
    st.write("Accuracy Values")
    st.dataframe(accuracy_values)
else: 
    st.write("")




