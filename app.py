import pandas as pd
import os
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def page():
    return render_template('webpage_test.html')

@app.route('/', methods=['GET','POST'])

def get_details():
    #saving all .txt files available in the folder in the list
    files= [file for file in os.listdir('data/') if file.endswith('.txt')]
    try:
        if request.method == 'POST':
            #taking the input from webpage filename, start line no. and end line no.
            
            file=request.form['file']
            start = request.form['start']
            end = request.form['end']
            
            if file == '':    
                file= 'file1'   #if the file_name field is empty then it takes default filename as file1.txt
            if file+'.txt' not in files:    #checks if file name is available
                raise ValueError(' Invalid File Name ')
            if start=='':
                start=int('0') #if the start line no filed is empty it takes default number as 0

            with open('data/'+ file +'.txt', encoding='utf-8',errors='ignore') as f:      #reading the text file
                d=(f.read()).replace('\t','').split('\n')     #preprocessing
                data=pd.DataFrame(d)       #converting to a dataframe 
                #print(type(start))
                if end=='':
                    end=len(data)         #if the end line no. field is empty then it takes the value as length of data
                if int(start)>len(data) or int(end)>len(data):      #checking whether the start/end values are valid
                     raise ValueError('Please enter valid line number, the max line no. in file is:'+str(len(data)))
            
    except Exception as e:
        response = value_error(value=e)
        return response
    
    return data[int(start):int(end)].to_html(header=False,index=False)  #passing start and end line no. to the dataframe



def value_error(value):
    error_msg = {}
    error_msg['error'] = "{}".format(f"{repr(value)}")
    #print(error_msg)
    return render_template('invalid.html', error=error_msg['error'])


if __name__ == '__main__':
    app.run(debug = True, use_reloader=False, port= 3000)


