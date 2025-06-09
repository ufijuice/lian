import pytest
import pandas as pd
from click.testing import CliRunner
import os
import sys

# Add the directory containing li_analyzer.py to the Python path
# This is to ensure that the li_analyzer module can be imported
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from li_analyzer import analyze

# Helper function to create dummy CSV files (already created them manually)
# For tests, we'll assume these files (sample_data_*.csv) are in the same directory or use tmp_path

def test_position_analysis(tmp_path):
    """Test the position analysis feature."""
    runner = CliRunner()
    # Use the pre-created sample_data_positions.csv
    # For a more isolated test, we'd create this file content here or use tmp_path to write it
    # For now, assuming it's accessible. If not, will adjust.

    # Create the sample_data_positions.csv in tmp_path for this test
    # Add 3 dummy lines to account for skiprows=3 in li_analyzer.py
    content_positions = """Dummy line 1
Dummy line 2
Dummy line 3
First Name,Last Name,URL,Email Address,Company,Position,Connected On
John,Doe,linkedin.com/johndoe,john.doe@email.com,Tech Solutions Inc.,Software Engineer,01/15/2022
Jane,Smith,linkedin.com/janesmith,jane.smith@email.com,Innovate Corp,software engineer,03/20/2021
Alex,Johnson,linkedin.com/alexj,alex.j@email.com,Data Insights LLC,Data Scientist,07/10/2023
Emily,White,linkedin.com/emilyw,emily.w@email.com,Web Creators Co.,Sr. Software Engineer,11/05/2020
Michael,Brown,linkedin.com/michaelb,mb@email.com,Marketing Masters,Junior Marketing Specialist,02/28/2023
Sarah,Davis,linkedin.com/sarahd,sarah.d@email.com,HealthFirst Org,Medical Intern,06/15/2022
David,Wilson,linkedin.com/davidw,david.w@email.com,Finance Group,Senior Manager,09/01/2019
Laura,Garcia,linkedin.com/laurag,laura.g@email.com,AI Future Inc.,Lead AI Researcher,04/22/2021
Chris,Lee,linkedin.com/chrisl,chris.l@email.com,BuildIt Construction,Project Manager,08/12/2020
Olivia,Martinez,linkedin.com/oliviam,olivia.m@email.com,Global Logistics,VP of Operations,01/30/2018
Robert,Anderson,linkedin.com/roberta,robert.a@email.com,SecureNet Systems,Chief Technology Officer,05/18/2017
Linda,Thomas,linkedin.com/lindat,linda.t@email.com,EducateWell,Curriculum Director,10/25/2019
James,Jackson,linkedin.com/jamesj,james.j@email.com,Innovate Corp,,12/01/2022
Sophia,Harris,linkedin.com/sophiah,sophia.h@email.com,Tech Solutions Inc.,Software Development Intern,07/01/2023
William,Clark,linkedin.com/williamc,william.c@email.com,Data Insights LLC,Senior Data Analyst,03/10/2020
"""
    sample_file = tmp_path / "sample_data_positions.csv"
    sample_file.write_text(content_positions)

    result = runner.invoke(analyze, ['--file', str(sample_file)])

    assert result.exit_code == 0
    output = result.output

    # Expected top job titles (normalized to lowercase)
    # software engineer: 2
    # data scientist: 1
    # sr. software engineer: 1
    # junior marketing specialist: 1
    # medical intern: 1
    # senior manager: 1
    # lead ai researcher: 1
    # project manager: 1
    # vp of operations: 1
    # chief technology officer: 1
    # (unknown for the empty one which becomes 'unknown' title and then 'Mid-level' seniority)

    assert "Top 10 Job Titles:" in output
    # Check for job titles and their counts, allowing for variable spacing
    assert any("software engineer" in line and "2" in line for line in output.splitlines())
    assert any("data scientist" in line and "1" in line for line in output.splitlines())
    assert any("sr. software engineer" in line and "1" in line for line in output.splitlines())
    assert any("junior marketing specialist" in line and "1" in line for line in output.splitlines())
    assert any("medical intern" in line and "1" in line for line in output.splitlines())
    assert any("senior manager" in line and "1" in line for line in output.splitlines())
    assert any("lead ai researcher" in line and "1" in line for line in output.splitlines())
    assert any("project manager" in line and "1" in line for line in output.splitlines())
    assert any("vp of operations" in line and "1" in line for line in output.splitlines())
    # The 10th could be one of several with count 1, e.g. chief technology officer, curriculum director, etc.
    # The 'unknown' title (from an empty Position) also has a count of 1, so its inclusion in top 10 is not guaranteed.
    # What's important is that it's handled in seniority (defaults to Mid-level).
    # So, we won't assert its presence in the Top 10 Job Titles list explicitly.


    # Expected counts based on corrected manual walkthrough:
    # Mid-level: 4
    # Senior: 3
    # Intern: 2
    # Executive: 2
    # Junior: 1
    # Lead: 1
    # Manager: 1 (Project Manager)
    # Director: 1

    assert "Seniority Level Distribution:" in output
    assert any("Mid-level" in line and "4" in line for line in output.splitlines())
    assert any("Senior" in line and "3" in line for line in output.splitlines())
    assert any("Intern" in line and "2" in line for line in output.splitlines())
    assert any("Executive" in line and "2" in line for line in output.splitlines())
    assert any("Junior" in line and "1" in line for line in output.splitlines())
    assert any("Lead" in line and "1" in line for line in output.splitlines())
    assert any("Manager" in line and "1" in line for line in output.splitlines())
    assert any("Director" in line and "1" in line for line in output.splitlines())

    # Test with missing 'Position' column
    content_missing_pos = """Dummy line 1
Dummy line 2
Dummy line 3
First Name,Last Name,URL,Email Address,Company,Connected On
Arthur,Dent,linkedin.com/arthurd,arthur.d@email.com,Earth Inc.,01/01/2020
"""
    sample_missing_pos_file = tmp_path / "sample_data_missing_pos.csv"
    sample_missing_pos_file.write_text(content_missing_pos)

    result_missing_pos = runner.invoke(analyze, ['--file', str(sample_missing_pos_file)])
    assert result_missing_pos.exit_code == 0
    output_missing_pos = result_missing_pos.output

    assert "Warning: Missing columns in CSV: ['Position']" in output_missing_pos
    assert "Top 10 Job Titles:" in output_missing_pos
    assert "N/A" in output_missing_pos # Should be N/A for titles
    assert "Seniority Level Distribution:" in output_missing_pos
    assert "N/A" in output_missing_pos # Should be N/A for seniority

