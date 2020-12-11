import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("medical_examination.csv")

# Add 'overweight' column
df['overweight'] = (df["weight"] / ((df["height"] / 100) ** 2) > 25).astype(int)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholestorol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
replace_values = {"cholesterol":{1:0, 2:1, 3:1}, "gluc":{1:0, 2:1, 3:1}}
df.replace(replace_values, inplace=True)

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    features = ["active", "alco", "cholesterol", "gluc", "overweight", "smoke", "cardio"]
    df_cat = df[features]


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the collumns for the catplot to work correctly.
    df_cat = df_cat.melt(id_vars="cardio")

    # Draw the catplot with 'sns.catplot()'
    g = sns.catplot(data=df_cat, kind="count", x="variable", hue="value", col="cardio")
    g.set_axis_labels("variable", "total")

    fig = g.fig

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi'])
                 & (df['height'] >= df['height'].quantile(0.025))
                 & (df['height'] <= df['height'].quantile(0.975))
                 & (df['weight'] >= df['weight'].quantile(0.025))
                 & (df['weight'] <= df['weight'].quantile(0.975))]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))



    # Set up the matplotlib figure
    fig, ax = plt.subplots()

    # Draw the heatmap with 'sns.heatmap()'
    ax = sns.heatmap(df_heat.corr(),
            mask=mask,
            square=True,
            annot=True,
            fmt='.1f',
            linewidths=.2)


    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig

draw_cat_plot()
draw_heat_map()