from django.shortcuts import render
from django.http import HttpResponse
from .forms import TradingForm
# Create your views here.


def handle_upload_file(f):  
    with open('upload/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)  

def building_json_outfile(candle):

    import json, os
    import pandas as pd
    import numpy as np

    csv_file = os.listdir('../upload/')[0]
    df = pd.read_csv('../upload/'+ csv_file)
    os.remove('../upload/'+ csv_file)
    df['DATE'] = pd.to_datetime(df['DATE'], format='%Y%m%d')


    json_file_path = '../download/candle.json'
    if os.path.exists(json_file_path):
        os.remove(json_file_path)

    if not os.path.exists(json_file_path):
        with open(json_file_path, "w") as f:
            f.write("[]")


    trade = json.load(open(json_file_path))


    k = candle
    for i in range(k,len(df), k):

        trade.append({
        'BANKNIFTY': df['BANKNIFTY'].iloc[i-k],
        'DATE':str(df['DATE'].iloc[i-k]),
        'TIME':df['TIME'].iloc[i-k],
        'OPEN': format(df['OPEN'].iloc[i-k:i].mean(), '.2f'),
        'HIGH': format(df['HIGH'].iloc[i-k:i].mean(), '.2f'),
        'LOW':format(df['LOW'].iloc[i-k:i].mean(), '.2f'),
        'CLOSE':format(df['CLOSE'].iloc[i-k:i].mean(), '.2f'),
        'VOLUME':format(df['VOLUME'].iloc[i-k:i].min(), '.2f'),
    })

        with open(json_file_path, 'w+') as file:
            json.dump(trade, file, indent=10)
    
    print('Success')


def index(request):
    if request.method=='POST':
        trade = TradingForm(request.POST, request.FILES)
        if trade.is_valid():
            handle_upload_file(request.FILES['file'])
            return HttpResponse('Form submitted successfully.')

    trade = TradingForm()
    return render(request, 'index.html', {'form': trade})
        
