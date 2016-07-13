from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
import http.client, urllib.request, urllib.parse, urllib.error, base64, json, datetime


# from .models import NextTrain
from .models import StationPrefs

# import forms
from .forms import NextTrainForm, StationPrefForm, ModelForm

def is_weekday(weekday):
    if weekday >= 0 and weekday <= 4:
        return 5
    else:
        return 7

def is_closed():
    now = datetime.datetime.now()
    hour = now.hour
    weekday = now.weekday()

    if (hour >= 0) & (hour < is_weekday(weekday)):
        # CLOSED
        return True
    else:
        return False

def checkPrefs(request):
    if request.user.is_authenticated():
        s_pref = StationPrefs.objects.filter(owner=request.user)
    else:
        s_pref = ""
    return s_pref

# Create your views here.
def index(request):
    """Display next train info for DC Metro system"""
    # Check for user station preferences

    if request.method != 'POST':
        # No data submitted; create blank form
        s_pref_2 = checkPrefs(request)
        form = NextTrainForm(initial={'station_choice': s_pref_2})

        message = """Next Train DC is designed to be a lightweight, and thus
                  the fastest, tool to help you catch the next arriving train.
                  Simply choose one or more of the stations below. If you
                  need to transfer to another line on your trip, make sure
                  you select the transfer station as well
                  to optimize your timing! Registration is optional,
                  but it's designed to save you time by allowing you to save
                  your favorite stations so that they're pre-selected the
                  next time you log in."""

        context = {'form': form, 'message': message}
        return render(request, 'next_train/index.html', context)
    else:
        nextTrain = []
        message = """Next Train DC is designed to be a lightweight, and thus
                  the fastest, tool to help you catch the next arriving train.
                  Simply choose one or more of the stations below. If you
                  need to transfer to another line on your trip, make sure
                  you select the transfer station as well
                  to optimize your timing! Registration is optional,
                  but it's designed to save you time by allowing you to save
                  your favorite stations so that they're pre-selected the
                  next time you log in."""
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

                if is_closed():
                    pLine = "Sorry, the DC Metro system is currently CLOSED."
                    nextTrain.append(pLine)
                else:
                    for metro in data['Trains']:
                        pLine = (metro['Line'] + metro['LocationName'] + ":" + "(" + metro['DestinationName'] + ")" + " next " + metro['Line'] + " line train in  " + metro['Min'] + " minutes")
                        nextTrain.append(pLine)

                conn.close()
                context = {'nextTrain': nextTrain, 'form': form, 'message': message}
                return render(request, 'next_train/index.html', context)
            except Exception as e:
                print("[Errno {0}] {1}".format(e.errno, e.strerror))

@login_required
def preferences(request):
    """Edit an existing entry"""
    s_pref_2 = checkPrefs(request)
    if request.method != 'POST':
        # Initial request; pre-fill form with current entry
        form = StationPrefForm(initial={'station_choice': s_pref_2})
    else:
        # POST data submitted; process data.
        form = StationPrefForm(request.POST)
        if form.is_valid():
            # s_choice = form.cleaned_data['station_choice']
            form.save(defOwner=request.user)
            # s_pref = form.save(commit=False)
            # s_pref.owner = request.user
            # s_pref.save()
            return HttpResponseRedirect(reverse('next_train:index'))
    context = {'form': form}
    return render(request, 'next_train/preferences.html', context)
