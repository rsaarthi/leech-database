from flask import Flask, render_template, request, session
import os
import pandas as pd

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session handling

# Load your dataset (adjust the path as necessary)
df = pd.read_excel('leech_data_table.xlsx', engine='openpyxl')

# Function to convert URLs to clickable 'Download' links
def convert_hyperlinks_to_html(df):
    # Assuming any cell that contains 'http' should be a hyperlink
    for col in df.columns:
        if df[col].dtype == 'O':  # Process only object (string) columns
            df[col] = df[col].apply(lambda x: f'<a href="{x}" target="_blank">Download</a>' if isinstance(x, str) and 'http' in x else x)
    return df

# Home page route
@app.route('/')
def home():
    return render_template('home.html')  # Render the home.html page

# About page route
@app.route('/about')
def about():
    return render_template('about.html')  # Render the about.html page

# Route for the developers page
@app.route('/developers')
def developers():
    return render_template('developers.html')  # Render the developers.html page


# Browse page route (browse by species or protein, with sorting options)
@app.route('/browse', methods=['GET', 'POST'])
def browse():
    browse_type = request.form.get('browse_type', 'species')  # Default to species
    reverse = request.form.get('reverse') == 'true'  # Check if reverse sorting is requested

    if browse_type == 'protein':
        # Sort the DataFrame by Protein name
        sorted_df = df.sort_values(by='Protein name', ascending=not reverse)
    else:
        # Sort the DataFrame by Species name (default)
        sorted_df = df.sort_values(by='Species name', ascending=not reverse)

    # Convert the sorted DataFrame to HTML table
    sorted_df_html = sorted_df.to_html(classes='table table-striped table-hover table-bordered', index=False, escape=False)
    
    return render_template('browse.html', tables=sorted_df_html)  # Render the browse.html page


# Search page route
@app.route('/search', methods=['POST'])
def search():
    search_value = request.form['search_value'].strip().lower()  # Get the search term from the form
    
    # Initialize an empty DataFrame to store matching rows
    matching_rows = pd.DataFrame()

    # Iterate through each column and search for the value
    for column in df.columns:
        matching_rows = pd.concat([matching_rows, df[df[column].astype(str).str.lower().str.contains(search_value)]], ignore_index=True)

    # Drop duplicate rows that might occur if the search value matches in multiple columns
    matching_rows = matching_rows.drop_duplicates()

    # Convert any hyperlinks to clickable 'Download' links
    matching_rows = convert_hyperlinks_to_html(matching_rows)

    # Convert the matching rows DataFrame to an HTML table
    if not matching_rows.empty:
        matching_rows_html = matching_rows.to_html(classes='table table-striped table-hover table-bordered', index=False, escape=False)
        matching_rows_html = matching_rows_html.replace('<td>', '<td class="sequence">')  # Add class to each cell for wrapping
    else:
        matching_rows_html = f"<p>No rows found where any column contains '{search_value}'.</p>"

    # Pass the HTML table to the search.html template for rendering
    return render_template('search.html', tables=matching_rows_html)

# Visitor hit counter route
@app.route('/hit-counter')
def hit_counter():
    # Track unique visitors using session
    if 'visited' not in session:
        session['visited'] = True
        with open('counter.txt', 'r+') as f:
            count = int(f.read())
            count += 1
            f.seek(0)
            f.write(str(count))
    
    # Read the current count
    with open('counter.txt', 'r') as f:
        visitor_count = f.read()
    
    return visitor_count  # Return the visitor count as plain text

# Run the Flask app
if __name__ == '__main__':
    # Initialize hit counter if not present
    if not os.path.exists('counter.txt'):
        with open('counter.txt', 'w') as f:
            f.write('0')
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
