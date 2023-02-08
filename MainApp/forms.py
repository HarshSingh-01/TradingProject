from django import forms  
class TradingForm(forms.Form):    
    file      = forms.FileField() # for creating file input  
    candle = forms.IntegerField(max_value=60, min_value=0)