# test_connection_growth and other tests will be added in subsequent steps.
# For now, just a placeholder.
def test_connection_growth(tmp_path):
    """Test the connection growth analysis feature."""
    runner = CliRunner()

    # --- Test Case 1: sample_data_growth.csv ---
    content_growth = """Dummy line 1
Dummy line 2
Dummy line 3
First Name,Last Name,URL,Email Address,Company,Position,Connected On
Paul,Atreides,linkedin.com/paula,paul.a@email.com,Arrakis Corp,CEO,01/10/2020
Duncan,Idaho,linkedin.com/duncani,duncan.i@email.com,Arrakis Corp,Swordmaster,02/15/2020
Gurney,Halleck,linkedin.com/gurneyh,gurney.h@email.com,Arrakis Corp,Troubadour,03/20/2021
Jessica,Atreides,linkedin.com/jessicaa,jessica.a@email.com,Arrakis Corp,Bene Gesserit,04/25/2021
Liet,Kynes,linkedin.com/lietk,liet.k@email.com,Arrakis Corp,Planetologist,05/30/2021
Stilgar,Ben Fifrawi,linkedin.com/stilgars,stilgar.s@email.com,Sietch Tabr,Naib,01/05/2022
Chani,Sihaya,linkedin.com/chanis,chani.s@email.com,Sietch Tabr,Sayyadina,02/10/2022
Vladimir,Harkonnen,linkedin.com/vladh,vlad.h@email.com,Harkonnen Corp,Baron,NotADate
Piter,De Vries,linkedin.com/piterv,piter.v@email.com,Harkonnen Corp,Mentat,04/15/2023
Feyd,Rautha,linkedin.com/feydr,feyd.r@email.com,Harkonnen Corp,Heir,05/20/2023
Rabban,Harkonnen,linkedin.com/rabbanh,rabban.h@email.com,Harkonnen Corp,Enforcer,INVALID_DATE_FORMAT
Leto,Atreides II,linkedin.com/letoaii,leto.aii@email.com,Arrakis Corp,God Emperor,07/01/2023
Irulan,Corrino,linkedin.com/irulanc,irulan.c@email.com,Corrino Corp,Historian,
Alia,Atreides,linkedin.com/aliaa,alia.a@email.com,Arrakis Corp,Abomination,12/31/2021
"""
    sample_file_growth = tmp_path / "sample_data_growth.csv"
    sample_file_growth.write_text(content_growth)

    result_growth = runner.invoke(analyze, ['--file', str(sample_file_growth)])
    assert result_growth.exit_code == 0
    output_growth = result_growth.output

    # Expected Connections by Year:
    # 2020: 2
    # 2021: 4 (3 from list + Alia)
    # 2022: 2
    # 2023: 3
    # Invalid dates: Vladimir, Rabban, Irulan (empty) are dropped.

    assert "Connections by Year:" in output_growth
    assert any("2020" in line and "2" in line for line in output_growth.splitlines())
    assert any("2021" in line and "4" in line for line in output_growth.splitlines())
    assert any("2022" in line and "2" in line for line in output_growth.splitlines())
    assert any("2023" in line and "3" in line for line in output_growth.splitlines())

    # Expected YoY Growth:
    # 2020: N/A (First Year)
    # 2021: ((4 - 2) / 2) * 100 = 100.00%
    # 2022: ((2 - 4) / 4) * 100 = -50.00%
    # 2023: ((3 - 2) / 2) * 100 = 50.00%

    assert "Year-over-Year Connection Growth (%):" in output_growth
    assert any("2020" in line and "N/A (First Year)" in line for line in output_growth.splitlines())
    assert any("2021" in line and "100.00%" in line for line in output_growth.splitlines())
    assert any("2022" in line and "-50.00%" in line for line in output_growth.splitlines())
    assert any("2023" in line and "50.00%" in line for line in output_growth.splitlines())

    # --- Test Case 2: sample_data_missing_cols.csv (missing 'Connected On') ---
    # This file is missing 'Position' and 'Connected On'
    content_missing_cols = """Dummy line 1
Dummy line 2
Dummy line 3
First Name,Last Name,URL,Email Address,Company
Arthur,Dent,linkedin.com/arthurd,arthur.d@email.com,Earth Inc.
"""
    sample_file_missing_cols = tmp_path / "sample_data_missing_cols.csv"
    sample_file_missing_cols.write_text(content_missing_cols)

    result_missing_cols = runner.invoke(analyze, ['--file', str(sample_file_missing_cols)])
    assert result_missing_cols.exit_code == 0
    output_missing_cols = result_missing_cols.output

    assert "Warning: Missing columns in CSV: ['Position', 'Connected On']" in output_missing_cols # Adjusted for both
    assert "Connections by Year:" in output_missing_cols
    assert "N/A" in output_missing_cols # Should be N/A for connections by year
    assert "Year-over-Year Connection Growth (%):" in output_missing_cols
    assert "Connection date data not available for growth analysis" in output_missing_cols

    # --- Test Case 3: sample_data_no_valid_dates.csv ---
    content_no_valid_dates = """Dummy line 1
Dummy line 2
Dummy line 3
First Name,Last Name,URL,Email Address,Company,Position,Connected On
Neo,Anderson,linkedin.com/neo,neo@email.com,Metacortex,The One,Invalid Date
Trinity,Unknown,linkedin.com/trinity,trinity@email.com,Nebuchadnezzar,Operator,Not A Date
Morpheus,Unknown,linkedin.com/morpheus,morpheus@email.com,Nebuchadnezzar,Captain,12345
"""
    sample_file_no_valid_dates = tmp_path / "sample_data_no_valid_dates.csv"
    sample_file_no_valid_dates.write_text(content_no_valid_dates)

    result_no_valid_dates = runner.invoke(analyze, ['--file', str(sample_file_no_valid_dates)])
    assert result_no_valid_dates.exit_code == 0
    output_no_valid_dates = result_no_valid_dates.output

    assert "Connections by Year:" in output_no_valid_dates
    assert "No valid connection dates found." in output_no_valid_dates
    assert "Year-over-Year Connection Growth (%):" in output_no_valid_dates
    assert "Connection date data not available for growth analysis" in output_no_valid_dates


