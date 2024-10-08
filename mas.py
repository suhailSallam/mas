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


# Setting page layout ( This command should be after importing libraries )
st.set_page_config(page_title='Maintenance Analysis System',page_icon=None,
                   layout='wide',initial_sidebar_state='auto', menu_items=None)
# Sidebar for input selections
st.sidebar.title('Maintenance Analysis System')
selectMB = st.sidebar.selectbox('Select Analysis :', ['Story_telling',
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
                                                      'Miscellaneous_Insights'
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
        range(1,50,1):'1:50',
        range(50,100,1):'50:100',
        range(100,150,1):'100:150',
        range(150,200,1):'150:200',
        range(200,300,1):'200:300',
        range(300,400,1):'300:400',
        range(400,500,1):'400:500',
        range(500,600,1):'500:600',
        range(600,700,1):'600:700',
        range(700,800,1):'700:800',
        range(800,900,1):'800:900',
        range(900,1000,1):'900:1000',
        range(1000,1500,1):'1000:1500',
        range(1500,2000,1):'1500:2000',
        range(2000,3000,1):'2000:3000'
    }
    df['cost_category'] = df['cost'].replace(cost_dict)
    # Save DataSet post processing to new Excel file
    df.to_excel('maintenance_cleaned_extended.xlsx')

# Visualization Functions
## Bar, Scatter, Line charts
def myPlot(data,plotType,title):
    data = data.sort_values(ascending=True)
    xs = data.index.astype(str)  
    ys = data.values
    if plotType == 'bar':
        fig = px.bar(x = xs, y = ys,color=ys,title=title+' Analysis')
    elif plotType == 'scatter':
        fig = px.scatter(x = xs, y = ys,color=ys,title=title+' Analysis')
    elif plotType == 'line':
        fig = px.line(x = xs, y = ys,title=title+' Analysis')
    fig.update_layout(title_x=0.5)
    #fig.show()
    st.plotly_chart(fig,theme=None, use_container_width=True)

def myPlot1(data,xs,ys,clr,plotType,title, sort_by=None, ascending=True):
    if sort_by is not None:
        data_sorted = data.sort_values(by=sort_by, ascending=ascending)
    else:
        data_sorted = data
    xt=str(xs)
    yt=str(ys)
    xs = data_sorted[xs].astype(str)  
    ys = data_sorted[ys]              
    clr = data_sorted[clr].astype(str)
    if plotType == 'bar':
        fig = px.bar(x = xs, y = ys,color=clr,title=title+' Analysis')
    elif plotType == 'scatter':
        fig = px.scatter(x = xs, y = ys,color=clr,title=title+' Analysis')
    elif plotType == 'line':
        fig = px.line(x = xs, y = ys,color=clr,title=title+' Analysis')
    fig.update_layout(title_x=0.5)
    fig.update_layout(
        xaxis_title=xt,
        yaxis_title=yt
)
    #fig.show()
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

## Combine DataFrames
def combine(data,first_field,first_field_count,field_grouped_on,resulting_field_value):
    data_first_cat = data[first_field].value_counts().reset_index()
    data_first_cat.columns = [first_field,first_field_count]
    data_merged = data.groupby([first_field])[field_grouped_on].sum().reset_index(name=resulting_field_value)
    data_merged = data_merged.merge(data_first_cat,on=first_field)
    return first_field_count, resulting_field_value, data_merged

# Main switch case
class SwitchMCase:
    ################################################################################################## Stoty Telling
    def case_Story_telling(self):
        st.header('Story Telling')
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

        class SwitchFCase:
            def case_yearIn(self):
                column = 'yearIn'
                myPlot(df[column].value_counts(),'bar','Field: ' + column.capitalize())
                return 'yearIn'
            def case_monthIn(self):
                column = 'monthIn'
                myPlot(df[column].value_counts(),'bar','Field: ' + column.capitalize())
                return 'monthIn'
            def case_monthNIn(self):
                column = 'monthNIn'
                myPlot(df[column].value_counts(),'bar','Field: ' + column.capitalize())
                return 'monthNIn'
            def case_dayIn(self):
                column = 'dayIn'
                myPlot(df[column].value_counts(),'bar','Field: ' + column.capitalize())
                return 'dayIn'
            def case_dayNIn(self):
                column = 'dayNIn'
                myPlot(df[column].value_counts(),'bar','Field: ' + column.capitalize())
                return 'dayNIn'
            def case_service_duration(self):
                column = 'service_duration'
                myPlot(df[column].value_counts(),'bar','Field: ' + column.capitalize())
                return 'service_duration'
            def case_damage_type(self):
                column = 'damage type'
                myPlot(df[column].value_counts(),'bar','Field: ' + column.capitalize())
                return 'damage type'
            def case_car(self):
                column = 'car'
                myPlot(df[column].value_counts(),'bar','Field: ' + column.capitalize())
                return 'car'
            def case_KMs_IN(self):
                column = 'KMs IN'
                myPlot(df[column].value_counts(),'bar','Field: ' + column.capitalize())
                return 'KMs_IN'
            def case_KMs_out(self):
                column = 'KMs out'
                myPlot(df[column].value_counts(),'bar','Field: ' + column.capitalize())
                return 'KMs_out'
            def case_KMs_Diff(self):
                column = 'KMs Diff'
                myPlot(df[column].value_counts(),'bar','Field: ' + column.capitalize())
                return 'KMs_Diff'
            def case_Fuel_in(self):
                column = 'Fuel in'
                myPlot(df[column].value_counts(),'bar','Field: ' + column.capitalize())
                return 'Fuel_in'
            def case_Fuel_out(self):
                column = 'Fuel out'
                myPlot(df[column].value_counts(),'bar','Field: ' + column.capitalize())
                return 'Fuel_out'
            def case_Fuel_Diff(self):
                column = 'Fuel Diff'
                myPlot(df[column].value_counts(),'bar','Field: ' + column.capitalize())
                return 'Fuel Diff'
            def case_yearReady(self):
                column = 'yearReady'
                myPlot(df[column].value_counts(),'bar','Field: ' + column.capitalize())
                return 'yearReady'
            def case_monthReady(self):
                column = 'monthReady'
                myPlot(df[column].value_counts(),'bar','Field: ' + column.capitalize())
                return 'monthReady'
            def case_monthNReady(self):
                column = 'monthNReady'
                myPlot(df[column].value_counts(),'bar','Field: ' + column.capitalize())
                return 'monthNReady'
            def case_dayReady(self):
                column = 'dayReady'
                myPlot(df[column].value_counts(),'bar','Field: ' + column.capitalize())
                return 'dayReady'
            def case_dayNReady(self):
                column = 'dayNReady'
                myPlot(df[column].value_counts(),'bar','Field: ' + column.capitalize())
                return 'dayNReady'
            def case_cost_category(self):
                column = 'cost_category'
                myPlot(df[column].value_counts(),'bar','Field: ' + column.capitalize())
                return 'cost_category'
            def case_location(self):
                column = 'location'
                myPlot(df[column].value_counts(),'bar','Field: ' + column.capitalize())
                return 'location'
            def case_corporate(self):
                column = 'corporate'
                myPlot(df[column].value_counts(),'bar','Field: ' + column.capitalize())
                return 'corporate'
            def case_delivered_by(self):
                column = 'delivered by'
                myPlot(df[column].value_counts(),'bar','Field: ' + column.capitalize())
                return 'delivered_by'
            def case_returned_by(self):
                column = 'returned by'
                myPlot(df[column].value_counts(),'bar','Field: ' + column.capitalize())
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
                                                      'returned_by'
                                                      ], key=3)
        
        def uni(column):
            df_column = df.get(column).value_counts()
            myPlot(df_column,'bar',column.capitalize()+' Count ')
            myPie(df.groupby([column])['car'].count().sort_values(ascending=False).head(5),column.capitalize()+' Count')
        df = load_data('maintenance_cleaned_extended.xlsx')
        class SwitchFCase:
            def case_yearIn(self):
                column = 'yearIn'
                uni(column)
                return 'yearIn'
            def case_monthIn(self):
                column = 'monthIn'
                uni(column)
                return 'monthIn'
            def case_monthNIn(self):
                column = 'monthNIn'
                uni(column)
                return 'monthNIn'
            def case_dayIn(self):
                column = 'dayIn'
                uni(column)
                return 'dayIn'
            def case_dayNIn(self):
                column = 'dayNIn'
                uni(column)
                return 'dayNIn'
            def case_service_duration(self):
                column = 'service_duration'
                uni(column)
                return 'service_duration'
            def case_damage_type(self):
                column = 'damage type'
                uni(column)
                return 'damage type'
            def case_car(self):
                column = 'car'
                uni(column)
                return 'car'
            def case_KMs_IN(self):
                column = 'KMs IN'
                uni(column)
                return 'KMs_IN'
            def case_KMs_out(self):
                column = 'KMs out'
                uni(column)
                return 'KMs_out'
            def case_KMs_Diff(self):
                column = 'KMs Diff'
                uni(column)
                return 'KMs_Diff'
            def case_Fuel_in(self):
                column = 'Fuel in'
                uni(column)
                return 'Fuel_in'
            def case_Fuel_out(self):
                column = 'Fuel out'
                uni(column)
                return 'Fuel_out'
            def case_Fuel_Diff(self):
                column = 'Fuel Diff'
                uni(column)
                return 'Fuel Diff'
            def case_yearReady(self):
                column = 'yearReady'
                uni(column)
                return 'yearReady'
            def case_monthReady(self):
                column = 'monthReady'
                uni(column)
                return 'monthReady'
            def case_monthNReady(self):
                column = 'monthNReady'
                uni(column)
                return 'monthNReady'
            def case_dayReady(self):
                column = 'dayReady'
                uni(column)
                return 'dayReady'
            def case_dayNReady(self):
                column = 'dayNReady'
                uni(column)
                return 'dayNReady'
            def case_cost_category(self):
                column = 'cost_category'
                uni(column)
                return 'cost_category'
            def case_location(self):
                column = 'location'
                uni(column)
                return 'location'
            def case_corporate(self):
                column = 'corporate'
                uni(column)
                return 'corporate'
            def case_delivered_by(self):
                column = 'delivered by'
                uni(column)
                return 'delivered_by'
            def case_returned_by(self):
                column = 'returned by'
                uni(column)
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
        return 'Time_Based_Insights'
    ################################################################################################## Location Based Insights
    def case_Lcation_Based_Insights(self):
        return 'Lcation_Based_Insights'
    ################################################################################################## Kilometers Insights
    def case_Kilometers_Insights(self):
        return 'Kilometers_Insights'
    ################################################################################################## Cost Category Insights
    def case_Cost_Category_Insights(self):
        return 'Cost_Category_Insights'
    ################################################################################################## Miscellaneous Insights
    def case_Miscellaneous_Insights(self):
        return 'Miscellaneous_Insights'

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