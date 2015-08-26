""" Railway module, to contain each of the obvious abstractions.  In more 
    formal terms, I'd be breaking each class into it's matching module. 
    Trying to keep it simple for now.
    """

import sys, os
from itertools import tee, izip

class NoSuchRoute(Exception):
    pass
class NoSuchStation(Exception):
    pass

class Station:
    """ Station is the local domain name of what is a vertex for our graph.
        """
    def __init__(self, name):
        self.stationname = name
        self.adjacent = {}
        self.distance = sys.maxint  # init to infinity
        self.visited = False
        self.previous = None

    def add_neighbor(self, neighbor, dist=0):
        self.adjacent[neighbor] = dist

    def connections(self):
        """ Returns station instances. """
        return self.adjacent.keys()
    
    def connection_names(self):
        return [ station.stationname for station in self.connections() ]

    def distance_to(self, neighbor):
        try:
            return self.adjacent[neighbor]
        except KeyError:
            raise NoSuchStation("No Such Route")

    def set_distance(self, dist):
        self.distance = dist

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return str(self.stationname) + \
               ' adjacent: ' + str([x.stationname for x in self.adjacent])

class RailSystem:
    def __init__(self):
        self.station_dict = {}
        self.num_stations = 0

    def __iter__(self):
        return iter(self.station_dict.values())

    def add_station(self, name):
        self.num_stations = self.num_stations + 1
        new_station = Station(name)
        self.station_dict[name] = new_station
        return new_station

    def get_station(self, n):
        try:
            station = self.station_dict[n]
        except KeyError:
            raise NoSuchStation("No station matching name: %s" % n)
        return station

    def add_rail(self, frm, to, dist = 0):
        if frm not in self.station_dict:
            self.add_station(frm)
        if to not in self.station_dict:
            self.add_station(to)

        self.station_dict[frm].add_neighbor(self.station_dict[to], dist)

    def get_stations(self):
        return self.station_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous

    def _find_paths(self, path, max_stops=1):
        if max_stops > 0:
            yield path
            station = self.get_station(path[-1])
            for x in station.connection_names():
                for p in self._find_paths(path + [x], max_stops - 1):
                    yield p

    def find_paths_from(self, stationname, max_stops):
        return self._find_paths([stationname], max_stops)

    def find_paths_from_to(self, startname, targetname, 
                                 max_stops=2, max_distance=sys.maxint):
        all_paths = self._find_paths([startname, targetname], max_stops)
        matching_paths = {}
        for path in all_paths:
            if path[-1] == targetname:
                matching_paths[self.distance_for_trip(path)] = path
        return matching_paths

    def station_pairs_for_trip(self, stationnames=[]):
        namepairs = pairwise(stationnames)
        for startname, targetname in namepairs:
            try:
                start = self.get_station(startname)
                target = self.get_station(targetname)
            except:
                raise NoSuchStation()
            yield (start, target)

    def distance_for_trip(self, stops=[]):
        distances=[]
        segments = self.station_pairs_for_trip(stops)
        for start, target in segments:
            if target in start.connections():
                distances.append(start.distance_to(target))
        return sum(distances) 

    def __str__(self):
        s = ""
        for station in self.station_dict.values():
            s = s + str(station) + os.linesep
        return s

def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def shortest(station, path):
    ''' make shortest path from s.previous'''
    if station.previous:
        path.append(station.previous.stationname)
        shortest(station.previous, path)
    return

def example_railsystem():
    railway = RailSystem()
    # Graph: AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7
    railway.add_rail('A', 'B', 5)  
    railway.add_rail('B', 'C', 4)
    railway.add_rail('C', 'D', 8)
    railway.add_rail('D', 'C', 8)
    railway.add_rail('D', 'E', 6)
    railway.add_rail('A', 'D', 5)
    railway.add_rail('C', 'E', 2)
    railway.add_rail('E', 'B', 3)
    railway.add_rail('A', 'E', 7)
    return railway

def example_trips():
    trips = [
     ['A', 'B', 'C'],
     ['A', 'D'],
     ['A', 'D', 'C'],
     ['A', 'E', 'B', 'C', 'D'],
     ['A', 'E', 'D']  ]
    return trips

def print_trip_distances(railway, trips=[]):
    for trip in trips:
        print "Output #%d: " % (trips.index(trip)+1),
        try:
            distance = railway.distance_for_trip(trip)
        except NoSuchStation, NoSuchRoute:
            print "NO SUCH ROUTE"

        if distance:
            # print "Distance for %s : %d" % (str(trip), distance)
            print "%d" % (distance)
        distance = 0

def provided_example():
    railway = example_railsystem()

    print 'RailSystem data:'
    for s in railway:
        for t in s.connections():
            sstationname = s.stationname
            tstationname = t.stationname
            print '( %s , %s, %3d)'  % ( sstationname, tstationname, s.distance_to(t))

    
if __name__ == '__main__':
    railway = example_railsystem()
    trips = example_trips()
    print_trip_distances(railway, trips)
    print "Output #6"
    print "Output #7"

    start = railway.get_station('A')
    target = railway.get_station('C')
    path = [start.stationname, target.stationname]
    shortest(target, path)
    print path
    shortest_a_to_c = path[::-1]
    print "Output #8: %s" % (str(shortest_a_to_c))

    paths = list(railway.find_paths_from('C', 30))
    # print paths
    paths_to_c = []
    for p in paths:
        if len(p) < 31:
            if p[-1] == 'C':
                paths_to_c.append(p)
    print "Output #9: %d" % ( len(paths_to_c) )

