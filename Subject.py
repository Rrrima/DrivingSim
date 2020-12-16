import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from Metadata import Metadata
from SingleTakeover import SingleTakeover

class Subject(object):
	def __init__(self,exp_name,sub_id,meta_dataset):
		self.sub_id = sub_id
		self.exp_name = exp_name
		self.prefix = 'Na_work_Sub_'
		self.metadata = meta_dataset
		self.data_path1 = os.path.join(self.exp_name,self.prefix+str(sub_id)+'_Drive_1.dat')
		self.data_path2 = os.path.join(self.exp_name,self.prefix+str(sub_id)+'_Drive_2.dat')
		self.meta_dict = {
		    'A': [4,0,0],
		    'B': [7,0,0],
		    'C': [4,1,0],
		    'D': [7,1,0],
		    'E': [4,0,1],
		    'F': [7,0,1],
		    'G': [4,1,1],
		    'H': [7,1,1],
		}

	def query_by_event(self,eid):
		if eid < 4:
			df = pd.read_table(self.data_path1,sep="\s+",low_memory=False)[1:]
			eid_trans = eid
		else:
			df = pd.read_table(self.data_path2,sep="\s+",low_memory=False)[1:]
			eid_trans = eid - 4
		df = df[1:]
		for col in df.columns:
			try:
				df[col] = pd.to_numeric(df[col])
			except:
				continue
		tor_point = df[df['User13'].diff()>=1]
		tor_point = list(tor_point['FRAME_NUM'])
		end_point = df[df['User13'].diff()<=-1]
		end_point = list(end_point['FRAME_NUM'])
		# get the takeover period lists
		takeover_list = []
		for i in range(len(tor_point)):
		    takeover_list.append([tor_point[i],end_point[i]])
		situation_id = self.metadata[self.metadata['subject']==self.sub_id].values[0][1:][eid]
		meta_org = self.meta_dict[situation_id[0]]
		meta = Metadata(self.sub_id,meta_org,eid)
		takeover = SingleTakeover(df,takeover_list[eid_trans],meta)
		return takeover

