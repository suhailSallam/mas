# Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import plotly.express as px
import plotly.io as pio
import plotly
from ydata_profiling import  ProfileReport
import PyQt5 as qt
from IPython.display import display, Markdown
import streamlit as st
import streamlit.components.v1 as comp
from wordcloud import WordCloud
import arabic_reshaper
from bidi.algorithm import get_display


# Setting page layout ( This command should be after importing libraries )
st.set_page_config(page_title='Maintenance Analysis System',page_icon=None,
                   layout='wide',initial_sidebar_state='auto', menu_items=None)
# Sidebar for input selections
st.sidebar.title('Maintenance Analysis System')
selectLang = st.sidebar.selectbox('Select Language اختر اللغة :', ['English','العربية'], key=100)
selectMB = st.sidebar.selectbox('Select Analysis :', ['Home',
                                                      'Story_telling',
                                                      'Overview',
                                                      'DataSet',
                                                      'Explore_fields',
                                                      'Explore_value_counts',
                                                      'Cost_Insights',
                                                      'Service_Duration_Insights',
                                                      'Damage_Type_Insights',
                                                      'Car_Model_Insights',
                                                      'Fuel_Insights',
                                                      'Time_Based_Insights',
                                                      'Lcation_Based_Insights',
                                                      'Kilometers_Insights',
                                                      'Cost_Category_Insights',
                                                      'Miscellaneous_Insights',
                                                      'Service_Location_Profitability_Insights'
                                                      ], key=1)

with st.sidebar:
    st.markdown("""
    <style>
    :root {
      --header-height: 50px;
    }
    .css-z5fcl4 {
      padding-top: 2.5rem;
      padding-bottom: 5rem;
      padding-left: 2rem;
      padding-right: 2rem;
      color: blue;
    }
    .css-1544g2n {
      padding: 0rem 0.5rem 1.0rem;
    }
    [data-testid="stHeader"] {
        background-image: url(/app/static/icons8-astrolabe-64.png);
        background-repeat: no-repeat;
        background-size: contain;
        background-origin: content-box;
        color: blue;
    }

    [data-testid="stHeader"] {
        background-color: rgba(28, 131, 225, 0.1);
        padding-top: var(--header-height);
    }

    [data-testid="stSidebar"] {
        background-color: #e3f2fd; /* Soft blue */
        margin-top: var(--header-height);
        color: blue;
        position: fixed; /* Ensure sidebar is fixed */
        width: 250px; /* Fixed width */
        height: 100vh; /* Full height of the viewport */
        z-index: 999; /* Ensure it stays on top */
        overflow-y: auto; /* Enable scrolling for overflow content */
        padding-bottom: 2rem; /* Extra padding at the bottom */
    }

    [data-testid="stToolbar"]::before {
        content: "Maintenance Analysis System";
    }

    [data-testid="collapsedControl"] {
        margin-top: var(--header-height);
    }

    [data-testid="stSidebarUserContent"] {
        padding-top: 2rem;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        [data-testid="stSidebar"] {
            width: 100%; /* Sidebar takes full width on small screens */
            height: auto; /* Adjust height for small screens */
            position: relative; /* Sidebar is not fixed on small screens */
            z-index: 1000; /* Ensure it stays on top */
        }

        .css-z5fcl4 {
            padding-left: 1rem; /* Adjust padding for smaller screens */
            padding-right: 1rem;
        }

        [data-testid="stHeader"] {
            padding-top: 1rem; /* Adjust header padding */
        }

        [data-testid="stToolbar"] {
            font-size: 1.2rem; /* Adjust font size for the toolbar */
        }
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
<style>
div[data-testid="metric-container"] {
   background-color: rgba(28, 131, 225, 0.1);
   border: 1px solid rgba(28, 131, 225, 0.1);
   padding: 5% 5% 5% 10%;
   border-radius: 5px;
   color: rgb(30, 103, 119);
   text-align: center; /* Center the text */
   overflow-wrap: break-word;
   font-size: 14px; 
   display: flex;
   flex-direction: column
}

/* breakline for metric text         */
div[data-testid="metric-container"]
> label[data-testid="stMetricLabel"]
> div {
   font-size: 12px; 
   text-align: center;
   overflow-wrap: break-word;
   white-space: break-spaces;
   color: red;
   display: flex;
   flex-direction: column
}
</style>
"""
, unsafe_allow_html=True)



# Cache data loading and processing
@st.cache_data
def load_data(file):
    df = pd.read_excel(file)
    return df

# Analyze DataSet function
def analyzeDataSet(DataSet,state):
    st.subheader('Display data')
    st.write(DataSet)
    DataSet.info()
    st.subheader('Describe Data')
    st.write(DataSet.describe().round(2))
    st.subheader('DataFrame for Information about Dataset')
    information_DataSet = pd.DataFrame({"name": DataSet.columns,
                     "non-nulls": len(DataSet)-DataSet.isnull().sum().values,
                     "nulls": DataSet.isnull().sum().values,
                     "type": DataSet.dtypes.values})
    display(Markdown(information_DataSet.to_markdown()))
    st.write(information_DataSet)
    # Construct rows
    info_list=[]
    for column in DataSet.columns:
        row = [column,
               min(DataSet[column]),
               max(DataSet[column]),
               DataSet[column].nunique(),
               DataSet[column].isna().sum(),
               DataSet.duplicated().sum()
              ]
        info_list.append(row)
    st.subheader('DataFrame for information about Dataset Values') 
    # Convert List to DataFrame
    info_df = pd.DataFrame(data = info_list,
                            columns=['Column_name',
                                     'Minimum_value',
                                     'Maximum_value',
                                     'Number_of_unique_records',
                                     'Number_of_null_records',
                                     'Number_of_duplicated_records'
                                    ])
    st.write(info_df)
    #display(Markdown(info_df.to_markdown()))
    st.subheader('show data types')
    st.write(info_df.dtypes)
    st.write('Remove comment character if you want to proceed Running Ydata Report')
    #pf = ProfileReport(DataSet)
    #if state == 'pre':
    #    pf.to_file('maintenance_BEFORE_pre_process.html')
    #elif state == 'post':
    #    pf.to_file('maintenance_AFTER_pre_process.html')
    #else :
    #    print('for state of analysis, use "pre" or "post"')

# Data pre processing
## Date Processing
### Extract yearIn, monthIn, monthNIn, dayIn, dayNIn from 'Date in' field
def DataPreProcessing(data):
    df=data
    df['yearIn'] = df['date in'].dt.year
    df['monthIn'] = df['date in'].dt.month
    df['monthNIn'] = df['date in'].dt.month_name()
    df['dayIn'] = df['date in'].dt.day
    df['dayNIn'] = df['date in'].dt.day_name()
    ### Extract yearReady, monthReady, monthNReady, dayReady, dayNReady from 'date ready' field
    df['yearReady'] = df['date ready'].dt.year
    df['monthReady'] = df['date ready'].dt.month
    df['monthNReady'] = df['date ready'].dt.month_name()
    df['dayReady'] = df['date ready'].dt.day
    df['dayNReady'] = df['date ready'].dt.day_name()
    ### Calculate service duration
    df['service_duration'] = (df['date ready'] - df['date in']).dt.days + 1
    ## Categorization
    ### Cost Category
    cost_dict = {
        range(1,50,1)     :'0001:0050',
        range(50,100,1)   :'0050:0100',
        range(100,150,1)  :'0100:0150',
        range(150,200,1)  :'0150:0200',
        range(200,300,1)  :'0200:0300',
        range(300,400,1)  :'0300:0400',
        range(400,500,1)  :'0400:0500',
        range(500,600,1)  :'0500:0600',
        range(600,700,1)  :'0600:0700',
        range(700,800,1)  :'0700:0800',
        range(800,900,1)  :'0800:0900',
        range(900,1000,1) :'0900:1000',
        range(1000,1500,1):'1000:1500',
        range(1500,2000,1):'1500:2000',
        range(2000,3000,1):'2000:3000'
    }
    df['cost_category'] = df['cost'].replace(cost_dict)
    # Save DataSet post processing to new Excel file
    #df.to_excel('maintenance_cleaned_extended.xlsx')

# Visualization Functions
## Bar, Scatter, Line charts
def myPlot(data, plotType, title, x_label, y_label):
    data = data.sort_values(ascending=False)
    xs = data.index.astype(str)  # Convert index to strings for x-axis
    ys = data.values  # y-axis values
    # Calculate mean
    mean_value = ys.mean()
    # Get only values above the mean
    above_mean_data = data[data > mean_value]
    # Get only values below the mean
    below_mean_data = data[data < mean_value]
    # Sort values above mean in descending order and select top 3
    top3_above_mean = above_mean_data.sort_values(ascending=False).head(3)
    # Sort values below mean in descending order and select bottom 3
    bot3_below_mean = below_mean_data.sort_values(ascending=False).tail(3)
    # Create color mapping: blue for top 3 above mean, red for bottom 3 below mean, gray for others
    colors = ['blue' if index in top3_above_mean.index 
              else 'red' if index in bot3_below_mean.index 
              else 'gray' 
              for index in data.index]
    if plotType == 'bar':
        fig = px.bar(x=xs, y=ys, title=title + ' Analysis')
        fig.update_traces(marker_color=colors)  # Bar-specific color update
    elif plotType == 'scatter':
        fig = px.scatter(x=xs, y=ys, title=title + ' Analysis')
        fig.update_traces(marker=dict(color=colors))  # Scatter-specific color update
    elif plotType == 'pie':
        fig = px.pie(names=xs, values=ys, title=title + ' Analysis')
        fig.update_traces(marker=dict(colors=colors))  # Pie-specific color update
    elif plotType == 'line':
        fig = px.line(x=xs, y=ys, title=title + ' Analysis')
    # Update layout for custom axis labels
    fig.update_layout(
        title_x=0.0,
        xaxis_title=x_label,  # Custom x-axis label
        yaxis_title=y_label   # Custom y-axis label
    )
    st.plotly_chart(fig,theme=None, use_container_width=True)

def myPlot1(data, xs, ys, clr, plotType, title, sort_by=None, ascending=True):
    if sort_by is not None:
        data_sorted = data.sort_values(by=sort_by, ascending=ascending)
    else:
        data_sorted = data
    xt = str(xs)
    yt = str(ys)
    xs = data_sorted[xs]
    ys = data_sorted[ys]
    clrt= str(clr)
    clr = data_sorted[clr].astype(str) if clr else None
    if plotType == 'bar':
        fig = px.bar(x=xs, y=ys, color=clr, title=title + ' Analysis')
    elif plotType == 'scatter':
        fig = px.scatter(x=xs, y=ys, color=clr, title=title + ' Analysis')
    elif plotType == 'line':
        fig = px.line(x=xs, y=ys, color=clr, title=title + ' Analysis')
    fig.update_layout(title_x=0.0)
    fig.update_layout(xaxis_title=xt, yaxis_title=yt)
    fig.update_layout(legend_title_text=clrt)
    st.plotly_chart(fig,theme=None, use_container_width=True)

def myPlot11(data, xs, ys, clr, plotType, title, sort_by=None, ascending=True):
    if sort_by is not None:
        data_sorted = data.sort_values(by=sort_by, ascending=ascending)
    else:
        data_sorted = data
    xt = str(xs)
    yt = str(ys)
    xs = data_sorted[xs]
    ys = data_sorted[ys]
    #clr = data_sorted[clr].astype(str) if clr else None
    if plotType == 'bar':
        fig = px.bar(x=xs, y=ys, title=title + ' Analysis')
        fig.update_traces(marker_color=clr)  # Bar-specific color update
    elif plotType == 'scatter':
        fig = px.scatter(x=xs, y=ys, title=title + ' Analysis')
        fig.update_traces(marker=dict(color=clr))  # Scatter-specific color update
    elif plotType == 'line':
        fig = px.line(x=xs, y=ys, title=title + ' Analysis')
        fig.update_traces(marker_color=clr)  # Bar-specific color update
    fig.update_layout(title_x=0.0)
    fig.update_layout(xaxis_title=xt, yaxis_title=yt)
#    fig.show()
    st.plotly_chart(fig,theme=None, use_container_width=True)

    
def myPlot2(data, plotType, title):
    xs = data.index.astype(str)  # Index (x-axis)
    ys = data.values  # Values (y-axis)

    # Plot based on the plotType
    if plotType == 'bar':
        fig = px.bar(x=xs, y=ys, color=ys, title=title + ' Analysis')
    elif plotType == 'scatter':
        fig = px.scatter(x=xs, y=ys, color=ys, title=title + ' Analysis')
    elif plotType == 'line':
        fig = px.line(x=xs, y=ys, title=title + ' Analysis')

    # Center the title
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig,theme=None, use_container_width=True)
    
def myBoxPlot(data,x,y,color,title):
    fig = px.box(data, x=x, y=y, color=color, title=title)
    fig.update_layout(
        title_x=0.5,
        xaxis_title=str(x),
        yaxis_title=str(y)
    )
    #fig.show()
    st.plotly_chart(fig,theme=None, use_container_width=True)

## Sunburst chart
def mySunBurst(data, name, value, title):
    fig = px.sunburst(
        data_frame=data,
        #path=['cost_category', 'damage type'],   # Add both cost_category and damage type to the hierarchy
        path=name,
        values=value,  # Define the values (damage_count)
        title=title+' Analysis'
    )
    fig.update_layout(title_x=0.45)
    #fig.show()
    st.plotly_chart(fig,theme=None, use_container_width=True)
def mySunBurst1(data, name1,name2, value,clr, title):
    fig = px.sunburst(
        data_frame=data,
        path=[name1,name2],   # Add both cost_category and damage type to the hierarchy
        #path=name,
        values=value,  # Define the values (damage_count)
        color=clr,
        title=title +' Analysis'
    )
    fig.update_layout(title_x=0.0)
    fig.update_layout(height=600, margin=dict(t=50, l=25, r=25, b=25))
    st.plotly_chart(fig,theme=None, use_container_width=True)
## Pie chart
def myPie(data,title_prefix):
    name  = data.index
    value = data.values
    fig = px.pie(data_frame=data,
                 names = name, 
                 values = value,
                 title ='Top 5 '+ title_prefix +' Analysis'
                )
    fig.update_layout(title_x=0.5)
    #fig.show()
    st.plotly_chart(fig,theme=None, use_container_width=True)
# Functions
## Combine DataFrames
def combine(data,first_field,first_field_count,field_grouped_on,resulting_field_value):
    data_first_cat = data[first_field].value_counts().reset_index()
    data_first_cat.columns = [first_field,first_field_count]
    data_merged = data.groupby([first_field])[field_grouped_on].sum().reset_index(name=resulting_field_value)
    data_merged = data_merged.merge(data_first_cat,on=first_field)
    return first_field_count, resulting_field_value, data_merged

## TopTailCount
def TopTailCount(data,count,groupField,SumField):
    # Get top & Tail COUNT records based on total groupFiled
    top = data.groupby(groupField)[SumField].sum().sort_index(ascending=False).nlargest(count).index
    tail = data.groupby(groupField)[SumField].sum().sort_index(ascending=False).nsmallest(count).index
    # Filter for top corporates
    top_filtered_data = data[data[groupField].isin(top)].sort_index(ascending=False)
    tail_filtered_data = data[data[groupField].isin(tail)].sort_index(ascending=False)
    return top_filtered_data, tail_filtered_data

## Assign_color
def assign_color(index,top ,tail):
    if index in top.index:
        return 'blue'
    elif index in tail.index:
        return 'red'
    else:
        return 'gray'

## Coloring
def coloring(data,top,tail):
    colors = [assign_color(index,top,tail) for index in data.index]
    return colors

