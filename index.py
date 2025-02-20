import concurrent.futures
import json
import time

from test.cubrid import CUBRID

from test.odbc import ODBC


sample = 50000

cubrid = CUBRID()
odbc = ODBC()

cubrid.stress_load = sample
odbc.stress_load = sample

time.sleep(5)
cubrid.test()
time.sleep(5)
odbc.test()
with open("./data1.json", "w") as file:
    json.dump({"cubrid": cubrid.report, "odbc": odbc.report }, file, indent=4)


cubrid.sample_test(20, 2500)
time.sleep(5)
odbc.sample_test(20, 2500)

with open("./sampling1.json", "w") as file:
    json.dump({"cubrid": cubrid.report_sampling, "odbc": odbc.report_sampling}, file, indent=4)