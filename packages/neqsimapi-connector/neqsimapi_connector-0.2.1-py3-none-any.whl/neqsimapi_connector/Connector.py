import asyncio
import json
from urllib.parse import urljoin

import httpx
import requests

from neqsimapi_connector.BearerAuth import BearerAuth

MAX_RETRIES = 3


def get_url_NeqSimAPI(use_test: bool = False) -> str:
    """Get base url to NeqSimAPI.

    Args:
        use_test (bool, optional): Set true to get url to test environment. Defaults to False.

    Returns:
        str: Base url to NeqSimAPI.
    """
    if use_test:
        return "https://api-neqsimapi-dev.radix.equinor.com"
    else:
        return "https://neqsimapi.app.radix.equinor.com"


def get_auth_NeqSimAPI() -> BearerAuth:
    """Get authentication object containing bearer token.

    Returns:
        BearerAuth: Authentication object for use with request session.
    """
    tenantID = "3aa4a235-b6e2-48d5-9195-7fcf05b459b0"
    client_id = "dde32392-142b-4933-bd87-ecdd28d7250f"
    scope = ["api://dde32392-142b-4933-bd87-ecdd28d7250f/Calculate.All"]

    return BearerAuth.get_bearer_token_auth(
        tenantID=tenantID, clientID=client_id, scopes=scope
    )