## SumOfsum
def sumOfsum(data,groupField1,groupField2,sumField):
    # Step 1: Calculate total sum of CorpLocCostSum for each corporate
    df_field1_sum = data.groupby(groupField1)[sumField].sum().reset_index(name='First Sum')
    # Step 2: Merge the total sum back into the original DataFrame
    df_field2_sum = data.groupby([groupField1, groupField2])[sumField].sum().reset_index(name='Total Sum')
    # Step 3: Merge the total sum of each corporate into this grouped data
    df_field2_sum = df_field2_sum.merge(df_field1_sum, on=groupField1)
    # Step 4: Sort by the total corporate cost (TotalCorpCost) and within that by CorpLocCostSum
    df_field2_sum = df_field2_sum.sort_values(by=['First Sum', 'Total Sum'], ascending=False)
    # Step 5: Drop the 'TotalCorpCost' column if you no longer need it
    df_field2_sum = df_field2_sum.drop(columns=['First Sum'])
    return df_field2_sum
## Corporate Client Profitability Insights
### Corporate Client Profitability
def Corporate_Client_Profitability():
    text="Our analysis indicates that customers vary significantly in their profitability. This information should guide our decisions about which branches to keep, close, or expand based on their ability to generate sustainable revenue."
    display(Markdown('#### *'+text+'*'))

    df = load_data('maintenance_cleaned_extended.xlsx')
    df_corporate = df.groupby('corporate')['cost'].sum().reset_index(name='Corporate Totla Service Cost').sort_values(by='Corporate Totla Service Cost',ascending=False)
    top_filterd_data, tail_filtered_data = TopTailCount(df_corporate,3,'corporate','Corporate Totla Service Cost')
    colors = coloring(df_corporate,top_filterd_data, tail_filtered_data)
    myPlot11(df_corporate,'corporate','Corporate Totla Service Cost',colors,'bar','Corporate Client Profitability', sort_by='Corporate Totla Service Cost', ascending=False)

## Corporate Client Profitability across Service Locations
def Corporate_Client_Profitability_across_Service_Locations():
    selectChart = st.sidebar.selectbox('Select Chart :',['bar','sunburst'], key=16)

    df = load_data('maintenance_cleaned_extended.xlsx')
    corporate_Location = sumOfsum(df,'corporate','location','cost')
    if   selectChart =='bar':
        text = "Analysis reveals significant variations in profitability across different client companies. This suggests a need to focus on branches serving the largest and most profitable clients, while evaluating the performance of other branches to improve their efficiency and increase their overall contribution to profits"
        display(Markdown('#### *'+text+'*'))
        myPlot1(corporate_Location,'corporate','Total Sum','location','bar','Corporate Client Profitability across Service Locations', sort_by=None, ascending=True)
    elif selectChart == 'sunburst':
        text = "Analysis reveals significant variations in profitability across different client companies. This suggests a need to focus on branches serving the largest and most profitable clients, while evaluating the performance of other branches to improve their efficiency and increase their overall contribution to profits"
        display(Markdown('#### *'+text+'*'))
        mySunBurst1(corporate_Location, 'corporate','location', 'Total Sum', 'Total Sum', 'Corporate Client Profitability across Service Locations')

## Corporate Top COUNT Clients Profitability
def Corporate_Top_COUNT_Clients_Profitability():
    text="The chart visually represents the magnitude of the profit contribution from each of the major companies to the company's total profits. It can be observed that company 'Xe' is the largest contributor to profits, followed by 'Jordan Transports' and then 'Vestas'."
    display(Markdown('#### *'+text+'*'))

    df = load_data('maintenance_cleaned_extended.xlsx')
    top_filtered_data, tail_filtered_data = TopTailCount(df,5,'corporate','cost')
    myData = top_filtered_data.groupby('corporate')['cost'].sum().reset_index(name='Corporate Cost Sum').sort_values('Corporate Cost Sum',ascending=False)
    myPlot1(myData,'corporate','Corporate Cost Sum',None,'bar','Corporate Top Clients Profitability', sort_by=None, ascending=True)

## Top Corporates and Their Service Locations' Income Distribution
def Top_Corporates_and_Their_Service_Locations_Income_Distribution():
    text="This chart provides a breakdown of the total revenue generated by our top clients, analyzing the contributions from each of our service locations."
    display(Markdown('#### *'+text+'*'))

    df = load_data('maintenance_cleaned_extended.xlsx')
    top_filtered_data, tail_filtered_data = TopTailCount(df,5,'corporate','cost')
    myData = sumOfsum(top_filtered_data,'corporate','location','cost')
    myPlot1(myData,'corporate','Total Sum','location','bar',"Top Corporates and Their Service Locations' Income Distribution", sort_by=None, ascending=True)

    text="This chart provides a breakdown of the total revenue generated by our top clients, analyzing the contributions from each of our service locations."
    display(Markdown('#### *'+text+'*'))
    mySunBurst1(myData, 'corporate','location', 'Total Sum', 'Total Sum', "Top Corporates and Their Service Locations' Income Distribution")
## Service Location Profitability
## Top 5 Corporates and Their Top 5 Service Locations' Income Distribution
def Top_5_Corporates_and_Their_Top_5_Service_Locations_Income_Distribution():
    selectChart = st.sidebar.selectbox('Select Chart :',['bar','sunburst'], key=17)
    df = load_data('maintenance_cleaned_extended.xlsx')
    corporate_Location = sumOfsum(df,'corporate','location','cost')
    top_5_corporates = df.groupby('corporate')['cost'].sum().sort_index(ascending=False).nlargest(5).index
    # Step 1: Filter for the top 5 corporates
    filtered_data_top_corporates = corporate_Location[corporate_Location['corporate'].isin(top_5_corporates)]
    # Step 2: For each corporate, find the top 5 service locations based on income
    top_profitable_locations_per_corporate = pd.DataFrame()
    for corporate in top_5_corporates:
        # Get the top 5 locations for this corporate
        top_locations = (filtered_data_top_corporates[filtered_data_top_corporates['corporate'] == corporate]
                         .nlargest(5, 'Total Sum'))
        # Identify the less profitable locations for this corporate (those not in the top 5)
        all_locations_for_corporate = filtered_data_top_corporates[filtered_data_top_corporates['corporate'] == corporate]
        top_profitable_locations = all_locations_for_corporate[all_locations_for_corporate['location'].isin(top_locations['location'])]
        # Append the less profitable locations to the  less DataFrame
        top_profitable_locations_per_corporate = pd.concat([top_profitable_locations_per_corporate, top_profitable_locations])
    if   selectChart =='bar':
        text="The chart illustrates the income distribution for the top 5 companies and their top 5 service locations. 'Xe' stands out with the highest revenue, supported by locations such as 'Al-Azazi' and 'Al-Sharqiya'. Some companies may share the same service locations or benefit from different ones."
        display(Markdown('#### *'+text+'*'))
        myPlot1(top_profitable_locations_per_corporate,'corporate','Total Sum','location','bar',"Top 5 Corporates and Their Top 5 Service Locations' Income Distribution", sort_by=None, ascending=True)
    elif selectChart == 'sunburst':
        text="The chart illustrates the income distribution for the top 5 companies and their top 5 service locations. 'Xe' stands out with the highest revenue, supported by locations such as 'Al-Azazi' and 'Al-Sharqiya'. Some companies may share the same service locations or benefit from different ones."
        display(Markdown('#### *'+text+'*'))
        mySunBurst1(top_profitable_locations_per_corporate,'corporate','location','Total Sum','Total Sum',"Top 5 Corporates and Their Top 5 Service Locations' Income Distribution")

## Less Profitable Corporates (Not in Top 5)
def Less_Profitable_Corporates_Not_in_Top_5():
    text="The chart illustrates the income distribution for the less profitable companies, these should be encoureged through different ways to maximize their dealing with Ahmad Company ."
    display(Markdown('#### *'+text+'*'))
    df = load_data('maintenance_cleaned_extended.xlsx')
    print('Total Corporates =',df['corporate'].nunique(), 'Less Profitable Corporates (Not in Top 5)=',df['corporate'].nunique() - 5)

    # Filter Corporates, get the tail corporates base on cost sum
    top_filtered_data, tail_filtered_data = TopTailCount(df,50,'corporate','cost')
    # Get the dataframe for these tail corporates
    myData = tail_filtered_data.groupby('corporate')['cost'].sum().reset_index(name='Total Sum').sort_values(by='Total Sum',ascending=False)
    # Plot the chart
    myPlot1(myData,'corporate','Total Sum',None,'bar',"Less Profitable Corporates (Not in Top 5)", sort_by=None, ascending=True)
    
## Less_Profitable_Service_Locations_for_Each_Top_5_Corporate
def Less_Profitable_Service_Locations_for_Each_Top_5_Corporate():
    df = load_data('maintenance_cleaned_extended.xlsx')
    corporate_Location = sumOfsum(df,'corporate','location','cost')
    top_5_corporates = df.groupby('corporate')['cost'].sum().sort_index(ascending=False).nlargest(5).index
    # Step 1: Filter for the top 5 corporates
    filtered_data_top_corporates = corporate_Location[corporate_Location['corporate'].isin(top_5_corporates)]

    # Step 2: For each corporate, find the top 5 service locations based on income
    less_profitable_locations_per_corporate = pd.DataFrame()

    for corporate in top_5_corporates:
        # Get the top 5 locations for this corporate
        top_locations = (filtered_data_top_corporates[filtered_data_top_corporates['corporate'] == corporate]
                         .nlargest(5, 'Total Sum'))
        # Identify the less profitable locations for this corporate (those not in the top 5)
        all_locations_for_corporate = filtered_data_top_corporates[filtered_data_top_corporates['corporate'] == corporate]
        less_profitable_locations = all_locations_for_corporate[~all_locations_for_corporate['location'].isin(top_locations['location'])]
        # Append the less profitable locations to the  less DataFrame
        less_profitable_locations_per_corporate = pd.concat([less_profitable_locations_per_corporate, less_profitable_locations])

    # Display the less profitable service locations
    #print("Less profitable service locations (not in top 5 for each corporate):")
    #print(less_profitable_locations_per_corporate[['corporate', 'location', 'Total Sum']].sort_values(by='Total Sum'))

    text="The chart illustrates the income distribution for the less profitable locations, these should investgated, opertional cost vs income, if the operational cost is more than income, then they should be closed immediatly, employees can be shifted to other profitable locations, else their customers should be encoureged through different ways to maximize their dealing with these locations, hence, with Ahmad Company through hot discount promotions."
    display(Markdown('#### *'+text+'*'))
    myPlot1(less_profitable_locations_per_corporate,'location','Total Sum','corporate','bar',"Less Profitable Service Locations (Not in Top 5 for Each Corporate)", sort_by=None, ascending=True)

def Top_Profitable_Service_Locations_for_Each_Top_5_Corporate():
    df = load_data('maintenance_cleaned_extended.xlsx')
    corporate_Location = sumOfsum(df,'corporate','location','cost')
    top_5_corporates = df.groupby('corporate')['cost'].sum().sort_index(ascending=False).nlargest(5).index
    # Step 1: Filter for the top 5 corporates
    filtered_data_top_corporates = corporate_Location[corporate_Location['corporate'].isin(top_5_corporates)]

    # Step 2: For each corporate, find the top 5 service locations based on income
    top_profitable_locations_per_corporate = pd.DataFrame()

    for corporate in top_5_corporates:
        # Get the top 5 locations for this corporate
        top_locations = (filtered_data_top_corporates[filtered_data_top_corporates['corporate'] == corporate]
                         .nlargest(5, 'Total Sum'))
        # Identify the top profitable locations for this corporate (those in the top 5)
        all_locations_for_corporate = filtered_data_top_corporates[filtered_data_top_corporates['corporate'] == corporate]
        top_profitable_locations = all_locations_for_corporate[all_locations_for_corporate['location'].isin(top_locations['location'])]
        # Append the top profitable locations to the top  DataFrame
        top_profitable_locations_per_corporate = pd.concat([top_profitable_locations_per_corporate, top_profitable_locations])

    # Display the top profitable service locations
    #print("top profitable service locations (in top 5 for each corporate):")
    #print(top_profitable_locations_per_corporate[['corporate', 'location', 'Total Sum']].sort_values(by='Total Sum'))
    text="The chart illustrates the income distribution for the top profitable locations, employees of these locations should rewarded."
    display(Markdown('#### *'+text+'*'))
    myPlot1(top_profitable_locations_per_corporate,'location','Total Sum','corporate','bar',"Top Profitable Service Locations ( in Top 5 for Each Corporate)", sort_by=None, ascending=True)

