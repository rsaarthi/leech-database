from flask import Flask, render_template_string, request
import pandas as pd

app = Flask(__name__)

# Load your CSV file into a DataFrame
df = pd.read_csv('leech_data.csv')

# HTML template with Bootstrap styling for the home page
html_template_home = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Leech Protein Search</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            padding: 20px;
            background-color: #f8f9fa;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center">Leech Protein Search</h1>
        <form action="/search" method="post">
            <div class="mb-3">
                <input type="text" class="form-control" name="search_value" placeholder="Enter search term" required>
            </div>
            <button type="submit" class="btn btn-primary">Search</button>
        </form>
    </div>
    <!-- Bootstrap JS and dependencies -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# HTML template with Bootstrap styling for the results page
html_template_results = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search Results</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            padding: 20px;
            background-color: #f8f9fa;
        }
        .table-container {
            max-width: 100%;
            overflow-x: auto;
            margin-top: 20px;
        }
        .table {
            min-width: 600px;
        }
        .table th, .table td {
            text-align: center;
            vertical-align: middle;
        }
        /* Ensure text wrapping in the Sequence column */
        .table td.sequence {
            white-space: pre-wrap; /* Allows text to wrap */
            word-wrap: break-word; /* Breaks long words */
            max-width: 200px; /* Set a max-width to prevent columns from stretching too far */
            overflow-wrap: break-word; /* Ensures long words break */
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center">Search Results</h1>
        <div class="table-container">
            {{ tables|safe }}
        </div>
        <a href="/" class="btn btn-secondary mt-3">New Search</a>
    </div>
    <!-- Bootstrap JS and dependencies -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_template_home)

@app.route('/search', methods=['POST'])
def search():
    search_value = request.form['search_value'].strip().lower()

    # Initialize an empty DataFrame to store matching rows
    matching_rows = pd.DataFrame()

    # Iterate through each column and search for the value
    for column in df.columns:
        matching_rows = pd.concat([matching_rows, df[df[column].astype(str).str.lower().str.contains(search_value)]], 
                                  ignore_index=True)

    # Drop duplicate rows that might occur if the search value matches in multiple columns
    matching_rows = matching_rows.drop_duplicates()

    # Convert the result to HTML and add a class to the Sequence column
    if not matching_rows.empty:
        result_html = matching_rows.to_html(classes='table table-striped table-hover table-bordered', index=False)
        # Add class to each cell in the Sequence column
        result_html = result_html.replace('<td>', '<td class="sequence">')
    else:
        result_html = "<p>No rows found where any column contains '{}'.</p>".format(search_value)

    return render_template_string(html_template_results, tables=result_html)

if __name__ == '__main__':
    app.run(debug=True)
