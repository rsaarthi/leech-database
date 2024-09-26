from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load your DataFrame (Adjust the path to your Excel file as needed)
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

        return render_template('search_results.html', tables=[matching_rows.to_html(classes='data')], titles=matching_rows.columns.values)
    
    # Render the sorted data initially
    return render_template('search.html', tables=[sorted_df.to_html(classes='data')], titles=sorted_df.columns.values)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template_string, request
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

# HTML template with Bootstrap for the home page
html_template_home = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Leech Protein Search</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            padding: 20px;
            background-color: #f8f9fa;
        }
    </style>
<style>
/* Background image with 30% opacity */
body {
  background-image: url('');
  background-size: cover;
  background-repeat: no-repeat;
  background-attachment: fixed;
}

.overlay {
  background-color: rgba(255, 255, 255, 0.7);
  padding: 20px;
}
</style>



<title>The Leech Database (Ldb)</title>
<meta name="keywords" content="Leech, Protein, Species, Hirulin, Hirudin, Lefaxin">
<meta name="description" content="The Leech Database">
<meta name="author" content="Aarthi, Anbarasu, Raghavi">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Lato">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

<link href="./default.css" rel="stylesheet" type="text/css" media="screen">

<!-- Header -->
<header class="w3-display-container w3-content w3-wide" style="max-width:1500px;" id="home">
  <img class="w3-image" src="" alt="Medicinal leech" width="1500" height="800" style="opacity:0.3;">
<!--  <div class="w3-display-middle w3-margin-top w3-center">  →
    <h1 class="w3-xxlarge w3-text-white"><span class="w3-padding w3-black w3-opacity-min"></span> <span class="w3-hide-small w3-text-light-grey">The Leech Database</span></h1>
  </div>
</header>

</head>
</head>




<body>


<div class="overlay">
  <!-- Navbar (sit on top) -->
  <div class="w3-top">
    <div class="w3-bar w3-white w3-wide w3-padding w3-card">
      <a href="#home" class="w3-bar-item w3-button">The Leech Database <b>Ldb</b></a>
    </div>
  </div>

  <!-- start header -->
  <div id="header"></div>
  <div class="w3-center w3-hide-small">
    <a href="G:/My Drive/The Leech database/pages/homepage.htm" class="w3-bar-item w3-button">Home</a>
    <a href="G:/My Drive/The Leech database/pages/about.htm" class="w3-bar-item w3-button">About</a>
    <div class="w3-dropdown-hover w3-hide-small">
      <button class="w3-padding-large w3-button" title="Browse">Browse <i class="fa fa-caret-down"></i></button>     
      <div class="w3-dropdown-content w3-bar-block w3-card-4">
        <a href="G:/My Drive/The Leech database/pages/browse.htm" class="w3-bar-item w3-button">Index</a>
        <a href="G:/My Drive/The Leech database/pages/browse.htm" class="w3-bar-item w3-button">Protein wise</a>
        <a href="G:/My Drive/The Leech database/pages/browse.htm" class="w3-bar-item w3-button">Species wise</a>
      </div>
    </div>
    <a href="G:/My Drive/The Leech database/pages/search.htm" class="w3-bar-item w3-button">Search</a>
    <a href="G:/My Drive/The Leech database/pages/gallery.htm" class="w3-bar-item w3-button">Gallery</a>
    <a href="G:/My Drive/The Leech database/pages/developers.htm" class="w3-bar-item w3-button">Contact</a>
  </div>

  
    <div class="container">
        <h1 class="text-center">Leech Protein Search</h1>
        <form action="/search" method="post">
            <div class="mb-3">
                <input type="text" class="form-control" name="search_value" placeholder="Enter search term" required>
            </div>
            <button type="submit" class="btn btn-primary">Search</button>
        </form>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# HTML template with Bootstrap for the results page
html_template_results = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search Results</title>
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
            white-space: pre-wrap;
            word-wrap: break-word;
            max-width: 200px;
            overflow-wrap: break-word;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center">Search Results</h1>
        <div class="table-container">
            {{ tables|safe }}  <!-- Ensures that the table with <a> tags is rendered as HTML -->
        </div>
        <a href="/" class="btn btn-secondary mt-3">New Search</a>
    </div>
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
