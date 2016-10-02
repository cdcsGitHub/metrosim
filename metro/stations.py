#-------------------------------------------------------------------------------
# Name:        stations.py
# Purpose:
#
# Author:      Clay
#
# Created:     15/10/2013
# Copyright:   (c) Clay 2013
#-------------------------------------------------------------------------------

class Station:
    def __init__ (self, station):
        self.s = station
        #self.p = passList
        self.station_capacity = []
    def fill_station(self, passList):
        for i in passList:
            if i[0] == self.s:
                self.station_capacity.append(i)
    def station_load(self, station):
        self.station_capacity.append(station)
    def station_unload(self, station):
        self.station_capacity = [x for x in self.station_capacity if x != station]
    def station_name(self):
        return self.s
    def station_occupancy(self):
        return len(self.station_capacity)