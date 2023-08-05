from __future__ import absolute_import
import logging
from celery import shared_task
from geopy.exc import ConfigurationError, GeocoderQueryError, GeocoderTimedOut
from celery_geolocator.config import configuration
from celery_geolocator.geocoders import GoogleRateLimitedGeocoder, RateLimitExceededException, GOOGLEV3_GEOCODER, \
    NOMINATIM_GEOCODER, NominatimRateLimitedGeocoder

logger = logging.getLogger(__name__)

__author__ = 'brent'


@shared_task
def geocode(unformatted_address, geocode_type=GOOGLEV3_GEOCODER, api_key=None):
    exception = False
    address, point, raw = None, None, None
    if geocode_type == GOOGLEV3_GEOCODER:
        api_key = api_key if api_key else configuration.get('Google', {}).get('API_KEY')
        try:
            geocoder = GoogleRateLimitedGeocoder.getInstance()
            geocoder.initialize(daily_rate=configuration['Google']['daily_rate'],
                                google_api_key=api_key)
            address, point, raw = geocoder.geocode(unformatted_address)
        except RateLimitExceededException as e:
            exception = "rate limit exceeded"
        except (ConfigurationError, GeocoderQueryError, AttributeError) as e:
            # If a None value was returned by the geocoder, we pythonically let it through an AttributeError
            logger.exception(e)
            exception = "bad query"
        except Exception as e:
            exception = str(type(e))
    elif geocode_type == NOMINATIM_GEOCODER:
        try:
            geocoder = NominatimRateLimitedGeocoder.getInstance()
            address, point, raw = geocoder.geocode(unformatted_address)
        except (ConfigurationError, GeocoderQueryError, AttributeError, GeocoderTimedOut) as e:
            # If a None value was returned by the geocoder, we pythonically let it through an AttributeError
            # Nominatim times out on calls it finds to complex
            logger.exception(e)
            exception = "bad query"
        except Exception as e:
            exception = str(type(e))

    return exception, address, point, raw, geocode_type
