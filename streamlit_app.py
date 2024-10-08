import streamlit as st
import pandas as pd
from functions import st_read_from_snowflake, st_execute_query_on_snowflake

# Function to fetch data from the EXTRA_TABLES table
def get_extra_tables_data():
    query = "SELECT * FROM EXTRA_TABLES"
    df = st_read_from_snowflake(query)
    return df

# Function to get the top 5 users from Snowflake
def get_top_5_users():
    query = """
    SELECT
        user_name,
        COUNT(query_id) AS total_queries,
        ROUND((SUM(execution_time) / 1000 / 60), 2) AS total_exec_minutes,
        ROUND(SUM(credits_used_cloud_services), 2) AS credits_consumed
    FROM
        snowflake.account_usage.query_history
    WHERE
        start_time > CURRENT_DATE()-7 
        AND user_name NOT IN ('CDC_USER', 'SYSTEM', 'MIS_USER')
        AND credits_used_cloud_services > 0                             
    GROUP BY
        1
    HAVING credits_consumed > 0
    ORDER BY
        4 DESC
    LIMIT
        5
    """
    df = st_read_from_snowflake(query)
    return df

# Main Streamlit App
def main():
    st.title("Streamlit Dashboard")

    # Create two columns in the UI
    col1, col2 = st.columns(2)

    # Left Column: Display data from EXTRA_TABLES
    with col1:
        st.header("EXTRA_TABLES Data")
        df_extra = get_extra_tables_data()
        st.dataframe(df_extra)

    # Right Column: Top 5 Users
    with col2:
        st.header("Top 5 Users")
        df_users = get_top_5_users()
        if not df_users.empty:
            st.dataframe(df_users)
        else:
            st.write("No data found for the top 5 users.")

    # Placeholder for additional widgets in the bottom area (to be added later)
    st.write("Additional widgets will be displayed here.")

if __name__ == "__main__":
    main()
