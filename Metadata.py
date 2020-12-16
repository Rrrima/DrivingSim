
class Metadata(object):
	def __init__(self,sub_id,meta,eid):
		self.id = sub_id
		self.meta = meta
		self.tbtc = meta[0]
		self.traffic_density = meta[1]
		self.workload = meta[2]
		self.event_list = ['bicycle_lc','cons_onleft_lk','cons_ahead_lc','sens_error_lk','car_ahead_lc','no_mark_cv','sens_error_cv','car_shoulder_lc']
		if eid%2 != 0:
			self.scenario = self.event_list[7-eid]
		else:
			self.scenario = self.event_list[eid]