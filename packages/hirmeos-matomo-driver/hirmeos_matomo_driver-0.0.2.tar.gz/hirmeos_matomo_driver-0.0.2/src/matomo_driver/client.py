from dataclasses import dataclass
from typing import Any, Dict, Iterator, List

import requests
from requests.exceptions import HTTPError

from .logic import compile_regexes, search_regexes
from .serializers import MatomoEventCategory, MatomoEvent, MatomoUrlResult


@dataclass
class MatomoClient:
    """Provide an entry point into the matomo api."""

    base_url: str
    site_id: int
    token: str | None = None

    def __post_init__(self):
        self.base_parameters = dict(
            idSite=self.site_id,
            token_auth=self.token,
            module='API',
            period='day',
            format='JSON',
            filter_limit=-1,
        )

    def _get_request(self, **additional_parameters) -> Any:
        """Perform a get request and return a JSON response.

        Args:
            **additional_parameters: Request parameters.

        Returns:
            Any: JSON from the response.
        """
        parameters = self.base_parameters.copy()
        parameters.update(**additional_parameters)

        response = requests.get(self.base_url, params=parameters)
        if response.status_code != 200:
            response.raise_for_status()

        _json = response.json()
        if isinstance(_json, dict) and _json.get('result') == 'error':
            raise HTTPError(_json.get('message', 'Unknown Error'))

        return _json

    def _fetch_url_results(self, **params) -> Iterator[MatomoUrlResult]:
        """Request URL results and filter out invalid data."""
        regexes = params.pop('re_include', []), params.pop('re_exclude', [])
        _include, _exclude = compile_regexes(*regexes)
        _params = dict(expanded=1, flat=1, showColumns='url,nb_visits')
        _params.update(**params)

        return (
            MatomoUrlResult(**result) for result in self._get_request(**_params)
            if 'url' in result and search_regexes(_include, result['url'])
            and not search_regexes(_exclude, result['url'])
        )

    def get_page_urls(
            self,
            search_date: str,
            depth: int,
            segment: str = None,
            include_regexes: list = None,
            exclude_regexes: list = None,
    ) -> Iterator[MatomoUrlResult]:
        """Perform a getPageUrls request and return serialized results.

        Args:
            search_date (str): YYYY-MM-DD.
            depth (int): URL depth.
            segment (str): Matomo segment, if available.
            include_regexes (list): Regex patterns of expected URL matches,
            exclude_regexes (list): False positives matches by include_regexes.

        Yields:
            MatomoUrlResult: Serialized JSON response.
        """
        return self._fetch_url_results(
            date=search_date,
            depth=depth,
            segment=segment,
            method='Actions.getPageUrls',
            re_include=include_regexes,
            re_exclude=exclude_regexes,
        )

    def get_downloads(
            self,
            search_date: str,
            depth: int,
            segment: str = None,
            include_regexes: list = None,
            exclude_regexes: list = None,
    ) -> Iterator[MatomoUrlResult]:
        """Perform a getDownloads request and return serialized results."""
        return self._fetch_url_results(
            date=search_date,
            depth=depth,
            segment=segment,
            method='Actions.getDownloads',
            re_include=include_regexes,
            re_exclude=exclude_regexes,
        )

    def get_category_id_mappings(self, search_date, segment=None):
        """Helper method - fetch ID mappings for each event category."""
        parameters = dict(
            date=search_date,
            segment=segment,
            method='Events.getCategory',
            showColumns='label,idsubdatatable',
        )
        return self._get_request(**parameters)

    def get_events_by_category_id(
            self,
            search_date: str,
            category_id: int,
            segment: str = None,

    ) -> List[Dict]:
        """Fetch event metrics by category ID.

        Args:
            search_date (str): YYYY-MM-DD.
            category_id (int): ID of category to search.
            segment (str): Matomo segment, if available.

        Returns:
            List: Json results containing event metrics.
        """
        parameters = dict(
            date=search_date,
            idSubtable=category_id,
            segment=segment,
            method='Events.getNameFromCategoryId',
            showColumns='label,nb_visits',
        )
        return self._get_request(**parameters)

    def events_from_categories(self, search_date, target_categories):
        """Fetch event metrics matching the names of target categories."""
        results = self.get_category_id_mappings(search_date)
        for result in results:
            event_category = MatomoEventCategory(**result)
            if event_category.name in target_categories:
                event_metrics = self.get_events_by_category_id(
                    search_date,
                    event_category.id,
                )
                for event in event_metrics:
                    event.update(category=event_category.name)
                    yield MatomoEvent(**event)

    def query_date_range(
            self,
            method: str,
            start_date: str,
            end_date: str,
            depth: int,
            segment: str | None = None,
    ) -> Any:
        """Search Matomo over a date range.

        Args:
            method (str): Matomo API Method
            start_date (str): Date to search from
            end_date (str): Date to search until
            depth (int): Url depth to search
            segment (str): Matomo segment, if available.

        Returns:
            Any: JSON response from Matomo.
        """
        parameters = self.base_parameters.copy()
        parameters.update(
            method=method,
            depth=depth,
            period='range',
            date=f'{start_date},{end_date}',
            segment=segment,
        )
        
        return self._get_request(**parameters)
