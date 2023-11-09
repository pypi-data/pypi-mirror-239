import json
from typing import List

import requests

from molgenis.api_support import BlockAll
from molgenis.eucan_connect.errors import EucanError
from molgenis.eucan_connect.model import Catalogue
from molgenis.eucan_connect.printer import Printer


class SourceCollector:
    """
    Main class for collecting data from the different source catalogues.
    """

    def __init__(self, catalogue: Catalogue):
        """
        :param Catalogue catalogue:
        """

        self.catalogue = catalogue
        self.printer = Printer()
        self.catalogue_session = requests.Session()
        self.catalogue_session.cookies.policy = BlockAll()

    def get_birthcohorts_data(self):
        # Get the total number of cohorts from birthcohorts.net ######
        limit = 10
        user_agent = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        )
        url = (
            "http://www.birthcohorts.net/wp-content/themes/x-child/"
            "rss.cohorts.php?limit="
        )
        source_data = []
        page = 1
        studies = True
        while studies:
            response = requests.get(
                url + str(limit) + "&page=" + str(page) + "&json",
                headers={"User-Agent": user_agent},
            )
            page = page + limit

            if "cohort" not in response.json().keys():
                break  # All cohorts are retrieved

            source_data.extend(response.json()["cohort"])

        self._check_source_data(source_data)
        return source_data

    def get_datacatalogue_data(self):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        if self.catalogue.networks:
            networks = ""
            for network in self.catalogue.networks.split(","):
                networks = networks + json.dumps(network.strip()) + ", "

            query = (
                """query {Cohorts (filter: {networks: { id: { like:
            ["""
                + networks[:-2]
                + """]}}} ) {id, name, acronym, description, startYear,
             countries {name}, networks {id}}}"""
            )
        else:
            query = """query {Cohorts {id, name, acronym, description, startYear,
                    countries {name}, networks {id}}}"""

        url = self.catalogue.catalogue_url + "/catalogue/graphql"
        response = self.catalogue_session.post(
            url, headers=headers, json={"query": query}
        )

        source_data = response.json()["data"]["Cohorts"]
        self._check_source_data(source_data)
        return source_data

    def get_mica_data(self):
        """
        Retrieving study data from a Mica server
        """
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        mica_studies = []
        if self.catalogue.networks:
            mica_studies.extend(
                self._mica_network_study_ids(self.catalogue.networks, headers)
            )

        mica_studies.extend(self._mica_study_ids(headers))

        mica_data = self._mica_study_data(list(set(mica_studies)), headers)

        return mica_data

    def _mica_study_ids(self, headers, start: int = 0, batch_size: int = 100) -> List:
        """
        Get a list with study IDs from a catalogue by using the Mica REST API Client.
        The REST API Client that is used here returns not only the IDs,
        but also study information. It however turns out that this is
        'summary' information and it does not contain all necessary data
        for the EUCAN-Connect Catalogue. Therefore this API is only used for
        retrieving a list with study IDs. Depending on the value of param amount
        only the total amount of studies or the real study information is returned
        @param start: study number (row) to start from, default is 0
        @param batch_size: number of studies to be returned
                           if < totalCount, batch_size = totalCount
        @param headers: request headers
        """

        studies: list = []

        study_url = self.catalogue.catalogue_url + "/ws/studies/_rql"
        if not self.catalogue.catalogue_query:
            study_query = "query=study(limit(" + str(start) + ","
        else:
            study_query = (
                "query=study("
                + self.catalogue.catalogue_query
                + ",limit("
                + str(start)
                + ","
            )

        response = self.catalogue_session.post(
            study_url,
            headers=headers,
            data=study_query + str(batch_size) + "),fields(*))",
        )

        n_studies = response.json()["studyResultDto"]["totalHits"]

        if n_studies <= batch_size:
            studies_summary = response.json()["studyResultDto"][
                "obiba.mica.StudyResultDto.result"
            ]["summaries"]
        else:
            response = self.catalogue_session.post(
                study_url,
                headers=headers,
                data=study_query + str(n_studies) + "),fields(*))",
            )

            studies_summary = response.json()["studyResultDto"][
                "obiba.mica.StudyResultDto.result"
            ]["summaries"]

        for study in studies_summary:
            studies.append(study["id"])

        return studies

    def _mica_network_study_ids(self, mica_networks: str, headers: dict) -> List:
        """
        Get a list with study IDs that are in the networks in the list
        from a catalogue by using one of the Mica REST API Clients.
        The REST API Client that is used here returns not only the IDs, but also other
        network information. Only the study IDs are stored.

        @param mica_networks: List: a list with networks.
        @param headers: dict: headers to use in the API request.
        """
        studies: list = []
        for network in mica_networks.split(","):
            network_url = (
                self.catalogue.catalogue_url + "/ws/network/" + network.lower().strip()
            )

            response = self.catalogue_session.get(network_url, headers=headers)

            for study in response.json()["studySummaries"]:
                if study.get("design") == "cohort_study":
                    studies.append(study["id"])

        return studies

    def _mica_study_data(self, mica_studies: List, headers: dict):
        """
        Get the data of all studies from a catalogue by using the Mica REST API Client.
        It returns the complete study data.
        @param mica_studies: List: a list with the data of Mica studies.
        """
        source_data = []
        for study in mica_studies:
            study_url = self.catalogue.catalogue_url + "/ws/study/" + study
            response = self.catalogue_session.get(study_url, headers=headers)
            source_data.append(response.json())

        self._check_source_data(source_data)
        return source_data

    def _check_source_data(self, source_data: List):
        if len(source_data) == 0:
            raise EucanError(f"No {self.catalogue.description} source data found!")
        else:
            with self.printer.indentation():
                self.printer.print(
                    f"Number of {self.catalogue.description} studies is "
                    f"{len(source_data)}"
                )
