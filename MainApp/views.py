from django.shortcuts import render
from django.http import HttpResponse, response, HttpResponseRedirect
from .forms import TradingForm
# Create your views here.


def handle_upload_file(f):  
    with open('upload/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)  

def json_output_file(candle):

    import json, os
    import pandas as pd
    import numpy as np
    folder_path = 'upload/'
    csv_file = os.listdir(folder_path)[0]
    df = pd.read_csv(folder_path + csv_file)
    if os.path.exists(folder_path + csv_file):
         os.remove(folder_path + csv_file)
    df['DATE'] = pd.to_datetime(df['DATE'], format='%Y%m%d')


    download_path = 'download/'
    json_file_path = download_path + 'candle.json'
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
        # file_upload = request.FILES['file']
        # candel_value = request.POST['candle_value']
        # print(candel_value)
        if trade.is_valid():
            handle_upload_file(request.FILES['file'])
            candle = int(request.POST['candle'])
            json_output_file(candle)
            return HttpResponseRedirect('/download')

    trade = TradingForm()
    context = {'form': trade}
   
    

    return render(request, 'index.html', context=context)

def download(request):
    return render(request, 'download.html')


        
