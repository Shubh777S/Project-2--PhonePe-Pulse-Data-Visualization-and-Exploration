import pandas as pd
import mysql.connector as sql                     
import streamlit as st
import plotly.express as px                       
from streamlit_option_menu import option_menu
import mysql.connector 
from PIL import Image
import geopandas as gpd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Creating connection with mysql workbench
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="laptop",
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
st.markdown("<h1 style='color: #6F36AD; text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.7);'>PhonePe Pulse Data Visualization and Exploration</h1>", unsafe_allow_html=True)
# SETTING-UP BACKGROUND IMAGE
st.markdown(f""" <style>.stApp {{
                        background:url("data:image/jpeg;base64,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");
                        background-size: cover}}
                     </style>""", unsafe_allow_html=True)


import base64
# Add image to the sidebar
image_path = r"C:\Users\Vozon Comsof Pvt Ltd\Documents\data_science-shubh\phonepe.logoo.jpg"
st.sidebar.markdown(f'<img src="data:image/png;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}" alt="PhonePe Logo" style="width:80%;">', unsafe_allow_html=True)


# Option menu
SELECT = option_menu(
    menu_title=None,
    options=["About", "Home", "Top Charts", "Explore Data", "Insights"],
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
    Type = st.selectbox("**Type**", ("Transactions", "Users", "Insurance", "Transaction Type"))

# Home
if SELECT == "About":
    col1, col2 = st.columns(2)
    col1.image(Image.open(r"C:\Users\Vozon Comsof Pvt Ltd\Documents\data_science-shubh\PhonePe-Logo.png"), width=200)
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
    st.markdown("## :green[Top Charts:]")
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
        level_options = ["State", "District", "Pincodes"]
        selected_level = st.selectbox("Select Level", level_options)
        if selected_level == "State":
            st.markdown("### :violet[Top 10 States]")
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

        elif selected_level == "District":
            st.markdown("### :violet[Top 10 Districts]")
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

        elif selected_level == "Pincodes":
            st.markdown("### :violet[Top 10 Pincodes]")
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
        level_options_users = ["Brand", "District", "State"]
        selected_level = st.selectbox("Select Level", level_options_users)

        if selected_level == "Brand":
            st.markdown("### :violet[Top 10 Brands]")
            cursor.execute(f"select Brands, sum(Transaction_count) as Total_Count, avg(Percentage)*100 as Avg_Percentage from aggregated_user where Years = {Year} and Quarter = {Quarter} group by Brands order by Total_Count desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
            fig = px.bar(df, title='Top 10',
                        y="Total_Users",
                        x="Brand",
                        orientation='v',
                        color='Avg_Percentage',
                        color_continuous_scale=px.colors.qualitative.Set1)
            st.plotly_chart(fig, use_container_width=True)   

        elif selected_level == "District":
            st.markdown("### :violet[Top 10 Districts]")
            cursor.execute(f"select Districts, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where Years = {Year} and Quarter = {Quarter} group by Districts order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                        title='Top 10',
                        y="Total_Users",
                        x="District",
                        orientation='v',
                        color='Total_Users',
                        color_continuous_scale=px.colors.qualitative.Set1)
            st.plotly_chart(fig, use_container_width=True)

        elif selected_level == "State":
            st.markdown("### :violet[Top 10 States]")
            cursor.execute(f"select States, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where Years = {Year} and Quarter = {Quarter} group by states order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                        names='State',
                        title='Top 10',
                        color_discrete_sequence=px.colors.qualitative.Set1,
                        hover_data=['Total_Appopens'],
                        labels={'Total_Appopens': 'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

    elif Type == "Insurance":
        level_options_insurance = ["State", "District", "Pincodes"]
        selected_level = st.selectbox("Select Level", level_options_insurance)
        if selected_level == "State":
            st.markdown("### :violet[Top 10 States]")
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

        elif selected_level == "District":
            st.markdown("### :violet[Top 10 Districts]")
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

        elif selected_level == "Pincodes":
            st.markdown("### :violet[Top 10 Pincodes]")
            cursor.execute(
                f"SELECT pincodes, SUM(Transaction_count) AS Total_Transactions_Count, SUM(Transaction_amount) AS Total_Premium_Value FROM top_insurance WHERE Years = {Year} AND Quarter = {Quarter} GROUP BY pincodes ORDER BY Total_Premium_Value DESC LIMIT 10"
            )
            df = pd.DataFrame(cursor.fetchall(),
                            columns=['pincodes', 'Transactions_Count', 'Total_Premium_Value'])

            fig = px.pie(df, values='Total_Premium_Value',
                        names='pincodes',
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

# EXPLORE DATA - TRANSACTIONS
elif SELECT == "Explore Data":

    if Type == "Transactions":
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[All India States Data - Transactions]")
        cursor.execute(
            f"select States, sum(Transaction_count) AS Total_Transactions, sum(Transaction_amount) AS Total_amount FROM phonepe_data.aggregated_transaction WHERE Years = {Year} AND Quarter = {Quarter} GROUP BY States ORDER BY States"
        )
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
        df2 = pd.read_csv(r"C:\Users\Vozon Comsof Pvt Ltd\Documents\data_science-shubh\shubh-pr.2-phonepe pulse\IndiaStatesNames..csv")
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

        # Fetch the necessary data for df1_states
        cursor.execute(
            f"SELECT States FROM phonepe_data.aggregated_transaction WHERE Years = {Year} AND Quarter = {Quarter} GROUP BY States ORDER BY States"
        )
        df1_states = pd.DataFrame(cursor.fetchall(), columns=['State'])

        # Add a dropdown to select a specific state
        selected_state = st.selectbox("Select State", df1_states['State'].unique())

        # Check if selected_state is in the df1_states
        if selected_state not in df1_states['State'].values:
            st.warning(f"No data available for {selected_state}")
        else:
            # Continue with the rest of the code

            # EXPLORE DATA - TRANSACTIONS
            if Type == "Transactions":
                # Overall State Data - TOTAL APPOPENS - INDIA MAP
                st.markdown(f"## :violet[{selected_state} - Transactions]")

                # Fetch data for the selected state
                cursor.execute(
                    f"SELECT District, SUM(Transaction_count) AS Total_Transactions_Count, SUM(Transaction_amount) AS Total_amount FROM map_transaction WHERE Years = {Year} AND Quarter = {Quarter} AND States = '{selected_state}' GROUP BY District ORDER BY Total_amount DESC"
                )
                df_transactions = pd.DataFrame(cursor.fetchall(),
                                              columns=['District', 'Total_Transactions_Count', 'Total_amount'])

                # Create bar chart for transactions
                fig_transactions = px.bar(df_transactions, x="District", y="Total_Transactions_Count",
                                          title=f'Transactions in {selected_state} - Top Districts',
                                          color='District',
                                          color_discrete_sequence=px.colors.qualitative.Set3)
                st.plotly_chart(fig_transactions, use_container_width=True)

                # Create pie chart for transactions
                fig_pie_transactions = px.pie(df_transactions, values='Total_amount', names='District',
                                              title=f'Transactions in {selected_state} - Top Districts (Pie Chart)',
                                              color_discrete_sequence=px.colors.qualitative.Set1,
                                              hover_data=['Total_Transactions_Count'],
                                              labels={'Total_Transactions_Count': 'Total Transactions Count'})
                fig_pie_transactions.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie_transactions, use_container_width=True)


    elif Type == "Users":
        st.markdown("## :violet[All India States Data - Users]")
        cursor.execute(
            f"SELECT States, SUM(RegisteredUser) AS Total_Users, SUM(AppOpens) AS Total_App_Opens FROM phonepe_data.map_user WHERE Years = {Year} AND Quarter = {Quarter} GROUP BY States ORDER BY States"
        )
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users', 'Total_App_Opens'])
        df2 = pd.read_csv(r"C:\Users\Vozon Comsof Pvt Ltd\Documents\data_science-shubh\shubh-pr.2-phonepe pulse\IndiaStatesNames..csv")
        df1.Total_App_Opens = df1.Total_App_Opens.astype(float)

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

        # Fetch the necessary data for the list of states
        cursor.execute(
            f"SELECT States FROM phonepe_data.map_user WHERE Years = {Year} AND Quarter = {Quarter} GROUP BY States ORDER BY States"
        )
        df_states = pd.DataFrame(cursor.fetchall(), columns=['State'])

        # Add a dropdown to select a specific state
        selected_state = st.selectbox("Select State", df_states['State'].unique())

        # Check if selected_state is in the df_states
        if selected_state not in df_states['State'].values:
            st.warning(f"No data available for {selected_state}")
        else:
            # Fetch the necessary data for the list of districts in the selected state
            cursor.execute(
                f"SELECT Districts FROM phonepe_data.map_user WHERE Years = {Year} AND Quarter = {Quarter} AND States = '{selected_state}' GROUP BY Districts ORDER BY Districts"
            )
            df_districts = pd.DataFrame(cursor.fetchall(), columns=['District'])

            # Fetch the necessary data for the selected state
            cursor.execute(
                f"SELECT Districts, SUM(RegisteredUser) AS Total_Users, SUM(AppOpens) AS Total_App_Opens FROM phonepe_data.map_user WHERE Years = {Year} AND Quarter = {Quarter} AND States = '{selected_state}' GROUP BY Districts ORDER BY Total_App_Opens DESC"
            )
            df_users_state = pd.DataFrame(cursor.fetchall(), columns=['Districts', 'Total_Users', 'Total_App_Opens'])

            # Create bar chart for users in the selected state with different colors for each district
            fig_users_state = px.bar(df_users_state,
                                    x="Districts",
                                    y="Total_Users",
                                    title=f'Users in {selected_state}',
                                    color='Districts',  # Specify different colors for each district
                                    color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig_users_state, use_container_width=True)

            # Create pie chart for top 10 states
            cursor.execute(
                f"SELECT States, SUM(RegisteredUser) AS Total_Users, SUM(AppOpens) AS Total_App_Opens FROM phonepe_data.map_user WHERE Years = {Year} AND Quarter = {Quarter} GROUP BY States ORDER BY Total_Users DESC LIMIT 10"
            )
            df_top_states = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users', 'Total_App_Opens'])

            # Create pie chart for top 10 states
            fig_top_states = px.pie(df_top_states,
                                    values='Total_Users',
                                    names='State',
                                    title='Top 10 States',
                                    color_discrete_sequence=px.colors.qualitative.Set1,
                                    hover_data=['Total_App_Opens'],
                                    labels={'Total_App_Opens': 'Total App Opens'})

            fig_top_states.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_top_states, use_container_width=True)

    elif Type == "Insurance":
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[All India States Data - Insurance]")
        cursor.execute(
            f"select States, SUM(Insurance_count) AS Total_Insurance_Policies_Purchased, SUM(Insurance_amount) AS Total_Premium_Value FROM phonepe_data.aggregated_insurance WHERE Years = {Year} AND Quarter = {Quarter} GROUP BY States ORDER BY States")
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Insurance_Policies_Purchased', 'Total_Premium_Value'])
        df2 = pd.read_csv(r"C:\Users\Vozon Comsof Pvt Ltd\Documents\data_science-shubh\shubh-pr.2-phonepe pulse\IndiaStatesNames..csv")
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

       # Fetch the necessary data for the list of states
        cursor.execute(
            f"SELECT States FROM phonepe_data.map_insurance WHERE Years = {Year} AND Quarter = {Quarter} GROUP BY States ORDER BY States"
        )
        df_states = pd.DataFrame(cursor.fetchall(), columns=['State'])

        # Add a dropdown to select a specific state
        selected_state = st.selectbox("Select State", df_states['State'].unique())

        # Check if selected_state is in the df_states
        if selected_state not in df_states['State'].values:
            st.warning(f"No data available for {selected_state}")
        else:
            # Fetch the necessary data for the list of districts in the selected state
            cursor.execute(
                f"SELECT District FROM phonepe_data.map_insurance WHERE Years = {Year} AND Quarter = {Quarter} AND States = '{selected_state}' GROUP BY District ORDER BY District"
            )
            df_districts = pd.DataFrame(cursor.fetchall(), columns=['District'])

            # Fetch the necessary data for the selected state
            cursor.execute(
                f"SELECT District, SUM(Transaction_count) AS Total_Insurance_Policies_Purchased, SUM(Transaction_amount) AS Total_Premium_Value FROM phonepe_data.map_insurance WHERE Years = {Year} AND Quarter = {Quarter} AND States = '{selected_state}' GROUP BY District ORDER BY Total_Premium_Value DESC LIMIT 10"
            )
            df_insurance_state_district = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_Insurance_Policies_Purchased', 'Total_Premium_Value'])

            # Create bar chart for insurance policies in the selected state with different colors for each district
            fig_insurance_state_district = px.bar(
                df_insurance_state_district,
                x="District",
                y="Total_Insurance_Policies_Purchased",
                title=f'Insurance Policies in {selected_state}',
                color='District',  # Specify different colors for each district
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig_insurance_state_district, use_container_width=True)

            # Create pie chart for top 10 states
            cursor.execute(
                f"SELECT States, SUM(Transaction_count) AS Total_Insurance_Policies_Purchased, SUM(Transaction_amount) AS Total_Premium_Value FROM phonepe_data.map_insurance WHERE Years = {Year} AND Quarter = {Quarter} GROUP BY States ORDER BY Total_Premium_Value DESC LIMIT 10"
            )
            df_top_states = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Insurance_Policies_Purchased', 'Total_Premium_Value'])

            # Create pie chart for top 10 states
            fig_top_states = px.pie(
                df_top_states,
                values='Total_Insurance_Policies_Purchased',
                names='State',
                title='Top 10 States for Insurance',
                color_discrete_sequence=px.colors.qualitative.Set1,
                hover_data=['Total_Premium_Value'],
                labels={'Total_Premium_Value': 'Total Premium Value'}
            )

            fig_top_states.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_top_states, use_container_width=True)

#-----Insights------#
            
elif SELECT == "Insights":
    
    if Type == "Transactions":
        st.markdown("## :violet[Transaction Trends:]")
        st.info(
        """
        #### Explore Transaction Trends:
        - View the overall transaction trends for all India and specific states.
        - Analyze how transaction counts have evolved over the years.
        """
        )
        # Overall India Transaction Trends
        st.markdown("### :violet[All India Transaction Trends]")
        cursor.execute(
            f"SELECT Years, SUM(Transaction_amount) AS Total_Transaction_Amount FROM phonepe_data.aggregated_transaction GROUP BY Years ORDER BY Years"
        )
        df_all_india = pd.DataFrame(cursor.fetchall(), columns=['Years', 'Total_Transaction_Amount'])

        # Fetch the necessary data for the list of states
        cursor.execute(
            "SELECT DISTINCT States FROM phonepe_data.aggregated_transaction ORDER BY States"
        )
        df_states_insights = pd.DataFrame(cursor.fetchall(), columns=['State'])

        # Create a subplot with one y-axis for trendlines
        fig_all_india = go.Figure()

        # Add line trace for each state
        for state in df_states_insights['State'].unique():
            # Fetch the necessary data for the state
            cursor.execute(
                f"SELECT Years, SUM(Transaction_amount) AS Total_Transaction_Amount FROM phonepe_data.aggregated_transaction WHERE States = '{state}' GROUP BY Years ORDER BY Years"
            )
            df_state = pd.DataFrame(cursor.fetchall(), columns=['Years', 'Total_Transaction_Amount'])
            
            fig_all_india.add_trace(
                go.Scatter(x=df_state['Years'], y=df_state['Total_Transaction_Amount'], mode='lines+markers', name=state)
            )

        # Update layout and axes labels with increased space between trendlines
        fig_all_india.update_layout(
            title='All India Transaction Trends',
            xaxis=dict(title='Year'),
            yaxis=dict(title='Total Transaction Amount'),
            showlegend=True,
            margin=dict(l=50, r=50, t=50, b=10)  # Adjust these values to increase/decrease space
        )

        st.plotly_chart(fig_all_india, use_container_width=True)

        # Transaction Trends for Selected State
        st.markdown("### :violet[Transaction Trends for Selected State]")

        # Fetch the necessary data for the list of states
        cursor.execute(
            "SELECT DISTINCT States FROM phonepe_data.aggregated_transaction ORDER BY States"
        )
        df_states_insights = pd.DataFrame(cursor.fetchall(), columns=['State'])

        # Add a dropdown to select a specific state
        selected_state_insights = st.selectbox("Select State", df_states_insights['State'].unique())

        # Check if selected_state_insights is in the df_states_insights
        if selected_state_insights not in df_states_insights['State'].values:
            st.warning(f"No data available for {selected_state_insights}")
        else:
            # Fetch the necessary data for the selected state
            cursor.execute(
                f"SELECT Years, SUM(Transaction_amount) AS Total_Transaction_Amount FROM phonepe_data.aggregated_transaction WHERE States = '{selected_state_insights}' GROUP BY Years ORDER BY Years"
            )
            df_selected_state = pd.DataFrame(cursor.fetchall(), columns=['Years', 'Total_Transaction_Amount'])

            # Create a subplot with one y-axis for trendlines
            fig_selected_state = go.Figure()

            # Add line trace for the selected state
            fig_selected_state.add_trace(
                go.Scatter(x=df_selected_state['Years'], y=df_selected_state['Total_Transaction_Amount'], mode='lines+markers', name=selected_state_insights)
            )

            # Update layout and axes labels
            fig_selected_state.update_layout(
                title=f'Transaction Trends in {selected_state_insights}',
                xaxis=dict(title='Year'),
                yaxis=dict(title='Total Transaction Amount'),
                showlegend=True
            )
            
            st.plotly_chart(fig_selected_state, use_container_width=True)

    elif Type == "Users":
        # User Trends
        st.markdown("## :violet[User Trends]")
        st.info(
            """
            #### Explore User Trends:
            - View the overall user trends for all India and specific states.
            - Analyze how user counts have evolved over the years.
            """
        )

        # Overall India User Trends
        st.markdown("### :violet[All India User Trends]")
        cursor.execute(
            f"SELECT Years, SUM(RegisteredUser) AS Total_Users FROM phonepe_data.map_user GROUP BY Years ORDER BY Years"
        )
        df_all_india_users = pd.DataFrame(cursor.fetchall(), columns=['Years', 'Total_Users'])

        # Fetch the necessary data for the list of states
        cursor.execute(
            "SELECT DISTINCT States FROM phonepe_data.map_user ORDER BY States"
        )
        df_states_users = pd.DataFrame(cursor.fetchall(), columns=['State'])

        # Create a subplot with one y-axis for trendlines
        fig_all_india_users = go.Figure()

        # Add line trace for each state
        for state in df_states_users['State'].unique():
            # Fetch the necessary data for the state
            cursor.execute(
                f"SELECT Years, SUM(RegisteredUser) AS Total_Users FROM phonepe_data.map_user WHERE States = '{state}' GROUP BY Years ORDER BY Years"
            )
            df_state_users = pd.DataFrame(cursor.fetchall(), columns=['Years', 'Total_Users'])

            fig_all_india_users.add_trace(
                go.Scatter(x=df_state_users['Years'], y=df_state_users['Total_Users'], mode='lines+markers', name=state)
            )

        # Update layout and axes labels with increased space between trendlines
        fig_all_india_users.update_layout(
            title='All India User Trends',
            xaxis=dict(title='Year'),
            yaxis=dict(title='Total Users'),
            showlegend=True,
            margin=dict(l=50, r=50, t=50, b=10)  # Adjust these values to increase/decrease space
        )

        st.plotly_chart(fig_all_india_users, use_container_width=True)

        # User Trends for Selected State
        st.markdown("### :violet[User Trends for Selected State]")

        # Fetch the necessary data for the list of states
        cursor.execute(
            "SELECT DISTINCT States FROM phonepe_data.map_user ORDER BY States"
        )
        df_states_users = pd.DataFrame(cursor.fetchall(), columns=['State'])

        # Add a dropdown to select a specific state
        selected_state_users = st.selectbox("Select State", df_states_users['State'].unique())

        # Check if selected_state_users is in the df_states_users
        if selected_state_users not in df_states_users['State'].values:
            st.warning(f"No data available for {selected_state_users}")
        else:
            # Fetch the necessary data for the selected state
            cursor.execute(
                f"SELECT Years, SUM(RegisteredUser) AS Total_Users FROM phonepe_data.map_user WHERE States = '{selected_state_users}' GROUP BY Years ORDER BY Years"
            )
            df_selected_state_users = pd.DataFrame(cursor.fetchall(), columns=['Years', 'Total_Users'])

            # Create a subplot with one y-axis for trendlines
            fig_selected_state_users = go.Figure()

            # Add line trace for the selected state
            fig_selected_state_users.add_trace(
                go.Scatter(x=df_selected_state_users['Years'], y=df_selected_state_users['Total_Users'], mode='lines+markers', name=selected_state_users)
            )

            # Update layout and axes labels
            fig_selected_state_users.update_layout(
                title=f'User Trends in {selected_state_users}',
                xaxis=dict(title='Year'),
                yaxis=dict(title='Total Users'),
                showlegend=True
            )

            st.plotly_chart(fig_selected_state_users, use_container_width=True)

    elif Type == "Insurance":
        # Insurance Trends
        st.markdown("## :violet[Insurance Trends]")
        st.info(
            """
            #### Explore Insurance Trends:
            - View the overall insurance trends for all India and specific states.
            - Analyze how insurance counts have evolved over the years.
            """
        )

        # Overall India Insurance Trends
        st.markdown("### :violet[All India Insurance Trends]")
        cursor.execute(
            f"SELECT Years, SUM(Insurance_count) AS Total_Insurance_Count FROM phonepe_data.aggregated_insurance GROUP BY Years ORDER BY Years"
        )
        df_all_india_insurance = pd.DataFrame(cursor.fetchall(), columns=['Years', 'Total_Insurance_Count'])

        # Fetch the necessary data for the list of states
        cursor.execute(
            "SELECT DISTINCT States FROM phonepe_data.aggregated_insurance ORDER BY States"
        )
        df_states_insurance = pd.DataFrame(cursor.fetchall(), columns=['State'])

        # Create a subplot with one y-axis for trendlines
        fig_all_india_insurance = go.Figure()

        # Add line trace for each state
        for state in df_states_insurance['State'].unique():
            # Fetch the necessary data for the state
            cursor.execute(
                f"SELECT Years, SUM(Insurance_count) AS Total_Insurance_Count FROM phonepe_data.aggregated_insurance WHERE States = '{state}' GROUP BY Years ORDER BY Years"
            )
            df_state_insurance = pd.DataFrame(cursor.fetchall(), columns=['Years', 'Total_Insurance_Count'])

            fig_all_india_insurance.add_trace(
                go.Scatter(x=df_state_insurance['Years'], y=df_state_insurance['Total_Insurance_Count'], mode='lines+markers', name=state)
            )

        # Update layout and axes labels with increased space between trendlines
        fig_all_india_insurance.update_layout(
            title='All India Insurance Trends',
            xaxis=dict(title='Year'),
            yaxis=dict(title='Total Insurance Count'),
            showlegend=True,
            margin=dict(l=50, r=50, t=50, b=10)  # Adjust these values to increase/decrease space
        )

        st.plotly_chart(fig_all_india_insurance, use_container_width=True)

        # Insurance Trends for Selected State
        st.markdown("### :violet[Insurance Trends for Selected State]")

        # Fetch the necessary data for the list of states
        cursor.execute(
            "SELECT DISTINCT States FROM phonepe_data.aggregated_insurance ORDER BY States"
        )
        df_states_insurance = pd.DataFrame(cursor.fetchall(), columns=['State'])

        # Add a dropdown to select a specific state
        selected_state_insurance = st.selectbox("Select State", df_states_insurance['State'].unique())

        # Check if selected_state_insurance is in the df_states_insurance
        if selected_state_insurance not in df_states_insurance['State'].values:
            st.warning(f"No data available for {selected_state_insurance}")
        else:
            # Fetch the necessary data for the selected state
            cursor.execute(
                f"SELECT Years, SUM(Insurance_count) AS Total_Insurance_Count FROM phonepe_data.aggregated_insurance WHERE States = '{selected_state_insurance}' GROUP BY Years ORDER BY Years"
            )
            df_selected_state_insurance = pd.DataFrame(cursor.fetchall(), columns=['Years', 'Total_Insurance_Count'])

            # Create a subplot with one y-axis for trendlines
            fig_selected_state_insurance = go.Figure()

            # Add line trace for the selected state
            fig_selected_state_insurance.add_trace(
                go.Scatter(x=df_selected_state_insurance['Years'], y=df_selected_state_insurance['Total_Insurance_Count'], mode='lines+markers', name=selected_state_insurance)
            )

            # Update layout and axes labels
            fig_selected_state_insurance.update_layout(
                title=f'Insurance Trends in {selected_state_insurance}',
                xaxis=dict(title='Year'),
                yaxis=dict(title='Total Insurance Count'),
                showlegend=True
            )

            st.plotly_chart(fig_selected_state_insurance, use_container_width=True)

