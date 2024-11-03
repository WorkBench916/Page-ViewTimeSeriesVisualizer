import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col = [0], parse_dates = [0])

# Clean data
notTop2Percent = df['value'] < df['value'].quantile(0.975)

notBot2Percent = df['value'] > df['value'].quantile(0.025)

df = df[
    (notTop2Percent) &
    (notBot2Percent)
]


def draw_line_plot():
    # Draw line plot
    fig, axes = plt.subplots(figsize=(30,10))

    plt.plot(df.index, df['value'], color = 'red')

    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')




    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.strftime('%B')
    color_code = {
    'May': 'purple',
    'June': 'brown',
    'July': 'pink',
    'August': 'gray',
    'September': 'yellow',
    'October': 'cyan',
    'November': 'blue',
    'December': 'orange',
    'January': 'blue',
    'February': 'orange',
    'March': 'green',
    'April': 'red'
    }

    colors = df_bar['month'].map(color_code)

    df_pivot = df_bar.pivot_table(index='year', columns='month', values='value')
    month_order = [
    'January', 'February', 'March', 'April', 'May', 'June', 
    'July', 'August', 'September', 'October', 'November', 'December'
    ]
    df_pivot.columns = pd.Categorical(df_pivot.columns, categories=month_order, ordered=True)
    df_pivot = df_pivot.sort_index(axis=1)  # Sort columns based on the specified order

    years = df_pivot.index
    months = df_pivot.columns
    bar_width = 0.8 / len(months)

    # Draw bar plot
    fig, axes = plt.subplots(figsize=(10,10))

    for i, month in enumerate(months):
        plt.bar(
            x = years + i * bar_width,
            height = df_pivot[month],
            width = bar_width,
            color = colors.get(month),
            label=month
        )

    plt.xticks(years + bar_width * len(months) - 1 / 2.25, years) #center year labels
    plt.ylabel('Average Page Views')
    plt.xlabel('Years')
    plt.legend(title= 'Months', loc='upper left', fontsize = 'large')




    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box['date']]
    df_box['month'] = [d.strftime('%b') for d in df_box['date']]
    
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Convert 'month' to categorical with the specified order
    df_box['month'] = pd.Categorical(df_box['month'], categories=month_order, ordered=True)
    df_box.sort_values('month')

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(25,10))
    sns.boxplot(x = df_box['year'], y = df_box['value'], data = df_box, hue = df_box['year'], palette = 'tab10', legend = False, fliersize = 1, ax = axes[0])
    axes[0].set_ylabel('Page Views')
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    sns.boxplot(x = df_box['month'], y = df_box['value'], data = df_box, hue = df_box['month'], palette = sns.color_palette('husl',12), fliersize = 1, ax = axes[1])
    axes[1].set_ylabel('Page Views')
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')




    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
