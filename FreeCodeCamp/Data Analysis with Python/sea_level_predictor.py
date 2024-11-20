# Project number 5

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    # Read data from file
    df=pd.read_csv('/workspace/boilerplate-sea-level-predictor/epa-sea-level.csv')

    # Create scatter plot
    x=df['Year']
    y=df['CSIRO Adjusted Sea Level']

    fig, ax=plt.subplots()
    ax=plt.scatter(x,y)

    # Create first line of best fit
    # Use the linregress function from scipy.stats to get the slope and y-intercept of the line of best fit.
    reg=linregress(x,y)
    #Make the line go through the year 2050 to predict the sea level rise in 2050.
    x1=pd.Series([i for i in range(1880, 2051)])
    y1=reg.slope*x1+reg.intercept
    plt.plot(x1,y1,'green')

    # Create second line of best fit
    df2=df[df['Year']>=2000]
    x2=df2['Year']
    y2=df2['CSIRO Adjusted Sea Level']
    reg2=linregress(x2,y2)

    x3=pd.Series([i for i in range(2000, 2051)])
    y3=reg2.slope*x3+reg2.intercept
    plt.plot(x3,y3,'r')

    # Add labels and title
    #The x label should be Year, the y label should be Sea Level (inches), and the title should be Rise in Sea Level.
    plt.title('Rise in Sea Level')
    plt.xlabel('Year')
    plt.ylabel('Sea Level (inches)')

    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()