# Main switch case
class SwitchMCase:
    ################################################################################################## Stoty Telling
    def case_Home(self):
        if selectLang == 'English':
            st.title('Home Page')
            st.header('Maintenance Analysis System')
            st.subheader('Interactive Analysis Dashboard, Delivered to: "Ahmad Company"')
            st.image('Car Manitenance Services.jpeg')
        elif selectLang == 'العربية':
            st.title('الصفحة الرئيسية')
            st.header('نظام تحليل بيانات الصيانة')
            st.subheader('لوحة بيانات تحليلية تفاعلية، مقدمة لـ شركة أحمد ')
            st.image('Car Manitenance Services.jpeg')
            
        return 'Home'

    ################################################################################################## Stoty Telling
    def case_Story_telling(self):
        r0    = st.columns(1)[0]
        r1,r2 = st.columns((1,3))
        if selectLang == 'English':
            with r0:
                st.header('Story Telling')
            r1.image('investor1.png')
            r2.markdown('#                     ')
            r2.markdown('#                     ')
            r2.markdown('#                     ')
            r2.markdown('# Ahmad is an investor')
            #st.markdown('# Ahmad is an investor')
            st.markdown('###### Ahmad has established a company provides car service for different car damages, his company has a lot of locations in different cities in the country.')
            st.markdown("###### Ahmad's company deals only with corporates not individuals.")
            st.markdown('###### After one year, Ahmad felt that the profit generated from locations have problems, so he requested to do Data analysis with objective (maximizing the profit and minimizing any loss)')
            st.markdown('###### Ahmad cannot control the damage happens to cars, and cannot control to which service location this damage in certain car should go.')
            st.markdown('###### No information was provided with regard to location operational cost, employees salary, employees experience, the only available information is the provided dataset')
            st.markdown('#### ------------------------------------------------------------------------------------------------------------------------------------------')
            st.markdown('###### The dataset provides various details such as car information, damage types, dates, service locations, fuel levels, and cost categories.')
            st.markdown("##### To address Ahmad's situation and maximize income while minimizing loss, here are a few key areas of analysis:")
            st.markdown('1. Corporate Client Profitability')
            st.markdown('2. Service Location Profitability')
            st.markdown('3. Cost Category Optimization')
            st.markdown('4. Damage Type and Service Strategy')
            st.markdown('5. Service Duration Efficiency')
            st.markdown('###### While we should start exploring the dataset and its fields, and the relation of these field with each other to beter understanding the dataset, at the end we will reach to the above 5 analysis and provide the suitable recommendation')
            st.markdown('##### Follow us')
            st.markdown('### Suhail Sallam')
        elif selectLang == 'العربية':
            with r0:
                st.header('رواية القصة')
            r1.image('investor1.png')
            r2.markdown('#                     ')
            r2.markdown('#                     ')
            r2.markdown('#                     ')
            r2.markdown('# أحمد هو مستثمر')
            st.markdown('###### أحمد أسس شركة تقدم خدمات السيارات لأعطال متنوعة، وتوجد لشركته العديد من الفروع في مدن مختلفة في الدولة.')
            st.markdown('###### شركة أحمد تتعامل فقط مع الشركات وليس الأفراد.')
            st.markdown('###### بعد عام واحد، شعر أحمد أن الأرباح التي تولدها الفروع بها مشكلات، فطلب إجراء تحليل بيانات بهدف (زيادة الأرباح وتقليل أي خسائر).')
            st.markdown('###### أحمد لا يستطيع التحكم في الأعطال التي تحدث للسيارات، ولا يستطيع التحكم في أي موقع خدمة يجب أن تذهب إليه السيارة المتضررة.')
            st.markdown('###### لم يتم تقديم أي معلومات تتعلق بتكاليف التشغيل للموقع، أو رواتب الموظفين، أو خبراتهم، والمعلومات المتاحة فقط هي البيانات المقدمة.')
            st.markdown('#### ------------------------------------------------------------------------------------------------------------------------------------------')
            st.markdown('###### توفر مجموعة البيانات تفاصيل مختلفة مثل معلومات السيارة، أنواع الأضرار، التواريخ، مواقع الخدمة، مستويات الوقود، وفئات التكاليف.')
            st.markdown('##### لمعالجة موقف أحمد وزيادة الدخل مع تقليل الخسائر، إليك بعض المجالات الرئيسية للتحليل:')
            st.markdown('1. ربحية العملاء من الشركات')
            st.markdown('2. ربحية مواقع الخدمة')
            st.markdown('3. تحسين فئات التكاليف')
            st.markdown('4. نوع الضرر واستراتيجية الخدمة')
            st.markdown('5. كفاءة مدة الخدمة')
            st.markdown('###### بينما يجب أن نبدأ في استكشاف مجموعة البيانات وحقولها، والعلاقة بين هذه الحقول لفهم أفضل للبيانات، في النهاية سنصل إلى التحليلات الخمسة المذكورة أعلاه ونقدم التوصيات المناسبة.')
            st.markdown('##### تابعونا')
            st.markdown('### سهيل سلام')

        return 'case_Story_telling'
    ################################################################################################## Overview
    def case_Overview(self):
        st.header('Overview')
        return 'Overview'
    ################################################################################################## DataSet Exploration before pre processing and Post
    def case_DataSet(self):
        # Exploratory Data Analysis (EDA)
        ## Uni - Variance Analysis
        ### DataSet Exploration before pre processing and Post
        st.header('DataSet Exploration BEFORE pre-processing')
        df = load_data('maintenance_cleaned.xlsx')
        analyzeDataSet(df,'pre')
        DataPreProcessing(df)
        st.header('DataSet Exploration AFTER pre-processing')
        df = load_data('maintenance_cleaned_extended.xlsx')
        analyzeDataSet(df,'post')
        return 'DataSet Exploration before pre-processing ... Done.'
    ################################################################################################## Fields Exploration
    def case_Explore_fields(self):
        # Exploratory Data Analysis (EDA)
        ## Uni - Variance Analysis
        ### Fields Exploration
        st.header('Explore_fields')
        df = load_data('maintenance_cleaned_extended.xlsx')
        selectField = st.sidebar.selectbox('Select Field :', ['yearIn',
                                                      'monthIn',
                                                      'monthNIn',
                                                      'dayIn',
                                                      'dayNIn',
                                                      'service_duration',
                                                      'damage_type',
                                                      'car',
                                                      'KMs_IN',
                                                      'KMs_out',
                                                      'KMs_Diff',
                                                      'Fuel_in',
                                                      'Fuel_out',
                                                      'Fuel_Diff',
                                                      'yearReady',
                                                      'monthReady',
                                                      'monthNReady',
                                                      'dayReady',
                                                      'dayNReady',
                                                      'cost_category',
                                                      'location',
                                                      'corporate',
                                                      'delivered_by',
                                                      'returned_by'
                                                      ], key=2)
        selectChart = st.sidebar.selectbox('Select Chart :',
                                                     ['bar',
                                                      'scatter',
                                                      'pie',
                                                      'line'
                                                      ], key=14)

        class SwitchFCase:
            def case_yearIn(self):
                column = 'yearIn'
                myPlot(df[column].value_counts(),selectChart,'Field: ' + column.capitalize(),column.capitalize(), 'Count')
                return 'yearIn'
            def case_monthIn(self):
                column = 'monthIn'
                myPlot(df[column].value_counts(),selectChart,'Field: ' + column.capitalize(),column.capitalize(), 'Count')
                return 'monthIn'
            def case_monthNIn(self):
                column = 'monthNIn'
                myPlot(df[column].value_counts(),selectChart,'Field: ' + column.capitalize(),column.capitalize(), 'Count')
                return 'monthNIn'
            def case_dayIn(self):
                column = 'dayIn'
                myPlot(df[column].value_counts(),selectChart,'Field: ' + column.capitalize(),column.capitalize(), 'Count')
                return 'dayIn'
            def case_dayNIn(self):
                column = 'dayNIn'
                myPlot(df[column].value_counts(),selectChart,'Field: ' + column.capitalize(),column.capitalize(), 'Count')
                return 'dayNIn'
            def case_service_duration(self):
                column = 'service_duration'
                myPlot(df[column].value_counts(),selectChart,'Field: ' + column.capitalize(),column.capitalize(), 'Count')
                return 'service_duration'
            def case_damage_type(self):
                column = 'damage type'
                myPlot(df[column].value_counts(),selectChart,'Field: ' + column.capitalize(),column.capitalize(), 'Count')
                return 'damage type'
            def case_car(self):
                column = 'car'
                myPlot(df[column].value_counts(),selectChart,'Field: ' + column.capitalize(),column.capitalize(), 'Count')
                return 'car'
            def case_KMs_IN(self):
                column = 'KMs IN'
                myPlot(df[column].value_counts(),selectChart,'Field: ' + column.capitalize(),column.capitalize(), 'Count')
                return 'KMs_IN'
            def case_KMs_out(self):
                column = 'KMs out'
                myPlot(df[column].value_counts(),selectChart,'Field: ' + column.capitalize(),column.capitalize(), 'Count')
                return 'KMs_out'
            def case_KMs_Diff(self):
                column = 'KMs Diff'
                myPlot(df[column].value_counts(),selectChart,'Field: ' + column.capitalize(),column.capitalize(), 'Count')
                return 'KMs_Diff'
            def case_Fuel_in(self):
                column = 'Fuel in'
                myPlot(df[column].value_counts(),selectChart,'Field: ' + column.capitalize(),column.capitalize(), 'Count')
                return 'Fuel_in'
            def case_Fuel_out(self):
                column = 'Fuel out'
                myPlot(df[column].value_counts(),selectChart,'Field: ' + column.capitalize(),column.capitalize(), 'Count')
                return 'Fuel_out'
            def case_Fuel_Diff(self):
                column = 'Fuel Diff'
                myPlot(df[column].value_counts(),selectChart,'Field: ' + column.capitalize(),column.capitalize(), 'Count')
                return 'Fuel Diff'
            def case_yearReady(self):
                column = 'yearReady'
                myPlot(df[column].value_counts(),selectChart,'Field: ' + column.capitalize(),column.capitalize(), 'Count')
                return 'yearReady'
            def case_monthReady(self):
                column = 'monthReady'
                myPlot(df[column].value_counts(),selectChart,'Field: ' + column.capitalize(),column.capitalize(), 'Count')
                return 'monthReady'
            def case_monthNReady(self):
                column = 'monthNReady'
                myPlot(df[column].value_counts(),selectChart,'Field: ' + column.capitalize(),column.capitalize(), 'Count')
                return 'monthNReady'
            def case_dayReady(self):
                column = 'dayReady'
                myPlot(df[column].value_counts(),selectChart,'Field: ' + column.capitalize(),column.capitalize(), 'Count')
                return 'dayReady'
            def case_dayNReady(self):
                column = 'dayNReady'
                myPlot(df[column].value_counts(),selectChart,'Field: ' + column.capitalize(),column.capitalize(), 'Count')
                return 'dayNReady'
            def case_cost_category(self):
                column = 'cost_category'
                myPlot(df[column].value_counts(),selectChart,'Field: ' + column.capitalize(),column.capitalize(), 'Count')
                return 'cost_category'
            def case_location(self):
                column = 'location'
                myPlot(df[column].value_counts(),selectChart,'Field: ' + column.capitalize(),column.capitalize(), 'Count')
                return 'location'
            def case_corporate(self):
                column = 'corporate'
                myPlot(df[column].value_counts(),selectChart,'Field: ' + column.capitalize(),column.capitalize(), 'Count')
                return 'corporate'
            def case_delivered_by(self):
                column = 'delivered by'
                myPlot(df[column].value_counts(),selectChart,'Field: ' + column.capitalize(),column.capitalize(), 'Count')
                return 'delivered_by'
            def case_returned_by(self):
                column = 'returned by'
                myPlot(df[column].value_counts(),selectChart,'Field: ' + column.capitalize(),column.capitalize(), 'Count')
                return 'returned_by'

            def default_case(self):
                return "Default class method executed"
            def F_switch(self, value):
                method_name = f'case_{value}'
                method = getattr(self, method_name, self.default_case)
                return method()    
        # Usage
        F_switcher = SwitchFCase()
        F_result = F_switcher.F_switch(selectField)
        st.write('FIELDS: ',F_result)
        return 'Explore_fields'
    ################################################################################################## Fields Value Counts
    def case_Explore_value_counts(self):
        # Exploratory Data Analysis (EDA)
        ## Uni - Variance Analysis
        ### value_counts Exploration
        st.header('Explore_value_counts')
        df = load_data('maintenance_cleaned_extended.xlsx')
        selectField = st.sidebar.selectbox('Select Field :', ['yearIn',
                                                      'monthIn',
                                                      'monthNIn',
                                                      'dayIn',
                                                      'dayNIn',
                                                      'service_duration',
                                                      'damage_type',
                                                      'car',
                                                      'KMs_IN',
                                                      'KMs_out',
                                                      'KMs_Diff',
                                                      'Fuel_in',
                                                      'Fuel_out',
                                                      'Fuel_Diff',
                                                      'yearReady',
                                                      'monthReady',
                                                      'monthNReady',
                                                      'dayReady',
                                                      'dayNReady',
                                                      'cost_category',
                                                      'location',
                                                      'corporate',
                                                      'delivered_by',
                                                      'returned_by',
                                                      'plate_number'
                                                      ], key=3)
        selectChart = st.sidebar.selectbox('Select Chart :',
                                                     ['bar',
                                                      'scatter',
                                                      'pie',
                                                      'line'
                                                      ], key=14)

        
        def uni(column,chart):
            df_column = df.get(column).value_counts()
            myPlot(df_column,chart,column.capitalize()+' Count Values ', column.capitalize(), 'Count Values')
