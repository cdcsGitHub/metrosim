#-------------------------------------------------------------------------------
# Name:        Trains.py
# Purpose:
#
# Author:      Clay
#
# Created:     15/10/2013
# Copyright:   (c) Clay 2013
#-------------------------------------------------------------------------------
from collections import OrderedDict

class Train:
    def __init__ (self, line, cars, start, station_objects, metro):
        self.line = line
        self.cars = cars
        self.start = start
        self.max_capacity = self.cars*175
        self.transfers = ['Fort Totten','Gallery Place','King St-Old Town',"L'Enfant Plaza", 'Metro Center','Pentagon','Rosslyn','Stadium-Armory']
        self.train = []
        self.stations = station_objects
        self.metro = metro

    def station_number(self, station, line):
        position = station
        return line.keys().index(position)
##        for i in range(0, len(line)):
##            if line[i][0] == station:
##                position = i
##        return position

    def current_stop(self, stop):
        return self.line.keys()[self.station_number(stop, self.line)]
##        return self.line[self.station_number(stop, self.line)][0]

    def load(self, passenger):
        self.train.append(passenger)

    def unload(self, passenger):
        self.train = [x for x in self.train if x != passenger]

    def station_find(self, current_position):
        for i in self.stations:
            if i.station_name() == current_position:
                return i

    def get_line_name(self,line):
        if(line == self.metro[0]):
            return "Blue Line Left"
        elif (line == self.metro[1]):
            return "Blue Line Right"
        elif (line == self.metro[2]):
            return "Red Line Left"
        elif (line == self.metro[3]):
            return "Red Line Right"
        elif (line == self.metro[4]):
            return "Orange Line Left 1"
        elif (line == self.metro[5]):
            return "Orange Line Left 2"
        elif (line == self.metro[6]):
            return "Orange Line Right 1"
        elif (line == self.metro[7]):
            return "Orange Line Right 2"
        elif (line == self.metro[8]):
            return "Green Line Left"
        elif (line == self.metro[9]):
            return "Green Line Right"
        elif (line == self.metro[10]):
            return "Yellow Line Left 1"
        elif (line == self.metro[11]):
            return "Yellow Line Left 2"
        elif (line == self.metro[12]):
            return "Yellow Line Right 1"
        elif (line == self.metro[13]):
            return "Yellow Line Right 2"
        else:
            return "Error"

    def get_line(self,line):
        if(line == "Blue Line Left"):
            return self.metro[0]
        elif (line == "Blue Line Right"):
            return self.metro[1]
        elif (line == "Red Line Left"):
            return self.metro[2]
        elif (line == "Red Line Right"):
            return self.metro[3]
        elif (line == "Orange Line Left 1"):
            return self.metro[4]
        elif (line == "Orange Line Left 2"):
            return self.metro[5]
        elif (line == "Orange Line Right 1"):
            return self.metro[6]
        elif (line == "Orange Line Right 2"):
            return self.metro[7]
        elif (line == "Green Line Left"):
            return self.metro[8]
        elif (line == "Green Line Right"):
            return self.metro[9]
        elif (line == "Yellow Line Left 1"):
            return self.metro[10]
        elif (line == "Yellow Line Left 2"):
            return self.metro[11]
        elif (line == "Yellow Line Right 1"):
            return self.metro[12]
        elif (line == "Yellow Line Right 2"):
            return self.metro[13]
        else:
            return 'Error'

    def reverse_destination_line(self, dest, line):
        time = 0
        temp_dict = line.items()
        temp_dict.reverse()
        new_dict = OrderedDict(temp_dict)
        for key in new_dict.iterkeys():
            if key == dest:
                time = time + new_dict[key]
            else:
                time = time + 1 + new_dict[key]
        #print time
        return time

    def reverse_current_line(self, line):
        temp_dict = line.items()
        temp_dict.reverse()
        new_dict = OrderedDict(temp_dict)
        return new_dict

    def get_min(self, dictionary):
        keys = dictionary.keys()
        keys.sort(cmp=lambda a,b: cmp(dictionary[a],dictionary[b]))
        return keys[0]

    def split_dict(self, split_point, dictionary):
        split_list = []
        #print split_point
        for key in dictionary.iterkeys():
            #print key, split_point, dictionary.keys().index(key)
            if(dictionary.keys().index(key) >= dictionary.keys().index(split_point)):
                #print key
                split_list.append(key)
        return split_list

    def start_line(self, current_station, destination):
        destination_lines = []
        current_in_line = []
        transfer_lines = []
        to_transfer = {}

        for i in self.metro:
            if destination in i.iterkeys():
                destination_lines.append(i)
            if current_station in i.iterkeys():
                current_in_line.append(i)

        for i in current_in_line:
           # print i
            split = self.split_dict(current_station, i)
            #print split
            time = 0
            for j in split:
                if j in self.transfers:
                    for k in destination_lines:
                        for l in k:
                            if l == j:
                                to_transfer[self.get_line_name(i)] = time
                                transfer_lines.append(k)
                elif (self.station_number(j, i) == len(i)):
                    break
                else:
                    #print i[j]
                    time = time + 1 + i[j]
        #print to_transfer

        return self.get_line(self.get_min(to_transfer))

    def fastest_line(self, destination, current_station):
        prospective_lines = []
        destination_lines = []
        times = {}
        for i in self.metro:
            if current_station in i.iterkeys():
                prospective_lines.append(i)
        for i in prospective_lines:
            if destination in i.iterkeys():
                destination_lines.append(i)
        if(len(destination_lines) == 0):
            return self.line
        else:
            for k in destination_lines:
                time = 0
