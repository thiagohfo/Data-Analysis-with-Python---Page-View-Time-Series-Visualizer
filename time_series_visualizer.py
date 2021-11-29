import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=True, index_col='date')

# Clean data
df = df.drop(df[(df['value'] <= df['value'].quantile(0.025)) | (df['value'] >= df['value'].quantile(0.975))].index)

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots()
    df.plot(figsize=(18,10), color='red', ax=ax, legend=False)
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['Months'] = pd.DatetimeIndex(df_bar.index).month_name()
    df_bar['Years'] = pd.DatetimeIndex(df_bar.index).year
    df_bar = pd.DataFrame({'total' : df_bar.groupby(['Years', 'Months'])['value'].mean()}).reset_index().groupby(['Years', 'Months'])['total'].aggregate('first').unstack()
    #df_bar = pd.pivot_table(df_bar, values="total", index="Years",columns="Months")
    df_bar = df_bar[["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]]

    # Draw bar plot
    ax = df_bar.plot(kind="bar")
    fig = ax.get_figure()
    fig.set_size_inches(8, 7)
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    df_box['month'] = pd.Categorical(df_box['month'], ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    df_box.sort_values(by=['month'], inplace=True)
    
    #print(df_box.head(50))
    
    # Draw box plots (using Seaborn)
    fig, axs = plt.subplots(1,2, figsize=(16,8))
    sns.boxplot(x='year', y='value', data=df_box, ax=axs[0])
    axs[0].set_title('Year-wise Box Plot (Trend)')
    axs[0].set_xlabel('Year')
    axs[0].set_ylabel('Page Views')

    sns.boxplot(x='month', y='value', data=df_box, ax=axs[1])
    axs[1].set_title('Month-wise Box Plot (Seasonality)')
    axs[1].set_xlabel('Month')
    axs[1].set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
    