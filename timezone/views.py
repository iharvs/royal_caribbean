from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

import requests

from timezone.models import TZDBTimezone, TZDBZoneDetail, TZDBErrorLog

# Harvey's API
API_KEY = "9I4ISY0ZVGG4"

def index(request):
    return HttpResponse("Hello world, Royal Caribbean Group!")

def log_error(error_message):
    error_date = datetime.now().date()
    TZDBErrorLog.objects.create(ErrorDate=error_date, ErrorMessage=error_message)

# Endpoint to populate TZDB_TIMEZONES table
@csrf_exempt
def populate_timezones(request):
    if request.method == 'POST':
        try:
            # Delete all the records in TZDB_ZONE_DETAILS table
            TZDBTimezone.objects.all().delete()

            # Query TimezoneDB API to populate TZDB_TIMEZONES table
            response = requests.get(f'http://api.timezonedb.com/v2.1/list-time-zone?key={API_KEY}&format=json')
            response.raise_for_status()  # Raise exception for HTTP errors
            data = response.json()
            for zone in data['zones']:
                TZDBTimezone.objects.create(
                    CountryCode=str(zone['countryCode']),
                    CountryName=str(zone['countryName']),
                    ZoneName=str(zone['zoneName']),
                    GMTOffset=zone['gmtOffset'],
                    ImportDate=datetime.now().date()
                )
            
            getAllZones = TZDBTimezone.objects.all()
            zones = []
            for zone in getAllZones:
                zones.append({
                    "CountryName": zone.CountryName,
                    "CountryCode": zone.CountryCode,
                    "ZoneName" : zone.ZoneName,
                    "GMTOffset": zone.GMTOffset,
                    "ImportDate" : zone.ImportDate
                })
            return JsonResponse({'message': 'TZDB_TIMEZONES table populated successfully', "data": zones}, status=201)
        except Exception as e:
            # Relic log
            log_error(str(e))
            return JsonResponse({'error': str(e)}, status=500)
    else:
        log_error(str({'error': 'Method not allowed'}))
        return JsonResponse({'error': 'Method not allowed'}, status=405)

# Endpoint to populate TZDB_ZONE_DETAILS table

@csrf_exempt
def populate_zone_details(request):
    if request.method == 'POST':
        try:
            zone_name = str(request.POST.get('zone'))
            zones = TZDBTimezone.objects.filter(ZoneName=zone_name)
            if zones.exists():
                timezone = zones.first()

                response = requests.get(f'http://api.timezonedb.com/v2.1/get-time-zone?key={API_KEY}&format=json&by=zone&zone={timezone.ZoneName}&country={timezone.CountryCode}')
                response.raise_for_status()  # Raise exception for HTTP errors
                data = response.json()

                # Extract data from the response
                country_name = timezone.CountryName if timezone else None
                country_code = timezone.CountryCode if timezone else None
                zone_name = timezone.ZoneName if timezone else None
                gmt_offset = timezone.GMTOffset if timezone else None
                
                # Extract DST, ZoneStart, and ZoneEnd values from the response
                dst = data.get('dst')
                if dst is None:
                    dst = 0
                zone_start = data.get('zoneStart')
                if zone_start is None:
                    zone_start = 0
                zone_end = data.get('zoneEnd')
                if zone_end is None:
                    zone_end = 0

                import_date = datetime.now().date()

                TZDBZoneDetail.objects.filter(ZoneName=zone_name).all().delete()

                # Create TZDBZoneDetail object with the extracted data
                TZDBZoneDetail.objects.create(
                    CountryName=country_name,
                    CountryCode=country_code,
                    ZoneName=zone_name,
                    GMTOffset=gmt_offset,
                    DST=dst,
                    ZoneStart=zone_start,
                    ZoneEnd=zone_end,
                    ImportDate=import_date
                )

                zoneDetail = TZDBZoneDetail.objects.filter(ZoneName=zone_name).first()
                serialized_data = {
                    "CountryName": zoneDetail.CountryName,
                    "CountryCode": zoneDetail.CountryCode,
                    "ZoneName" : zoneDetail.ZoneName,
                    "GMTOffset": zoneDetail.GMTOffset,
                    "DST": zoneDetail.DST,
                    "ZoneStart": zoneDetail.ZoneStart,
                    "ZoneEnd" : zoneDetail.ZoneEnd,
                    "ImportDate" : zoneDetail.ImportDate
                }
                
                return JsonResponse({'message': 'TZDBZoneDetail object created successfully', 'data': serialized_data}, status=201)
            else:
                log_error(str({'error': 'Zone not found'}))
                return JsonResponse({'error': 'Zone not found'}, status=404)
        except Exception as e:
            # Relic log
            log_error(str(e))
            return JsonResponse({'error': str(e)}, status=500)
    else:
        log_error(str({'error': 'Method not allowed'}))
        return JsonResponse({'error': 'Method not allowed'}, status=405)
