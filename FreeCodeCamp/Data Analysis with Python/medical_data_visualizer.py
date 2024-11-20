# Project number 3

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1 Import the data from medical_examination.csv and assign it to the df variable
df = pd.read_csv('/workspace/boilerplate-medical-data-visualizer/medical_examination.csv')

# 2 Create the overweight column in the df variable
df['overweight'] = (df['weight']/((df['height']/100)**2)>25).astype(int)

# 3 Normalize data by making 0 always good and 1 always bad. If the value of cholesterol or gluc is 1, set the value to 0. If the value is more than 1, set the value to 1.
df['cholesterol']=(df['cholesterol']>1).astype(int)
df['gluc']=(df['gluc']>1).astype(int)

# 4 Draw the Categorical Plot in the draw_cat_plot function
def draw_cat_plot():
    # 5 Create a DataFrame for the cat plot using pd.melt with values from cholesterol, gluc, smoke, alco, active, and overweight in the     df_cat variable.
    df_cat = df_cat=pd.melt(df, id_vars=['cardio'], value_vars=['cholesterol','gluc','smoke','alco','active','overweight'] )

    # 6 Group and reformat the data in df_cat to split it by cardio. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index()
    df_cat=df_cat.rename(columns={0:'total'})

    # 7 Convert the data into long format and create a chart that shows the value counts of the categorical features using the following method provided by the seaborn library import : sns.catplot()
    # 8 Get the figure for the output and store it in the fig variable
    fig = sns.catplot(data=df_cat,kind="bar", x="variable", y="total", hue="value", col="cardio").fig

    # 9 Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig

# 10 Draw the Heat Map in the draw_heat_map function
def draw_heat_map():
    # 11 Clean the data. Filter out the following patient segments that represent incorrect data
    df_heat = df[(df['ap_lo'] <= df['ap_hi'])&
                (df['height'] >= df['height'].quantile(0.025)) &
                (df['height'] <= df['height'].quantile(0.975)) &
                (df['weight'] >= df['weight'].quantile(0.025)) &
                (df['weight'] <= df['weight'].quantile(0.975))]

    # 12 Calculate the correlation matrix and store it in the corr variable
    corr =df_heat.corr()

    # 13 Generate a mask for the upper triangle and store it in the mask variable
    mask = np.triu(corr)

    # 14 Set up the matplotlib figure
    fig, ax = plt.subplots()

    # 15 Plot the correlation matrix using the method provided by the seaborn library import: sns.heatmap()
    sns.heatmap(data=corr,mask=mask, annot=True, square=True,fmt=".1f", linewidths=1, center=0.08, cbar_kws={'shrink':0.5})

    # 16 Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
