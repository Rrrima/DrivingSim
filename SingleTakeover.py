import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class SingleTakeover(object):
    def __init__(self,data,frames,meta):
        self.id = meta.id
        self.tbtc = meta.tbtc
        self.traffic_density = meta.traffic_density
        self.workload = meta.workload
        self.scenario = meta.scenario
        self.start_frame = frames[0]
        self.end_frame = frames[1]
        self.frames = data[(data['FRAME_NUM']<=self.end_frame) & (data['FRAME_NUM']>=self.start_frame)] 
        self.tor_time = self.get_time_by_frameid(self.start_frame)
        self.aut_time = self.get_time_by_frameid(self.end_frame)
        self.headdistance = self.frames['HeadwayDistance']
        self.long_speed_arr = self.frames['Velocity']
        self.lat_speed_arr = self.frames['LatVelocity']
        self.steer_arr = self.frames['Steer']
        self.long_acc = self.frames['LonAccel']
        self.lat_acc = self.frames['LatAccel']
        self.headtime = self.frames['HeadwayTime']
        self.bicycle_velocity = self.frames['User7']
        self.bicycle_x = self.frames['User8']
        self.bicycle_y = self.frames['User9']
        self.car_velocity = self.frames['User10']
        self.car_x = self.frames['User11']
        self.car_y = self.frames['User12']
        self.x = self.frames['XPos']
        self.y = self.frames['YPos']
        self.lane = np.array(self.frames['Lane'])
        # print(self.lane)
        self.ttc, self.ttc_time, self.changetime = self.calculate_ttc()
        # self.ttc2 = self.calculate_ttc2()
        # self.ttc2 = self.calculate_ttc2()

    def __str__(self):
        meta_str = 'id:{},tbtc:{},trad:{},wl:{},sce:{}'.format(self.id ,self.tbtc, self.traffic_density,self.workload,self.scenario)
        tot = self.calculate_tot_time()
        print("="*30)
        print(meta_str)
        print("="*30)
        print(tot)
        print("minimum time to collision:", self.ttc,self.ttc2)
        return ""

    def get_time_by_frameid(self,fid):
        return self.frames[self.frames['FRAME_NUM']==fid]['VidTime'].values[0]

    def get_time_by_endframe(self,fid):
        return self.get_time_by_frameid(fid) - self.tor_time       

    def calculate_tot_time(self):
        try:
            btot = self.frames[self.frames['Brake'].gt(9.9)]['VidTime'].values[0]
        except:
            btot = self.aut_time
        try:
            stot = self.frames[self.frames['Steer'].abs().gt(0.034889)]['VidTime'].values[0]
        except:
            stot = self.aut_time 
        try:
            gtot = self.frames[self.frames['Throttle'].gt(0.9)]['VidTime'].values[0]
        except:
            gtot = self.aut_time 
        btot = btot - self.tor_time
        stot = stot - self.tor_time
        gtot = gtot - self.tor_time
        return {'brake_tot':btot, 'steer_tot':stot, 'gas_tot':gtot,'min_tot':min(btot,stot,gtot)}

    def calculate_ttc(self):
        inital_lane = self.lane[0]
        if 'bicycle' in self.scenario:
            objv = self.bicycle_velocity
        elif 'car' in self.scenario:
            objv = self.car_velocity 
        i = 0
        while (i<len(self.lane)) and (self.lane[i]==inital_lane):
            i+=1
        print(len(self.lane),'   ',i)
        deltav = np.array(self.long_speed_arr)[0:i] - np.array(objv)[0:i]
        vs = []
        for v in deltav:
            if v > 0:
                vs.append(v)
            else:
                vs.append(0.00001)
        velocity = np.array(vs)
        headdis = np.array(self.headdistance)[0:i]
        minttc = min(np.divide(headdis,velocity))
        point = np.argmin(np.divide(headdis,velocity))
        ttc_time = self.frames.iloc[point]['VidTime']-self.tor_time
        changetime = self.frames.iloc[i-1]['VidTime']-self.tor_time
        return minttc, ttc_time, changetime

    def calculate_ttc2(self):
        headdis = np.array(self.y - self.bicycle_x)
        if 'bicycle' in self.scenario:
            objv = self.bicycle_velocity
        elif 'car' in self.scenario:
            objv = self.car_velocity 
        deltav = np.array(self.long_speed_arr) - np.array(objv)
        vs = []
        for v in deltav:
            if v > 0:
                vs.append(v)
            else:
                vs.append(0.00001)
        velocity = np.array(vs)
        minttc = min(np.divide(headdis,velocity))
        return minttc

