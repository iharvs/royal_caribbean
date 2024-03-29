
# Royal Caribbean

| How to run this files? | |
| --- | --- |
| **Migrate**            | `python manage.py migrate` or `python3 manage.py migrate` |
| **Run the server**     | `python manage.py runserver` or `python3 manage.py runserver` |
| **Create super admin** | `python manage.py createsuperuser` or `python3 manage.py createsuperuser` |


| Superadmin Account | |
| ------------- | ------------- |
| **User** | admin |
| **Email** | admin@example.com |
| **Password** | admin |
| **Admin Link** | http://127.0.0.1:8000/admin |

| Get List (Endpoint) | |
| ------------- | ------------- |
| **Method** | **POST** |
| **Request** | {} |
| **URL** | http://127.0.0.1:8000/timezone/populate_timezones |

| Get Time Zone (Endpoint) | |
| ------------- | ------------- |
| **Method** | **POST** |
| **Request** | `{zone: 'Pacific/Wallis'}` |
| **URL** | http://127.0.0.1:8000/timezone/populate_zone_details |

**Project Overview:**
- Create a python script to query the TimezoneDB API and populate the tables TZDB_TIMEZONES and TZDB_ZONE_DETAILS
- Your script should handle errors when retrieving the API and log them into the table TZDB_ERROR_LOG.
- TZDB_TIMEZONES is to be deleted every time you script runs and populated with data from the API.
- TZDB_ZONE_DETAILS is to be populated incrementally, not adding rows if the data in the table already exists. Hint: To achieve number 4 you can create a stage table before writing into TZDB_ZONE_DETAILS.

**Notes:**
- To get access to the API provided by TimezoneDB go to: https://timezonedb.com and create an account (free), you will be provided with a Key that you can use in your scripts.
- You can use your preferred database to upload the data.

**There are a few endpoints to use:**
- Get List: Use this one to populate the TZDB_TIMEZONES table.
- Get Time Zone: Use this one to populate TZDB_ZONE_DETAILS
