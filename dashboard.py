import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px



def read_data():
    data_path = Path(__file__).parents[0] 
    df = pd.read_csv(data_path / "supahcoolsoft.csv", index_col=0)

    # Cleaning the dataframe
    tmp=pd.DataFrame()
    tmp=df[df['Position']=='AI Specialist']
    tmp=tmp[tmp['Salary_SEK'].isnull()==False]
    m=df.Salary_SEK.isnull()==True
    df.loc[m, ['Salary_SEK']]=tmp['Salary_SEK'].median().astype(float)

    #df[df['Salary_SEK'].isnull()==True].Salary_SEK
    df=df[df['Position'].isnull()==False]
    df=df[df['Department'].isnull()==False]

    #df=df.set_index('EmployeeID')
    return df

def layout():

    df = read_data()
    # to fix streamlits comma for thousands
    df_reset = df.reset_index(names=["EmployeeID"])  #.style.format({"year": lambda x: f"{x}"})


    st.title("Supahcoolsoft")

    st.write("This is a simple dashboard about Supahcoolsoft")

    st.header("Raw data")
    st.write("This shows the raw data")
    st.dataframe(df_reset)

    st.write(f"Number of employees {df_reset['EmployeeID'].count()}, average age is {format(df_reset['Age'].mean(),'.0f')} years and average salary {format(df['Salary_SEK'].mean(),'.0f')} SEK/month ")

    st.header("Trends per department")

    tmp2=pd.DataFrame()
    tmp2=df.groupby(by='Department')

    region = st.selectbox("Choose region", tmp2['Department'])

    region_stats = df[df['Department']==region]['Salary_SEK'].describe()
    cols = st.columns(4)
    stats = ["min", "50%", "max"]
    labels = ["min", "median", "max"]
    for col, stat, label in zip(cols, stats, labels):
        with col:
            st.metric(label=label, value=f"{region_stats[stat]:.0f}")


    df2=df[df['Department']==region].sort_values(by='Age')

    st.header("Employees per department")

    fig=px.bar(tmp2['Department'].count(),
               title=f"Employees per department",
        labels={"index":"Department", "value":"Number of Employees"},
        )

    
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig)

    st.header("Histogram salary")

    fig2=px.histogram(df['Salary_SEK'], nbins=12,
                      title=f"Employees salary - histogram",
                      labels={"count":"Number of employees", "value":"Salary"},
                      )

    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2)

    st.header("Boxplot salary by department")

    fig2=px.box(df, x='Department', y='Salary_SEK',
                      title=f"Employees salary per department",
                      labels={"index":"Department", "value":"Salary_SEK"},
                      )

    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2)

    st.header("Histogram salary")

    fig3=px.histogram(df['Age'], nbins=12,
                      title=f"Employees age - histogram",
                      labels={"count":"Number of employees", "value":"Age"},
                      )

    fig3.update_layout(showlegend=False)
    st.plotly_chart(fig3)

    st.header("Boxplot age by department")

    fig4=px.box(df, x='Department', y='Age',
                      title=f"Employees age per department",
                      labels={"index":"Department", "value":"Age"},
                      )

    fig4.update_layout(showlegend=False)
    st.plotly_chart(fig4)

    read_css()


def read_css():
    css_path = Path(__file__).parent / "style.css"

    with open(css_path) as css:
        st.markdown(
            f"<style>{css.read()}</style>",
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    # print(read_data())
    layout()

