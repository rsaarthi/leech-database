from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Load your DataFrame
df = pd.read_csv('leech_data.csv')

@app.route('/', methods=['GET', 'POST'])
def browse():
    sort_by = request.args.get('sort_by', 'Species name')  # Default sort by 'Species name'
    if sort_by not in df.columns:
        sort_by = 'Species name'  # Fallback to default column if invalid
    sorted_df = df.sort_values(by=sort_by)

    if request.method == 'POST':
        search_value = request.form.get('search_value')
        search_type = request.form.get('search_type')

        if not search_value or not search_type:
            return render_template('leech_search.html', error="Please provide both search value and search type.")

        if search_type == 'species':
            matching_rows = sorted_df[sorted_df['Species name'].str.contains(search_value, case=False, na=False)]
        elif search_type == 'protein':
            matching_rows = sorted_df[sorted_df['Protein name'].str.contains(search_value, case=False, na=False)]
        else:
            matching_rows = pd.DataFrame()

        matching_rows = matching_rows.drop_duplicates()
        return render_template('leech_results.html', tables=[matching_rows.to_html(classes='data', escape=False, index=False)], titles=matching_rows.columns.values)

    return render_template('leech_search.html', tables=[sorted_df.to_html(classes='data', escape=False, index=False)], titles=sorted_df.columns.values)

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    if index >= len(df):
        return "Index out of range", 404

    if request.method == 'POST':
        species_name = request.form.get('species_name')
        protein_name = request.form.get('protein_name')
        # Update DataFrame
        df.at[index, 'Species name'] = species_name
        df.at[index, 'Protein name'] = protein_name
        df.to_excel('leech_data.xlsx', index=False)  # Save changes to the Excel file
        return redirect(url_for('browse'))

    row = df.iloc[index]
    return render_template('leech_edit.html', row=row, index=index)

if __name__ == '__main__':
    app.run(debug=True)
