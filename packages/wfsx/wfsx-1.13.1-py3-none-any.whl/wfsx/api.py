from fms.fmsextract import *
from wfsx.apivalidation import *
from fms.vehicle_data import fms_vehicle_Data
from wfsx.common import *
from wfsx.parseexcel import *
from cdxg.logging import log
import traceback, json


class apicall(cdxg.TestCase):

    def apicall(self, testcase, apiendpoint, xmethod, payload, params, tdata, headers, exresults, schemavar, gtypes,
                xlcreate, roles, sprints, cxUrl):
        global status_code, getalljson, gettet, sparams, callapis
        var_types, test_types, input_types = gtypes
        apiendpoint, xendpoint = self.get_entries(apiendpoint)
        xendpoint = xmethod + ':' + xendpoint
        base_Url = f'{Cdxg.base_url}'
        self.baseUrl = getbaseUrl(ddata=base_Url, urlString=cxUrl)
        apiendpoint = self.baseUrl + apiendpoint
        print('###################---API[' + str(xendpoint) + ']---############################')
        vroles = str(roles) + '.json'
        getfms = fms_vehicle_Data()
        try:
            start_time = time.time()
            if tdata == 'filterdata' or tdata.startswith('filterdata') or 'filterdata' in tdata:
                log.info('*****FilterData*****')
                getfms.get_fms_data(roles, self.baseUrl, headers, apiept=xendpoint, tdata=tdata)

            if 'mixdata' in tdata:
                log.info('*****MixData*****')
                getfms.get_mix_data(roles, self.baseUrl, headers, apiept=xendpoint, param=params, tdata=tdata)

            if tdata != 'None' and '@' in tdata:
                tdatax = str(tdata).split('@')[1:][0]
                params = get_test_data(params=params, tdata=tdatax, epoint=str(xendpoint).split(':')[1])

            params = get_defined_data(apipoint=str(xendpoint).split(':')[1], ddata=params)
            if params != 'None' and params.startswith('/') and params is not None:
                if '*' in params:
                    sparams, params = str(params).split('*')
                else:
                    sparams = params
                apiendpoint = apiendpoint + sparams
                xendpoint = xendpoint + sparams

            if xmethod == 'GET':
                callapis = self.get(apiendpoint, data=payload, params=params, verify=False, headers=headers)

            if xmethod == 'POST':
                payload = get_vehicle_dict(payload, roles, tdata, apipoint=xendpoint.split(':')[1])
                callapis = self.post(apiendpoint, data=payload, params=params, verify=False, headers=headers)

            if xmethod == 'PUT':
                payload = get_vehicle_dict(payload, roles, tdata, apipoint=xendpoint.split(':')[1])
                callapis = self.put(apiendpoint, data=payload, params=params, verify=False, headers=headers)

            if xmethod == 'PATCH':
                payload = get_vehicle_dict(payload, roles, tdata, apipoint=xendpoint.split(':')[1])
                callapis = self.patch(apiendpoint, data=payload, params=params, verify=False, headers=headers)

            if xmethod == 'DELETE':
                payload = get_vehicle_dict(payload, roles, tdata, apipoint=xendpoint.split(':')[1])
                callapis = self.delete(apiendpoint, data=payload, params=params, verify=False, headers=headers)

            log.info(getcURL(xmethod, apiendpoint, payload, params))
            status_code, getalljson = saved_response_Data(start_time, vroles, callapis, tdata)
            saved_request_Data(payload, vroles, tdata)
            try:
                gettet = json.loads(payload)
            except json.JSONDecodeError as e:
                gettet = payload

            if exresults.startswith('sql'):
                exresults = self.getDataSql(exresults, roles)
            else:
                if '/' in xendpoint:
                    xpoint = str(xendpoint).split('/')
                    xendpoint = xpoint[0]
                exresults = get_data_expected(exresults, xendpoint)

            getresults = api_valid(gxdata=schemavar, expectedresults=exresults, txjson=getalljson,
                                   gtypes=gtypes, var_types=var_types, statuscode=status_code)
            return status_code, getresults, xendpoint, payload, exresults, params
        except Exception as e:
            time_elapsed = 00  # timedelta(seconds=round(elapsed_time_secs))
            get_results(xlcreate, roles, testcase, xendpoint, payload, params, exresults, 'ScriptError:' + str(e),
                        results='FAILED', fontx='FC2C03',
                        elapsed_secs=time_elapsed, comments=schemavar, sprints=sprints)
            print(traceback.print_exc())

    def get_entries(self, apiendpoint):
        if '/' in apiendpoint:
            apoint = str(apiendpoint).split('/')
            # apiendpoint = get_defined_data(apipoint=apoint[len(apoint) - 1], ddata=apiendpoint)
            apiendpoint = get_defined_data(apipoint=getepoint(apoint), ddata=apiendpoint)
            return apiendpoint, getepoint(apoint)  # apoint[len(apoint) - 1]
        else:
            return apiendpoint, apiendpoint

    def getDataSql(self, sQLx, dbname):
        # Get results using Sqlite3
        sqlx, tbname, query = str(sQLx).split('|')
        global apipoint
        if '_' in dbname:
            xpoint = str(dbname).split('_')
            if len(xpoint) > 2:
                abx = []
                for lex in range(0, 2):
                    abx.append(xpoint[lex])
                apipoint = '_'.join(abx)
            else:
                apipoint = str(xpoint[0])
        tbname = apipoint + '_' + tbname
        getresult = engConnect(rindex=tbname, getdata=query, dbname=str(dbname) + '.db')
        print('-------------------')
        print(getresult)
        print('-------------------')
        return getresult

    def getbaseUrl(self, ddata, urlString):
        print(ddata)
        print(urlString)
        match = re.search(r'{(.*?)}', ddata)
        print(match)
        if match:
            extracted_string = match.group(1)
            print(extracted_string)
            replaced_string = ddata.replace(str('{' + extracted_string + '}'), str(urlString))
            print(replaced_string)
            return replaced_string
