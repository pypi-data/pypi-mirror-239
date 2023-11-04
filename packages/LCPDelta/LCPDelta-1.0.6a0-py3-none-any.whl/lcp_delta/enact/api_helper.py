import requests
import json
import calendar
from datetime import date, datetime
import pandas as pd
from lcp_delta import global_helper_methods
from typing import List, Dict

from .credentials_holder import CredentialsHolder
class APIHelper:

    def __init__(self, username : str, public_api_key : str):
        """ Enter your credentials and use the methods below to get data from Enact.

        Args:
            username (str): Enact Username. Please contact the Enact team if you are unsure about what your username or public api key are.
            public_api_key (str): Public API Key provided by Enact. Please contact the Enact team if you are unsure about what your username or public api key are.
        """
        self.enact_credentials = CredentialsHolder(username, public_api_key)

    # Helper functions
    @staticmethod
    def convert_date_time_to_right_format(date_time_to_check : datetime) -> str:
        if not (isinstance(date_time_to_check, date) or isinstance(date_time_to_check, datetime)):
            raise TypeError('Inputted date must be a date or datetime')

        converted_date = date_time_to_check.strftime('%Y-%m-%dT%H:%M:%SZ')
        return converted_date

    def post_request(self, endpoint : str, request_details : Dict, verify=None):
        headers = {'Authorization': 'Bearer ' + self.enact_credentials.bearer_token,
                   'Content-Type': 'application/json',
                   'cache-control': 'no-cache'}

        response_raw = requests.post(endpoint, data=json.dumps(request_details), headers = headers, verify=verify)

        if response_raw.status_code != 200:
            response_raw = self.handle_error_and_get_updated_response(endpoint, request_details, headers, response_raw)

        response = json.loads(response_raw.text)

        if 'Messages' in response:
            self.raise_exception_for_enact_error(response)
        return response

    def handle_error_and_get_updated_response(self, endpoint : str, request_details : Dict, headers , response_raw):
        # check if bearer token has expired and if it has create a new one
        if response_raw.status_code == 401 and 'WWW-Authenticate' in response.headers:
            response_raw = self.handle_authorisation_error(endpoint, request_details, headers)

        if response_raw.status_code == 400:
           raise Exception(json.loads(response_raw.text))

        response = json.loads(response_raw.text)
        return response

    def raise_exception_for_enact_error(self, response):
        error_messages = response['Messages']
        for error_message in error_messages:
            if 'ErrorCode' in error_message and error_message['ErrorCode']:
                # An error code is present, so raise an exception with the error message
                raise Exception(f"ErrorCode: {error_message['ErrorCode']}. {error_message['Message']}")

    def handle_authorisation_error(self, endpoint : str, request_details : Dict, headers : Dict):
        retry_count = 0
        while retry_count < self.enact_credentials.MAX_RETRIES:
            self.enact_credentials.get_bearer_token(self.enact_credentials.username, self.enact_credentials.public_api_key)
            headers['Authorization'] = 'Bearer ' + self.enact_credentials.bearer_token

                # Retry the POST request with the new bearer token
            response = requests.post(endpoint, data=json.dumps(request_details), headers=headers)

            if response.status_code != 401:
                    # Successful response, no need to retry
                break

            retry_count += 1

        if retry_count == self.enact_credentials.MAX_RETRIES:
            raise Exception("Failed to obtain a valid bearer token after multiple attempts.")
        return response

    # Series:
    def get_series_data(self, series_id : str, date_from : datetime.date, date_to : datetime.date, country_id : str, option_id : List[str] = None, half_hourly_average : bool = False, request_time_zone_id : str = None, time_zone_id : str = None) -> pd.DataFrame:
        """Get series data for a specific series ID.

        This method retrieves the series data for a specific series ID from the Enact API. It allows specifying the date range, option ID, half-hourly average, and country ID.

        Args:
            series_id `str`: This is the Enact ID for the requested series, as defined in the query generator on the 'General' tab.

            date_from `datetime.datetime`: This is the start of the date-range being requested. Defaults to today's date.

            date_to `datetime.datetime`: This is the end of the date-range being requested. If a single day is wanted, then this will be the same as the From value. Defaults to today's date.

            option_id `List[str]`: If the selected Series has options, then this is the Enact ID for the requested Option, as defined in the query generator on the 'General' tab. If this is not sent, then data for all options will be sent back (but capped to the first 10). Defaults to None.

            country_id `str` (optional): The country ID for filtering the data. Defaults to "Gb".

            half_hourly_average `bool` (optional): Flag to indicate whether to retrieve half-hourly average data. Defaults to False.

        Note that the arguments required for specific enact data can be found on the site.

        Returns:
            Response: The response object containing the series data.
        """
        endpoint = 'https://enactapifd.lcp.uk.com/EnactAPI/Series/Data_V2'

        date_from = self.convert_date_time_to_right_format(date_from)
        date_to = self.convert_date_time_to_right_format(date_to)

        request_details = {
            "SeriesId": series_id,
            "CountryId": country_id,
            "From": date_from,
            "To": date_to,
            "halfHourlyAverage": half_hourly_average
        }

        if option_id is not None:
            if not global_helper_methods.is_list_of_strings(option_id):
                raise Exception("Option ID input must be a list of strings")
            request_details["OptionId"] = option_id

        if request_time_zone_id is not None:
            request_details["requestTimeZoneId"] = request_time_zone_id

        if time_zone_id is not None:
            request_details["timeZoneId"] = time_zone_id

        response = self.post_request(endpoint, request_details)

        try:

            df = pd.DataFrame(response['data'])
            first_key = next(iter(response['data']))
            df = df.set_index(first_key)

            return df
        except (ValueError, TypeError, IndexError):
            return response

    def get_series_info(self, series_id : str, country_id : str = None) -> Dict:
        """Get information about a specific series.

        This method retrieves information about a specific series based on the given series ID. Optional country ID can be provided to filter the series information.

        Args:
            series_id `str`: This is the Enact ID for the requested series, as defined in the query generator on the 'General' tab.
            country_id `str` (optional): The country ID to filter the series information. Defaults to None. If this is not provided, then details will be displayed for the first country available for this series.
        """
        endpoint = 'https://enactapifd.lcp.uk.com/EnactAPI/Series/Info'
        request_details = {
            "SeriesId": series_id
        }

        if country_id is not None:
            request_details["CountryId"] = country_id

        response = self.post_request(endpoint, request_details)
        return response

    # Plant Details:
    def get_plant_details_by_id(self, plant_id : str) -> Dict:
        """Get details of a plant based on the plant ID.

        This method retrieves details of a specific plant based on the provided plant ID.
        Args:
            plant_id `str`: The ID of the plant to retrieve details for.
        """
        endpoint = 'https://enactapifd.lcp.uk.com/EnactAPI/Plant/Data/PlantInfo'
        request_details = {
            "PlantId": plant_id
        }
        response = self.post_request(endpoint, request_details)
        return response

    def get_plants_by_fuel_and_country(self, fuel_id : str, country_id : str) -> List[str]:
        """Get a list of plants based on fuel and country.

        This method retrieves a list of plants based on the specified fuel and country.

        Args:
            fuel_id `str`: The fuel that you would like plant data for.
            country_id `str` (optional): The country that you would like the plant data for. Defaults to "Gb".

        Returns:
            Response: The response object containing the plant data.
        """
        endpoint = 'https://enactapifd.lcp.uk.com/EnactAPI/Plant/Data/PlantList'

        request_details = {
            "Country": country_id,
            "Fuel": fuel_id
        }
        response = self.post_request(endpoint, request_details)
        return response

    #History of Forecasts:
    def get_history_of_forecast_for_given_date(self, series_id : str, date : datetime, country_id : str, option_id : str = None) -> pd.DataFrame:
        """Gets the history of a forecast for a given date

        Args:
            series_id `str`: The Enact ID for the requested Series, as defined in the query generator on the 'General' tab.

            date `datetime.date`: The date you want all iterations of the forecast for.

            country_id `str` (optional): This is the Enact ID for the requested Country, as defined in the query generator on the 'General' tab. Defaults to "Gb".

            option_id `List[str]` (optional): If the selected Series has options, then this is the Enact ID for the requested Option, as defined in the query generator on the 'General' tab.
                                          If this is not sent, then data for all options will be sent back (but capped to the first 10). Defaults to None.
        Returns:
            Response: This holds all data for the requested series on the requested date .
                    The first row will provide all the dates we have a forecast iteration for.
                    All other rows correspond to the data-points at each value of the first array.
        """
        endpoint = 'https://enactapifd.lcp.uk.com/EnactAPI/HistoryOfForecast/Data_V2'

        date = self.convert_date_time_to_right_format(date)

        request_details = {
            "SeriesId": series_id,
            "CountryId": country_id,
            "Date": date,
        }

        if option_id is not None:
            if not global_helper_methods.is_list_of_strings(option_id):
                raise Exception("Option ID input must be a list of strings")
            request_details["OptionId"] = option_id

        response = self.post_request(endpoint, request_details)

        data = response['data']
        df = pd.DataFrame(data)
        first_key = next(iter(data))
        df = df.set_index(first_key)

        return df

    def get_history_of_forecast_for_date_range(self, series_id : str, date_from : str, date_to : str, country_id : str, option_id : List[str] = None) -> Dict[str, pd.DataFrame]:
        """Gets the history of a forecast for a given date

        Args:
            series_id `str`: The Enact ID for the requested Series, as defined in the query generator on the 'General' tab.
            date_from `datetime.datetime`: The start date you want all iterations of the forecast for.
            date_to `datetime.datetime`: The end date you want all iterations of the forecast for.
            country_id `str` (optional): This is the Enact ID for the requested Country, as defined in the query generator on the 'General' tab. Defaults to "Gb".
            option_id `List[str]` (optional): If the selected Series has options, then this is the Enact ID for the requested Option, as defined in the query generator on the 'General' tab.
                                          If this is not sent, then data for all options will be sent back (but capped to the first 10). Defaults to None.
        Returns:
            Response: This holds all data for the requested series on the requested date .
                    The first row will provide all the dates we have a forecast iteration for.
                    All other rows correspond to the data-points at each value of the first array.
        """
        endpoint = 'https://enactapifd.lcp.uk.com/EnactAPI/HistoryOfForecast/Data_V2'

        date_from = self.convert_date_time_to_right_format(date_from)
        date_to = self.convert_date_time_to_right_format(date_to)

        request_details = {
            "SeriesId": series_id,
            "CountryId": country_id,
            "From": date_from,
            "To": date_to
        }

        if option_id is not None:
            if not global_helper_methods.is_list_of_strings(option_id):
                raise Exception("Option ID input must be a list of strings")
            request_details["OptionId"] = option_id

        response = self.post_request(endpoint, request_details)

        output : Dict[str, pd.DataFrame] = {}
        for date_str, data in response['data'].items():
            df = pd.DataFrame(data)
            first_key = next(iter(data))
            df = df.set_index(first_key)
            output[date_str] = df

        return output

    #BOA:
    def get_bm_data_by_period(self, date : datetime, period : int, include_accepted_times : bool = False) -> Dict:
        """Get BM (Balancing Mechanism) data for a specific date and period.

        This method retrieves the BM (Balancing Mechanism) data for a specific date and period.
        The date should be in the correct format, and the period should be an integer.

        Args:
            date `datetime.datetime`: The date that you would like the BOD data for.
            period `int`: The period for which to retrieve the BM data.
            include_accepted_times `bool`: Choose whether object include BOA accepted times or not

        Returns:
            Response: The response object containing the BM data.

        Raises:
            TypeError: If the period is not an integer.
        """

        endpoint = 'https://enactapifd.lcp.uk.com/EnactAPI/BOA/Data'

        if not isinstance(period, int):
            raise TypeError('Please enter an integer period')

        date = self.convert_date_time_to_right_format(date)

        request_details = {
            "Date": date,
            "Period": period
        }

        if include_accepted_times is not False:
            request_details["includeAcceptedTimes"] = "True"

        response = self.post_request(endpoint, request_details)
        return response

    def get_bm_data_by_search(self, date : datetime, option : str = "all", search_string : str = None, include_accepted_times : bool = False) -> Dict:
        """Get BM data based for a specific date and search criteria.

        Args:
            date `datetime.datetime`: The date for which to retrieve the BM data.
            option `str`: This allows you to select whether you want to search for BOA data for plants, fuels or just return everything. Can be set to "plant", "fuel", "all"
            search_string `str`: The search string to match against the BM data. If Option is "plant", this allows you to search for all BOA actions from plants with BMU ID containing "CARR" (e.g. all Carrington units).
                                If option is "fuel", this allows you to search for all BOA actions from plants with fuel type "Coal". If Option is "all", this must not be sent to work.        
            include_accepted_times `bool`: Determine whether the returned object includes a column for accepted times in the response object
        Returns:
            Response: The response object containing the BM data.
        """
        endpoint = 'https://enactapifd.lcp.uk.com/EnactAPI/BOA/Data'

        date = self.convert_date_time_to_right_format(date)

        request_details = {
            "Date": date,
            "Option": option,
            "SearchString" : search_string
        }

        if include_accepted_times is not False:
            request_details["includeAcceptedTimes"] = "True"

        response = self.post_request(endpoint, request_details)
        return response

    #Leaderboard:
    def get_leaderboard_data(self, date_from, date_to, revenue_metric = "PoundPerMwPerH", market_price_assumption = "WeightedAverageDayAheadPrice", gas_price_assumption = "DayAheadForward") -> pd.DataFrame:
        """Get leaderboard data for a specific date range.

        Args:
            date_from `datetime.datetime`: The start date of the leaderboard data.

            date_to `datetime.datetime`: The end date of the leaderboard data.
                                     If a single day is wanted, then this will be the same as the From value.

            revenue_metric `str` (optional): This is the unit which revenues will be measured in for the leaderboard.
                                            Possible options are: Pound or PoundPerMwPerH.
                                            If not included the default is PoundPerMwPerH.

            market_price_assumption `str` (optional): This is the price assumption for wholesale revenues on the leaderboard.
                                                     Possible options are: WeightedAverageDayAheadPrice, EpexDayAheadPrice, NordpoolDayAheadPrice, IntradayPrice or BestPrice.
                                                     Defaults to WeightedAverageDayAheadPrice.

            gas_price_assumption `str` (optional): The gas price assumption to filter the leaderboard data.
                                                  Possible options are: DayAheadForward, DayAheadSpot, WithinDaySpot or CheapestPrice.
                                                  If not included the default is DayAheadForward.
        """

        endpoint = 'https://enactapifd.lcp.uk.com/EnactAPI/Leaderboard/Data'

        date_from = self.convert_date_time_to_right_format(date_from)
        date_to = self.convert_date_time_to_right_format(date_to)

        request_details = {
            "From" : date_from,
            "To" : date_to,
            "RevenueMetric" : revenue_metric,
            "MarketPriceAssumption" : market_price_assumption,
            "GasPriceAssumption" : gas_price_assumption
        }

        response = self.post_request(endpoint, request_details)

        df = pd.DataFrame(response['data'][1:])
        df.columns = response['data'][0]
        df = df.set_index('Plant - ID')

        return df

    #Ancillary Contracts:
    def get_ancillary_contract_data(self, ancillary_contract_type : str, option_one : str | int, option_two : int | str = None) -> Dict:
        endpoint = 'https://enactapifd.lcp.uk.com/EnactAPI/Ancillary/Data'

        request_details = {
            "AncillaryContractType" : ancillary_contract_type,
            "OptionOne": option_one,
        }

        if option_two is not None:
            request_details["OptionTwo"] = option_two

        response = self.post_request(endpoint, request_details)
        return response

    def get_DCL_contracts(self, date_requested : datetime) -> pd.DataFrame:
        """Returns DCL (Dynamic Containment Low) contracts for a provided day

        Args:
            date_requested `datetime.datetime`: The date for which to retrieve DCL contracts.

        Raises:
            TypeError: If the inputted date is not of type `date` or `datetime`.
        """
        if not (isinstance(date_requested, date) or isinstance(date_requested, datetime)):
            raise TypeError('Requested date must be of type date or datetime')
        month_year = "-".join([str(date_requested.month), str(date_requested.year)])
        response = self.get_ancillary_contract_data("DynamicContainmentEfa", month_year, date_requested.day)

        return self.convert_api_response_for_dynamic_product(response)

    def get_DCH_contracts(self, date_requested : datetime) -> pd.DataFrame:
        """Returns DCH (Dynamic Containment High) contracts for a provided day

        Args:
            date_requested (datetime.date or datetime.datetime): The date for which to retrieve DCH contracts.

        Raises:
            TypeError: If the inputted date is not of type `date` or `datetime`.
        """
        if not (isinstance(date_requested, date) or isinstance(date_requested, datetime)):
            raise TypeError('Requested date must be a date or datetime')
        month_year = "-".join([str(date_requested.month), str(date_requested.year)])
        response = self.get_ancillary_contract_data("DynamicContainmentEfaHF", month_year, date_requested.day)
        return self.convert_api_response_for_dynamic_product(response)

    def get_DML_contracts(self, date_requested : datetime) -> pd.DataFrame:
        """Returns DML (Dynamic Moderation Low) contracts for a provided day

        Args:
            date_requested `datetime.datetime`: The date for which to retrieve DML contracts.

        Raises:
            TypeError: If the inputted date is not of type `date` or `datetime`.
        """
        if not (isinstance(date_requested, date) or isinstance(date_requested, datetime)):
            raise TypeError('Requested date must be a date or datetime')
        month_year = "-".join([str(date_requested.month), str(date_requested.year)])
        response = self.get_ancillary_contract_data("DynamicModerationLF", month_year, date_requested.day)
        return self.convert_api_response_for_dynamic_product(response)

    def get_DMH_contracts(self, date_requested : datetime) -> pd.DataFrame:
        """Returns DMH (Dynamic Moderation High) contracts for a provided day

        Args:
            date_requested (datetime.date or datetime.datetime): The date for which to retrieve DMH contracts.

        Raises:
            TypeError: If the inputted date is not of type `date` or `datetime`.
        """
        if not (isinstance(date_requested, date) or isinstance(date_requested, datetime)):
            raise TypeError('Requested date must be a date or datetime')
        month_year = "-".join([str(date_requested.month), str(date_requested.year)])
        response = self.get_ancillary_contract_data("DynamicModerationHF",month_year, date_requested.day)
        return self.convert_api_response_for_dynamic_product(response)

    def get_DRL_contracts(self, date_requested : datetime) -> pd.DataFrame:
        """Returns DRL (Dynamic Regulation Low) contracts for a provided day

        Args:
            date_requested `datetime.date`: The date for which to retrieve DRL contracts.

        Raises:
            TypeError: If the inputted date is not of type `date` or `datetime`.
        """
        if not (isinstance(date_requested, date) or isinstance(date_requested, datetime)):
            raise TypeError('Inputted date must be a date or datetime')
        month_year = "-".join([str(date_requested.month), str(date_requested.year)])
        response = self.get_ancillary_contract_data("DynamicRegulationLF", month_year, date_requested.day)
        return self.convert_api_response_for_dynamic_product(response)

    def get_DRH_contracts(self, date_requested : datetime) -> pd.DataFrame:
        """Returns DRH (Dynamic Regulation High) contracts for a provided day

        Args:
            date `datetime.date`: The date for which to retrieve DRH contracts.

        Raises:
            TypeError: If the inputted date is not of type `date` or `datetime`.
        """
        if not (isinstance(date_requested, date) or isinstance(date_requested, datetime)):
            raise TypeError('Requested date must be a date or datetime')
        month_year = "-".join([str(date_requested.month), str(date_requested.year)])
        response = self.get_ancillary_contract_data("DynamicRegulationHF", month_year, date_requested.day)
        return self.convert_api_response_for_dynamic_product(response)

    def convert_api_response_for_dynamic_product(self, response : Dict) -> pd.DataFrame:
        df = pd.DataFrame(response['data'][0]['Data'])
        df = df.set_index('orderId')
        return df

    def get_FFR_contracts(self, tender_number) -> pd.DataFrame:
        """Returns FFR (Firm Frequency Response) tender results for a given tender round

        Args:
            tender_number `int`: The tender number for the round that you wish to procure
        """
        response = self.get_ancillary_contract_data("Ffr",tender_number)

        df = pd.DataFrame(response['data'][0]['DataByTender'])
        df = df.set_index('tenderNumber')

        return df

    def get_STOR_contracts(self, date_requested : datetime) -> pd.DataFrame:
        """Returns STOR (Short Term Operating Reserve) results for a given date

        Args:
            date_requested `datetime.date`: The date for which to retrieve STOR contracts.

        Raises:
            TypeError: If the inputted date is not of type `date` or `datetime`.
        """
        if not (isinstance(date_requested, date) or isinstance(date_requested, datetime)):
            raise TypeError('Requested date must be a date or datetime')
        year_month_day = "-".join([str(date_requested.year), str(date_requested.month), str(date_requested.day)])
        response = self.get_ancillary_contract_data("StorDayAhead",year_month_day)

        df = pd.DataFrame(response['data'][0]['Data'])

        return df

    def get_SFFR_contracts(self, date_requested : datetime) -> pd.DataFrame:
        """Returns SFFR (Static Firm Frequency Response) results for a given date

        Args:
            date_requested `datetime.date`: The date for which to retrieve SFFR contracts.

        Raises:
            TypeError: If the inputted date is not of type `date` or `datetime`.
        """
        if not (isinstance(date_requested, date) or isinstance(date_requested, datetime)):
            raise TypeError('Requested date must be a date or datetime')

        month_year = "-".join([str(date_requested.month), str(date_requested.year)])
        response = self.get_ancillary_contract_data("SFfr", month_year, date_requested.day)

        df = pd.DataFrame(response['data'][0]['DataByRow'])

        return df

    def get_MFR_contracts(self, month : int, year : int) -> pd.DataFrame:
        """Returns MFR tender results for a given month and year

        Args:
            month `int`: Corresponding month for the data requested
            year `int`: Corresponding year for the data requested
        """
        if not 0 < month <= 12:
            raise ValueError("Month must be an integer less than 12")
        month_name = calendar.month_name[month]

        response = self.get_ancillary_contract_data("ManFr", year, month_name)

        updated_rows = []

        for row in response['data'][0]['DataByPlant']:
            price_data = row['data']
            del row['data']
            price_data.update(row)
            updated_rows.append(price_data)

        df = pd.DataFrame(updated_rows)

        return df
    #News table
    def get_news_table(self, table_id : str) -> List:
        """Will return the selected mews table you would like data from.

        Args:
            table_id `str`: This is the News table you would like the data from. The options include:

                            Table Header                                            Table ID:
                            BM Warming Instructions	                                BmStartupDetails
                            Forward BSAD Trades	                                    Bsad
                            Additional MW changes (additional GT / SEL reduction	CapacityChanges
                            Triads	                                                Traids
                            Elexon System Warnings	                                Elexon
                            LCP Alerts	                                            LCP
                            Entsoe News	                                            Entsoe

        """
        endpoint = 'https://enactapifd.lcp.uk.com/EnactAPI/Newstable/Data'
        request_details = {
            "TableId" : table_id,
        }

        response = self.post_request(endpoint, request_details)
        return response
    # EPEX:
    def get_epex_trades_by_contract_id(self, contract_id : str) -> List:
        """Get executed EPEX trades of a contract, given the Contract ID

        Args:
            contract_id `int`: The ID associated with the EPEX contract you would like executed trades for.

        """
        endpoint = 'https://enact-epex.azurefd.net/EnactAPI/Data/TradesFromContractId'

        request_details = {
            "ContractId" : contract_id,
        }

        response = self.post_request(endpoint, request_details)
        return response

    def get_epex_trades(self, type : str, date : datetime, period : int) -> List:
        """Get executed EPEX trades of a contract, given the date, period and type

        Args:
            type `str`: The type associated with the EPEX contract you would like executed trades for. The options are "HH", "1H", "2H", "4H", "3 Plus 4", "Overnight", "Peakload", "Baseload", "Ext. Peak".

            date `datetime.datetime`: The date associated with the EPEX contract you would like executed trades for.

            period `int`: The period associated with the EPEX contract you would like executed trades for.

        Raises:
            `TypeError`: If the period is not an integer.
                       If the inputted date is not of type `date` or `datetime`.

        """
        endpoint = 'https://enact-epex.azurefd.net/EnactAPI/Data/Trades'

        date = self.convert_date_time_to_right_format(date)

        if not isinstance(period, int):
            raise TypeError('Please enter an integer period')

        request_details = {
            "Type" : type,
            "Date" : date,
            "Period" : period
        }

        response = self.post_request(endpoint, request_details)
        return response

    def get_epex_order_book(self, type : str, date : datetime, period : int) -> Dict:
        """Get order book of a contract,given the date, period and type

        Args:
            type `str`: The type associated with the EPEX contract you would like executed trades for. The options are "HH", "1H", "2H", "4H", "3 Plus 4", "Overnight", "Peakload", "Baseload", "Ext. Peak".

            date `datetime.datetime`: The date associated with the EPEX contract you would like executed trades for.

            period `int`: The period associated with the EPEX contract you would like executed trades for.

        Raises:
            `TypeError`: If the period is not an integer.
                       If the inputted date is not of type `date` or `datetime`.
        """
        endpoint = 'https://enact-epex.azurefd.net/EnactAPI/Data/OrderBook'

        date = self.convert_date_time_to_right_format(date)

        if not isinstance(period, int):
            raise TypeError('Please enter an integer period')

        request_details = {
            "Type" : type,
            "Date" : date,
            "Period" : period
        }

        response = self.post_request(endpoint, request_details)
        return response

    def get_epex_order_book_by_contract_id(self, contract_id : str):
        """Get EPEX order book by contract ID

        Args:
            contract_id `int`: The ID associated with the EPEX contract you would like the order book for.

        """
        endpoint = 'https://enact-epex.azurefd.net/EnactAPI/Data/OrderBookFromContractId'

        request_details = {
            "ContractId" : contract_id,
        }

        response = self.post_request(endpoint, request_details)
        return response

    def get_epex_contracts(self, date : datetime) -> List:
        """Get EPEX contracts for a given day

        Args:
            date `datetime.datetime`: The date you would like all contracts for.

        Raises:
            `TypeError`: If the inputted date is not of type `date` or `datetime`.

        """
        endpoint = 'https://enact-epex.azurefd.net/EnactAPI/Data/Contracts'

        date = self.convert_date_time_to_right_format(date)

        request_details = {
            "Date" : date,
        }

        response = self.post_request(endpoint, request_details)
        return response