##                start = k.keys()[self.station_number(current_station, k)]
                #print start, destination
                #print current_station, destination
                split_line = self.split_dict(current_station, k)
                #print "yay", split_line
                name = self.get_line_name(k)
                for l in split_line:
                    #print l
                    if l != destination and self.station_number(l, k) == len(k):
                        time = time + 1 + k[l] + self.reverse_destination_line(destination, k)
                        times[name] = time
                    elif l == destination:
                        time = time + k[l]
                        times[name] = time
                    else:
                        time = time + 1 + k[l]
            #print times
            return self.get_line(self.get_min(times))

    def in_line_check(self, station):
        boolean = False
        if(station in self.line.iterkeys()):
                boolean = True
        return boolean

    def dest_line_check(self, destination, line):
        boolean = False
        if(destination in line.iterkeys()):
                boolean = True
        return boolean

##    def move(self):
##        for i in self.line.iterkeys():
##            temp = self.station_find(i)
##            for k in temp.station_capacity:
##                if(len(self.train) < self.max_capacity and self.start_line(i, k[1]) == self.line and k[2] == 0 and i != k[1]):
##                    self.load(k)
##                    temp.station_unload(k)
##            if (temp.station_name() in self.transfers):
##                for l in self.train:
##                    #print l[1], i
##                    destination_line = self.fastest_line(l[1], i)
##                    if (destination_line != self.line and self.dest_line_check(self.current_stop(i), destination_line) == True):
##                        self.unload(l)
##                        l[2] = l[2] + 1 + self.line[i]
##                        temp.station_load(l)
##
##                for m in temp.station_capacity:
##                    if(self.fastest_line(m[1],i) == self.line):
##                        self.load(m)
##                        temp.station_unload(m)
##
##            for j in self.train:
##                if j[1] == temp.station_name():
##                    temp.station_load(j)
##                    self.unload(j)
##                else:
##                    j[2] = j[2] + 1 + self.line[i]
##
##    def reverse_move(self):
##        reverse_line = self.reverse_current_line(self.line)
##        for i in reverse_line.iterkeys():
##            temp = self.station_find(i)
##            for k in temp.station_capacity:
##                if(len(self.train) < self.max_capacity and self.start_line(i, k[1]) == self.line and k[2] == 0 and i != k[1]):
##                    self.load(k)
##                    temp.station_unload(k)
##            if (temp.station_name() in self.transfers):
##                for l in self.train:
##                    destination_line = self.fastest_line(l[1], i)
##                    if (destination_line != self.line and self.dest_line_check(self.current_stop(i), destination_line) == True):
##                        self.unload(l)
##                        l[2] = l[2] + 1
##                        temp.station_load(l)
##                for m in temp.station_capacity:
##                    if(self.fastest_line(m[1],i) == self.line):
##                        self.load(m)
##                        temp.station_unload(m)
##            for j in self.train:
##                if j[1] == temp.station_name():
##                    temp.station_load(j)
##                    self.unload(j)
##                else:
##                    j[2] = j[2] + 1 + reverse_line[i]
