import pycanlii.pycanliibase as base
import pycanlii.enums as enums
import requests
from bs4 import BeautifulSoup

class CaseDatabase(base.PyCanliiBase):
    """
    A database of CanLII Cases. This object is both indexable and iterable. These are both abstractions of the API.
    The API allows a maximum of 10000 cases at a time, so when populating the database it will grab all of the cases
    for you. If you are doing a loop or indexing very far into a CaseDatabase that is very large, be wary of 403 response codes,
    as by default you're limited to 10 requests per second by the CanLII API. When a 403 response code is received an
    HTTPError will be raised.

    Attributes:
        :name: A string representing the name of this CaseDatabase
        :id: A string representing the ID of this caseDatabase
        :jurisdiction: A Jurisdiction enum instance representing the Jurisdiction of this case
    """

    def __init__(self, data, apikey, language=enums.Language.en):
        base.PyCanliiBase.__init__(self, apikey, language)
        self.name = data['name']
        self.id = data["databaseId"]
        self.jurisdiction = enums.Jurisdiction[data['jurisdiction']]
        self._cases = []
        self._index = 0
        self._full = False

    def _getCases(self, extension=10000):
        cases = self._request("http://api.canlii.org/v1/caseBrowse", True, self.id,
                              offset=self._index, resultCount=extension).json()['cases']

        self._index += len(cases)
        if (len(cases) < extension):
            self._full = True

        for case in cases:
            self._cases.append(Case(case, self._key))


    def __iter__(self):
        i = 0
        while(not self._full):
            self._getCases()
            while i < self._index:
                yield self._cases[i]
                i += 1

    def __getitem__(self, item):
        i = 0
        while(self._index <= item):
            self._getCases()
        return self._cases[i]



class Case(base.PyCanliiBase):
    """
    An object representing a CanLII Case

    Attributes:
        :content: A BeautifulSoup object representing the HTML content of this case
        :caseId: A string representing the caseId of this case
        :databaseId: A string representing the databaseId of this case
        :title: A string representing the title of this case
        :citation: A string representing the citation of this case
        :url: A string representing the URL where this case can be found
        :docketNumber: A string representing the docketNumber of this case
        :startDate: A date object  date of this case
    """

    def __init__(self, data, apikey):
        caseid = data["caseId"]
        if type(caseid) == str:
            self.caseId = caseid
        elif 'en' in caseid:
            self.caseId = caseid["en"]
            language = enums.Language.en
        else:
            self.caseId = caseid["fr"]
            language = enums.Language.fr
        base.PyCanliiBase.__init__(self, apikey, language)
        self.databaseId = data['databaseId']
        self.title = data['title']
        self.citation = data['citation']

        self._populated = False
        self._url = None
        self._docketNumber = None
        self._decisionDate = None

        # Used to store the content of the case
        self._content = None

    def _populate(self):
        if not self._populated:
            case = self._request("http://api.canlii.org/v1/caseBrowse", True, self.databaseId, self.caseId)
            case = case.json()
            self._url = case['url']
            self._docketNumber = case['docketNumber']
            self._decisionDate = self._getDate(case['decisionDate'])

            self._populated = True

    @property
    def content(self):
        if not self._content:
            req = requests.get(self.url)
            self._content = req.content

        return self._content

    def citedCases(self):
        """
        Returns a list of up to a maximum of 5 cases that are cited by this one.

        :return: A list of up to a maximum of 5 cases that are cited by this one, if there are no cited cases, None is returned
        """
        response = self._request("http://api.canlii.org/v1/caseCitatorTease/", True,
                            self.databaseId, self.caseId, "citedCases").json()

        if "citedCases" in response:
            cases = response["citedCases"]
            l = []
            for case in cases:
                l.append(Case(case, self._key))
            return l
        else:
            return None

    def citingCases(self):
        """
        Returns a list of up to a maximum of 5 cases that are citing this one.

        :return: A list of up to a maximum of 5 cases that are citing this one, if there are no citing cases, None is returned
        """
        response = self._request("http://api.canlii.org/v1/caseCitatorTease/", True,
                            self.databaseId, self.caseId, "citingCases").json()

        if "citingCases" in response:
            cases = response["citingCases"]
            l = []
            for case in cases:
                l.append(Case(case, self._key))
            return l
        else:
            return None

    def citedLegislation(self):
        """
        Returns a list of up to a maximum of 5 pieces of legislation that are cited by this one.

        :return: A list of up to a maximum of 5 pieces of legislation that are cited by this one, if there are no cited
         legislation, None is returned
        """
        response = self._request("http://api.canlii.org/v1/caseCitatorTease/", True,
                            self.databaseId, self.caseId, "citedLegislations").json()

        if "citedCases" in response:
            cases = response["citedLegislation"]
            l = []
            for case in cases:
                l.append(Case(case, self._key))
            return l
        else:
            return None

    @property
    def url(self):
        self._populate()
        return self._url

    @property
    def docketNumber(self):
        self._populate()
        return self._docketNumber

    @property
    def decisionDate(self):
        self._populate()
        return self._decisionDate
