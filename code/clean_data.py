import requests
import datetime
import json


def extract_timeseriesx(raw_data):
    """Extracts a list of timeseries from the raw data dict."""
    return raw_data["value"]["timeSeries"]


def extract_metadata_from_timeseries(timeseries):
    """Extracts metadata from a timeseries dict."""
    site_name = timeseries["sourceInfo"]["siteName"]
    latitude = timeseries["sourceInfo"]["geoLocation"]["geogLocation"]["latitude"]
    longitude = timeseries["sourceInfo"]["geoLocation"]["geogLocation"]["longitude"]
    variable_name = timeseries["variable"]["variableName"]

    return {
        "site_name": site_name,
        "latitude": float(latitude),
        "longitude": float(longitude),
        "variable_name": variable_name
    }


def extract_values_from_timerseries(timeseries):
    """Extracts the values from a timeseries dict."""
    values = timeseries["values"][0]["value"]

    result = []
    for value_entry in values:
        value = float(value_entry["value"])
        dt_str = value_entry["dateTime"]
        dt_str = dt_str[:-1] + "000" if dt_str.endswith(".000") else dt_str
        dt = datetime.datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%f")
        result.append({"value": value, "datetime": dt})

    return result


def extract_data_from_timeseries(timeseries):
    """Combines metadata and values into a list of dicts."""
    metadata = extract_metadata_from_timeseries(timeseries)
    values = extract_values_from_timerseries(timeseries)

    result = []
    for value_entry in values:
        merged_entry = {**metadata, **value_entry}
        result.append(merged_entry)

    return result


def extract_data(data):
    timeseriesx = extract_timeseriesx(data)

    result = []
    for timeseries in timeseriesx:
        extracted_data = extract_data_from_timeseries(timeseries)
        result.extend(extracted_data)

    return result


if __name__ == "__main__":
    example_timeseries = {
        "sourceInfo": {
            "siteName": "KH-65-40-707 (Galveston)",
            "siteCode": [
                {"value": "292338095063601", "network": "NWIS", "agencyCode": "USGS"}
            ],
            "timeZoneInfo": {
                "defaultTimeZone": {"zoneOffset": "-06:00", "zoneAbbreviation": "CST"},
                "daylightSavingsTimeZone": {
                    "zoneOffset": "-05:00",
                    "zoneAbbreviation": "CDT",
                },
                "siteUsesDaylightSavingsTime": True,
            },
            "geoLocation": {
                "geogLocation": {
                    "srs": "EPSG:4326",
                    "latitude": 29.39416667,
                    "longitude": -95.1102778,
                },
                "localSiteXY": [],
            },
            "note": [],
            "siteType": [],
            "siteProperty": [
                {"value": "GW", "name": "siteTypeCd"},
                {"value": "12040204", "name": "hucCd"},
                {"value": "48", "name": "stateCd"},
                {"value": "48167", "name": "countyCd"},
            ],
        },
        "variable": {
            "variableCode": [
                {
                    "value": "62610",
                    "network": "NWIS",
                    "vocabulary": "NWIS:UnitValues",
                    "variableID": 51413516,
                    "default": True,
                }
            ],
            "variableName": "Groundwater level above NGVD 1929, feet",
            "variableDescription": "Groundwater level above NGVD 1929, feet",
            "valueType": "Derived Value",
            "unit": {"unitCode": "ft"},
            "options": {"option": [{"name": "Statistic", "optionCode": "00000"}]},
            "note": [],
            "noDataValue": -999999.0,
            "variableProperty": [],
            "oid": "51413516",
        },
        "values": [
            {
                "value": [
                    {
                        "value": "-64.58",
                        "qualifiers": ["A", "1"],
                        "dateTime": "2022-06-28T13:16:00.000",
                    },
                    {
                        "value": "-65.87",
                        "qualifiers": ["P", "1"],
                        "dateTime": "2022-09-14T14:01:00.000",
                    },
                ],
                "qualifier": [
                    {
                        "qualifierCode": "1",
                        "qualifierDescription": "Static",
                        "qualifierID": 0,
                        "network": "NWIS",
                        "vocabulary": "uv_rmk_cd",
                    },
                    {
                        "qualifierCode": "A",
                        "qualifierDescription": "Approved for publication -- Processing and review completed.",
                        "qualifierID": 1,
                        "network": "NWIS",
                        "vocabulary": "uv_rmk_cd",
                    },
                    {
                        "qualifierCode": "P",
                        "qualifierDescription": "Provisional data subject to revision.",
                        "qualifierID": 2,
                        "network": "NWIS",
                        "vocabulary": "uv_rmk_cd",
                    },
                ],
                "qualityControlLevel": [],
                "method": [{"methodID": 1}],
                "source": [],
                "offset": [],
                "sample": [],
                "censorCode": [],
            }
        ],
        "name": "USGS:292338095063601:62610:00000",
    }

    expected_metadata = {
        "site_name": "KH-65-40-707 (Galveston)",
        "latitude": 29.39416667,
        "longitude": -95.1102778,
        "variable_name": "Groundwater level above NGVD 1929, feet",
    }

    expected_values = [
        {"value": -64.58, "datetime": datetime.datetime(2022, 6, 28, 13, 16)},
        {"value": -65.87, "datetime": datetime.datetime(2022, 9, 14, 14, 1)},
    ]

    expected_data = [
        {
            "value": -64.58,
            "datetime": datetime.datetime(2022, 6, 28, 13, 16),
            "site_name": "KH-65-40-707 (Galveston)",
            "latitude": 29.39416667,
            "longitude": -95.1102778,
            "variable_name": "Groundwater level above NGVD 1929, feet",
        },
        {
            "value": -65.87,
            "datetime": datetime.datetime(2022, 9, 14, 14, 1),
            "site_name": "KH-65-40-707 (Galveston)",
            "latitude": 29.39416667,
            "longitude": -95.1102778,
            "variable_name": "Groundwater level above NGVD 1929, feet",
        },
    ]

    assert extract_metadata_from_timeseries(example_timeseries) == expected_metadata

    assert extract_values_from_timerseries(example_timeseries) == expected_values

    assert extract_data_from_timeseries(example_timeseries) == expected_data