from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the Excel file using openpyxl engine
df = pd.read_excel('leech_data_table.xlsx', engine='openpyxl')

# Function to convert URLs to clickable 'Download' links
def convert_hyperlinks_to_html(df):
    # Assuming any cell that contains 'http' should be a hyperlink
    for col in df.columns:
        if df[col].dtype == 'O':  # Process only object (string) columns
            df[col] = df[col].apply(lambda x: f'<a href="{x}" target="_blank">Download</a>' if isinstance(x, str) and 'http' in x else x)
    return df

@app.route('/', methods=['GET', 'POST'])
def browse():
    if request.method == 'POST':
        search_value = request.form.get('search_value')
        search_type = request.form.get('search_type')
        
        if not search_value or not search_type:
            return render_template('browse.html', error="Please provide both search value and search type.")

        if search_type == 'species':
            matching_rows = df[df['Species name'].str.contains(search_value, case=False, na=False)]
        elif search_type == 'protein':
            matching_rows = df[df['Protein name'].str.contains(search_value, case=False, na=False)]
        else:
            matching_rows = pd.DataFrame()

        matching_rows = matching_rows.drop_duplicates()

        return render_template('browse_results.html', tables=[matching_rows.to_html(classes='data')], titles=matching_rows.columns.values)
    
    return render_template('browse.html')

if __name__ == '__main__':
    app.run(debug=True)
