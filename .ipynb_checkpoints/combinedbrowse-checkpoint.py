from flask import Flask, render_template_string, request
import pandas as pd

app = Flask(__name__)

# Load the Excel file using openpyxl engine
df = pd.read_excel('leech_data_table.xlsx', engine='openpyxl')

# Function to convert URLs to clickable 'Download' links
def convert_hyperlinks_to_html(df):
    for col in df.columns:
        if df[col].dtype == 'O':  # Process only object (string) columns
            df[col] = df[col].apply(lambda x: f'<a href="{x}" target="_blank">Download</a>' if isinstance(x, str) and 'http' in x else x)
    return df



@app.route('/', methods=['GET', 'POST'])
def browse():
    sort_by = request.args.get('sort_by', 'Species name')  # Default sort by 'Species name'

    # Sort the DataFrame based on the specified column
    if sort_by not in df.columns:
        sort_by = 'Species name'  # Fallback to default column if invalid
    sorted_df = df.sort_values(by=sort_by)

    if request.method == 'POST':
        search_value = request.form.get('search_value')
        search_type = request.form.get('search_type')
        
        # Validate input
        if not search_value or not search_type:
            return render_template('search.html', error="Please provide both search value and search type.")

        # Search by the specified type
        if search_type == 'species':
            matching_rows = sorted_df[sorted_df['Species name'].str.contains(search_value, case=False, na=False)]
        elif search_type == 'protein':
            matching_rows = sorted_df[sorted_df['Protein name'].str.contains(search_value, case=False, na=False)]
        else:
            matching_rows = pd.DataFrame()

    # Drop duplicate rows that might occur if the search value matches in multiple columns
    matching_rows = matching_rows.drop_duplicates()

    # Convert any hyperlinks to clickable 'Download' links
    matching_rows = convert_hyperlinks_to_html(matching_rows)

    # Convert the result to HTML and ensure escape=False to allow rendering of hyperlinks
    if not matching_rows.empty:
        result_html = matching_rows.to_html(classes='table table-striped table-hover table-bordered', index=False, escape=False)
        result_html = result_html.replace('<td>', '<td class="sequence">')  # Add class to each cell for wrapping
    else:
        result_html = f"<p>No rows found where any column contains '{search_value}'.</p>"

    return render_template_string(html_template_results, tables=result_html)

if __name__ == '__main__':
    app.run(debug=True)
