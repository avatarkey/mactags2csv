import pandas as pd
import plotly.express as px
from datetime import datetime

# Load the CSV file
csv_file = "tagged_files.csv"
df = pd.read_csv(csv_file)

# Convert 'Date Created' to datetime
df['Date Created'] = pd.to_datetime(df['Date Created'])

# Group by 'Tag' and 'Date Created', then count the number of files
df_grouped = df.groupby(['Tag', 'Date Created']).size().reset_index(name='File Count')

# Sort by 'Date Created' to ensure the line graph is plotted correctly
df_grouped = df_grouped.sort_values(by='Date Created')

# Create a cumulative sum of file counts for each tag over time
df_grouped['Cumulative File Count'] = df_grouped.groupby('Tag')['File Count'].cumsum()

# Calculate the total accumulated number of files for each tag
total_files_per_tag = df_grouped.groupby('Tag')['Cumulative File Count'].max().reset_index()

# Sort tags by the total accumulated number of files (descending order)
sorted_tags = total_files_per_tag.sort_values(by='Cumulative File Count', ascending=False)['Tag'].tolist()

# Reorder the DataFrame based on the sorted tags
df_grouped['Tag'] = pd.Categorical(df_grouped['Tag'], categories=sorted_tags, ordered=True)
df_grouped = df_grouped.sort_values(['Tag', 'Date Created'])

# Create the line graph using Plotly
fig = px.line(
    df_grouped,
    x='Date Created',
    y='Cumulative File Count',
    color='Tag',
    title='File Growth Over Time by Tag (Sorted by Accumulated Files)',
    labels={
        'Date Created': 'Time',
        'Cumulative File Count': 'Number of Files',
        'Tag': 'Tag'
    }
)

# Customize the layout
fig.update_layout(
    xaxis_title='Time',
    yaxis_title='Number of Files',
    legend_title='Tag',
    hovermode='x unified'
)

# Export the graph as an interactive HTML file
fig.write_html("file_growth_graph.html")

# Show the graph
fig.show()