#        df = load_data('maintenance_cleaned_extended.xlsx')
        class SwitchFCase:
            def case_yearIn(self):
                column = 'yearIn'
                uni(column,selectChart)
                return 'yearIn'
            def case_monthIn(self):
                column = 'monthIn'
                uni(column,selectChart)
                return 'monthIn'
            def case_monthNIn(self):
                column = 'monthNIn'
                uni(column,selectChart)
                return 'monthNIn'
            def case_dayIn(self):
                column = 'dayIn'
                uni(column,selectChart)
                return 'dayIn'
            def case_dayNIn(self):
                column = 'dayNIn'
                uni(column,selectChart)
                return 'dayNIn'
            def case_service_duration(self):
                column = 'service_duration'
                uni(column,selectChart)
                return 'service_duration'
            def case_damage_type(self):
                column = 'damage type'
                uni(column,selectChart)
                return 'damage type'
            def case_car(self):
                column = 'car'
                uni(column,selectChart)
                return 'car'
            def case_KMs_IN(self):
                column = 'KMs IN'
                uni(column,selectChart)
                return 'KMs_IN'
            def case_KMs_out(self):
                column = 'KMs out'
                uni(column,selectChart)
                return 'KMs_out'
            def case_KMs_Diff(self):
                column = 'KMs Diff'
                uni(column,selectChart)
                return 'KMs_Diff'
            def case_Fuel_in(self):
                column = 'Fuel in'
                uni(column,selectChart)
                return 'Fuel_in'
            def case_Fuel_out(self):
                column = 'Fuel out'
                uni(column,selectChart)
                return 'Fuel_out'
            def case_Fuel_Diff(self):
                column = 'Fuel Diff'
                uni(column,selectChart)
                return 'Fuel Diff'
            def case_yearReady(self):
                column = 'yearReady'
                uni(column,selectChart)
                return 'yearReady'
            def case_monthReady(self):
                column = 'monthReady'
                uni(column,selectChart)
                return 'monthReady'
            def case_monthNReady(self):
                column = 'monthNReady'
                uni(column,selectChart)
                return 'monthNReady'
            def case_dayReady(self):
                column = 'dayReady'
                uni(column,selectChart)
                return 'dayReady'
            def case_dayNReady(self):
                column = 'dayNReady'
                uni(column,selectChart)
                return 'dayNReady'
            def case_cost_category(self):
                column = 'cost_category'
                uni(column,selectChart)
                return 'cost_category'
            def case_location(self):
                column = 'location'
                uni(column,selectChart)
                return 'location'
            def case_corporate(self):
                column = 'corporate'
                uni(column,selectChart)
                return 'corporate'
            def case_delivered_by(self):
                column = 'delivered by'
                uni(column,selectChart)
                return 'delivered_by'
            def case_returned_by(self):
                column = 'returned by'
                uni(column,selectChart)
                return 'returned_by'
            def case_plate_number(self):
                column = 'plate number'
                uni(column,selectChart)
                return 'plate number'

            def default_case(self):
                return "Default class method executed"
            def F_switch(self, value):
                method_name = f'case_{value}'
                method = getattr(self, method_name, self.default_case)
                return method()    
        # Usage
        F_switcher = SwitchFCase()
        F_result = F_switcher.F_switch(selectField)
        st.write('FIELDS: ',F_result)

        return 'Explore_value_counts'
    ################################################################################################## Cost Insights
    def case_Cost_Insights(self):
        st.header('Cost_Insights')
        df = load_data('maintenance_cleaned_extended.xlsx')
        selectCostInsight = st.sidebar.selectbox('Select Cost Insight :',
                                                 ['Average_repair_cost_per_damage_type',
                                                  'Total_cost_distribution_across_different_damage_types',
                                                  'Comparison_of_repair_costs_across_car_models',
                                                  'Total_and_average_repair_costs_by_service_location',
                                                  'Repair_costs_broken_down_by_year_month',
                                                  'Relationship_between_cost_and_service_duration',
                                                  'Relationship_between_cost_and_kilometers_driven_KMs_in_and_out',
                                                  'Cost_comparisons_across_different_fuel_levels_fuel_in_vs_fuel_out',
                                                  'Total_cost_distribution_across_different_years',
                                                  'Total_cost_distribution_across_different_car_models',
                                                  'Total_cost_distribution_across_different_locations',
                                                  'Total_cost_distribution_across_different_corporates',
                                                  'Total_cost_distribution_across_different_delivered_by_persons',
                                                  'Total_cost_distribution_across_different_returned_by_persons',
                                                  'Total_cost_distribution_across_different_returned_by_other_persons',
                                                  'Count_distribution_across_different_returned_by_other_persons',
                                                  'Total_cost_of_each_Damage_type_for_each_Cost_Category',
                                                  'Total_cost_of_each_year_for_each_month_name'
                                                 ], key=4)
        class SwitchCICase:
            def case_Average_repair_cost_per_damage_type(self):
                #### Average repair cost per damage type
                df_average_cost = df.groupby(['damage type'])['cost'].mean().reset_index(name='Average Cost')
                myPlot1(
                    data=df_average_cost,
                    xs='damage type',
                    ys='Average Cost',
                    clr='damage type',
                    plotType='bar',
                    title='Average repair cost per damage type',
                    sort_by=['Average Cost'],
                    ascending=[True]
                    )
                mySunBurst(df_average_cost, name=['damage type'], value='Average Cost',title='Average repair cost per damage type')
                return 'Average_repair_cost_per_damage_type'
        
            def case_Total_cost_distribution_across_different_damage_types(self):
                #### Total cost distribution across different damage types
                df_cost_damage = df.groupby(['damage type'])['cost'].sum().reset_index(name='Total Damage Cost')
                myPlot1(
                    data=df_cost_damage,
                    xs='damage type',
                    ys='Total Damage Cost',
                    clr='damage type',
                    plotType='bar',
                    title='Total repair cost per damage type',
                    sort_by=['Total Damage Cost'],
                    ascending=[True]
                )
                #SunBurst
                mySunBurst(df_cost_damage, name=['damage type'], value='Total Damage Cost',title='Total cost distribution across different damage types')
                #Box
                myBoxPlot(data=df,x='damage type',y='cost',color='damage type',title='Distribution of repair costs across different damage types')
                #Pie
                fig = px.pie(df_cost_damage, names='damage type', values='Total Damage Cost', color='damage type', title='Proportion of Total Costs by Damage Type')
                st.plotly_chart(fig,theme=None, use_container_width=True)
                #line
                fig = px.line(df.sort_values(by='date ready',ascending=True), x='date ready', y='cost', color='damage type', title='Cost Over Time by Damage Type')
                st.plotly_chart(fig,theme=None, use_container_width=True)
                #Scatter
                frequency , Total_Damage_Cost, dataMerged = combine(df,'damage type','frequency','cost','Total Damage Cost')
                df_frequency = df['damage type'].value_counts().reset_index()
                df_frequency.columns = ['damage type', 'frequency']
                df_merged = df_cost_damage.groupby('damage type')['Total Damage Cost'].sum().reset_index()
                df_merged = df_merged.merge(df_frequency, on='damage type')
                fig = px.scatter(dataMerged, x='damage type', y=frequency, size=Total_Damage_Cost,
                                 color='damage type',title='Frequency vs Total Cost by Damage Type')
                st.plotly_chart(fig,theme=None, use_container_width=True)
                return 'Total_cost_distribution_across_different_damage_types'
            def case_Comparison_of_repair_costs_across_car_models(self):
                #### Comparison of repair costs across car models
                myBoxPlot(data=df,x='car',y='cost',color='car',title='Comparison of repair costs across car models')
                return 'Comparison_of_repair_costs_across_car_models'
            def case_Total_and_average_repair_costs_by_service_location(self):
                #### Total and average repair costs by service location
                total_costs = df.groupby('location')['cost'].sum().reset_index(name='total_cost')
                average_costs = df.groupby('location')['cost'].mean().reset_index(name='average_cost')
                # Merge total and average costs into one DataFrame
                merged_df = pd.merge(total_costs, average_costs, on='location')
                # Melt the DataFrame to make it long-form for a grouped bar chart
                melted_df = pd.melt(merged_df, id_vars='location', value_vars=['total_cost', 'average_cost'], 
                                    var_name='Cost Type', value_name='Cost')
                # Plot grouped bar chart
                fig = px.bar(melted_df, x='Cost', y='location', color='Cost Type',
                             barmode='group',
                             title="Total and Average Repair Costs by Service Location",
                             labels={'Cost': 'Repair Cost', 'location': 'Service Location', 'Cost Type': 'Type of Cost'},
                             orientation='h')
                # Show the plot
                st.plotly_chart(fig,theme=None, use_container_width=True)
                return 'Total_and_average_repair_costs_by_service_location'
            def case_Repair_costs_broken_down_by_year_month(self):
                #### Repair costs broken down by year, month
                df_cost_yearReady_monthReady = df.groupby(['yearReady','monthReady'])['cost'].sum().reset_index(name='cost_yearReady_monthReady_sum')
                # Line
                fig = px.line(df_cost_yearReady_monthReady, x='monthReady', y='cost_yearReady_monthReady_sum', color='yearReady', 
                             title='Repair costs broken down by year, month',
                             labels={'cost_yearReady_monthReady_sum': 'Repair Cost', 'monthReady': 'Month', 'yearReady': 'Year'})
                fig.update_layout(title_x=0.5)
                st.plotly_chart(fig,theme=None, use_container_width=True)
                #bar group
                fig = px.bar(df_cost_yearReady_monthReady, x='monthReady', y='cost_yearReady_monthReady_sum', color='yearReady', 
                             barmode='group',title='Repair costs broken down by year, month',
                             labels={'cost_yearReady_monthReady_sum': 'Repair Cost', 'monthReady': 'Month', 'yearReady': 'Year'})
                fig.update_layout(title_x=0.5)
                st.plotly_chart(fig,theme=None, use_container_width=True)
                #density_heatmap
                fig = px.density_heatmap(df_cost_yearReady_monthReady, x='monthReady', y='yearReady', z='cost_yearReady_monthReady_sum', 
                                         title="Heatmap of Repair costs broken down by year, month",
                                         labels={'cost_yearReady_monthReady_sum': 'Repair Cost', 'monthReady': 'Month', 'yearReady': 'Year'})
                fig.update_layout(title_x=0.5)
                st.plotly_chart(fig,theme=None, use_container_width=True)

                return 'Repair_costs_broken_down_by_year_month'
            def case_Relationship_between_cost_and_service_duration(self):
                #### Relationship between cost and service duration
                fig = px.scatter(df, x='service_duration', y='cost', size='cost',
                                 color='damage type',title='Relationship between cost and service duration per damage type',
                                labels={'service_duration': 'Service Duration in Days', 'cost': 'Cost', 'damage type': 'Damage Type'})
                fig.update_layout(title_x=0.5)
                st.plotly_chart(fig,theme=None, use_container_width=True)
                return 'Relationship_between_cost_and_service_duration'
            def case_Relationship_between_cost_and_kilometers_driven_KMs_in_and_out(self):
                #### Relationship between cost and kilometers driven (KMs in and out)
                fig = px.scatter(df, x='KMs Diff', y='cost', size='cost',
                                 color='damage type',title='Relationship between cost and kilometers driven (KMs in and out)',
                                 labels={'service_duration': 'Service Duration in Days', 'cost': 'Cost', 'damage type': 'Damage Type'})
                fig.update_layout(title_x=0.5)
                st.plotly_chart(fig,theme=None, use_container_width=True)
                return 'Relationship_between_cost_and_kilometers_driven_(KMs in and out)'
            def case_Cost_comparisons_across_different_fuel_levels_fuel_in_vs_fuel_out(self):
                #### Cost comparisons across different fuel levels (fuel in vs fuel out)
                #### Cost vs Fuel In and Fuel Out
                fig = px.scatter(df, x='Fuel in', y='cost', 
                                          color='Fuel out',  
                                          title='Cost vs Fuel In and Fuel Out',
                                          labels={'Fuel in': 'Fuel In', 'cost': 'Repair Cost', 'Fuel out': 'Fuel Out'},trendline='ols')
                fig.update_layout(title_x=0.5)
                st.plotly_chart(fig,theme=None, use_container_width=True)
                #### Fuel In vs Fuel Out (Cost represented by bubble size)
                fig = px.scatter(df, x='Fuel in', y='Fuel out', size='cost', color='cost',
                                 title='Fuel In vs Fuel Out (Cost represented by bubble size)',
                                 labels={'Fuel in': 'Fuel In', 'Fuel out': 'Fuel Out', 'cost': 'Repair Cost'})
                fig.update_layout(title_x=0.5)
                st.plotly_chart(fig,theme=None, use_container_width=True)
                #### Average Repair Costs for Fuel In vs Fuel Out (Heatmap)
                df_agg = df.groupby(['Fuel in', 'Fuel out'])['cost'].mean().reset_index()

                fig = px.density_heatmap(df_agg, x='Fuel in', y='Fuel out', z='cost', 
                                         title='Average Repair Costs for Fuel In vs Fuel Out (Heatmap)',
                                         labels={'Fuel in': 'Fuel In', 'Fuel out': 'Fuel Out', 'cost': 'Avg Repair Cost'})
                fig.update_layout(title_x=0.5)
                st.plotly_chart(fig,theme=None, use_container_width=True)
                #### Cost Distribution by Fuel In and Out (Combined Violin Plot)
                fig = px.violin(df, x='Fuel in', y='cost', color='Fuel out', 
                                title='Cost Distribution by Fuel In and Out (Combined Violin Plot)',
                                labels={'Fuel in': 'Fuel In', 'cost': 'Repair Cost', 'Fuel out': 'Fuel Out'})
                fig.update_layout(title_x=0.5)
                st.plotly_chart(fig,theme=None, use_container_width=True)
                return 'Cost comparisons across different fuel levels (fuel in vs fuel out)'
            def case_Total_cost_distribution_across_different_years(self):
                #### Total cost distribution across different years
                df_year_cost = df.groupby(['yearReady'])['cost'].sum().reset_index(name='total_year_cost')
                mySunBurst(df_year_cost, name=['yearReady'], value='total_year_cost',title='Total cost distribution across different years')
                myPlot1(
                    data=df_year_cost,
                    xs='yearReady',
                    ys='total_year_cost',
                    clr='total_year_cost',
                    plotType='bar',
                    title='Total cost distribution across different years',
                    sort_by=['total_year_cost'],
                    ascending=[True]
                )
                return 'Total_cost_distribution_across_different_years'
            def case_Total_cost_distribution_across_different_car_models(self):
                #### Total cost distribution across different car models
                df_car_cost = df.groupby(['car'])['cost'].sum().reset_index(name='total_car_cost')
                mySunBurst(df_car_cost, name=['car'], value='total_car_cost',title='Total cost distribution across different car models')
                myPlot1(
                    data=df_car_cost,
                    xs='car',
                    ys='total_car_cost',
                    clr='total_car_cost',
                    plotType='bar',
                    title='Total cost distribution across different car models',
                    sort_by=['total_car_cost'],
                    ascending=[True]
                )
                return 'Total_cost_distribution_across_different_car_models'
            def case_Total_cost_distribution_across_different_locations(self):
                #### Total cost distribution across different locations
                df_location_cost = df.groupby(['location'])['cost'].sum().reset_index(name='total_location_cost')
                mySunBurst(df_location_cost, name=['location'], value='total_location_cost',title='Total cost distribution across different locations')
                myPlot1(
                    data=df_location_cost,
                    xs='location',
                    ys='total_location_cost',
                    clr='total_location_cost',
                    plotType='bar',
                    title='Total cost distribution across different locations',
                    sort_by=['total_location_cost'],
                    ascending=[True]
                )
                return 'Total_cost_distribution_across_different_locations'
            def case_Total_cost_distribution_across_different_corporates(self):
                #### Total cost distribution across different corporates
                df_corporate_cost = df.groupby(['corporate'])['cost'].sum().reset_index(name='total_corporate_cost')
                mySunBurst(df_corporate_cost, name=['corporate'], value='total_corporate_cost',title='Total cost distribution across different corporates')
                myPlot1(
                    data=df_corporate_cost,
                    xs='corporate',
                    ys='total_corporate_cost',
                    clr='total_corporate_cost',
                    plotType='bar',
                    title='Total cost distribution across different corporate',
                    sort_by=['total_corporate_cost'],
                    ascending=[True]
                )
                return 'Total_cost_distribution_across_different_corporates'
            def case_Total_cost_distribution_across_different_delivered_by_persons(self):
                #### Total cost distribution across different delivered by persons
                df_deliveredBy_cost = df.groupby(['delivered by'])['cost'].sum().reset_index(name='total_deliveredBy_cost')
                mySunBurst(df_deliveredBy_cost, name=['delivered by'], value='total_deliveredBy_cost',title='Total cost distribution across different delivered by persons')
                myPlot1(
                    data=df_deliveredBy_cost,
                    xs='delivered by',
                    ys='total_deliveredBy_cost',
                    clr='total_deliveredBy_cost',
                    plotType='bar',
                    title='Total cost distribution across different delivered by persons',
                    sort_by=['total_deliveredBy_cost'],
                    ascending=[True]
                )
                return 'Total_cost_distribution_across_different_delivered_by_persons'                
            def case_Total_cost_distribution_across_different_returned_by_persons(self):
                #### Total cost distribution across different returned by persons
                df_returnedBy_cost = df.groupby(['returned by'])['cost'].sum().reset_index(name='total_returnedBy_cost')
                mySunBurst(df_returnedBy_cost, name=['returned by'], value='total_returnedBy_cost',title='Total cost distribution across different returned by persons')
                myPlot1(
                    data=df_returnedBy_cost,
                    xs='returned by',
                    ys='total_returnedBy_cost',
                    clr='total_returnedBy_cost',
                    plotType='bar',
                    title='Total cost distribution across different returned by persons',
                    sort_by=['total_returnedBy_cost'],
                    ascending=[True]
                )
                return 'Total_cost_distribution_across_different_returned_by_persons'                
            def case_Total_cost_distribution_across_different_returned_by_other_persons(self):
                #### Total cost distribution across different returned by other persons
                deliveredByOthers_RB = df[(df.get('returned by') == df.get('delivered by')) ==False]['returned by'].reset_index(name='returnedByOthers')
                deliveredByOthers_CS = df[(df.get('returned by') == df.get('delivered by')) ==False]['cost'].reset_index(name='returnedByOthers_cost')
                deliveredByOthers_combined = deliveredByOthers_RB.join(deliveredByOthers_CS, lsuffix='_caller')
                deliveredByOthers_combined = deliveredByOthers_combined.drop(columns=['index_caller','index'])
                deliveredByOthers_cost = deliveredByOthers_combined.groupby(['returnedByOthers'])['returnedByOthers_cost'].sum().reset_index(name='total_returnedByOthers_cost')
                mySunBurst(deliveredByOthers_cost, name=['returnedByOthers'], value='total_returnedByOthers_cost',title='Total cost distribution across different returned by other persons')
                myPlot1(
                    data=deliveredByOthers_cost,
                    xs='returnedByOthers',
                    ys='total_returnedByOthers_cost',
                    clr='total_returnedByOthers_cost',
                    plotType='bar',
                    title='Total cost distribution across different returned by other persons',
                    sort_by=['total_returnedByOthers_cost'],
                    ascending=[True]
                )
                return 'Total_cost_distribution_across_different_returned_by_other_persons'                
            def case_Count_distribution_across_different_returned_by_other_persons(self):
                #### Count distribution across different returned by other persons
                #display(Markdown(deliveredByOthers_combined.to_markdown()))
                deliveredByOthers_RB = df[(df.get('returned by') == df.get('delivered by')) ==False]['returned by'].reset_index(name='returnedByOthers')
                deliveredByOthers_CS = df[(df.get('returned by') == df.get('delivered by')) ==False]['cost'].reset_index(name='returnedByOthers_cost')
                deliveredByOthers_combined = deliveredByOthers_RB.join(deliveredByOthers_CS, lsuffix='_caller')
                deliveredByOthers_combined = deliveredByOthers_combined.drop(columns=['index_caller','index'])
                deliveredByOthers_count = deliveredByOthers_combined['returnedByOthers'].value_counts().reset_index(name='total_returnedByOthers_count')
                #display(Markdown(deliveredByOthers_count.to_markdown()))
                mySunBurst(deliveredByOthers_count, name=['index'], value='total_returnedByOthers_count',title='Count distribution across different returned by other persons')
                myPlot1(
                    data=deliveredByOthers_count,
                    xs='index',
                    ys='total_returnedByOthers_count',
                    clr='total_returnedByOthers_count',
                    plotType='bar',
                    title='Count distribution across different returned by other persons ',
                    sort_by=['total_returnedByOthers_count'],
                    ascending=[True]
                )
                return 'Count_distribution_across_different_returned_by_other_persons'                
            def case_Total_cost_of_each_Damage_type_for_each_Cost_Category(self):
                #### Total cost of each Damage type for each Cost Category
                df_cost_damage = df.groupby(['cost_category','damage type'])['cost'].sum().reset_index(name='total_damage_cost')
                mySunBurst(df_cost_damage, name=['cost_category','damage type'], value='total_damage_cost',title='Total cost of each damage type for each cost category')
                return 'Total_cost_of_each_Damage_type_for_each_Cost_Category'                
            def case_Total_cost_of_each_year_for_each_month_name(self):
                #### Total cost of each year for each month name
                df_year_month_cost = df.groupby(['yearReady','monthNReady'])['cost'].sum().reset_index(name='total_year_month_cost')
                mySunBurst(df_year_month_cost, name=['yearReady','monthNReady'], value='total_year_month_cost',title='Total cost of each year for each month name')
                return 'Total_cost_of_each_year_for_each_month_name'

            def default_case(self):
                return "Default class method executed"
            def CI_switch(self, value):
                method_name = f'case_{value}'
                method = getattr(self, method_name, self.default_case)
                return method()    
        # Usage
        CI_switcher = SwitchCICase()
        CI_result = CI_switcher.CI_switch(selectCostInsight)
        st.write('Cost Insight: ',CI_result)

        return 'Cost_Insights'
    ################################################################################################## Service Duration Insights
    def case_Service_Duration_Insights(self):
        df = load_data('maintenance_cleaned_extended.xlsx')
        st.header('Service Duration Insights')
        selectServiceInsight = st.sidebar.selectbox('Select Service Duration Insight :',
                                                 ['Average_Service_Duration_by_Damage_Type',
                                                  'Service_Duration_distributed_within_each_damage_type',
                                                  'Service_duration_by_car_model',
                                                  'Average_service_duration_by_location',
                                                  'Average_Service_duration_trends_by_year_month',
                                                  'Correlation_between_service_duration_and_cost',
                                                  'Correlation_between_service_duration_and_kilometers_driven_during_repair_period',
                                                  'Fuel_Difference_vs_Service_Duration',
                                                  'Average_Service_Duration_by_Damage_Type_and_Cost_Category'
                                                 ], key=5)
        class SwitchSICase:
            def case_Average_Service_Duration_by_Damage_Type(self):
                ### Service Duration Analysis
                avg_service_duration_by_damage = df.groupby('damage type')['service_duration'].mean().round(1).sort_values().reset_index(name='AverageServiceDuration')
                mySunBurst(avg_service_duration_by_damage, name=['damage type'], value='AverageServiceDuration',title='Average Service Duration by Damage Type ')
                return 'Average_Service_Duration_by_Damage_Type'
            def case_Service_Duration_distributed_within_each_damage_type(self):
                #### Damage Type vs. Service Duration
                #### Which damage types tend to require the longest service durations?
                myBoxPlot(df, x='damage type', y='service_duration',color='damage type',title='Service Duration distributed within each damage type')
                return 'Service_Duration_distributed_within_each_damage_type'
            def case_Service_duration_by_car_model(self):
                #### Service duration by car model
                myBoxPlot(df, x='car', y='service_duration',color='car',title='Service duration by car model')
                return 'Service_duration_by_car_model'
            def case_Average_service_duration_by_location(self):
                #### Average Service duration by location
                avg_service_duration_by_damage = df.groupby('location')['service_duration'].mean().round(1).sort_index().reset_index(name='AverageServiceDuration')
                myPlot1(avg_service_duration_by_damage,'location','AverageServiceDuration','location','bar','Average service duration by location', sort_by='AverageServiceDuration', ascending=True)
                return 'Average_service_duration_by_location'
            def case_Average_Service_duration_trends_by_year_month(self):
                #### Service duration trends by  year - month
                service_duration_by_dateReady = df.groupby(['yearReady','monthReady'])['service_duration'].mean().round(1).sort_values().reset_index(name='ServiceDurationDateReady')
                myPlot1(service_duration_by_dateReady,'monthReady','ServiceDurationDateReady','yearReady','line','Average Service duration trends by year - month', sort_by='monthReady', ascending=True)
                return 'Average_Service_duration_trends_by_year_month'
            def case_Correlation_between_service_duration_and_cost(self):
                #### Correlation between service duration and cost
                #### Is there a correlation between the service duration and the cost of repair?
                fig = px.scatter(df, x='service_duration', y='cost',color='service_duration', title='Correlation between service duration and cost')
                fig.update_layout(title_x=0.5)
                #fig.show()
                st.plotly_chart(fig,theme=None, use_container_width=True)
                return 'Correlation_between_service_duration_and_cost'
            def case_Correlation_between_service_duration_and_kilometers_driven_during_repair_period(self):
                #### Correlation between service duration and kilometers driven during repair period
                fig = px.scatter(df, x='KMs Diff', y='service_duration',color='KMs Diff', title='Correlation between service duration and kilometers driven during repair period')
                fig.update_layout(title_x=0.5)
                #fig.show()
                st.plotly_chart(fig,theme=None, use_container_width=True)
                return 'Correlation_between_service_duration_and_kilometers_driven_during_repair_period'
            def case_Fuel_Difference_vs_Service_Duration(self):
                #### Fuel Diff vs. Service Duration
                #### Does the fuel difference (amount of fuel used) relate to the service duration?
                fig = px.scatter(df, x='Fuel Diff', y='service_duration',color='service_duration', title='Fuel Difference vs. Service Duration')
                fig.update_layout(title_x=0.5)
                #fig.show()
                st.plotly_chart(fig,theme=None, use_container_width=True)
                return 'Fuel_Difference_vs_Service_Duration'
            def case_Average_Service_Duration_by_Damage_Type_and_Cost_Category(self):
                #### What is the average service duration by damage type and cost_category
                avg_service_duration_by_damage_cost_category = df.groupby(['damage type','cost_category'])['service_duration'].mean().round(1).sort_values().reset_index(name='AverageServiceDuration')
                mySunBurst(avg_service_duration_by_damage_cost_category, name=['damage type','cost_category'], value='AverageServiceDuration',title='Average Service Duration by Damage Type')
                myPlot1(
                    data=avg_service_duration_by_damage_cost_category,
                    xs='damage type',
                    ys='AverageServiceDuration',
                    clr='cost_category',
                    plotType='bar',
                    title='Average Service Duration by Damage Type and Cost Category',
                    sort_by=['damage type','AverageServiceDuration'],
                    ascending=[True, True]
                )
                myPlot1(
                    data=avg_service_duration_by_damage_cost_category,
                    xs='damage type',
                    ys='AverageServiceDuration',
                    clr='cost_category',
                    plotType='scatter',
                    title='Average Service Duration by Damage Type and Cost Category',
                    sort_by=['cost_category', 'damage type'],
                    ascending=[True, True]
                )
                return 'Average_Service_Duration_by_Damage_Type_and_Cost_Category'

            def default_case(self):
                return "Default class method executed"
            def SI_switch(self, value):
                method_name = f'case_{value}'
                method = getattr(self, method_name, self.default_case)
                return method()    
        # Usage
        SI_switcher = SwitchSICase()
        SI_result = SI_switcher.SI_switch(selectServiceInsight)
        st.write('Service Duration Insight: ',SI_result)
        return 'Service_Duration_Insights'
    ################################################################################################## Damage Type Insights
    def case_Damage_Type_Insights(self):
        df = load_data('maintenance_cleaned_extended.xlsx')
        st.header('Damage Type Insights')
        selectDamageInsight = st.sidebar.selectbox('Select Damage Type Insight :',
                                                 ['Cost_category_and_damage_distribution',
                                                  'Damage_distribution_for_each_car_brand',
                                                  'Damage_distribution_for_each_location',
                                                  'Damage_types_in_relation_to_cost_category',
                                                  'Average_cost_per_damage_type',
                                                  'Damage_type_distribution_across_different_service_durations',
                                                  'Frequency_of_each_damage_type_across_the_dataset',
                                                  'Damage_type_distribution_across_different_cost_categories',
                                                  'Most_common_damage_types_per_car_mode',
                                                  'Most_common_damage_types_by_service_location',
                                                  'Damage_type_frequency_by_year_month',
                                                  'Most_frequent_damage_types_with_the_highest_associated_costs',
                                                  'Most_common_damage_types_for_vehicles_with_high_kilometers_KMs_in',
                                                  'Most_common_damage_types_for_vehicles_with_highest_kilometers_KMs_in'
                                                 ], key=6)
        class SwitchDICase:
            def case_Cost_category_and_damage_distribution(self):
                ### Damage Type Analysis
                #### Cost category and damage distribution
                #### How Many Damage type in each Cost Category
                df_cost_cat_damage = df.groupby(['cost_category', 'damage type'])['damage type'].count().reset_index(name='damage_count')
                mySunBurst(df_cost_cat_damage, name=['cost_category', 'damage type'], value='damage_count',title='Cost category and damage distribution')
                myPlot1(
                    data=df_cost_cat_damage,
                    xs='cost_category',
                    ys='damage_count',
                    clr='damage type',
                    plotType='bar',
                    title='Cost category and damage distribution',
                    sort_by=['cost_category','damage type'],
                    ascending=[True, True]
                )
                return 'Cost_category_and_damage_distribution'
            def case_Damage_distribution_for_each_car_brand(self):
                ####  Damage distribution for each car brand
                #### What are car models for each damage type
                df_damage_car = df.groupby(['damage type','car'])['damage type'].count().reset_index(name='damage_car_count')
                mySunBurst(df_damage_car, name=['damage type','car'], value='damage_car_count',title='Damage distribution for each car brand')
                myPlot1(
                    data=df_damage_car,
                    xs='damage type',
                    ys='damage_car_count',
                    clr='car',
                    plotType='bar',
                    title='Damage distribution for each car brand',
                    sort_by=['damage type','car'],
                    ascending=[True, True]
                )
                return 'Damage_distribution_for_each_car_brand'
            def case_Damage_distribution_for_each_location(self):
                ####  Damage distribution for each location
                #### What are the locations for each damage type
                df_damage_location = df.groupby(['damage type','location'])['damage type'].count().reset_index(name='damage_location_count')
                mySunBurst(df_damage_location, name=['damage type','location'], value='damage_location_count',title='Damage distribution for each location')
                myPlot1(
                    data=df_damage_location,
                    xs='damage type',
                    ys='damage_location_count',
                    clr='location',
                    plotType='bar',
                    title='Damage distribution for each location',
                    sort_by=['damage type','location','damage_location_count'],
                    ascending=[True, True, False]
                )
                return 'Damage_distribution_for_each_location'
            def case_Damage_types_in_relation_to_cost_category(self):
                #### Damage types in relation to cost_category
                df_damage_cost_category = df.groupby(['damage type','cost_category'])['damage type'].count().reset_index(name='damage_cost_category_count')
                mySunBurst(df_damage_cost_category, name=['damage type','cost_category'], value='damage_cost_category_count',title=' Damage types in relation to cost_category')
                myPlot1(
                    data=df_damage_cost_category,
                    xs='damage type',
                    ys='damage_cost_category_count',
                    clr='cost_category',
                    plotType='bar',
                    title='Damage types in relation to cost_category',
                    sort_by=['damage type','damage_cost_category_count'],
                    ascending=[True, True]
                )
                return 'Damage_types_in_relation_to_cost_category'
            def case_Average_cost_per_damage_type(self):
                ### Average cost per damage type
                avg_cost_by_damage = df.groupby('damage type')['cost'].mean().round(1).sort_values().reset_index(name='AverageCost')
                mySunBurst(avg_cost_by_damage, name=['damage type'], value='AverageCost',title='Average cost per damage type')
                myPlot1(
                    data=avg_cost_by_damage,
                    xs='damage type',
                    ys='AverageCost',
                    clr='AverageCost',
                    plotType='bar',
                    title='Average const by Damage Type ',
                    sort_by=['AverageCost','damage type'],
                    ascending=[True, True]
                )
                return 'Average_cost_per_damage_type'
            def case_Damage_type_distribution_across_different_service_durations(self):
                #### Damage type distribution across different service durations
                #### Which damage types tend to require the longest service durations?
                myBoxPlot(df,x='damage type',y='service_duration',color='damage type',title='Damage type distribution across different service durations')
                return 'Damage_type_distribution_across_different_service_durations'
            def case_Frequency_of_each_damage_type_across_the_dataset(self):
                #### Frequency of each damage type across the dataset
                damage_Type_frequency = df.get('damage type').value_counts().sort_values()
                myPlot2(damage_Type_frequency,'bar','Frequency of each damage type across the dataset')
                return 'Frequency_of_each_damage_type_across_the_dataset'
            def case_Damage_type_distribution_across_different_cost_categories(self):
                #### Damage type distribution across different cost categories
                # Group by cost category and damage type, and count occurrences
                cost_category_damage_Type = df.groupby(['cost_category', 'damage type']).size().reset_index(name='Frequency')
                # Plot stacked bar chart
                fig = px.bar(cost_category_damage_Type,
                             x='damage type', 
                             y='Frequency', 
                             color='cost_category',
                             barmode='stack',  # Stacked bar chart
                             title="Damage type distribution across different cost categories",
                             labels={'Frequency': 'Damage Type Frequency', 'damage type': 'Damage Type', 'cost_category': 'Cost Category'}
                )
                fig.update_layout(title_x=0.5)
                st.plotly_chart(fig,theme=None, use_container_width=True)
                mySunBurst(cost_category_damage_Type, name=['damage type','cost_category' ], value='Frequency',title='Damage type distribution across different cost categories')
                return 'Damage_type_distribution_across_different_cost_categories'
            def case_Most_common_damage_types_per_car_mode(self):
                #### Most common damage types per car model
                damage_Type_car = df.groupby(['damage type','car'])['damage type'].count().reset_index(name='Frequency')
                # Plot stacked bar chart
                fig = px.bar(damage_Type_car,
                             x='car', 
                             y='Frequency', 
                             color='damage type',
                             barmode='stack',
                             title="Most common damage types per car model",
                             labels={'car': 'Car Model', 'Frequency': 'Damage Frequency', 'damage type': 'Damage Type'}
                )
                fig.update_layout(title_x=0.5)
                st.plotly_chart(fig,theme=None, use_container_width=True)
                # Plot grouped bar chart
                fig = px.bar(damage_Type_car,
                             x='car', 
                             y='Frequency', 
                             color='damage type',
                             barmode='group',
                             title="Most common damage types per car model",
                             labels={'car': 'Car Model', 'Frequency': 'Damage Frequency', 'damage type': 'Damage Type'}
                )
                fig.update_layout(title_x=0.5)
                st.plotly_chart(fig,theme=None, use_container_width=True)
                return 'Most_common_damage_types_per_car_mode'
            def case_Most_common_damage_types_by_service_location(self):
                #### Most common damage types by service location
                damage_Type_location = df.groupby(['location','damage type'])['damage type'].count().reset_index(name='Frequency')
                # Plot stacked bar chart
                fig = px.bar(damage_Type_location,
                             x='location', 
                             y='Frequency', 
                             color='damage type',
                             barmode='stack',
                             title="Most common damage types by service location",
                             labels={'location': 'Service Location', 'Frequency': 'Damage Frequency', 'damage type': 'Damage Type'}
                )
                fig.update_layout(title_x=0.5)
                st.plotly_chart(fig,theme=None, use_container_width=True)
                # Plot grouped bar chart
                fig = px.bar(damage_Type_location,
                             x='location', 
                             y='Frequency', 
                             color='damage type',
                             barmode='group',
                             title="Most common damage types by service location",
                             labels={'location': 'Service Location', 'Frequency': 'Damage Frequency', 'damage type': 'Damage Type'}
                )
                fig.update_layout(title_x=0.5)
                st.plotly_chart(fig,theme=None, use_container_width=True)
                return 'Most_common_damage_types_by_service_location'
            def case_Damage_type_frequency_by_year_month(self):
                #### Damage type frequency by year, month
                damage_Type_YM_frequency = df.groupby(['yearReady','monthReady'])['monthReady'].count().sort_values().reset_index(name='Frequency')
                myPlot1(damage_Type_YM_frequency,'monthReady','Frequency','yearReady','line','Damage type frequency by year, month', sort_by='monthReady', ascending=True)
                return 'Damage_type_frequency_by_year_month'
            def case_Most_frequent_damage_types_with_the_highest_associated_costs(self):
                #### Most frequent damage types with the highest associated costs
                # Group data by damage type to get frequency and sum of costs
                damage_cost = df.groupby('damage type').agg(
                    Frequency=('damage type', 'size'),# Frequency of each damage type
                    Total_Cost=('cost', 'sum')        # Sum of associated costs for each damage type
                ).reset_index()
                # Plot the scatter plot
                fig = px.scatter(damage_cost,
                                 x='Frequency', 
                                 y='Total_Cost', 
                                 text='damage type',  # Display damage type as labels for the points
                                 title="Most frequent damage types with the highest associated costs",
                                 labels={'Frequency': 'Damage Frequency', 'Total_Cost': 'Total Cost'},
                                 size='Frequency',    # Optional: make the size of the points represent the frequency
                                 color='damage type'  # Optional: color the points by damage type
                )
                st.plotly_chart(fig,theme=None, use_container_width=True)
                return 'Most_frequent_damage_types_with_the_highest_associated_costs'
            def case_Most_common_damage_types_for_vehicles_with_high_kilometers_KMs_in(self):
                #### Most common damage types for vehicles with high kilometers (KMs in)
                # Group by damage type and sum the kilometers
                damage_Type_KMsIn_total = df.groupby('damage type')['KMs IN'].sum().sort_values()
                myPlot2(damage_Type_KMsIn_total, 'bar', 'Most common damage types for vehicles with high kilometers (KMs in)')
                return 'Most_common_damage_types_for_vehicles_with_high_kilometers_KMs_in'
            def case_Most_common_damage_types_for_vehicles_with_highest_kilometers_KMs_in(self):
                #### Most common damage types for vehicles with highest kilometers (KMs in)
                # Group by damage type and max the kilometers
                damage_Type_KMsIn_frequency = df.groupby('damage type')['KMs IN'].max().sort_values()
                myPlot2(damage_Type_KMsIn_frequency,'bar','Most common damage types for vehicles with highest kilometers (KMs in)')
                return 'Most_common_damage_types_for_vehicles_with_highest_kilometers_KMs_in'

            def default_case(self):
                return "Default class method executed"
            def DI_switch(self, value):
                method_name = f'case_{value}'
                method = getattr(self, method_name, self.default_case)
                return method()    
        # Usage
        DI_switcher = SwitchDICase()
        DI_result = DI_switcher.DI_switch(selectDamageInsight)
        st.write('Damage Type Insight: ',DI_result)
        return 'Damage_Type_Insights'
    ################################################################################################## Car Model Insights
    def case_Car_Model_Insights(self):
        df = load_data('maintenance_cleaned_extended.xlsx')
        st.header('Car Model Insights')
        selectCarInsight = st.sidebar.selectbox('Select Car Model Insight :',
                                                 ['Most_frequently_serviced_car_models',
                                                  'Average_repair_cost_per_car_model',
                                                  'Total_costs_per_car_model_across_all_damage_types',
                                                  'Most_common_damage_types_for_each_car_model',
                                                  'Service_duration_per_car_model',
                                                  'Kilometers_driven_KMs_diff_by_car_model',
                                                  'Car_model_distribution_by_service_location'
                                                 ], key=7)
        class SwitchCMCase:
            def case_Most_frequently_serviced_car_models(self):
                #### Most frequently serviced car models
                most_frequent_Serviced_car = df.groupby('car').size().sort_values(ascending=False).reset_index(name='Frequecy of servecing')
                myPlot1(most_frequent_Serviced_car,xs='car',ys='Frequecy of servecing',clr='car',plotType='bar',title='Most frequently serviced car models', sort_by=None, ascending=True)
                return 'Most_frequently_serviced_car_models'
            def case_Average_repair_cost_per_car_model(self):
                #### Average repair cost per car model
                average_cost_car = df.groupby('car')['cost'].mean().sort_values(ascending=False).reset_index(name='Average Repait Cost')
                myPlot1(average_cost_car,xs='car',ys='Average Repait Cost',clr='car',plotType='bar',title='Average repair cost per car model', sort_by=None, ascending=True)
                return 'Average_repair_cost_per_car_model'
            def case_Total_costs_per_car_model_across_all_damage_types(self):
                #### Total costs per car model across all damage types
                total_cost_damage_car = df.groupby(['car','damage type'])['cost'].sum().sort_values(ascending=False).reset_index(name='Total Costs')
                myPlot1(total_cost_damage_car,xs='car',ys='Total Costs',clr='damage type',plotType='bar',title='Total costs per car model across all damage types', sort_by=None, ascending=True)
                # Plot SunBurst chart
                mySunBurst(data=total_cost_damage_car, name=['car','damage type'], value='Total Costs', title='Total costs per car model across all damage types')
                return 'Total_costs_per_car_model_across_all_damage_types'
            def case_Most_common_damage_types_for_each_car_model(self):
                #### Most common damage types for each car model
                damage_Type_car = df.groupby(['damage type','car'])['damage type'].count().reset_index(name='Frequency')
                # Plot stacked bar chart
                fig = px.bar(damage_Type_car, 
                             x='car', 
                             y='Frequency', 
                             color='damage type',
                             barmode='stack',
                             title="Most common damage types for each car model",
                             labels={'car': 'Car Model', 'Frequency': 'Damage Frequency', 'damage type': 'Damage Type'}
                            )
                fig.update_layout(title_x=0.5)
                st.plotly_chart(fig,theme=None, use_container_width=True)
                # Plot grouped bar chart
                fig = px.bar(damage_Type_car,
                            x='car', 
                            y='Frequency', 
                            color='damage type',
                            barmode='group',
                            title="Most common damage types for each car model",
                            labels={'car': 'Car Model', 'Frequency': 'Damage Frequency', 'damage type': 'Damage Type'}
                            )
                fig.update_layout(title_x=0.5)
                st.plotly_chart(fig,theme=None, use_container_width=True)
                return 'Most_common_damage_types_for_each_car_model'
            def case_Service_duration_per_car_model(self):
                #### Service duration per car model
                myBoxPlot(df,x='car',y='service_duration',color='damage type',title='Service duration per car model')
                return 'Service_duration_per_car_model'
            def case_Kilometers_driven_KMs_diff_by_car_model(self):
                #### Kilometers driven (KMs diff) by car model
                KMsDiff_car = df.groupby(['car'])['KMs Diff'].size().sort_values(ascending=False).reset_index(name='KMs Difference')
                myPlot1(KMsDiff_car,xs='car',ys='KMs Difference',clr='car',plotType='bar',title='Kilometers driven (KMs diff) by car model', sort_by=None, ascending=True)
                return 'Kilometers_driven_KMs_diff_by_car_model'
            def case_Car_model_distribution_by_service_location(self):
                #### Car model distribution by service location
                # Group by location and car model, and count the occurrences
                location_car = df.groupby(['location', 'car']).size().reset_index(name='Count')

                # Plot stacked bar chart
                fig = px.bar(location_car, 
                             x='location', 
                             y='Count', 
                             color='car',
                             barmode='stack',
                             title='Car Model Distribution by Service Location',
                             labels={'count': 'Number of Cars', 'location': 'Service Location'}
                            )

                fig.update_layout(title_x=0.5)
                st.plotly_chart(fig,theme=None, use_container_width=True)
                return 'Car_model_distribution_by_service_location'

            def default_case(self):
                return "Default class method executed"
            def CM_switch(self, value):
                method_name = f'case_{value}'
                method = getattr(self, method_name, self.default_case)
                return method()    
        # Usage
        CM_switcher = SwitchCMCase()
        CM_result = CM_switcher.CM_switch(selectCarInsight)
        st.write('Car Model Insight: ',CM_result)

        
        
        return 'Car_Model_Insights'
    ################################################################################################## Fuel Insights
    def case_Fuel_Insights(self):
        df = load_data('maintenance_cleaned_extended.xlsx')
        st.header('Fuel Insights')
        selectFuelInsight = st.sidebar.selectbox('Select Fuel Insight :',
                                                 ['Relationship_between_fuel_levels_fuel_in_vs_fuel_out_and_repair_costs',
                                                  'Relationship_between_fuel_levels_and_service_duration',
                                                  'Fuel_consumption_differences_across_car_models',
                                                  'Fuel_consumption_vs_kilometers_driven_during_service',
                                                  'Fuel_usage_distribution_across_different_damage_types'
                                                 ], key=8)
        class SwitchFLCase:
            def case_Relationship_between_fuel_levels_fuel_in_vs_fuel_out_and_repair_costs(self):
                #### Relationship between fuel levels (fuel in vs. fuel out) and repair costs
                # Create a long-form DataFrame for comparison of fuel in and fuel out
                df_long = df.melt(id_vars='cost', value_vars=['Fuel in', 'Fuel out'],
                                  var_name='Fuel Type', value_name='Fuel Level')
                # Scatter plot: fuel in/fuel out vs. repair cost
                fig = px.scatter(df_long, 
                                 x='Fuel Level',    # Fuel levels on X-axis (combined fuel in and out)
                                 y='cost',   # Repair cost on Y-axis
                                 color='Fuel Type', # Distinguish between fuel in and out
                                 title='Relationship between fuel levels (fuel in vs. fuel out) and repair costs',
                                 labels={'Fuel Level': 'Fuel Levels (In/Out)', 'cost': 'Repair Cost'}
                                )
                fig.update_layout(title_x=0.5)
                st.plotly_chart(fig,theme=None, use_container_width=True)
                return 'Relationship_between_fuel_levels_fuel_in_vs_fuel_out_and_repair_costs'
            def case_Relationship_between_fuel_levels_and_service_duration(self):
                #### Relationship between fuel levels and service duration
                # Create a long-form DataFrame for comparison of fuel in and fuel out
                df_long = df.melt(id_vars='service_duration', value_vars=['Fuel in', 'Fuel out'],
                                  var_name='Fuel Type', value_name='Fuel Level')
                # Scatter plot: fuel in/fuel out vs. service duration
                fig = px.scatter(df_long, 
                                 x='Fuel Level',    # Fuel levels on X-axis (combined fuel in and out)
                                 y='service_duration',   # Service duration on Y-axis
                                 color='Fuel Type', # Distinguish between fuel in and out
                                 title='Relationship between fuel levels and service duration',
                                 labels={'Fuel Level': 'Fuel Levels (In/Out)', 'service_duration': 'Service Duration'}
                                )
                fig.update_layout(title_x=0.5)
                st.plotly_chart(fig,theme=None, use_container_width=True)
                return 'Relationship_between_fuel_levels_and_service_duration'
            def case_Fuel_consumption_differences_across_car_models(self):
                #### Fuel consumption differences across car models
                myBoxPlot(data=df,x='car',y='Fuel Diff',color=None,title='Fuel consumption differences across car models')
                return 'Fuel_consumption_differences_across_car_models'
            def case_Fuel_consumption_vs_kilometers_driven_during_service(self):
                #### Fuel consumption vs kilometers driven during service
                # Scatter plot: Fuel Consumption vs. kilometers driven during service
                fig = px.scatter(df, 
                                 x='KMs Diff',      # Kilometers Difference
                                 y='Fuel Diff',          # Fuel Difference
                                 color='service_duration', # Distinguish as per service duration
                                 title='Fuel consumption vs kilometers driven during service',
                                 labels={'KMs Diff': 'Kilometers Difference', 'Fuel Diff': 'Fuel Difference'}
                                )
                fig.update_layout(title_x=0.5)
                st.plotly_chart(fig,theme=None, use_container_width=True)
                return 'Fuel_consumption_vs_kilometers_driven_during_service'
            def case_Fuel_usage_distribution_across_different_damage_types(self):
                #### Fuel usage distribution across different damage types
                myBoxPlot(data=df,x='damage type',y='Fuel Diff',color=None,title='Fuel usage distribution across different damage types')
                return 'Fuel_usage_distribution_across_different_damage_types'
            
            def default_case(self):
                return "Default class method executed"
            def FL_switch(self, value):
                method_name = f'case_{value}'
                method = getattr(self, method_name, self.default_case)
                return method()    
        # Usage
        FL_switcher = SwitchFLCase()
        FL_result = FL_switcher.FL_switch(selectFuelInsight)
        st.write('Fuel Insight: ',FL_result)
        
        return 'Fuel_Insights'
    ################################################################################################## Time Based Insights
    def case_Time_Based_Insights(self):
        df = load_data('maintenance_cleaned_extended.xlsx')
        st.header('Time Based Insights')
        selectTimeInsight = st.sidebar.selectbox('Select Time Based Insight :',
                                                 ['Trends_in_the_number_of_repairs_over_time',
                                                  'Average_repair_costs_by_year_month_or_day',
                                                  'Seasonal_trends_in_repair_costs_and_damage_types',
                                                  'Changes_in_service_duration_over_time',
                                                  'Cost_categories_that_are_more_common_in_specific_months',
                                                  'Trends_in_fuel_consumption_over_time'
                                                 ], key=9)
        class SwitchTICase:
            def case_Trends_in_the_number_of_repairs_over_time(self):
                #### Trends in the number of repairs over time
                date_count = df.groupby(['date in']).size().reset_index(name='Count').sort_values(by='date in')
                myPlot1(date_count,'date in','Count',None,'line','Trends in the number of repairs over time', sort_by=None, ascending=True)
                print("The line chart above shows the trends in the number of repairs from January 2015 to early 2016. Here's an analysis of the ")
                print("visualized data:")
                print("      1.High Variability:")
                print("        There is a high degree of fluctuation in the number of repairs over the observed time frame. The number of repairs ")
                print("        spikes significantly at certain points, especially around May 2015 and November 2015, where you see sharp peaks.")
                print("      2.Distinct Spikes:")
                print("        The spike around May 2015 shows over 50 repairs in that period, which is much higher compared to the rest of the")
                print("         timeline.There is another notable peak around December 2015 with around 30 repairs.")
                print("      3.General Downward Trend at the Start:")
                print("        At the beginning of the year (January 2015), the number of repairs is initially quite high but then sharply drops")
                print("         and fluctuates at a lower level through the remainder of the year, punctuated by the occasional spikes.")
                print("      4.Seasonality or Cyclic Patterns:")
                print("        While the data does not show a clear repeating seasonal pattern, the large spikes in May and November could suggest")
                print("        some underlying factors driving repairs during these months, such as weather changes or specific events.")
                print("      5.Consistent Low Activity:")
                print("        Between the peaks, the number of repairs seems to stabilize at a relatively low range (between 0 and 10 repairs)")
                print("        for most of the time.")

                print("Suggestions:")
                print("      1.Identifying the Causes of the Peaks:")
                print("        it might be useful to investigate the root causes of the repair spikes in May 2015 and December 2015.")
                print("        Are there specific incidents or external factors during those months that led to increased repairs?")
                print("      2.Breakdown by Categories:")
                print("        Repair type:")
                print("          here is a break down to the number of repairs by repair type to identify whether particular types of repairs are")
                print("          responsible for the spikes.")
                print("        Location:")
                print("          here is a break down to the number of repairs by location to identify whether particular types of repairs are")
                print("      3.Moving Averages:")
                print("        this chart shows applying a moving average to this data, that could help smooth out the fluctuations and reveal")
                print("        longer-term trends.")
                # Group by damage type and date to get the count of repairs per type over time
                category_count = df.groupby(['date in', 'damage type']).size().reset_index(name='Count')
                # Create a line chart showing the trends in repairs broken down by repair type
                myPlot1(category_count,'date in','Count','damage type','line','Trends in the number of repairs over time by Damage Type', sort_by=None, ascending=True)
                # Group by location and date to get the count of repairs per type over time
                category_count = df.groupby(['date in', 'location']).size().reset_index(name='Count')
                # Create a line chart showing the trends in repairs broken down by repair type
                myPlot1(category_count,'date in','Count','location','line','Trends in the number of repairs over time by location', sort_by=None, ascending=True)
                # First, group by date to get the number of repairs per date
                date_count = df.groupby(['date in']).size().reset_index(name='Count')
                # Calculate a 7-day moving average for the number of repairs
                date_count['Moving_Avg'] = date_count['Count'].rolling(window=7).mean()
                # Create a line chart showing the original data and the moving average
                fig = px.line(date_count, 
                              x='date in', 
                              y='Count', 
                              title='Trends in the number of repairs over time with Moving Average')
                # Add the moving average as another line
                fig.add_scatter(x=date_count['date in'], 
                                y=date_count['Moving_Avg'], 
                                mode='lines', 
                                name='7-day Moving Average', 
                                line=dict(color='orange'))
                # Adjust layout
                fig.update_layout(title_x=0.5, xaxis_title='Date', yaxis_title='Number of Repairs')
                # Show the plot
                st.plotly_chart(fig,theme=None, use_container_width=True)
                return 'Trends_in_the_number_of_repairs_over_time'
            def case_Average_repair_costs_by_year_month_or_day(self):
                #### Average repair costs by year, month, or day
                date_average = df.groupby(['date in'])['cost'].mean().reset_index().sort_values(by='date in')
                myPlot1(date_average,'date in','cost',None,'line','Trends in average repair cost over time', sort_by=None, ascending=True)

                # Group by year
                df['year']  = df['date in'].dt.year
                date_average = df.groupby('year')['cost'].mean().reset_index()
                date_average['year']=date_average['year'].astype(str)
                myPlot1(date_average, 'year', 'cost', None, 'line', 'Trends in average repair cost over time', sort_by=None, ascending=True)

                # Concatenate year and month into a new 'year_month' column
                # Extract the year and month, ensuring the month is two digits
                df['year_month'] = df['year'].astype(str) + '_' + df['date in'].dt.month.astype(str).str.zfill(2)
                # Group by year_month
                date_average = df.groupby('year_month')['cost'].mean().reset_index().sort_values(by='year_month')
                myPlot1(date_average, 'year_month', 'cost', None, 'line', 'Trends in average repair cost over time', sort_by=None, ascending=True)
                return 'Average_repair_costs_by_year_month_or_day'
            def case_Seasonal_trends_in_repair_costs_and_damage_types(self):
                #### Seasonal trends in repair costs and damage types
                #density_heatmap
                fig = px.density_heatmap(df, x='date in', y='damage type', z='cost', 
                                         title="Seasonal trends in repair costs and damage types",
                                         labels={'cost': 'Repair Cost', 'date in': 'Date', 'damage type': 'Damage Type'})
                fig.update_layout(title_x=0.5)
                st.plotly_chart(fig,theme=None, use_container_width=True)
                return 'Seasonal_trends_in_repair_costs_and_damage_types'
            def case_Changes_in_service_duration_over_time(self):
                #### Changes in service duration over time
                date_service_duration = df.groupby('date in')['service_duration'].sum().reset_index().sort_values(by='date in')
                myPlot1(date_service_duration, 'date in', 'service_duration', None, 'line', 'Changes in service duration over time - DAILY', sort_by=None, ascending=True)

                df['year_month'] = df['date in'].dt.year.astype(str) + '_' + df['date in'].dt.month.astype(str).str.zfill(2)
                # Group by year_month
                date_service_duration = df.groupby('year_month')['service_duration'].sum().reset_index().sort_values(by='year_month')
                myPlot1(date_service_duration, 'year_month', 'service_duration', None, 'line', 'Changes in service duration over time - MONTHLY', sort_by=None, ascending=True)
                return 'Changes_in_service_duration_over_time'
            def case_Cost_categories_that_are_more_common_in_specific_months(self):
                #### Cost categories that are more common in specific months
                fig = px.bar(df,
                             x='date in', 
                             y='cost_category', 
                             color='cost_category',
                             barmode='stack',  # Stacked bar chart
                             title="Cost categories that are more common in Daily Basis",
                             labels={'date in': 'Date', 'cost_category': 'Cost Category'}
                            )
                fig.update_layout(title_x=0.5)
                st.plotly_chart(fig,theme=None, use_container_width=True)

                df['year_month'] = df['date in'].dt.year.astype(str) + '_' + df['date in'].dt.month.astype(str).str.zfill(2)
                # Group by year_month
                #date_cost_category = df.groupby('year_month')['cost_category'].size().reset_index().sort_values(by='year_month')
                #myPlot1(df.sort_values(by='year_month'), 'year_month', 'cost_category', None, 'bar', 'Cost categories that are more common in specific months', sort_by=None, ascending=True)
                fig = px.bar(df,
                             x='year_month', 
                             y='cost_category', 
                             color='cost_category',
                             barmode='stack',  # Stacked bar chart
                             title="Cost categories that are more common in years - months",
                             labels={'year_month': 'Date', 'cost_category': 'Cost Category'}
                            )
                fig.update_layout(title_x=0.5)
                st.plotly_chart(fig,theme=None, use_container_width=True)
                return 'Cost_categories_that_are_more_common_in_specific_months'
            def case_Trends_in_fuel_consumption_over_time(self):
                #### Trends in fuel consumption over time
                df['year_month'] = df['date in'].dt.year.astype(str) + '_' + df['date in'].dt.month.astype(str).str.zfill(2)
                # Group by year_month
                date_Fuel_Diff = df.groupby('year_month')['Fuel Diff'].sum().reset_index().sort_values(by='year_month')
                myPlot1(date_Fuel_Diff, 'year_month', 'Fuel Diff', None, 'line', 'Trends in fuel consumption over time', sort_by=None, ascending=True)

                date_Fuel_Diff = df.groupby(['year_month', 'damage type']).sum().reset_index().sort_values(by='year_month')
                myPlot1(date_Fuel_Diff, 'year_month', 'Fuel Diff', 'damage type', 'line', 'Trends in fuel consumption over time', sort_by=None, ascending=True)
                return 'Trends_in_fuel_consumption_over_time'
            
            def default_case(self):
                return "Default class method executed"
            def TI_switch(self, value):
                method_name = f'case_{value}'
                method = getattr(self, method_name, self.default_case)
                return method()    
        # Usage
        TI_switcher = SwitchTICase()
        TI_result = TI_switcher.TI_switch(selectTimeInsight)
        st.write('Time Based Insight: ',TI_result)
        
        return 'Time_Based_Insights'
    ################################################################################################## Location Based Insights
    def case_Lcation_Based_Insights(self):
        df = load_data('maintenance_cleaned_extended.xlsx')
        st.header('Location Based Insights')
        selectLocationInsight = st.sidebar.selectbox('Select Location Based Insight :',
                                                 ['Average_cost_of_repairs_by_service_location',
                                                  'Total_number_of_repairs_completed_at_each_location',
                                                  'Service_duration_across_different_locations',
                                                  'Most_common_damage_types_by_location',
                                                  'Comparison_of_car_models_serviced_at_different_locations'
                                                 ], key=10)
        class SwitchLCCase:
            def case_Average_cost_of_repairs_by_service_location(self):
                #### Average cost of repairs by service location
                Avg_cost_location = df.groupby(['location'])['cost'].mean().reset_index(name='Average_location_Cost').sort_values(by='Average_location_Cost')
                myPlot1(Avg_cost_location,'location','Average_location_Cost',None,'bar','Average cost of repairs by service location', sort_by=None, ascending=True)
                return 'Average_cost_of_repairs_by_service_location'
            def case_Total_number_of_repairs_completed_at_each_location(self):
                #### Total number of repairs completed at each location
                Location_frequency = df.groupby(['location']).size().reset_index(name='Location Frequency').sort_values(by='Location Frequency')
                myPlot1(Location_frequency,'location','Location Frequency',None,'bar','Total number of repairs completed at each location', sort_by=None, ascending=True)
                return 'Total_number_of_repairs_completed_at_each_location'
            def case_Service_duration_across_different_locations(self):
                #### Service duration across different locations
                Avg_service_duraton_location = df.groupby(['location'])['service_duration'].mean().round(2).reset_index(name='Average Service Duration').sort_values(by='Average Service Duration')
                myPlot1(Avg_service_duraton_location,'location','Average Service Duration',None,'bar','Average Service duration across different locations', sort_by=None, ascending=True)
                return 'Service_duration_across_different_locations'
            def case_Most_common_damage_types_by_location(self):
                #### Most common damage types by location
                damage_Type_location = df.groupby(['damage type','location'])['location'].count().reset_index(name='Frequency')
                # Plot stacked bar chart
                fig = px.bar(damage_Type_location,
                             x='location', 
                             y='Frequency', 
                             color='damage type',
                             barmode='stack',
                             title="Most common damage types by location",
                             labels={'location': 'Service Location', 'Frequency': 'Damage Frequency', 'damage type': 'Damage Type'}
                            )
                fig.update_layout(title_x=0.5)
                st.plotly_chart(fig,theme=None, use_container_width=True)
                # Plot grouped bar chart
                fig = px.bar(damage_Type_location,
                             x='location', 
                             y='Frequency', 
                             color='damage type',
                             barmode='group',
                             title="Most common damage types by location",
                             labels={'location': 'Service Location', 'Frequency': 'Damage Frequency', 'damage type': 'Damage Type'}
                            )
                fig.update_layout(title_x=0.5)
                st.plotly_chart(fig,theme=None, use_container_width=True)
                return 'Most_common_damage_types_by_location'
            def case_Comparison_of_car_models_serviced_at_different_locations(self):
                #### Comparison of car models serviced at different locations
                car_location = df.groupby(['location','car']).size().reset_index(name='Car Model').sort_values(by='Car Model')
                fig = px.bar(car_location,
                             x='location', 
                             y='Car Model', 
                             color='car',
                             barmode='stack',
                             title="Comparison of car models serviced at different locations",
                             labels={'location': 'Service Location', 'car': 'Car Model', 'Car Model': 'Count of Car Model serviced'}
                            )
                fig.update_layout(title_x=0.5)
                st.plotly_chart(fig,theme=None, use_container_width=True)
                return 'Comparison_of_car_models_serviced_at_different_locations'
            
            def default_case(self):
                return "Default class method executed"
            def LC_switch(self, value):
                method_name = f'case_{value}'
                method = getattr(self, method_name, self.default_case)
                return method()    
        # Usage
        LC_switcher = SwitchLCCase()
        LC_result = LC_switcher.LC_switch(selectLocationInsight)
        st.write('Location Based Insight: ',LC_result)
        
        return 'Lcation_Based_Insights'
    ################################################################################################## Kilometers Insights
    def case_Kilometers_Insights(self):
        df = load_data('maintenance_cleaned_extended.xlsx')
        st.header('Kilometers Insights')
        selectKilometersInsight = st.sidebar.selectbox('Select Kilometers Insight :',
                                                 ['Relationship_between_kilometers_driven_KMs_diff_and_repair_costs',
                                                  'Relationship_between_kilometers_driven_KMs_diff_and_repair_costs_per_damage_type',
                                                  'Relationship_between_kilometers_driven_KMs_diff_and_repair_costs_per_service_location',
                                                  'Relationship_between_kilometers_driven_KMs_diff_and_repair_costs_per_service_duration',
                                                  'Correlation_between_kilometers_driven_and_service_duration',
                                                  'Kilometers_driven_distribution_by_car_model',
                                                  'Kilometers_driven_distribution_by_damage_type',
                                                  'Kilometers_driven_by_service_location'
                                                 ], key=11)
        class SwitchKLCase:
            def case_Relationship_between_kilometers_driven_KMs_diff_and_repair_costs(self):
                #### Relationship between kilometers driven (KMs diff) and repair costs
                myPlot1(df,'KMs Diff','cost',None,'scatter','Relationship between kilometers driven (KMs diff) and repair costs', sort_by=None, ascending=True)
                return 'Relationship_between_kilometers_driven_KMs_diff_and_repair_costs'
            def case_Relationship_between_kilometers_driven_KMs_diff_and_repair_costs_per_damage_type(self):
                #### Relationship between kilometers driven (KMs diff) and repair costs per damage type
                myPlot1(df,'KMs Diff','cost','damage type','scatter','Relationship between kilometers driven (KMs diff) and repair costs per damage type', sort_by=None, ascending=True)
                return 'Relationship_between_kilometers_driven_KMs_diff_and_repair_costs_per_damage_type'
            def case_Relationship_between_kilometers_driven_KMs_diff_and_repair_costs_per_service_location(self):
                #### Relationship between kilometers driven (KMs diff) and repair costs per service location
                myPlot1(df,'KMs Diff','cost','location','scatter','Relationship between kilometers driven (KMs diff) and repair costs per service location', sort_by=None, ascending=True)
                return 'Relationship_between_kilometers_driven_KMs_diff_and_repair_costs_per_service_location'
            def case_Relationship_between_kilometers_driven_KMs_diff_and_repair_costs_per_service_duration(self):
                #### Relationship between kilometers driven (KMs diff) and repair costs per service duration
                myPlot1(df,'KMs Diff','cost','service_duration','scatter','Relationship between kilometers driven (KMs diff) and repair costs per service duration', sort_by=None, ascending=True)
                return 'Relationship_between_kilometers_driven_KMs_diff_and_repair_costs_per_service_duration'
            def case_Correlation_between_kilometers_driven_and_service_duration(self):
                #### Correlation between kilometers driven and service duration
                myPlot1(df,'KMs Diff','service_duration',None,'scatter','Correlation between kilometers driven and service duration', sort_by=None, ascending=True)
                return 'Correlation_between_kilometers_driven_and_service_duration'
            def case_Kilometers_driven_distribution_by_car_model(self):
                #### Kilometers driven distribution by car model
                myBoxPlot(data=df,x='car',y='KMs Diff',color=None,title='Kilometers driven distribution by car model')
                return 'Kilometers_driven_distribution_by_car_model'
            def case_Kilometers_driven_distribution_by_damage_type(self):
                #### Kilometers driven distribution by damage type
                myBoxPlot(data=df,x='damage type',y='KMs Diff',color='damage type',title='Kilometers driven distribution by damage type')
                return 'Kilometers_driven_distribution_by_damage_type'
            def case_Kilometers_driven_by_service_location(self):
                #### Kilometers driven by service location
                KMs_Diff_location = df.groupby(['location'])['KMs Diff'].sum().reset_index(name='Total Kilometers Difference').sort_values(by='Total Kilometers Difference')
                myPlot1(KMs_Diff_location,'location','Total Kilometers Difference',None,'bar','Kilometers driven by service location', sort_by=None, ascending=True)
                return 'Kilometers_driven_by_service_location'
            
            def default_case(self):
                return "Default class method executed"
            def KL_switch(self, value):
                method_name = f'case_{value}'
                method = getattr(self, method_name, self.default_case)
                return method()    
        # Usage
        KL_switcher = SwitchKLCase()
        KL_result = KL_switcher.KL_switch(selectKilometersInsight)
        st.write('Kilometers Insight: ',KL_result)
        
        return 'Kilometers_Insights'
    ################################################################################################## Cost Category Insights
    def case_Cost_Category_Insights(self):
        df = load_data('maintenance_cleaned_extended.xlsx')
        st.header('Cost Category Insights')
        selectCostCategoryInsight = st.sidebar.selectbox('Select Cost Category Insight :',
                                                 ['Distribution_of_damage_types_across_different_cost_categories',
                                                  'Relationship_between_cost_categories_and_car_models',
                                                  'Comparison_of_service_duration_across_different_cost_categories',
                                                  'Cost_category_breakdown_by_location',
                                                  'Trends_in_cost_categories_over_time'
                                                 ], key=12)
        class SwitchCCCase:
            def case_Distribution_of_damage_types_across_different_cost_categories(self):
                #### Distribution of damage types across different cost categories
                damageType_costCategory = df.groupby(['damage type','cost_category']).size().reset_index(name='Count').sort_values(by='Count')
                Maximum_row = damageType_costCategory.loc[damageType_costCategory['Count'].idxmax()]
                r11,r12,r13,r14 = st.columns(4)
                r11.metric('Maximum Damage Type',Maximum_row['damage type'])
                r12.metric('Cost Category',Maximum_row['cost_category'])
                r13.metric('Count',Maximum_row['Count'])
                myPlot1(damageType_costCategory,'damage type','Count','cost_category','bar','Distribution of damage types across different cost categories', sort_by=None, ascending=True)
                return 'Distribution_of_damage_types_across_different_cost_categories'
            def case_Relationship_between_cost_categories_and_car_models(self):
                #### Relationship between cost categories and car models
                car_costCategory = df.groupby(['car','cost_category']).size().reset_index(name='Count').sort_values(by=['car'])
                Maximum_row = car_costCategory.loc[car_costCategory['Count'].idxmax()]
                r11,r12,r13,r14 = st.columns(4)
                r11.metric('Car of Maximum Service Count',Maximum_row['car'])
                r12.metric('Cost Category',Maximum_row['cost_category'])
                r13.metric('Count',Maximum_row['Count'])
                myPlot1(car_costCategory,'car','Count','cost_category','bar','Relationship between cost categories and car models', sort_by=None, ascending=True)
                return 'Relationship_between_cost_categories_and_car_models'
            def case_Comparison_of_service_duration_across_different_cost_categories(self):
                #### Comparison of service duration across different cost categories
                Maximum_row = df.loc[df['service_duration'].idxmax()]
                r11,r12,r13,r14 = st.columns(4)
                r11.metric('Cost Category of Maximum Service Duration',Maximum_row['cost_category'])
                r12.metric('Maximum Service Duration',Maximum_row['service_duration'])
                myBoxPlot(data=df,x='cost_category',y='service_duration',color='cost_category',title='Comparison of service duration across different cost categories')
                return 'Comparison_of_service_duration_across_different_cost_categories'
            def case_Cost_category_breakdown_by_location(self):
                #### Cost category breakdown by location
                location_costCategory = df.groupby(['location','cost_category']).size().reset_index(name='Count').sort_values(by=['location'])
                Maximum_row = location_costCategory.loc[location_costCategory['Count'].idxmax()]
                r11,r12,r13,r14 = st.columns(4)
                r11.metric('Location of Maximum Service Count',Maximum_row['location'])
                r12.metric('Cost Category',Maximum_row['cost_category'])
                r13.metric('Count',Maximum_row['Count'])
                myPlot1(location_costCategory,'location','Count','cost_category','bar','Cost category breakdown by location', sort_by=None, ascending=True)
                return 'Cost_category_breakdown_by_location'
            def case_Trends_in_cost_categories_over_time(self):
                #### Trends in cost categories over time
                df['year_month'] = df['date ready'].dt.year.astype(str) + '_' + df['date ready'].dt.month.astype(str).str.zfill(2)
                date_costCategory = df.groupby(['year_month','cost_category']).size().reset_index(name='Frequency').sort_values(by='year_month')
                Maximum_row = date_costCategory.loc[date_costCategory['Frequency'].idxmax()]
                r11,r12,r13,r14 = st.columns(4)
                r11.metric('The year and month of Maximum cost category frequency',Maximum_row['year_month'])
                r12.metric('Cost Category',Maximum_row['cost_category'])
                r13.metric('Frequency',Maximum_row['Frequency'])
                
                myPlot1(date_costCategory,'year_month','Frequency','cost_category','line','Trends in cost categories over time', sort_by=None, ascending=True)
                return 'Trends_in_cost_categories_over_time'
            
            def default_case(self):
                return "Default class method executed"
            def CC_switch(self, value):
                method_name = f'case_{value}'
                method = getattr(self, method_name, self.default_case)
                return method()    
        # Usage
        CC_switcher = SwitchCCCase()
        CC_result = CC_switcher.CC_switch(selectCostCategoryInsight)
        st.write('Cost Category Insight: ',CC_result)

        return 'Cost_Category_Insights'
    ################################################################################################## Miscellaneous Insights
    def case_Miscellaneous_Insights(self):
        df = load_data('maintenance_cleaned_extended.xlsx')
        st.header('Miscellaneous Insights')
        selectMiscellaneousInsight = st.sidebar.selectbox('Select Miscellaneous Insight :',
                                                 ['Relationship_between_kilometers_driven_KMs_in_and_KMs_out_and_damage_types',
                                                  'Impact_of_corporate_on_cost',
                                                  'Impact_of_corporate_on_service_duration',
                                                  'Impact_of_delivery_method_on_cost',
                                                  'Impact_of_delivery_method_on_service_duration',
                                                  'Correlation_between_notes_and_high_cost_repairs'
                                                 ], key=13)
        class SwitchMSCase:
            def case_Relationship_between_kilometers_driven_KMs_in_and_KMs_out_and_damage_types(self):
                #### Relationship between kilometers driven (KMs in and KMs out) and damage types
                Maximum_row = df.loc[df['KMs Diff'].idxmax()]
                r11,r12,r13,r14 = st.columns(4)
                r11.metric('The Damage type that has maximum Kilometers difference is :',Maximum_row['damage type'])
                r12.metric('The maximum Kilometers difference is :',Maximum_row['KMs Diff'])
                myBoxPlot(data=df,x='damage type',y='KMs Diff',color='damage type',title='Relationship between kilometers driven (KMs in and KMs out) and damage types')
                return 'Relationship_between_kilometers_driven_KMs_in_and_KMs_out_and_damage_types'
            def case_Impact_of_corporate_on_cost(self):
                ##### Impact of corporate on cost
                corporate_cost = df.groupby(['corporate'])['cost'].sum().reset_index(name='CostSum').sort_values(by='CostSum')
                Maximum_row = corporate_cost.loc[corporate_cost['CostSum'].idxmax()]
                r11,r12,r13,r14 = st.columns(4)                
                r11.metric('The corporate that has maximum Total cost is :',Maximum_row['corporate'])
                r12.metric('The maximum total cost is :',Maximum_row['CostSum'])
                myPlot1(corporate_cost,'corporate','CostSum','corporate','bar','Impact of corporate on cost', sort_by=None, ascending=True)
                return 'Impact_of_corporate_on_cost'
            def case_Impact_of_corporate_on_service_duration(self):
                ##### Impact of corporate on service duration
                corporate_service_duration = df.groupby(['corporate'])['service_duration'].size().reset_index(name='Count').sort_values(by='Count')
                Maximum_row = corporate_service_duration.loc[corporate_service_duration['Count'].idxmax()]
                r11,r12,r13,r14 = st.columns(4)
                r11.metric('The corporate that has maximum service duration is :',Maximum_row['corporate'])
                r12.metric('The maximum service duration is :',Maximum_row['Count'])
                myPlot1(corporate_service_duration,'corporate','Count','corporate','bar','Impact of corporate on service duration', sort_by=None, ascending=True)
                return 'Impact_of_corporate_on_service_duration'
            def case_Impact_of_delivery_method_on_cost(self):
                ##### Impact of delivery method on cost
                delivered_by_cost = df.groupby(['delivered by'])['cost'].sum().reset_index(name='CostSum').sort_values(by='CostSum')
                Maximum_row = delivered_by_cost.loc[delivered_by_cost['CostSum'].idxmax()]
                r11,r12,r13,r14 = st.columns(4)                
                r11.metric('The delivery method that has maximum Total cost is :',Maximum_row['delivered by'])
                r12.metric('The maximum total cost is :',Maximum_row['CostSum'])
                myPlot1(delivered_by_cost,'delivered by','CostSum','delivered by','bar','Impact of delivery method on cost', sort_by=None, ascending=True)
                return 'Impact_of_delivery_method_on_cost'
            def case_Impact_of_delivery_method_on_service_duration(self):
                ##### Impact of delivery method on service duration
                delivered_by_service_duration = df.groupby(['delivered by'])['service_duration'].size().reset_index(name='Count').sort_values(by='Count')
                Maximum_row = delivered_by_service_duration.loc[delivered_by_service_duration['Count'].idxmax()]
                r11,r12,r13,r14 = st.columns(4)                
                r11.metric('The delivered method that has maximum service duration is :',Maximum_row['delivered by'])
                r12.metric('The maximum service duration is :',Maximum_row['Count'])
                myPlot1(delivered_by_service_duration,'delivered by','Count','delivered by','bar','Impact of delivered method on service duration', sort_by=None, ascending=True)
                return 'Impact_of_delivery_method_on_service_duration'
            def case_Correlation_between_notes_and_high_cost_repairs(self):
                #### Correlation between notes and high_cost repairs
                font_path = 'majalla.ttf'  # Ensure this is in the correct folder or provide a full path
                text = ' '.join(df['notes'].astype(str))
                reshaped_text = arabic_reshaper.reshape(text)
                bidi_text = get_display(reshaped_text)
                wordcloud = WordCloud(font_path=font_path, width=1000, height=800).generate(bidi_text)
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis('off')
                st.pyplot(plt)

                return 'Correlation_between_notes_and_high_cost_repairs'
            
            def default_case(self):
                return "Default class method executed"
            def MS_switch(self, value):
                method_name = f'case_{value}'
                method = getattr(self, method_name, self.default_case)
                return method()    
        # Usage
        MS_switcher = SwitchMSCase()
        MS_result = MS_switcher.MS_switch(selectMiscellaneousInsight)
        st.write('Miscellaneous Insight: ',MS_result)
        return 'Miscellaneous_Insights'

    ################################################################################################## Service Location Profitability Insights
    def case_Service_Location_Profitability_Insights(self):
        st.header('Service Location Profitability Insights')
        selectServiceLocationProfitabilityInsight = st.sidebar.selectbox('Se;ect Service Location Profitability Insight :',
                                                 ['Overview',
                                                  'Corporate_Client_Profitability',
                                                  'Corporate_Client_Profitability_across_Service_Locations',
                                                  'Corporate_Top_COUNT_Clients_Profitability',
                                                  'Top_Corporates_and_Their_Service_Locations_Income_Distribution',
                                                  'Top_5_Corporates_and_Their_Top_5_Service_Locations_Income_Distribution',
                                                  'Less_Profitable_Corporates_Not_in_Top_5',
                                                  'Less_Profitable_Service_Locations_for_Each_Top_5_Corporate',
                                                  'Top_Profitable_Service_Locations_for_Each_Top_5_Corporate'
                                                 ], key=15)

        class SwitchSLPCase:
            def case_Overview(self):
                df = load_data('maintenance_cleaned_extended.xlsx')
                r11,r12,r13,r14 = st.columns(4)
                r21,r22,r23,r24 = st.columns(4)
                r31,r32         = st.columns(2)
                r41,r42         = st.columns(2)
                r51             = st.columns(1)[0]
                r61             = st.columns(1)[0]
                r11.metric('Corporates Count',df['corporate'].nunique())
                r12.metric('Locations Count',df['location'].nunique())
                TotalIncomeGenerated = df['cost'].sum()
                TotalIncomeGeneratedFromTop5 = df.groupby('corporate')['cost'].sum().nlargest(5).sum()
                r21.metric('Total Income',TotalIncomeGenerated)
                r22.metric('Top 5 corporates Income',TotalIncomeGeneratedFromTop5)
                r23.metric('Percentage of',f"{TotalIncomeGeneratedFromTop5 / TotalIncomeGenerated:0.1%}")
                
                with r31:
                    Corporate_Client_Profitability()
                with r32:
                    Corporate_Client_Profitability_across_Service_Locations()
                with r41:
                    Top_5_Corporates_and_Their_Top_5_Service_Locations_Income_Distribution()
                with r42:
                    Less_Profitable_Corporates_Not_in_Top_5()
                with r51:
                    Top_Profitable_Service_Locations_for_Each_Top_5_Corporate()
                with r61:
                    te00 = 'RECOMANDATIONS'
                    te01 = '1. Top corporates should be taken care through special Unit'
                    te02 = '2. Top corporates should be receive promaotion in order to increase Income'
                    te03 = '3. Top locations employees who serve the top corporates should be rewarded'
                    te04 = '4. less profitable locations should be investegated for opreational cost, if exceeds its generated income, should be closed immediatly to minimize loss'
                    te05 = '5. less profitable locations with income more than operational cost should have some promotion to grap more customers in order to maximize income'
                    te06 = '6. less profitable corporates should be graped with discounts and promotions in order to maximize income'
                    
                    ta00 = 'التوصيات'
                    ta01 = '1. يجب العناية بالشركات الكبرى عبر وحدة خاصة'
                    ta02 = '2. يجب أن تتلقى الشركات الكبرى عروض للصيانة تجذبها للشركة بهدف تعظيم الأرباح'
                    ta03 = '3. موظفي الفروع الأعلى التي خدمت أعلى الشركات يجب أن يتم مكافأتهم'
                    ta04 = '4. يجب تقصي تكاليف تشغيل الفروع التي تزيد تكاليف تشغيلها عن دخلها، وهذه يجب اغلاقها فوراً من أجل وقف الخسارة'
                    ta05 = '5. الفروع التي تكاليف تشغيلها أقل من ايراداتها يجب أن تقدم عروض لتجذب المزيد من الزبائن بهدف تعظيم الأرباح'
                    ta06 = '6. الشركات التي نجني منها أرباح قليلة يجب التركيز عليها بالعروض من أجل جذبها بهدف تعظيم الأرباح'
                    if selectLang == 'English':
                        st.write(te00)
                        st.write(te01)
                        st.write(te02)
                        st.write(te03)
                        st.write(te04)
                        st.write(te05)
                        st.write(te06)
                    elif selectLang == 'العربية':
                        st.write(ta00)
                        st.write(ta01)
                        st.write(ta02)
                        st.write(ta03)
                        st.write(ta04)
                        st.write(ta05)
                        st.write(ta06)
                
                return 'Overview'
            def case_Corporate_Client_Profitability(self):
                Corporate_Client_Profitability()
                return 'Corporate_Client_Profitability'
            def case_Corporate_Client_Profitability_across_Service_Locations(self):
                Corporate_Client_Profitability_across_Service_Locations()
                return 'Corporate_Client_Profitability_across_Service_Locations'
            def case_Corporate_Top_COUNT_Clients_Profitability(self):
                Corporate_Top_COUNT_Clients_Profitability()
                return 'Corporate_Top_COUNT_Clients_Profitability'
            def case_Top_Corporates_and_Their_Service_Locations_Income_Distribution(self):
                Top_Corporates_and_Their_Service_Locations_Income_Distribution()
                return 'Top_Corporates_and_Their_Service_Locations_Income_Distribution'
            def case_Top_5_Corporates_and_Their_Top_5_Service_Locations_Income_Distribution(self):
                Top_5_Corporates_and_Their_Top_5_Service_Locations_Income_Distribution()
                return 'Top_5_Corporates_and_Their_Top_5_Service_Locations_Income_Distribution'
            def case_Less_Profitable_Corporates_Not_in_Top_5(self):
                Less_Profitable_Corporates_Not_in_Top_5()
                return 'Less_Profitable_Corporates_Not_in_Top_5'
            def case_Less_Profitable_Service_Locations_for_Each_Top_5_Corporate(self):
                Less_Profitable_Service_Locations_for_Each_Top_5_Corporate()
                return 'Less_Profitable_Service_Locations_for_Each_Top_5_Corporate'
            def case_Top_Profitable_Service_Locations_for_Each_Top_5_Corporate(self):
                Top_Profitable_Service_Locations_for_Each_Top_5_Corporate()
                return 'Top_Profitable_Service_Locations_for_Each_Top_5_Corporate'
            
            def default_case(self):
                return "Default class method executed"
            def SLP_switch(self, value):
                method_name = f'case_{value}'
                method = getattr(self, method_name, self.default_case)
                return method()    
        # Usage
        SLP_switcher = SwitchSLPCase()
        SLP_result = SLP_switcher.SLP_switch(selectServiceLocationProfitabilityInsight)
        st.write('Service Location Profitability Insight: ',SLP_result)
        return 'Service_Location_Profitability_Insight'



    # Needed to switch case
    def default_case(self):
        return "Default class method executed"
    def M_switch(self, value):
        method_name = f'case_{value}'
        method = getattr(self, method_name, self.default_case)
        return method()

# Usage
M_switcher = SwitchMCase()
M_result = M_switcher.M_switch(selectMB)
st.write('MAIN: ',M_result)

st.sidebar.write('')
st.sidebar.markdown('Made with :heart: by: [Suhail Sallam](https://www.youtube.com/@suhailsallam)')
