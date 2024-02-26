import pandas as pd
import mysql.connector as sql                     
import streamlit as st
import plotly.express as px                       
from streamlit_option_menu import option_menu
import mysql.connector 
from PIL import Image
import geopandas as gpd

# Creating connection with mysql workbench
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="abcd",
    database="phonepe_data")
# Creating a cursor
cursor = mydb.cursor()

#streamlit page settings:

# streamlit page settings:
st.set_page_config(
    page_title="PhonePe Pulse Data Visualization and Exploration",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add title to the main page
st.markdown("<h1 style='color: #6F36AD;'>PhonePe Pulse Data Visualization and Exploration</h1>", unsafe_allow_html=True)
import base64
# Add image to the sidebar
image_path = r"C:\Users\\Documents\data_science-shubh\New-PhonePe-Logo.png"
st.sidebar.markdown(f'<img src="data:image/png;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}" alt="PhonePe Logo" style="width:70%;">', unsafe_allow_html=True)

# Option menu
SELECT = option_menu(
    menu_title=None,
    options=["About", "Home", "Top Charts", "Explore Data"],
    icons=["clipboard", "house", "bar-chart", "toggles", "at"],
    default_index=2,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#6F36AD", "size": "cover", "width": "100"},
        "icon": {"color": "black", "font-size": "20px"},
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
        "nav-link-selected": {"background-color": "#6F36AD"}
    })

with st.sidebar:
    st.markdown("**Filters**")
    year_key = "year_slider"
    quarter_key = "quarter_slider"
    Year = st.slider("**Year**", key=year_key, min_value=2018, max_value=2023)
    Quarter = st.slider("Quarter", key=quarter_key, min_value=1, max_value=4)
    Type = st.selectbox("**Type**", ("Transactions", "Transaction Type","Users", "Insurance"))

# Home
if SELECT == "About":
    col1, col2 = st.columns(2)
    col1.image(Image.open(r"C:\Users\\Documents\data_science-shubh\PhonePe-Logo.png"), width=200)
    with col1:
        st.subheader("About PhonePe")
        st.info("Established in December 2015")
        st.info("A leading Indian fintech company headquartered in Bengaluru")
        st.info("Pioneered by Sameer Nigam, Rahul Chari, and Burzin Engineer")
        st.info("Launched its UPI-based app in August 2016")
        st.info("Today, as a Flipkart subsidiary, PhonePe stands as a key player in the digital payments landscape.")
if SELECT == "Home":
    st.subheader("Welcome to the PhonePe Pulse Dashboard!")
    st.info(
        "This dashboard provides key insights and analytics related to PhonePe, one of the leading fintech companies in India."
    )
    st.info(
        "Explore different sections like 'Top Charts' and 'Explore Data' to gain valuable information about PhonePe's performance and impact."
    )
    st.info(
        "Use the navigation menu on the left to switch between sections and discover interesting data points and trends."
    )
    st.info(
        "The PhonePe dashboard is designed to offer a comprehensive view of PhonePe's digital payment ecosystem. "
        "It helps you understand trends, user behavior, and transaction patterns, providing valuable insights for strategic decision-making."
    )
    st.info(
        "Gain a deeper understanding of PhonePe's role in the financial landscape, track top charts, and explore data to make informed decisions in the rapidly evolving fintech industry."
    )

