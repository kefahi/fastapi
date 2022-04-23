import json
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

from api.debug.tests import test as debug

debug_response = debug()
report = [ {"sms": debug_response}, ]
for one in report:
    name = next(iter(one))
    for api in one[name]:
        endpoint = next(iter(api))
        print(WARNING + name + ENDC, end =" : ")
        print(OKGREEN + endpoint + ENDC, end =" : response code = ")
        print(OKCYAN + str(api[endpoint]["response"]["code"]) + ENDC)


    #print(json.dumps(one[name], indent=2, sort_keys=True, default=str))

#print(json.dumps(report, indent=2, sort_keys=True, default=str))


