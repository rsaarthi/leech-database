from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
import pandas as pd
import sqlite3

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session handling

# Load your dataset (adjust the path as necessary)
df = pd.read_excel('leech_data_table.xlsx', engine='openpyxl')



# Initialize database connection
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Create a table for visitor count if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visitor_count (
            id INTEGER PRIMARY KEY,
            count INTEGER DEFAULT 0
        )
    ''')
    # Initialize with one row if empty
    cursor.execute('SELECT COUNT(*) FROM visitor_count')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO visitor_count (count) VALUES (0)')
        conn.commit()
    conn.close()

# Call this function at startup
init_db()




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
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Increment the visitor count by 1
    cursor.execute('UPDATE visitor_count SET count = count + 1 WHERE id = 1')
    conn.commit()
    # Fetch the updated count
    cursor.execute('SELECT count FROM visitor_count WHERE id = 1')
    visitor_count = cursor.fetchone()[0]
    conn.close()
    
    # Pass the visitor count to the template
    return render_template('home.html', visitor_count=visitor_count)

# Context processor to make visitor count available to all templates
@app.context_processor
def inject_visitor_count():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT count FROM visitor_count WHERE id = 1')
    visitor_count = cursor.fetchone()[0]
    conn.close()
    return dict(visitor_count=visitor_count)


# About page route
@app.route('/about')
def about():
    return render_template('about.html')  # Render the about.html page

# Route for the developers page
@app.route('/developers')
def developers():
    return render_template('developers.html')  # Render the developers.html page

# Gallery page route
@app.route('/gallery')
def gallery():
    return render_template('gallery.html')  # Render the gallery.html page

# Publications page route
@app.route('/publications')
def publications():
    return render_template('publications.html')  # Render the publications.html page

# Contact page route
@app.route('/contact')
def contact():
    return render_template('contact.html')  # Render the contact.html page

# Route to handle contact form submission
@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    
    # Process the form data (e.g., save to a database, send an email, etc.)
    # For now, we’ll just print the information (or log it)
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Message: {message}")
    
    # Show a success message (you can use Flask's flash for feedback)
    flash('Thank you for your message! We will get back to you shortly.', 'success')
    
    return redirect(url_for('contact'))  # Redirect to the contact page

# Resources page route
@app.route('/resources')
def resources():
    return render_template('resources.html')  # Render the resources.html page

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

    # Convert any hyperlinks to shortened clickable 'Download' links
    sorted_df = convert_hyperlinks_to_html(sorted_df)

    # Convert the sorted DataFrame to an HTML table
    sorted_df_html = sorted_df.to_html(classes='table table-striped table-hover table-bordered', index=False, escape=False)
    
    return render_template('browse.html', tables=sorted_df_html)  # Render the browse.html page

# Search page route
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_value = request.form['search_value'].strip().lower()

        # Initialize an empty DataFrame to store matching rows
        matching_rows = pd.DataFrame()

        # Iterate through each column and search for the value
        for column in df.columns:
            matching_rows = pd.concat([matching_rows, df[df[column].astype(str).str.lower().str.contains(search_value)]], ignore_index=True)

        # Drop duplicate rows that might occur
        matching_rows = matching_rows.drop_duplicates()

        # Convert any hyperlinks to shortened clickable 'Download' links
        matching_rows = convert_hyperlinks_to_html(matching_rows)

        # Convert the matching rows DataFrame to an HTML table
        if not matching_rows.empty:
            matching_rows_html = matching_rows.to_html(classes='table table-striped table-hover table-bordered', index=False, escape=False)
            matching_rows_html = matching_rows_html.replace('<td>', '<td class="sequence">')  # Add class for wrapping
        else:
            matching_rows_html = f"<p>No rows found for '{search_value}'.</p>"

        # Render the search results
        return render_template('search.html', tables=matching_rows_html)

    # If the request method is GET, render the search form
    return render_template('search.html')

# Run the Flask app
if __name__ == '__main__':
    
    app.run(debug=False, host='0.0.0.0')