def test_empty_csv(tmp_path):
    """Test handling of an empty CSV file (only headers, or headers + 3 skipped lines then headers)."""
    runner = CliRunner()

    # Case 1: CSV with only headers after skipping initial lines
    content_header_only = """Dummy line 1
Dummy line 2
Dummy line 3
First Name,Last Name,URL,Email Address,Company,Position,Connected On
"""
    sample_file_header_only = tmp_path / "sample_data_header_only.csv"
    sample_file_header_only.write_text(content_header_only)

    result_header_only = runner.invoke(analyze, ['--file', str(sample_file_header_only)])
    assert result_header_only.exit_code == 0
    output_header_only = result_header_only.output

    assert "Total Connections: 0" in output_header_only
    assert "Unique Companies: 0" in output_header_only
    assert "Top 5 Companies:" in output_header_only
    assert "Series([], )" in output_header_only # For Top 5 companies list (empty series)
    assert "Connections by Year:" in output_header_only
    # The message for empty/no valid dates is "No valid connection dates found."
    assert "No valid connection dates found." in output_header_only # This is correct
    assert "Year-over-Year Connection Growth (%):" in output_header_only
    assert "Connection date data not available for growth analysis" in output_header_only # This is correct
    assert "Top 10 Job Titles:" in output_header_only
    assert "Series([], )" in output_header_only # For Top 10 job titles list (empty series)
    assert "Seniority Level Distribution:" in output_header_only
    assert "Series([], )" in output_header_only # For Seniority distribution list (empty series)

    # Case 2: Truly empty CSV (or what amounts to it after skiprows)
    # If the file has less than 4 lines, pd.read_csv might raise an EmptyDataError BEFORE li_analyzer.py even gets to print much.
    # The current try-except in li_analyzer.py for pd.read_csv is generic.
    # Let's test a file that becomes empty after skiprows.
    content_effectively_empty = """Dummy line 1
Dummy line 2
Dummy line 3
""" # No header line after dummy lines
    sample_file_eff_empty = tmp_path / "sample_data_eff_empty.csv"
    sample_file_eff_empty.write_text(content_effectively_empty)
    result_eff_empty = runner.invoke(analyze, ['--file', str(sample_file_eff_empty)])
    # This should be caught by the "Error reading CSV: EmptyDataError" or similar from pandas.
    # The current error message in li_analyzer is "Error reading CSV: {e}"
    assert result_eff_empty.exit_code == 0 # The script itself doesn't exit with error due to try/except
    assert "Error reading CSV:" in result_eff_empty.output # Check for generic error message
    # It's tricky to assert the exact pandas error message as it might vary.
    # The key is that our script handles it by printing an error and exiting gracefully.


