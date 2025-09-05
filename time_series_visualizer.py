import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
np.float = float
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
from matplotlib.ticker import StrMethodFormatter
register_matplotlib_converters()


current_dir = os.path.dirname(os.path.abspath(__file__))

# Import data
df = pd.read_csv( "fcc-forum-pageviews.csv")

# Clean data
quantile = df['value'].quantile(0.025)
mask = df["value"] > quantile
df = df[mask]
df['date'] = pd.to_datetime(df['date'], errors='coerce')


def draw_line_plot():
    fig, ax = plt.subplots(figsize=(15,5))
    ax.plot(df['date'], df['value'], color='red', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.ticklabel_format(style='plain', axis='y')

    # Salva no mesmo diretório do script
    fig.savefig( 'line_plot.png')
    return fig


def draw_bar_plot():
    df_bar = df.copy()
    df_bar['year'] = df_bar['date'].dt.year
    df_bar['month'] = df_bar['date'].dt.strftime('%B')  
    df_bar['month_num'] = df_bar['date'].dt.month       

    # Agrupa por ano e mês, calcula média diária
    df_grouped = df_bar.groupby(['year','month','month_num'])['value'].mean().reset_index()

    # Pivot: anos no eixo X, meses como barras
    df_pivot = df_grouped.pivot(index='year', columns='month', values='value')

    # Ordena os meses
    month_order = ['January','February','March','April','May','June',
                   'July','August','September','October','November','December']
    df_pivot = df_pivot[month_order]

    # Plot
    fig = df_pivot.plot(kind='bar', figsize=(12,8)).get_figure()
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.title("Average Daily Page Views per Month")
    plt.legend(title="Months")

    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    fig.savefig(os.path.join(current_dir, 'bar_plot.png'))

    return fig


def draw_box_plot():
    df_box = df.copy()
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')
    df_box['month_num'] = df_box['date'].dt.month
    df_box = df_box.sort_values('month_num')

    fig, axes = plt.subplots(1, 2, figsize=(15,5))
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # salva no diretório atual
    fig.savefig('box_plot.png')  
    return fig