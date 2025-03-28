import click
import pandas as pd
from datetime import datetime

@click.command()
@click.option('--file', required=True, type=click.Path(exists=True), help='Path to LinkedIn CSV file')
def analyze(file):
    """Analyze LinkedIn profile data from a CSV file."""
    # Load CSV into a pandas DataFrame, skipping the first 3 rows
    try:
        df = pd.read_csv(file, skiprows=3)
    except Exception as e:
        click.echo(f"Error reading CSV: {e}")
        return

    # Expected columns based on LinkedIn export
    expected_cols = ['First Name', 'Last Name', 'URL', 'Email Address', 'Company', 'Position', 'Connected On']
    missing_cols = [col for col in expected_cols if col not in df.columns]
    if missing_cols:
        click.echo(f"Warning: Missing columns in CSV: {missing_cols}")

    # Basic analysis
    total_connections = len(df)
    unique_companies = df['Company'].nunique() if 'Company' in df else 0
    top_companies = df['Company'].value_counts().head(5) if 'Company' in df else "N/A"

    # Connection time analysis
    if 'Connected On' in df:
        df['Connected On'] = pd.to_datetime(df['Connected On'], errors='coerce')
        connections_by_year = df['Connected On'].dt.year.value_counts().sort_index()
    else:
        connections_by_year = "N/A"

    # Output results
    click.echo(f"Total Connections: {total_connections}")
    click.echo(f"Unique Companies: {unique_companies}")
    click.echo("Top 5 Companies:")
    click.echo(top_companies.to_string() if top_companies != "N/A" else "N/A")
    click.echo("Connections by Year:")
    click.echo(connections_by_year.to_string() if connections_by_year != "N/A" else "N/A")
