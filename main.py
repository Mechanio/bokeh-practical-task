###NO FILTERS IMPLEMENTED
###NO FILTERS IMPLEMENTED
###NO FILTERS IMPLEMENTED
import pandas as pd
from bokeh.plotting import figure, show, output_file, save
from bokeh.models import ColumnDataSource, FactorRange, HoverTool
from bokeh.transform import factor_cmap
from bokeh.layouts import column


df = pd.read_csv("Titanic-Dataset.csv")


# 1. Data Preparation
def data_prep():
    df.fillna(value={'Cabin': 'Unknown', 'Embarked': 'Unknown'}, inplace=True)  # Fill missing values
    # df = df[df['Age'] > 0]
    # or
    df['Age'].interpolate(inplace=True)
    df['AgeGroup'] = df['Age'].apply(lambda x: 'Child' if x < 18 else ('Young Adult' if x < 30 else ('Adult' if x < 60 else 'Senior')))
    survival_rate = df.groupby('AgeGroup')['Survived'].mean() * 100
    df['SurvivalRate'] = df['AgeGroup'].map(survival_rate)


# 2. Visualization
def age_group_survival(dataframe):
    survival_rates = dataframe.groupby('AgeGroup')['SurvivalRate'].mean().to_dict()
    source_age_group = ColumnDataSource(data=dict(age_groups=list(survival_rates.keys()), survival_rates=list(survival_rates.values())))

    p = figure(x_range=list(survival_rates.keys()), height=350, title="Age Group Survival",
               toolbar_location=None, tools="", x_axis_label="Age Group", y_axis_label="Survival Rate (%)")

    p.vbar(x='age_groups', top='survival_rates', source=source_age_group, width=0.9)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    hover = HoverTool(tooltips=[("Age Group", "@age_groups"), ("Survival Rate (%)", "@survival_rates")])
    p.add_tools(hover)
    return p


def class_and_gender(dataframe):
    class_gender_survival = dataframe.groupby(['Pclass', 'Sex'])['Survived'].mean() * 100
    class_gender_survival = class_gender_survival.unstack()
    classes = ['1st', '2nd', '3rd']
    genders = list(class_gender_survival.columns)
    data = {'classes': classes}
    for gender in genders:
        data[gender] = list(class_gender_survival[gender])
    x = [(pclass, gender) for pclass in classes for gender in genders]
    counts = sum(zip(data['female'], data['male']), ())
    source_class_gender = ColumnDataSource(data=dict(x=x, counts=counts))

    p = figure(x_range=FactorRange(*x), height=350, title="Survival Rates by Class and Gender", toolbar_location=None,
               tools="", x_axis_label="Class and Gender", y_axis_label="Survival Rate (%)")

    p.vbar(x='x', top='counts', width=0.8, source=source_class_gender,
            fill_color=factor_cmap('x', palette=['#e84d60', '#718dbf'], factors=genders, start=1, end=2))
    hover = HoverTool(tooltips=[("Class and Gender", "@x"), ("Survival Rate (%)", "@counts")])
    p.add_tools(hover)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.xaxis.major_label_orientation = 1
    return p


def fare_survival(dataframe):
    class_colors = {1: 'blue', 2: 'green', 3: 'red'}
    df['color'] = dataframe['Pclass'].map(class_colors)
    source_fare = ColumnDataSource(data=dict(Fare=dataframe['Fare'], Survived=dataframe['Survived'], color=dataframe['color']))

    p = figure(height=350, title="Fare vs. Survival",
                toolbar_location=None, tools="", x_axis_label="Fare", y_axis_label="Survived")
    p.circle(x='Fare', y='Survived', size=8, color='color', fill_alpha=0.6, source=source_fare)
    hover = HoverTool(tooltips=[("Fare", "@Fare"), ("Survived", "@Survived"), ("Class", "@color")])
    p.add_tools(hover)
    return p


data_prep(df)
p1 = age_group_survival(df)
p2 = class_and_gender(df)
p3 = fare_survival(df)

layout = column(p1, p2, p3)
show(layout)
output_file("result.html")
save(layout)