# TOP CHARTS
elif SELECT == "Top Charts":
    st.markdown("## :green[Top Charts]")
    st.info(
        """
        #### Explore Key Insights:
        - View the overall ranking for a specific Year and Quarter.
        - Identify the top 10 States and Districts based on total transactions and spending on PhonePe.
        - Compare Transaction (Payment) Types based on the Total Transactions.
        - Discover the top 10 States and Districts by the number of PhonePe users and their app engagement.
        - Uncover the top 10 mobile brands and their usage percentages among PhonePe users.
        - In Insurance, explore top 10 States and Districts by total Insurance Count and Amount.
        """, icon="📈")

    # Top Charts - TRANSACTIONS
    if Type == "Transactions":
        col1, col2, col3 = st.columns([1, 1, 1], gap="medium")
        with col1:
            st.markdown("### :violet[State]")
            cursor.execute(
                f"select States, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from phonepe_data.aggregated_transaction where Years = {Year} and Quarter = {Quarter} group by States order by Total desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transactions_count', 'Total_Transaction_amount'])
            fig = px.pie(df, values='Total_Transaction_amount',
                         names='State',
                         title='Top 10',
                         color_discrete_sequence=px.colors.qualitative.Set1,
                         hover_data=['Total_Transactions_count'],
                         labels={'Total_Transactions_count': 'Total_Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### :violet[District]")
            cursor.execute(
                f"select District, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from map_transaction where Years = {Year} and Quarter = {Quarter} group by District order by Total desc limit 10")
            df = pd.DataFrame(cursor.fetchall(),
                              columns=['District', 'Transactions_Count', 'Total_Transaction_amount'])

            fig = px.pie(df, values='Total_Transaction_amount',
                         names='District',
                         title='Top 10',
                         color_discrete_sequence=px.colors.qualitative.Set1,
                         hover_data=['Transactions_Count'],
                         labels={'Transactions_Count': 'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        with col3:
            st.markdown("### :violet[Pincodes]")
            cursor.execute(
                f"select pincodes, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_transaction where Years = {Year} and Quarter = {Quarter} group by pincodes order by Total desc limit 10")
            df = pd.DataFrame(cursor.fetchall(),
                              columns=['pincodes', 'Transactions_Count', 'Total_Transaction_amount'])

            fig = px.pie(df, values='Total_Transaction_amount',
                         names='pincodes',
                         title='Top 10',
                         color_discrete_sequence=px.colors.qualitative.Set1,
                         hover_data=['Transactions_Count'],
                         labels={'Transactions_Count': 'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

    # Top Charts - Users:
    elif Type == "Users":
        col1,col2,col3 = st.columns([2,2,2],gap="medium")
        
        with col1:
            st.markdown("### :violet[Brands]")
            cursor.execute(f"select Brands, sum(Transaction_count) as Total_Count, avg(Percentage)*100 as Avg_Percentage from aggregated_user where Years = {Year} and Quarter = {Quarter} group by Brands order by Total_Count desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
            fig = px.bar(df,title='Top 10',
                         x="Total_Users",
                         y="Brand",orientation='h',
                         color='Avg_Percentage',
                         color_continuous_scale=px.colors.qualitative.Set1)
            st.plotly_chart(fig,use_container_width=True)   
    
        with col2:
            st.markdown("### :violet[District]")
            cursor.execute(f"select Districts, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where Years = {Year} and Quarter = {Quarter} group by Districts order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.qualitative.Set1)
            st.plotly_chart(fig,use_container_width=True)
              
            
        with col3:
            st.markdown("### :violet[State]")
            cursor.execute(f"select States, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where Years = {Year} and Quarter = {Quarter} group by states order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.qualitative.Set1,
                             hover_data=['Total_Appopens'],
                             labels={'Total_Appopens':'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)


    elif Type == "Insurance":
        col1, col2, col3 = st.columns([1, 1, 1], gap="medium")

        with col1:
            st.markdown("### :violet[State]")
            cursor.execute(
                f"SELECT States, SUM(Insurance_count) AS Total_Insurance_Policies_Purchased, SUM(Insurance_amount) AS Total_Premium_Value FROM aggregated_insurance WHERE Years = {Year} AND Quarter = {Quarter} GROUP BY States ORDER BY Total_Premium_Value DESC LIMIT 10"
            )
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Insurance_Policies_Purchased', 'Total_Premium_Value'])
            fig = px.pie(df, values='Total_Premium_Value',
                        names='State',
                        title='Top 10 ',
                        color_discrete_sequence=px.colors.qualitative.Set1,
                        hover_data=['Total_Insurance_Policies_Purchased'],
                        labels={'Total_Insurance_Policies_Purchased': 'Total Insurance Policies Purchased'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### :violet[District]")
            cursor.execute(
                f"SELECT District, SUM(Transaction_count) AS Total_Transactions_Count, SUM(Transaction_amount) AS Total_Premium_Value FROM map_insurance WHERE Years = {Year} AND Quarter = {Quarter} GROUP BY District ORDER BY Total_Premium_Value DESC LIMIT 10"
            )
            df = pd.DataFrame(cursor.fetchall(),
                            columns=['District', 'Transactions_Count', 'Total_Premium_Value'])

            fig = px.pie(df, values='Total_Premium_Value',
                        names='District',
                        title='Top 10 ',
                        color_discrete_sequence=px.colors.qualitative.Set1,
                        hover_data=['Transactions_Count'],
                        labels={'Transactions_Count': 'Total Insurance Policies Purchased'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

    elif Type == "Transaction Type":
        st.markdown("## :violet[Top Transaction(Payment) Type]")
        cursor.execute(
            f"select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from phonepe_data.aggregated_transaction where Years= {Year} and Quarter = {Quarter} group by Transaction_type order by Transaction_type")
        df = pd.DataFrame(cursor.fetchall(), columns=['Transaction_type', 'Total_Transactions', 'Total_amount'])
        fig = px.bar(df,
                    
                    x="Transaction_type",
                    y="Total_Transactions",
                    orientation='v',
                    color='Total_amount',
                    color_continuous_scale=px.colors.qualitative.Set1)
        st.plotly_chart(fig, use_container_width=False)

#------Explore DAta-----#
            
elif SELECT == "Explore Data":


    # EXPLORE DATA - TRANSACTIONS
    if Type == "Transactions":
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[All India States Data - Transactions]")
        cursor.execute(
            f"select States, sum(Transaction_count) AS Total_Transactions, sum(Transaction_amount) AS Total_amount FROM phonepe_data.aggregated_transaction WHERE Years = {Year} AND Quarter = {Quarter} GROUP BY States ORDER BY States")
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
        df2 = pd.read_csv(r"C:\Users\\Documents\data_science-shubh\shubh-pr.2-phonepe pulse\IndiaStatesNames..csv")
        df1.Total_amount = df1.Total_amount.astype(float)
        

        # Merge data with state names
        df1 = pd.merge(df2, df1, how='left', left_on='State', right_on='State')

        fig = px.choropleth(df1,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color='Total_amount',
                            color_continuous_scale='sunset',
                            hover_data=['State', 'Total_Transactions', 'Total_amount'])  # Add hover_data parameter

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig, use_container_width=True)


    # EXPLORE DATA - Users:
    elif Type == "Users":
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[All India States Data - Users]")
        cursor.execute(
            f"select States, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_App_Opens from phonepe_data.map_user where Years = {Year} and Quarter = {Quarter} group by States order by States")
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users', 'Total_App_Opens'])
        df2 = pd.read_csv(r"C:\Users\\Documents\data_science-shubh\shubh-pr.2-phonepe pulse\IndiaStatesNames..csv")
        df1.Total_App_Opens = df1.Total_App_Opens.astype(float)
        
        # Check if there is data for Jammu & Kashmir and Ladakh
        # If not, you may need to add them manually to df1
        
        # Example:
        # df1 = df1.append({'State': 'Jammu & Kashmir', 'Total_Users': 0, 'Total_App_Opens': 0}, ignore_index=True)
        # df1 = df1.append({'State': 'Ladakh', 'Total_Users': 0, 'Total_App_Opens': 0}, ignore_index=True)

        # Merge data with state names
        df1 = pd.merge(df2, df1, how='left', left_on='State', right_on='State')

        fig = px.choropleth(df1,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color='Total_App_Opens',
                            color_continuous_scale='sunset',
                            hover_data=['State', 'Total_Users', 'Total_App_Opens'])  # Add hover_data parameter

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig, use_container_width=True)


    elif Type == "Insurance":
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[All India States Data - Insurance]")
        cursor.execute(
            f"select States, SUM(Insurance_count) AS Total_Insurance_Policies_Purchased, SUM(Insurance_amount) AS Total_Premium_Value FROM phonepe_data.aggregated_insurance WHERE Years = {Year} AND Quarter = {Quarter} GROUP BY States ORDER BY States")
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Insurance_Policies_Purchased', 'Total_Premium_Value'])
        df2 = pd.read_csv(r"C:\Users\\Documents\data_science-shubh\shubh-pr.2-phonepe pulse\IndiaStatesNames..csv")
        df1.Total_Premium_Value = df1.Total_Premium_Value.astype(float)
        
        # Merge data with state names
        df1 = pd.merge(df2, df1, how='left', left_on='State', right_on='State')

        fig = px.choropleth(df1,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color='Total_Premium_Value',
                            color_continuous_scale='sunset',
                            hover_data=['State', 'Total_Insurance_Policies_Purchased', 'Total_Premium_Value'])  # Add hover_data parameter

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig, use_container_width=True)
