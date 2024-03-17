import plotly.graph_objs as go
import pandas as pd
from dash import dcc
from .git_statistics import extract_git_stats


def display_commit_graph(repo_path):
    stats = extract_git_stats(repo_path)
    if "error" in stats:
        return dcc.Graph()

    df = pd.DataFrame({
        "Commit Date": pd.to_datetime([commit for commit in stats['commit_dates']], utc=True),
        "Commit Count": 1
    })
    df['Commit Date'] = df['Commit Date'].dt.tz_convert(None)  # Remove o fuso horário
    df['Commit Date'] = df['Commit Date'].dt.date  # Converte para apenas a data

    df_group = df.groupby('Commit Date').count().reset_index()

    fig = go.Figure(data=[
        go.Scatter(x=df_group['Commit Date'], y=df_group['Commit Count'], mode='lines+markers')
    ])
    fig.update_layout(title='Commits Over Time', xaxis_title='Date', yaxis_title='Number of Commits')

    return dcc.Graph(figure=fig)
