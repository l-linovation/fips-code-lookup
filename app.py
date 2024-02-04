from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    fips = None
    if request.method == 'POST':
        input1 = request.form['input1']
        print('received code:', input1)
        fips = lookup_fips(input1)
    return render_template('index.html', fips=fips)

def lookup_fips(input1):
    # Read in the .csv file
    infile = 'data/fips_lookup.csv'
    indf = pd.read_csv(infile, dtype = 'str')  # keep the leading 0 in the FIPS column when load to data frame

    input_str = str(input1)

    # first two digits for state
    state_code = input_str[0:2] + '000'
    subdf_state = indf.query("FIPS == @state_code")
    
    print('state_code:', state_code)
    print('the same as input_str?', state_code == input1)
    
    subdf_county = indf.query("FIPS == @input_str")
    if len(subdf_county) == 1:
        state = subdf_state['COUNTY/STATE'].values[0]
        if input_str == state_code:
            return (state)
        else:
            county = subdf_county['COUNTY/STATE'].values[0] + ', ' + state
        return(county)
    else:
        return "Enter a valid FIPS code."
    
if __name__ == '__main__':
    app.run(debug=True)