def test_file_not_found():
    """Test file not found error handling."""
    # Use CliRunner(mix_stderr=False) to capture stderr separately
    runner = CliRunner(mix_stderr=False)
    # Intentionally provide a non-existent file path
    result = runner.invoke(analyze, ['--file', 'non_existent_file.csv'])

    # click.Path(exists=True) should handle this.
    # It typically exits with code 2 and prints an error message to stderr.
    assert result.exit_code != 0 # Should be non-zero for an error
    # The exact error message can vary based on Click's version and OS.
    # Checking for "Error: Invalid value for '--file': Path 'non_existent_file.csv' does not exist."
    # This is a common format for Click's error messages.
    assert "Error: Invalid value for '--file'" in result.stderr
    assert "non_existent_file.csv' does not exist" in result.stderr


def test_missing_cols_overall(tmp_path):
    """Test handling of a CSV missing multiple key columns ('Position', 'Connected On')."""
    runner = CliRunner()
    content_missing_all_key_cols = """Dummy line 1
Dummy line 2
Dummy line 3
First Name,Last Name,URL,Email Address,Company
Arthur,Dent,linkedin.com/arthurd,arthur.d@email.com,Earth Inc.
Ford,Prefect,linkedin.com/fordp,ford.p@email.com,Betelgeuse Corp.
"""
    sample_file = tmp_path / "sample_data_missing_all_key_cols.csv"
    sample_file.write_text(content_missing_all_key_cols)

    result = runner.invoke(analyze, ['--file', str(sample_file)])
    assert result.exit_code == 0
    output = result.output

    assert "Warning: Missing columns in CSV: ['Position', 'Connected On']" in output

    assert "Connections by Year:" in output
    assert "N/A" in output # For Connections by Year

    assert "Year-over-Year Connection Growth (%):" in output
    assert "Connection date data not available for growth analysis" in output

    assert "Top 10 Job Titles:" in output
    assert "N/A" in output # For Top 10 Job Titles

    assert "Seniority Level Distribution:" in output
    assert "N/A" in output # For Seniority Level Distribution


def test_no_valid_dates(tmp_path):
    """Test handling of CSV with 'Connected On' column present but no valid/parseable dates."""
    runner = CliRunner()
    content_no_valid_dates = """Dummy line 1
Dummy line 2
Dummy line 3
First Name,Last Name,URL,Email Address,Company,Position,Connected On
Neo,Anderson,linkedin.com/neo,neo@email.com,Metacortex,The One,Invalid Date
Trinity,Unknown,linkedin.com/trinity,trinity@email.com,Nebuchadnezzar,Operator,Not A Date
Morpheus,Unknown,linkedin.com/morpheus,morpheus@email.com,Nebuchadnezzar,Captain,12345
"""
    sample_file_no_valid_dates = tmp_path / "sample_data_no_valid_dates.csv"
    sample_file_no_valid_dates.write_text(content_no_valid_dates)

    result_no_valid_dates = runner.invoke(analyze, ['--file', str(sample_file_no_valid_dates)])
    assert result_no_valid_dates.exit_code == 0
    output_no_valid_dates = result_no_valid_dates.output

    # Check that Position analysis is still attempted (and likely 'N/A' or empty due to minimal data)
    # but the main focus is on date handling.
    assert "Top 10 Job Titles:" in output_no_valid_dates
    assert "Seniority Level Distribution:" in output_no_valid_dates

    assert "Connections by Year:" in output_no_valid_dates
    assert "No valid connection dates found." in output_no_valid_dates
    assert "Year-over-Year Connection Growth (%):" in output_no_valid_dates
    assert "Connection date data not available for growth analysis" in output_no_valid_dates
