from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
import http.client, urllib.request, urllib.parse, urllib.error, base64, json, datetime


# from .models import NextTrain
from .forms import NextTrainForm



# Create your views here.
def index(request):
    """Display next train info for DC Metro system"""
    if request.method != 'POST':
        # No data submitted; create blank form
        form = NextTrainForm()
        context = {'form': form}
        return render(request, 'next_train/index.html', context)
    else:
        nextTrain = []
        # POST data submitted; process data.
        form = NextTrainForm(request.POST)
        if form.is_valid():
            s_choice = form.cleaned_data['station_choice']

            count = 0
            if len(s_choice) > 1:
                for sc in s_choice:
                    if count == 0:
                        s_choices = sc
                        count = count + 1
                    else:
                        s_choices = s_choices + "," + sc
                        count = count + 1
            else:
                s_choices = s_choice[0]

            #s_choices = "F01,B01"

            pLine = ""
            headers = {
                # Request headers
                'api_key': '8208f715ee594384adb3e22fe3a42394',
            }

            params = urllib.parse.urlencode({
            })

            try:
                conn = http.client.HTTPSConnection('api.wmata.com')
                conn.request("GET","/StationPrediction.svc/json/GetPrediction/%s?%s" % (s_choices, params), "{body}", headers)
                response = conn.getresponse()
                data = json.loads(response.read().decode('utf-8'))
                #metro = json.loads(data)

                for metro in data['Trains']:
                    pLine = metro['LocationName'] + ":" + "(" + metro['DestinationName'] + ")" + " next " + metro['Line'] + " line train in  " + metro['Min'] + " minutes"
                    nextTrain.append(pLine)

                if not nextTrain and not is_open():
                    pLine = "Sorry, the DC Metro system is currently CLOSED."
                    nextTrain.append(pLine)

                #print(data)
                conn.close()
                context = {'nextTrain': nextTrain, 'form': form}
                return render(request, 'next_train/index.html', context)
            except Exception as e:
                print("[Errno {0}] {1}".format(e.errno, e.strerror))
