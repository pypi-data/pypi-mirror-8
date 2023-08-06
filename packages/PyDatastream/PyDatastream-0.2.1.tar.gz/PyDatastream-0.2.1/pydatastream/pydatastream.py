import pandas as pd
import datetime as dt
import warnings
from suds.client import Client

### TODO: RequestRecordAsXML is more efficient than RequestRecord as it does not return
###       datatypes for each value (thus response is ~2 times smaller)
### TODO: Constituesnts: L___~LIST~REP and not ~XREF (deprecated)
### TODO: ~REP for static requests
### TODO: Check "datatype search" for useful requests

WSDL_URL = 'http://dataworks.thomson.com/Dataworks/Enterprise/1.0/webserviceclient.asmx?WSDL'


class DatastreamException(Exception):
    pass


class Datastream:
    def __init__(self, username, password, url=WSDL_URL):
        """Creating connection to the Thomson Reuters Dataworks Enterprise (DWE) server
           (former Thomson Reuters Datastream).
        """
        self.client = Client(url, username=username, password=password)

        self.show_request = False   # If True then request string will be printed
        self.last_status = None     # Will contain status of last request
        self.raise_on_error = True  # if True then error request will raise, otherwise
                                    # either empty dataframe or partially retrieved
                                    # data will be returned

        ### Trying to connect
        try:
            self.ver = self.version()
        except:
            raise DatastreamException('Can not retrieve the data')

        ### Creating UserData object
        self.userdata = self.client.factory.create('UserData')
        self.userdata.Username = username
        self.userdata.Password = password

        ### Check available data sources
        if 'Datastream' not in self.sources():
            warnings.warn("'Datastream' source is not available for given subscription!")

    @staticmethod
    def info():
        print 'Datastream Navigator:'
        print 'http://product.datastream.com/navigator/'
        print ''
        print 'Datastream documentation:'
        print 'http://dtg.tfn.com/data/DataStream.html'
        print ''
        print 'Dataworks Enterprise documentation:'
        print 'http://dataworks.thomson.com/Dataworks/Enterprise/1.0/'

    def version(self):
        """Return version of the TR DWE."""
        res = self.client.service.Version()
        return '.'.join([str(x) for x in res[0]])

    def system_info(self):
        """Return system information."""
        res = self.client.service.SystemInfo()
        res = {str(x[0]):x[1] for x in res[0]}

        to_str = lambda arr: '.'.join([str(x) for x in arr[0]])
        res['OSVersion'] = to_str(res['OSVersion'])
        res['RuntimeVersion'] = to_str(res['RuntimeVersion'])
        res['Version'] = to_str(res['Version'])

        res['Name'] = str(res['Name'])
        res['Server'] = str(res['Server'])
        res['LocalNameCheck'] = str(res['LocalNameCheck'])
        res['UserHostAddress'] = str(res['UserHostAddress'])

        return res

    def sources(self):
        """Return available sources of data."""
        res = self.client.service.Sources(self.userdata, 0)
        return [str(x[0]) for x in res[0]]

    def request(self, query, source='Datastream',
                fields=None, options=None, symbol_set=None, tag=None):
        """General function to retrieve one record in raw format.

           query - query string for DWE system. This may be a simple instrument name
                   or more complicated request. Refer to the documentation for the
                   format.
           source - The name of datasource (default: "Datastream")
           fields - Fields to be retrieved (used when the requester does not want all
                    fields to be delivered).
           options - Options for specific data source. Many of datasources do not require
                     opptions string. Refer to the documentation of the specific
                     datasource for allowed syntax.
           symbol_set - The symbol set used inside the instrument (used for mapping
                        identifiers within the request. Refer to the documentation for
                        the details.
           tag - User-defined cookie that can be used to match up requests and response.
                 It will be returned back in the response. The string should not be
                 longer than 256 characters.
        """
        if self.show_request:
            print 'Request:', query

        rd = self.client.factory.create('RequestData')
        rd.Source = source
        rd.Instrument = query
        if fields is not None:
            rd.Fields = self.client.factory.create('ArrayOfString')
            rd.Fields.string = fields
        rd.SymbolSet = symbol_set
        rd.Options = options
        rd.Tag = tag

        return self.client.service.RequestRecord(self.userdata, rd, 0)

    def request_many(self, queries, source='Datastream',
                     fields=None, options=None, symbol_set=None, tag=None):
        """General function to retrieve one record in raw format.

           query - list of query strings for DWE system.
           source - The name of datasource (default: "Datastream")
           fields - Fields to be retrieved (used when the requester does not want all
                    fields to be delivered).
           options - Options for specific data source. Many of datasources do not require
                     opptions string. Refer to the documentation of the specific
                     datasource for allowed syntax.
           symbol_set - The symbol set used inside the instrument (used for mapping
                        identifiers within the request. Refer to the documentation for
                        the details.
           tag - User-defined cookie that can be used to match up requests and response.
                 It will be returned back in the response. The string should not be
                 longer than 256 characters.
           NB! source, options, symbol_set and tag are assumed to be identical for all
               requests in the list
        """
        if self.show_request:
            print 'Requests:', queries

        if not isinstance(queries, list):
            queries = [queries]

        req = self.client.factory.create('ArrayOfRequestData')
        req.RequestData = []
        for q in queries:
            rd = self.client.factory.create('RequestData')
            rd.Source = source
            rd.Instrument = q
            if fields is not None:
                rd.Fields = self.client.factory.create('ArrayOfString')
                rd.Fields.string = fields
            rd.SymbolSet = symbol_set
            rd.Options = options
            rd.Tag = tag

            req.RequestData.append(rd)

        return self.client.service.RequestRecords(self.userdata, req, 0)[0]

    #====================================================================================
    def status(self, record=None):
        """Extract status from the retrieved data and save it as a property of an object.
           If record with data is not specified then the status of previous operation is
           returned.

           status - dictionary with data source, string with request and status type,
                    code and message.

           status['StatusType']: 'Connected' - the data is fine
                                 'Stale'     - the source is unavailable. It may be
                                               worthwhile to try again later
                                 'Failure'   - data could not be obtained (e.g. the
                                               instrument is incorrect)
                                 'Pending'   - for internal use only
           status['StatusCode']: 0 - 'No Error'
                                 1 - 'Disconnected'
                                 2 - 'Source Fault'
                                 3 - 'Network Fault'
                                 4 - 'Access Denied' (user does not have permissions)
                                 5 - 'No Such Item' (no instrument with given name)
                                 11 - 'Blocking Timeout'
                                 12 - 'Internal'
        """
        if record is not None:
            self.last_status = {'Source': str(record['Source']),
                                'StatusType': str(record['StatusType']),
                                'StatusCode': record['StatusCode'],
                                'StatusMessage': str(record['StatusMessage']),
                                'Request': str(record['Instrument'])}
        return self.last_status

    def _test_status_and_warn(self):
        """Test status of last request and post warning if necessary.
        """
        status = self.last_status
        if status['StatusType'] != 'Connected':
            if isinstance(status['StatusMessage'], (str, unicode)):
                warnings.warn('[DWE] ' + status['StatusMessage'])
            elif isinstance(status['StatusMessage'], list):
                warnings.warn('[DWE] ' + ';'.join(status['StatusMessage']))

    #====================================================================================
    @staticmethod
    def extract_data(raw):
        """Extracts data from the raw response and returns it as a dictionary."""
        return {x[0]: x[1] for x in raw['Fields'][0]}

    def parse_record(self, raw, indx=0):
        """Parse raw data (that is retrieved by "request") and return pandas.DataFrame.
           Returns tuple (data, metadata)

           data - pandas.DataFrame with retrieved data.
           metadata - pandas.DataFrame with info about symbol, currency, frequency,
                      displayname and status of given request
        """
        suffix = '' if indx==0 else '_%i'%(indx+1)

        ### Parsing status
        status = self.status(raw)

        ### Testing if no errors
        if status['StatusType'] != 'Connected':
            if self.raise_on_error:
                raise DatastreamException('%s (error %i): %s --> "%s"' %
                                          (status['StatusType'], status['StatusCode'],
                                           status['StatusMessage'], status['Request']))
            else:
                self._test_status_and_warn()
                return pd.DataFrame(), {}

        record = self.extract_data(raw)
        get_field = lambda fldname: record[fldname+suffix]

        try:
            error = get_field('INSTERROR')
            if self.raise_on_error:
                raise DatastreamException('Error: %s --> "%s"' %
                                          (error, status['Request']))
            else:
                self.last_status['StatusMessage'] = error
                self.last_status['StatusType'] = 'INSTERROR'
                self._test_status_and_warn()
                metadata = {'Frequency':'','Currency':'','DisplayName':'',
                            'Symbol':'', 'Status': error}
        except KeyError:
            ### Parsing metadata of the symbol
            ### NB! currency might be returned as symbol thus "unicode" should be used
            metadata = {'Frequency': str(get_field('FREQUENCY')),
                        'Currency': unicode(get_field('CCY')),
                        'DisplayName': unicode(get_field('DISPNAME')),
                        'Symbol': str(get_field('SYMBOL')),
                        'Status': 'OK'}

        ### Fields with data
        if suffix=='':
            fields = [str(x) for x in record if '_' not in x]
        else:
            fields = [str(x) for x in record if suffix in x]

        ### Filter metadata
        meta_fields = ['CCY', 'DISPNAME', 'FREQUENCY', 'SYMBOL', 'DATE', 'INSTERROR']
        fields = [x.replace(suffix,'') for x in fields
                  if not any([y in x for y in meta_fields])]

        if 'DATE'+suffix in record:
            date = record['DATE'+suffix]
        elif 'DATE' in record:
            date = record['DATE']
        else:
            date = None

        if len(fields)>0 and date is not None:
            ### Check if we have a single value or a series
            if isinstance(date, dt.datetime):
                data = pd.DataFrame({x:[get_field(x)] for x in fields},
                                    index=[date])
            else:
                data = pd.DataFrame({x:get_field(x)[0] for x in fields},
                                    index=date[0])
        else:
            data = pd.DataFrame()

        metadata = pd.DataFrame(metadata, index=[indx])
        metadata = metadata[['Symbol','DisplayName','Currency','Frequency','Status']]
        return data, metadata

    #====================================================================================
    @staticmethod
    def construct_request(ticker, fields=None, date=None,
                          date_from=None, date_to=None, freq=None):
        """Construct a request string for querying TR DWE.

           tickers - ticker or symbol
           fields  - list of fields.
           date    - date for a single-date query
           date_from, date_to - date range (used only if "date" is not specified)
           freq    - frequency of data: daily('D'), weekly('W') or monthly('M')

           Some of available fields:
           P  - adjusted closing price
           PO - opening price
           PH - high price
           PL - low price
           VO - volume, which is expressed in 1000's of shares.
           UP - unadjusted price
           OI - open interest

           MV - market value
           EPS - earnings per share
           DI - dividend index
           MTVB - market to book value
           PTVB - price to book value
           ...

           The full list of data fields is available at http://dtg.tfn.com/.
        """
        if isinstance(ticker, list):
            request = ','.join(ticker)
        else:
            request = ticker
        if fields is not None:
            if isinstance(fields, (str, unicode)):
                request += '~='+fields
            elif isinstance(fields, list) and len(fields)>0:
                request += '~='+','.join(fields)
        if date is not None:
            request += '~@'+pd.to_datetime(date).strftime('%Y-%m-%d')
        else:
            if date_from is not None:
                request += '~'+pd.to_datetime(date_from).strftime('%Y-%m-%d')
            if date_to is not None:
                request += '~:'+pd.to_datetime(date_to).strftime('%Y-%m-%d')
        if freq is not None:
            request += '~'+freq
        return request

    #====================================================================================
    def fetch(self, tickers, fields=None, date=None,
              date_from=None, date_to=None, freq='D', only_data=True):
        """Fetch data from TR DWE.

           tickers - ticker or list of tickers
           fields  - list of fields.
           date    - date for a single-date query
           date_from, date_to - date range (used only if "date" is not specified)
           freq    - frequency of data: daily('D'), weekly('W') or monthly('M')
           only_data - if True then metadata will not be returned

           NB! in case list of tickers is requested, pandas.Panel is returned.

           Some of available fields:
           P  - adjusted closing price
           PO - opening price
           PH - high price
           PL - low price
           VO - volume, which is expressed in 1000's of shares.
           UP - unadjusted price
           OI - open interest

           MV - market value
           EPS - earnings per share
           DI - dividend index
           MTVB - market to book value
           PTVB - price to book value
           ...

           The full list of data fields is available at http://dtg.tfn.com/.
        """
        query = self.construct_request(tickers, fields, date, date_from, date_to, freq)
        raw = self.request(query)

        if isinstance(tickers, (str, unicode)) or len(tickers)==1:
            (data, metadata) = self.parse_record(raw)
        elif isinstance(tickers, list):
            metadata = pd.DataFrame()
            data = {}
            for indx in range(len(tickers)):
                (dat, meta) = self.parse_record(raw, indx)
                data[tickers[indx]] = dat
                metadata = metadata.append(meta, ignore_index=False)

            data = pd.Panel(data).swapaxes('items', 'minor')
        else:
            raise DatastreamException(('First argument should be either ticker or '
                                       'list of tickers'))

        if only_data:
            return data
        else:
            return data, metadata

    #====================================================================================
    def get_OHLCV(self, ticker, date=None, date_from=None, date_to=None):
        """Get Open, High, Low, Close prices and daily Volume for a given ticker.

           ticker  - ticker or symbol
           date    - date for a single-date query
           date_from, date_to - date range (used only if "date" is not specified)

           Returns pandas.Dataframe with data. If error occurs, then it is printed as
           a warning.
        """
        (data, meta) = self.fetch(ticker+"~OHLCV", None, date, date_from, date_to, 'D',
                                  only_data=False)
        return data

    def get_OHLC(self, ticker, date=None, date_from=None, date_to=None):
        """Get Open, High, Low and Close prices for a given ticker.

           ticker  - ticker or symbol
           date    - date for a single-date query
           date_from, date_to - date range (used only if "date" is not specified)

           Returns pandas.Dataframe with data. If error occurs, then it is printed as
           a warning.
        """
        (data, meta) = self.fetch(ticker+"~OHLC", None, date, date_from, date_to, 'D',
                                  only_data=False)
        return data

    def get_price(self, ticker, date=None, date_from=None, date_to=None):
        """Get Close price for a given ticker.

           ticker  - ticker or symbol
           date    - date for a single-date query
           date_from, date_to - date range (used only if "date" is not specified)

           Returns pandas.Dataframe with data. If error occurs, then it is printed as
           a warning.
        """
        (data, meta) = self.fetch(ticker, None, date, date_from, date_to, 'D',
                                  only_data=False)
        return data

    #====================================================================================
    def get_constituents(self, index_ticker, date=None, return_raw=False):
        """ Get a list of all constituents of a given index.

            index_ticker - Datastream ticker for index
            date         - date for which list should be retrieved (if None then
                           list of present constituents is retrieved)
            return_raw   - Method does not parse the response to pd.DataFrame format
                           and returns the raw dict (for debugging purposes)
        """
        if date is not None:
            str_date = pd.to_datetime(date).strftime('%m%y')
        else:
            str_date = ''
        query = 'L' + index_ticker + str_date + '~XREF'
        raw = self.request(query)

        ### Parsing status
        status = self.status(raw)

        ### Testing if no errors
        if status['StatusType'] != 'Connected':
            if self.raise_on_error:
                raise DatastreamException('%s (error %i): %s --> "%s"' %
                                          (status['StatusType'], status['StatusCode'],
                                           status['StatusMessage'], status['Request']))
            else:
                self._test_status_and_warn()
                return pd.DataFrame()

        ### Convert record to dict
        record = self.extract_data(raw)
        if return_raw:
            return record

        ### All fields that are available
        fields = [x for x in record if '_' not in x]
        fields.remove('DATE')

        ### Number of elements
        num = len([x[0] for x in record if 'SYMBOL' in x])

        ### field naming 'CCY', 'CCY_2', 'CCY_3', ...
        fld_name = lambda field, indx: field if indx==0 else field+'_%i'%(indx+1)

        ### Construct pd.DataFrame
        res = pd.DataFrame({fld:[record[fld_name(fld,ind)]
                                 if fld_name(fld,ind) in record else ''
                                 for ind in range(num)]
                            for fld in fields})
        return res
