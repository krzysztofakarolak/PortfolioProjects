# Project number 4

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('/workspace/boilerplate-page-view-time-series-visualizer/fcc-forum-pageviews.csv', index_col='date', parse_dates=['date'])

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025))&(df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig, ax=plt.subplots(figsize=(30,10))
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    sns.lineplot(data=df, legend=False, palette='husl')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar.reset_index(inplace=True)
    df_bar['Year'] = [d.year for d in df_bar.date]
    df_bar['Month'] = [d.month_name() for d in df_bar.date]
    missing_data = {
        "Year": [2016, 2016, 2016, 2016],
        "Month": ['January', 'February', 'March', 'April'],
        "value": [0, 0, 0, 0]}

    df_bar = pd.concat([pd.DataFrame(missing_data), df_bar]) # for 49 bars instead 45 or 57

    # Draw bar plot
    fig, ax=plt.subplots(figsize=(10,10))
    ax.set_title('Average Daily Page Views, Grouped by Year and Month')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    sns.barplot(x='Year', y='value', data=df_bar, hue='Month',
                    hue_order=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September','October', 'November', 'December'],
                    palette='colorblind', errorbar=None, legend=False)
    plt.legend(labels=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September','October', 'November', 'December'],title='Months')
    # adding legend outside the barplot takes 12 bars out of plot (so you have 45 or 49)
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(18, 6))

    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0], hue='year',palette="husl", legend=False)
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    sns.boxplot(x='month', y='value', data=df_box, order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ax=axes[1], hue='month',palette="husl", legend=False)
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig


# errors=10 all with numpy ==> in requirements.txt update seaborn package to seaborn==0.13.2, run .gitpod.yml, and those errors disappear