from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

import requests
from django.conf import settings
import datetime
from django.core import serializers

from .serializers import SetObjectsSerializer, CoreCardFieldsSerializer, GameplayFieldsSerializer
from .models import SetObjects, CoreCardFields, GameplayFields

class SetObjectsListView(APIView):
	"""
	List all SetObjects
	"""
	def get(self, request, format=None):
		setobjects = SetObjects.objects.all();
		serializer = SetObjectsSerializer(setobjects, many=True)
		return Response(serializer.data)

@api_view(['GET'])
def SetObjectsLoad(request):
	"""
	This would help to fetch all data and store it
	"""
	responseValue = LoadTracker();
	responseValue = [] if not responseValue else responseValue;

	novalTrackerResponse = LoadNovalTracker();
	if novalTrackerResponse:
		responseValue.append(novalTrackerResponse);

	return JsonResponse(responseValue, safe=False)

def LoadNovalTracker():
    """
    https://scryfall.com/docs/api/application/current
    """
	host = settings.SCRYFALL_HOST
	apipath = settings.SCRYFALL_API

	responseValue = []
	loadDate = datetime.date.today()
	sourceId = 'api.scryfall.com';
	foundObjects = SetObjects.objects.filter(source = sourceId, loadedDate = loadDate).count()

	if foundObjects > 0:
		print('api.scryfall.com: Source Id :{} has been loaded already for date: {} with count:{}'.format(sourceId, loadDate, foundObjects))
		return responseValue;

	resp = requests.get(host+apipath);
	if resp.status_code != 200:
		raise ApiError('NovalCovidData: Cannot Get Response: {}'.format(resp.status_code))

	responsedata=resp.json();
	for SetObjectsFound in responsedata:
		print(SetObjectsFound);
		countryInfo = SetObjectsFound['countryInfo']
		createdVal = datetime.datetime.utcnow()

		SetObjects.objects.update_or_create(source = sourceId,
		country_code =countryInfo['iso3'],
		country = SetObjectsFound['country'],
		state = '',
		region = '',
		latitude = float(countryInfo['lat']) if countryInfo['lat'] else 0,
		longitude= float(countryInfo['long']) if countryInfo['long'] else 0,
		loadedDate = loadDate,
		defaults = {    
			'cases' : int(SetObjectsFound['cases']) if SetObjectsFound['cases'] else 0,
			'deaths' : int(SetObjectsFound['deaths']) if SetObjectsFound['deaths'] else 0,
			'recovered' : int(SetObjectsFound['recovered']) if SetObjectsFound['recovered'] else 0,
			'todayCases': int(SetObjectsFound['todayCases']) if SetObjectsFound['todayCases'] else 0,
			'totalDeaths': int(SetObjectsFound['todayDeaths']) if SetObjectsFound['todayDeaths'] else 0,
			'active': int(SetObjectsFound['active']) if SetObjectsFound['active'] else 0,
			'critical': int(SetObjectsFound['critical']) if SetObjectsFound['critical'] else 0,
			'casesPerOneMillion': float(SetObjectsFound['casesPerOneMillion']) if SetObjectsFound['casesPerOneMillion'] else 0,
			'deathsPerOneMillion': float(SetObjectsFound['deathsPerOneMillion']) if SetObjectsFound['deathsPerOneMillion'] else 0,
			'created_at' : createdVal
		}
		)
		responseValue.append('source:{}, country:{}, cases:{}, deaths:{}, recovered:{}, active:{}, critical:{}'.format(sourceId, 
			SetObjectsFound['country'], SetObjectsFound['cases'], SetObjectsFound['deaths'], SetObjectsFound['recovered'],
			SetObjectsFound['active'], SetObjectsFound ['critical'] ));

	return responseValue;


def LoadTracker():
	host=settings.TRACKERHOST
	listapipath=settings.TRACKERLISTAPI
	getrecentapipath=settings.TRACKERGETLOCATIONAPI
	resp = requests.get(host+listapipath)
	if resp.status_code != 200:
		raise ApiError('TrackerData: Cannot list sources: {}'.format(resp.status_code))

	responseValue=[]

	for source in resp.json()["sources"]:
		loadDate = datetime.date.today()
		sourceId = 'tracker-api.{}'.format(source);

		foundObjects = SetObjects.objects.filter(source = sourceId, loadedDate = loadDate).count()

		if foundObjects > 0:
			print('TrackerData: Source Id :{} has been loaded already for date: {} with count:{}'.format(sourceId, loadDate, foundObjects))
			continue;

		print('TrackerData: Loading for sourceId:{} for date:{}'.format(sourceId, loadDate));

		val='{}{}?source={}'.format(host,getrecentapipath,source);
		resourceresp = requests.get(val)

		if resourceresp.status_code != 200:
			raise ApiError('Cannot fetch resource:{} detail: {}'.format(source,resourceresp.status_code))

		responsedata=resourceresp.json();
		recentdata={};
		recentdata['source'] = source;
		recentdata['latest'] = responsedata['latest'];
		recentdata['locations'] = responsedata['locations'];
		SetObjectsDataFromSource = responsedata['locations'];
		for SetObjectsFound in SetObjectsDataFromSource:
			countryInfo = SetObjectsFound['coordinates']
			caseInfo = SetObjectsFound['latest']
			createdVal = datetime.datetime.utcnow()

			SetObjects.objects.update_or_create(source = sourceId,
			country_code =SetObjectsFound['country_code'],
			country = SetObjectsFound['country'],
			state = SetObjectsFound['province'],
			region = SetObjectsFound['county'] if hasattr(SetObjectsFound, 'county') else '',
			latitude = float(countryInfo['latitude']) if countryInfo['latitude'] else 0,
			longitude= float(countryInfo['longitude']) if countryInfo['longitude'] else 0,
			loadedDate = loadDate,
			defaults = {    
				'cases' : int(caseInfo['confirmed']) if caseInfo['confirmed'] else 0,
				'deaths' : int(caseInfo['deaths']) if caseInfo['deaths'] else 0,
				'recovered' : int(caseInfo['recovered']) if caseInfo['recovered'] else 0,
				'created_at' : createdVal
			}
			)
			responseValue.append(recentdata);

		return responseValue;