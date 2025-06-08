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
        # Drop rows where 'Connected On' could not be parsed
        df.dropna(subset=['Connected On'], inplace=True)
        if not df.empty:
            connections_by_year = df['Connected On'].dt.year.value_counts().sort_index()

            # YoY Growth Calculation
            yearly_growth_rates = {}
            sorted_years = sorted(connections_by_year.index)

            for i, year in enumerate(sorted_years):
                current_year_connections = connections_by_year[year]
                if i == 0:
                    yearly_growth_rates[year] = "N/A (First Year)"
                else:
                    prev_year = sorted_years[i-1]
                    prev_year_connections = connections_by_year[prev_year]
                    if prev_year_connections == 0:
                        if current_year_connections > 0:
                            yearly_growth_rates[year] = "Infinite (New Connections)"
                        else:
                            yearly_growth_rates[year] = "N/A (No Change)"
                    else:
                        growth = ((current_year_connections - prev_year_connections) / prev_year_connections) * 100
                        yearly_growth_rates[year] = f"{growth:.2f}%"
            yearly_growth_rates_series = pd.Series(yearly_growth_rates)
        else:
            connections_by_year = "No valid connection dates found."
            yearly_growth_rates_series = "Connection date data not available for growth analysis."

    else:
        connections_by_year = "N/A"
        yearly_growth_rates_series = "Connection date data not available for growth analysis."

    # Position analysis
    top_n_titles = "N/A"
    seniority_distribution = "N/A"

    if 'Position' in df:
        # Normalize and extract job titles
        df['Job Title'] = df['Position'].str.lower().fillna('unknown')

        # Count job title frequency
        top_n_titles = df['Job Title'].value_counts().head(10)

        # Seniority level detection
        seniority_keywords = {
            'Intern': ["intern", "internship"],
            'Junior': ["junior", "jr."],
            'Mid-level': [], # Default if no other keywords found
            'Senior': ["senior", "sr.", "staff"],
            'Lead': ["lead", "team lead"],
            'Manager': ["manager", "mgr"],
            'Director': ["director", "dir"],
            'Executive': ["vp", "vice president", "cto", "ceo", "chief"]
        }

        def detect_seniority(title):
            title_lower = str(title).lower()
            for level, keywords in seniority_keywords.items():
                if any(keyword in title_lower for keyword in keywords):
                    return level
            return 'Mid-level' # Default if no keywords match

        df['Seniority Level'] = df['Job Title'].apply(detect_seniority)
        seniority_distribution = df['Seniority Level'].value_counts()

    # Output results
    click.echo(f"Total Connections: {total_connections}")
    click.echo(f"Unique Companies: {unique_companies}")
    click.echo("Top 5 Companies:")
    click.echo(top_companies.to_string() if isinstance(top_companies, pd.Series) else "N/A")
    click.echo("Connections by Year:")
    click.echo(connections_by_year.to_string() if isinstance(connections_by_year, pd.Series) else connections_by_year)
    click.echo("\nYear-over-Year Connection Growth (%):")
    click.echo(yearly_growth_rates_series.to_string() if isinstance(yearly_growth_rates_series, pd.Series) else yearly_growth_rates_series)

    click.echo("\nTop 10 Job Titles:")
    click.echo(top_n_titles.to_string() if isinstance(top_n_titles, pd.Series) else "N/A")
    click.echo("\nSeniority Level Distribution:")
    click.echo(seniority_distribution.to_string() if isinstance(seniority_distribution, pd.Series) else "N/A")
