"""Helper Functions for Plotting"""
import numpy as np

import plotly
import plotly.offline as pyoff
import plotly.figure_factory as ff
from plotly.offline import init_notebook_mode, iplot, plot
import plotly.graph_objs as go
init_notebook_mode(connected = True)

def generate_layout_bar(col_name):
    """
    Generate a layout object for bar chart
    """
    layout_bar = go.Layout(
        autosize=False,  # auto size the graph? use False if you are specifying the height and width
        width=800,  # height of the figure in pixels
        height=600,  # height of the figure in pixels
        title="Distribution of {} column".format(col_name),  # title of the figure
        # more granular control on the title font
        titlefont=dict(
            family='Courier New, monospace',  # font family
            size=14,  # size of the font
            color='black'  # color of the font
        ),
        # granular control on the axes objects
        xaxis=dict(
            tickfont=dict(
                family='Courier New, monospace',  # font family
                size=14,  # size of ticks displayed on the x axis
                color='black'  # color of the font
            )
        ),
        yaxis=dict(
            #         range=[0,100],
            title='Percentage',
            titlefont=dict(
                size=14,
                color='black'
            ),
            tickfont=dict(
                family='Courier New, monospace',  # font family
                size=14,  # size of ticks displayed on the y axis
                color='black'  # color of the font
            )
        ),
        font=dict(
            family='Courier New, monospace',  # font family
            color="white",  # color of the font
            size=12  # size of the font displayed on the bar
        )
    )
    return layout_bar


def plot_count_bar(dataframe_name, col_name, top_n=None):
    """
    Plot a bar chart for the categorical columns

    Arguments:
    dataframe name
    categorical column name

    Output:
    Plot
    """
    # create a table with value counts
    temp = dataframe_name[col_name].value_counts()
    if top_n is not None:
        temp = temp.head(top_n)
    # creating a Bar chart object of plotly
    data = [go.Bar(
            x=temp.index.astype(str),  # x axis values
            y=np.round(temp.values.astype(float) / temp.values.sum(), 4) * 100,  # y axis values
            text=['{}%'.format(i) for i in np.round(temp.values.astype(float) / temp.values.sum(), 4) * 100],
            # text to be displayed on the bar, we are doing this to display the '%' symbol along with the number on the bar
            textposition='auto',  # specify at which position on the bar the text should appear
            marker=dict(color='#0047AB'),)]  # change color of the bar
    # color used here Cobalt Blue
    layout_bar = generate_layout_bar(col_name=col_name)
    fig = go.Figure(data=data, layout=layout_bar)
    return iplot(fig)

def plot_bar(dataframe_name, cat_col_name, num_col_name, top_n = 20):
    """
    Plot a bar chart with the mentioned columns

    Arguments:
    dataframe name
    categorical column name
    numeric column name
    Output:
    Plot
    """
    # create a table with value counts
    dataframe_name = dataframe_name.sort_values(by = num_col_name, ascending = False)
    dataframe_name = dataframe_name.head(top_n)
    x = dataframe_name[cat_col_name]
    y = dataframe_name[num_col_name]
    # creating a Bar chart object of plotly
    data = [go.Bar(
            x=x,  # x axis values
            y=y,  # y axis values
            text=['{}%'.format(np.round(i,2)) for i in y],
            # text to be displayed on the bar, we are doing this to display the '%' symbol along with the number on the bar
            textposition='auto',  # specify at which position on the bar the text should appear
            marker=dict(color='#0047AB'),)]  # change color of the bar
    # color used here Cobalt Blue
    layout_bar = generate_layout_bar(col_name=cat_col_name)
    fig = go.Figure(data=data, layout=layout_bar)
    return iplot(fig)


def plot_hist(dataframe, col_name):
    """Plot histogram"""
    data = [go.Histogram(x=dataframe[col_name],
                         marker=dict(
        color='#CC0E1D',  # Lava (#CC0E1D)
        #         color = 'rgb(200,0,0)'   # you can provide color in HEX format or rgb format, genrally programmers prefer HEX format as it is a single string value and easy to pass as a variable
    ))]
    layout = go.Layout(title="Histogram of {}".format(col_name))
    fig = go.Figure(data=data, layout=layout)
    return iplot(fig)


def plot_multi_box(dataframe, col_name, num_col_name):
    """Plot multiple box plots based on the levels in a column"""
    data = []
    for i in dataframe[col_name].unique():
        trace = go.Box(y=dataframe[num_col_name][dataframe[col_name] == i],
                       name=i)
        data.append(trace)
    layout = go.Layout(title="Boxplot of levels in {} for {} column".format(col_name, num_col_name))
    fig = go.Figure(data=data, layout=layout)
    return (iplot(fig))

def plot_grouped_bar(dataframe,index_col, col1, col2):
    """Plot multiple box plots based on the levels in a column"""
    x = dataframe[index_col]
    y1 = dataframe[col1]
    y2 = dataframe[col2]
    text_y1 = np.round(y1, 2)
    text_y2 = np.round(y2, 2)
    data=[
        go.Bar(name='raw', x=x, y=y1, text = text_y1, textposition='auto'),
        go.Bar(name='shadow removed', x=x, y=y2, text = text_y2, textposition='auto'),
    ]
    fig = go.Figure(data)
    fig.update_layout(barmode='group', title = "Grouped bar chart for {} and {} columns, compared on {}".format(col1, col2,index_col))

    return (iplot(fig))