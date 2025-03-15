import click
import pandas as pd
from datetime import datetime

@click.command()
@click.option('--file', required=True, type=click.Path(exists=True), help='Path to LinkedIn CSV file')
def analyze(file):
    """Analyze LinkedIn profile data from a CSV file."""
    # Load CSV into a pandas DataFrame
    try:
        df = pd.read_csv(file)
    except Exception as e:
        click.echo(f"Error reading CSV: {e}")
        return

    # Expected columns
    expected_cols = ['first_name', 'last_name', 'li_url', 'email', 'company_name', 'position', 'connection_time']
    missing_cols = [col for col in expected_cols if col not in df.columns]
    if missing_cols:
        click.echo(f"Warning: Missing columns in CSV: {missing_cols}")

    # Basic analysis
    total_connections = len(df)
    unique_companies = df['company_name'].nunique() if 'company_name' in df else 0
    top_companies = df['company_name'].value_counts().head(5) if 'company_name' in df else "N/A"

    # Connection time analysis
    if 'connection_time' in df:
        df['connection_time'] = pd.to_datetime(df['connection_time'], errors='coerce')
        connections_by_year = df['connection_time'].dt.year.value_counts().sort_index()
    else:
        connections_by_year = "N/A"

    # Output results
    click.echo(f"Total Connections: {total_connections}")
    click.echo(f"Unique Companies: {unique_companies}")
    click.echo("Top 5 Companies:")
    click.echo(top_companies.to_string() if top_companies != "N/A" else "N/A")
    click.echo("Connections by Year:")
    click.echo(connections_by_year.to_string() if connections_by_year != "N/A" else "N/A")