class Connector:
    """Class for getting data from NeqSimAPI restful api."""

    def __init__(
        self,
        url: str = "",
        auth: BearerAuth = None,
        verifySSL: bool = True,
        timeout: float = 180.0,
    ):
        if url is None or len(url) == 0:
            self.base_url = get_url_NeqSimAPI()
        else:
            self.base_url = url

        if auth is None:
            auth = get_auth_NeqSimAPI()
        elif isinstance(auth, str):
            auth = BearerAuth(str)
        elif isinstance(auth, dict) and "access_result" in auth:
            auth = BearerAuth(auth["access_result"])

        self.auth = auth
        self.verifySSL = verifySSL

        self.session = None
        self.async_client = None

        if timeout is None:
            # Set time out to 3 minutes
            timeout = 60 * 3

        self.timeout = timeout

    def calculate(
        self, url: str, inputpoints: list, async_endpoint: bool = False
    ) -> list:
        """Make concurrent requests to a single end point.
         Each request is called async at client. Supports async end points.


        Args:
            url (str): Full or partial url to end point.
            data (list): List of (dict) datapoints.
            async_endpoint (bool, optional): Set True if end point is async. Defaults to False.

        Returns:
            list: Calculation output as a list of dictionaries.
        """

        async def get_multiple_response(input: list, output: list) -> None:
            """Helper function to call endpoint multiple times. Has no output, but places results in output list.

            Args:
                input_data_list (list): _description_
                output (list): _description_

            Returns:
                NONE: Nothing
            """

            if self.async_client is None:
                self.init_async_client()

            async def get_single_response(data: dict, semaphore: asyncio.Semaphore):
                """Helper function to get async task to get response from endpoint for a single set of input data.

                Args:
                    data (dict): Input data to pass to calculation

                Returns:
                    dict: Result from end point.
                """

                async with semaphore:
                    # With semaphore, limits the number of concurrent tasks. with pattern takes care of aquire and release.
                    if async_endpoint:
                        # End point is async.
                        res = await self.async_client.post(url=url, json=data)
                        try:
                            self.verify_result(res=res)
                        except ValueError:
                            response = res
                            res_json = None

                        if isinstance(res.json(), dict) and "id" in res.json().keys():
                            calc_id = res.json()["id"]
                            res_url = urljoin(self.base_url, f"results/{calc_id}")
                            j = 0
                            while (
                                j < 12 * 30
                            ):  # Break after waiting for 30+ minutes (5 seconds in sleep below*12*30)
                                response = await self.async_client.get(res_url)
                                i = 0
                                while not response.is_success and i < MAX_RETRIES:
                                    i = i + 1
                                    response = await self.async_client.get(res_url)

                                res_json = response.json()
                                if (
                                    isinstance(res_json, dict)
                                    and "status" in res_json.keys()
                                    and res_json["status"] == "working"
                                ):
                                    await asyncio.sleep(5)
                                else:
                                    break
                                j = j + 1

                        if response.text is None or len(response.text) == 0:
                            return {}

                        if isinstance(res_json, dict) and "result" in res_json.keys():
                            return res_json["result"]
                        else:
                            return json.loads(response.text)
                    else:
                        # End point is not async, but using asyncio methods to free client resources.
                        i = 0
                        response = await self.async_client.post(url=url, json=data)
                        try:
                            self.verify_result(response)
                            while not response.is_success and i < MAX_RETRIES:
                                i = i + 1
                                await asyncio.sleep(5)
                                response = await self.async_client.post(
                                    url=url, json=data
                                )
                                self.verify_result(response)
                        except ValueError:
                            pass

                        if response.text is None or len(response.text) == 0:
                            return {}
                        return json.loads(response.text)

            s = asyncio.Semaphore(16)
            tasks = []
            for data in input:
                task = asyncio.create_task(get_single_response(data=data, semaphore=s))
                tasks.append(task)

            responses = await asyncio.gather(*tasks)
            for response in responses:
                output.append(response)

        if self.base_url not in url:
            url = urljoin(self.base_url, url)

        if not isinstance(inputpoints, list):
            if isinstance(inputpoints, dict):
                inputpoints = [inputpoints]
            else:
                try:
                    inputpoints = list(inputpoints)
                except ValueError:
                    inputpoints = [inputpoints]

        output = []
        loop = asyncio.get_event_loop()
        loop.run_until_complete(get_multiple_response(inputpoints, output))
        return output

    def get(self, url: str) -> requests.Response:
        """Wrapper for GET with retry functionality

        Args:
            url (str):  Full or partial url to end point.

        Returns:
            requests.Response: Response object from GET call.
        """
        if self.session is None:
            self.init_session()

        if self.base_url not in url:
            url = urljoin(self.base_url, url)

        connection_timeout = 9
        i = 0
        res = self.session.get(url, timeout=(connection_timeout, self.timeout))
        while not self.verify_result(res) and i < MAX_RETRIES:
            i = i + 1
            res = self.session.get(url, timeout=(connection_timeout, self.timeout))

        return res

    def get_results(self, calculation_id: str, a_sync: bool = True) -> dict:
        """Get results from async end point with calculation id.

        Args:
            calculation_id (str): Calculation id. Returned when starting calculation with post or post_async.
            a_sync (bool, optional): Set False to loop internally while waiting for a reply from the calculation. Defaults to True.

        Returns:
            dict: Results when finished or dictionary with status.
        """

        res = self.get(url=urljoin(self.base_url, f"results/{calculation_id}"))

        if a_sync:
            return res.json()
        else:
            res = res.json()
            while (
                isinstance(res, dict)
                and "status" in res.keys()
                and res["status"] == "working"
            ):
                res = self.get_results(calculation_id=calculation_id, a_sync=a_sync)

            if isinstance(res, dict) and "result" in res.keys():
                res = res["result"]

        return res

    def post(self, url: str, data: dict) -> requests.Response:
        """Wrapper for POST with retry functionality.

        Args:
            url (str): Full or partial url to end point.
            data (dict): Data to pass to calculation.

        Returns:
            requests.Response: Response object from POST call.
        """
        if self.session is None:
            self.init_session()

        if self.base_url not in url:
            url = urljoin(self.base_url, url)

        connection_timeout = 9
        i = 0
        res = self.session.post(
            url, json=data, timeout=(connection_timeout, self.timeout)
        )

        while not self.verify_result(res) and i < MAX_RETRIES:
            i = i + 1
            res = self.session.post(
                url, json=data, timeout=(connection_timeout, self.timeout)
            )

        return res

    def post_result(self, url: str, data: dict) -> dict:
        res = self.post(url=url, data=data)

        return res.json()

    def post_async(self, url: str, data: dict) -> dict:
        """Post data to async endpoint and get status.
        NB! Results must be gotten with get_results()

        Args:
            url (str): Full or partial url to end point.
            data (dict): Data to pass to calculation.

        Returns:
            dict: Status dict or None if endpoint is not async.
        """
        res_json = self.post_result(url, data)

        if isinstance(res_json, dict) and "id" in res_json.keys():
            return res_json["id"], res_json["status"]

        return None

    def init_session(self):
        """Initialize Session object."""
        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.verify = self.verifySSL
        if self.verifySSL is False:
            requests.packages.urllib3.disable_warnings(
                requests.packages.urllib3.exceptions.InsecureRequestWarning
            )

    def init_async_client(self):
        """Initialize Async Client object."""
        connection_timeout = 9
        self.async_client = httpx.AsyncClient(
            auth=self.auth,
            timeout=httpx.Timeout(connection_timeout, pool=None, read=self.timeout),
        )

    def verify_result(self, res) -> int:
        if not isinstance(res, requests.models.Response) and not isinstance(
            res, httpx.Response
        ):
            print(res)

        if res.status_code == 200 or res.status_code == 202:
            return 1

        if res.status_code == 422:
            try:
                d = json.loads(res.text)
                d = d["detail"][0]
                property = d["loc"][1]
                msg = d["loc"][1]
            except Exception as ex:
                print(res.text)
                raise

            raise ValueError(
                f"Failed getting result input {property} is out of range, {msg}"
            )

        if res.status_code in [429, 500, 503, 504]:
            return 0

        if res.status_code > 400:
            res.raise_for_status()
