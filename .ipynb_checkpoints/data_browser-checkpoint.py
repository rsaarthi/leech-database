from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load your DataFrame (Adjust the path to your Excel file as needed)
df = pd.read_csv('leech_data.csv')


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
