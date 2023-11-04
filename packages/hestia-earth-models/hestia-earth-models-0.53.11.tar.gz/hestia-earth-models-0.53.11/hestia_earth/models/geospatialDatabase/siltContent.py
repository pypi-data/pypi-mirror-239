from hestia_earth.schema import MeasurementMethodClassification

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.measurement import _new_measurement, measurement_value
from . import MODEL, clayContent, sandContent

REQUIREMENTS = {
    "Site": {
        "or": [
            {"latitude": "", "longitude": ""},
            {"boundary": {}},
            {"region": {"@type": "Term", "termType": "region"}}
        ]
    }
}
RETURNS = {
    "Measurement": [{
        "value": "",
        "depthUpper": "0",
        "depthLower": "30",
        "methodClassification": "geospatial dataset"
    }]
}
TERM_ID = 'siltContent'
OTHER_TERM_IDS = [
    clayContent.TERM_ID,
    sandContent.TERM_ID
]
BIBLIO_TITLE = 'Harmonized World Soil Database Version 1.2. Food and Agriculture Organization of the United Nations (FAO).'  # noqa: E501


def _measurement(value: int):
    measurement = _new_measurement(TERM_ID, None, BIBLIO_TITLE)
    measurement['value'] = [value]
    measurement['depthUpper'] = 0
    measurement['depthLower'] = 30
    measurement['methodClassification'] = MeasurementMethodClassification.GEOSPATIAL_DATASET.value
    return measurement


def _run(measurements: list):
    value = 100 - sum([measurement_value(m) for m in measurements])
    return [_measurement(value)]


def _should_run(site: dict):
    measurements = [
        m for m in site.get('measurements', [])
        if m.get('term', {}).get('@id') in OTHER_TERM_IDS and len(m.get('value', [])) > 0
    ]
    has_all_measurements = len(measurements) == len(OTHER_TERM_IDS)

    logRequirements(site, model=MODEL, term=TERM_ID,
                    has_all_measurements=has_all_measurements,
                    measurements=';'.join([m.get('term', {}).get('@id') for m in measurements]))

    should_run = all([has_all_measurements])
    logShouldRun(site, MODEL, TERM_ID, should_run)
    return should_run, measurements


def run(site: dict):
    should_run, measurements = _should_run(site)
    return _run(measurements) if should_run else []
