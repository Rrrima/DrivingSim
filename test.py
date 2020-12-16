import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Subject import Subject
import sys

meta_data = pd.read_csv('meta.csv')
# demo_data = pd.read_csv('demo.csv')
# number of participants
def generate_expdata():
	num = 107
	btots = []
	stots = []
	gtots = []
	tots = []
	ttcs = []
	ids = []
	ttc_time = []
	tbtcs = []
	tds = []
	wls = []
	error_list = []
	cpoint = []


	for i in range(num):
	    sub_id = i+1
	    try:
		    print("create subject {}".format(sub_id))
		    sub = Subject('workload',sub_id,meta_data)
		    if sub_id%2 ==0:
		    	# for the bycycle event
		        # eid = 7
		        # for the car ahead event
		        eid = 3
		    else:
		        # eid = 0
		        eid = 4
		    print("    get event data {}".format(eid))
		    tt = sub.query_by_event(eid)
		    tot_dict = tt.calculate_tot_time()
		    b,s,g,t = tot_dict.values()
		    btots.append(b)
		    stots.append(s)
		    gtots.append(g)
		    tots.append(t)
		    ttcs.append(tt.ttc)
		    ttc_time.append(tt.ttc_time)
		    cpoint.append(tt.changetime)
		    ids.append(sub_id)
		    tbtcs.append(tt.tbtc)
		    tds.append(tt.traffic_density)
		    wls.append(tt.workload)
	    except:
	        error_list.append(sub_id)
	        e = sys.exc_info()[0]
	        print(e)
	        continue

	print("="*20,"subject with error","="*20)
	print(error_list)
	print("="*20,"==================","="*20)

	df = pd.DataFrame(list(zip(ids, btots, stots, gtots, tots, ttcs,ttc_time, tbtcs,tds,wls)), 
	               columns =['subject_id','brake', 'steer','gas','tot','ttc','ttc_time','changetime','tbtc','traffic_density','workload']) 
	df.to_csv('result_workload_bicycle_addlane2.csv',index=False)

# sub = Subject('workload',17,meta_data)
# tt = sub.query_by_event(0)
# print(tt.ttc_time)
if __name__ == '__main__':
	# sub = Subject('workload',1,meta_data)
	# tt = sub.query_by_event(0)
	# print(tt.ttc_time,tt.ttc)
	generate_expdata()