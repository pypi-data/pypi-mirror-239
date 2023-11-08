"""Constants."""
from enum import StrEnum

ATTR_RESULTS = "results"

AUTH_URL = "https://auth.live.homelync.io/oauth2?client={0}&secret={1}"
BASE_URL = "https://frontier.live.homelync.io/v1/"

HTTP_OK = 200

LOOKUPEVENTTYPE = "eventType"


class HomeLINKEndpoint(StrEnum):
    """HomeLINK Endpoints."""

    PROPERTIES = "property"
    PROPERTY = "property/{propertyreference}"
    PROPERTY_DEVICES = "property/{propertyreference}/devices"
    PROPERTY_ALERTS = "property/{propertyreference}/alerts"
    PROPERTY_INSIGHTS = "property/{propertyreference}/insights"
    PROPERTY_TAGS = "property/{propertyreference}/tags"
    DEVICES = "device"
    DEVICE = "device/{serialnumber}"
    DEVICES_ALERTS = "device/{serialnumber}/alerts"
    INSIGHTS = "insight"
    INSIGHT = "insight/{insightid}"
    LOOKUPS = "lookup/{lookuptype}"
    LOOKUP = "lookup/{lookuptype}/{lookupid}"
