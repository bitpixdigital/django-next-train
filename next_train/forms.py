from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

# from .models import Topic, Entry
from .models import StationPrefs

METRO_STATIONS = (
('F06', 'Anacostia'),
 ('F02', 'Archives-Navy Memorial-Penn Quarter'),
 ('C06', 'Arlington Cemetery'),
 ('K04', 'Ballston-MU'),
 ('G01', 'Benning Road'),
 ('A09', 'Bethesda'),
 ('C12', 'Braddock Road'),
 ('F11', 'Branch Ave'),
 ('B05', 'Brookland-CUA'),
 ('G02', 'Capitol Heights'),
 ('D05', 'Capitol South'),
 ('D11', 'Cheverly'),
 ('K02', 'Clarendon'),
 ('A05', 'Cleveland Park'),
 ('E09', 'College Park-U of MD'),
 ('E04', 'Columbia Heights'),
 ('F07', 'Congress Heights'),
 ('K01', 'Court House'),
 ('C09', 'Crystal City'),
 ('D10', 'Deanwood'),
 ('K07', 'Dunn Loring-Merrifield'),
 ('A03', 'Dupont Circle'),
 ('K05', 'East Falls Church'),
 ('D06', 'Eastern Market'),
 ('C14', 'Eisenhower Avenue'),
 ('A02', 'Farragut North'),
 ('C03', 'Farragut West'),
 ('D04', 'Federal Center SW'),
 ('D01', 'Federal Triangle'),
 ('C04', 'Foggy Bottom-GWU'),
 ('B09', 'Forest Glen'),
 ('B06', 'Fort Totten - RD'),
 ('E06', 'Fort Totten - YL/GR'),
 ('A08', 'Friendship Heights'),
 ('F01', 'Gallery Pl-Chinatown - YL/GR'),
 ('B01', 'Gallery Pl-Chinatown - RD'),
 ('E05', 'Georgia Ave-Petworth'),
 ('B11', 'Glenmont'),
 ('N03', 'Greensboro'),
 ('A11', 'Grosvenor-Strathmore'),
 ('C15', 'Huntington'),
 ('B02', 'Judiciary Square'),
 ('C13', 'King St-Old Town'),
 ('F03', "L'Enfant Plaza - YL/GR"),
 ('D03', "L'Enfant Plaza - OR/SV"),
 ('D12', 'Landover'),
 ('N01', 'McLean'),
 ('C02', 'McPherson Square'),
 ('A10', 'Medical Center'),
 ('C01', 'Metro Center - OR/SV'),
 ('A01', 'Metro Center - RD'),
 ('D09', 'Minnesota Ave'),
 ('G04', 'Morgan Boulevard'),
 ('E01', 'Mt Vernon Sq 7th St-Convention Center'),
 ('F05', 'Navy Yard-Ballpark'),
 ('F09', 'Naylor Road'),
 ('D13', 'New Carrollton'),
 ('B35', 'NoMa-Gallaudet'),
 ('C07', 'Pentagon'),
 ('C08', 'Pentagon City'),
 ('D07', 'Potomac Ave'),
 ('E08', "Prince George's Plaza"),
 ('B04', 'Rhode Island Ave-Brentwood'),
 ('A14', 'Rockville'),
 ('C10', 'Ronald Reagan Washington National Airport'),
 ('C05', 'Rosslyn'),
 ('E02', 'Shaw-Howard U'),
 ('B08', 'Silver Spring'),
 ('D02', 'Smithsonian'),
 ('F08', 'Southern Avenue'),
 ('N04', 'Spring Hill'),
 ('D08', 'Stadium-Armory'),
 ('F10', 'Suitland'),
 ('B07', 'Takoma'),
 ('A07', 'Tenleytown-AU'),
 ('A13', 'Twinbrook'),
 ('N02', 'Tysons Corner'),
 ('E03', 'U Street/African-Amer Civil War Memorial/Cardozo'),
 ('B03', 'Union Station'),
 ('J02', 'Van Dorn Street'),
 ('A06', 'Van Ness-UDC'),
 ('K03', 'Virginia Square-GMU'),
 ('F04', 'Waterfront'),
 ('K06', 'West Falls Church-VT/UVA'),
 ('E07', 'West Hyattsville'),
 ('B10', 'Wheaton'),
 ('A12', 'White Flint'),
 ('A04', 'Woodley Park-Zoo/Adams Morgan')
)

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class NextTrainForm(forms.Form):
    station_choice = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'size':'10'}), choices=METRO_STATIONS)

class StationPrefForm(forms.Form):
    station_choice = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'size':'10'}), choices=METRO_STATIONS)
    def save(self, defOwner):
        clear = StationPrefs.objects.filter(owner=defOwner)
        clear.delete()
        s_choice = self.cleaned_data['station_choice']
        for choice in s_choice:
            stationData = StationPrefs(owner=defOwner, station=choice)
            stationData.save()
