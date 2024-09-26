from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)
df = pd.read_csv('leech_data.csv')
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
