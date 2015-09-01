"""Railway module, to contain each of the obvious abstractions.  In more 
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
    """Station is the local domain name of what is a vertex for our graph."""
    def __init__(self, name):
        self.name = name
        self.adjacent = {}
        self.distance = sys.maxint  # init to infinity
        self.visited = False
        self.previous = None

    def add_neighbor(self, neighbor, dist=0):
        self.adjacent[neighbor] = dist

    def connections(self):
        """Returns station instances."""
        return self.adjacent.keys()
    
    def connection_names(self):
        return [station.name for station in self.connections()]

    def distance_to(self, neighbor):
        try:
            return self.adjacent[neighbor]
        except KeyError:
            raise NoSuchStation("No Such Route")

    def __str__(self):
        return str(self.name) + \
               ' adjacent: ' + str([x.name for x in self.adjacent])

class TripStop:
    def __init__(self, station):
        """constructor requires a valid Station object. """
        self.station = station
        self.name = station.name
        self.prevstop = None
        self.nextstop = None
        self.visited = False
        self.first = False
        self.last = False

    def self.connections(self):
        return self.station.connections()

class Trip:
    def __init__(self, stations=[], names=[]):
        """construct a list of railway station stops using either names
           or station objects."""
        self.stops =  []
        if stations:
            for s in stations:
                self.add_stop(s)
        elif names:
            for n in names:
                self.add_stop_for_name(n)

    def add_stop(self, station):
        try:
            stop = TripStop(station)
            self.stops.append(stop)
        except:
            raise

    def segments(self):
        """return a list of pairs made of the steps of this trip."""
        segments = pairwise(self.stops)
        for start, target in segments:
            if target in start.connections():
                if start != target:
                    start.nextstop = target
                    target.prevstop = start
                    yield (start, target)
            else:
                raise NoSuchRoute("No such route when checking trip.segments")

    def distance(self):
        distance = 0
        for start, target in self.segments():
            distance = distance + start.distance_to(target)

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

    def distance_for_trip(self, stops=[]):
        distances=[]
        segments = self.station_pairs_for_trip(stops)
        for start, target in segments:
            if target in start.connections():
                distances.append(start.distance_to(target))
        return sum(distances) 

    def _find_trips(self, trip, max_stops=0):
        # import pdb; pdb.set_trace()
        print trip,
        if max_stops > 0:
            start = self.get_station(trip[0])
            target = self.get_station(trip[-1])
            print "start: ", start, " target: ", target
            if target in start.connections():
                if target != start:
                    yield trip
            for x in target.connection_names():
                for p in self._find_trips(trip + [x], max_stops - 1):
                    yield p

    def find_trips_from(self, name, max_stops):
        return self._find_trips([name], max_stops)

    def find_trips_from_to(self, startname, targetname, 
                                 max_stops=30, 
                                 max_distance=50):
        all_trips = self._find_trips([startname, targetname], max_stops)
        matching_trips = []
        for trip in all_trips:
            distance = self.distance_for_trip(trip)
            stops = len( list(trip) )
            print trip, distance, stops
            if trip[-1] == targetname:
                if distance <= max_distance and stops <= max_stops:
                    matching_trips.append(trip)
        return matching_trips

    def trips_with_distance(self, trips):
        """Assumes trips is a list of trip tuples containing strings."""
        # TODO: Consider making Trip and Trips (or Itineraries) classes
        distance_trips = { }
        for t in trips:
            distance = self.distance_for_trip(t)
            distance_trips[distance] = t
        return distance_trips

    def trips_with_stops(self, startname, targetname, max_stops=4):
        all_trips = self.find_trips_from_to(self, [startname, targetname], max_stops)
        return all_trips
        
    def trips_ordered_by_distance(self, trips):
        trips_dict = self.trips_with_distance(trips)
        ordered_distance = sorted(trips_dict.keys())
        for distance in ordered_distance:
            print "( ", distance, trips_dict[distance], " )"
            yield ( distance, trips_dict[distance] )

    def shortest_from_to(self, startname, targetname):
        import pdb; pdb.set_trace()
        all_trips = self.find_trips_from_to(startname, targetname, 15)
        ordered_trips = list( self.trips_ordered_by_distance(all_trips) )
        return ordered_trips[0]

    def station_pairs_for_trip(self, names=[]):
        namepairs = pairwise(names)
        for startname, targetname in namepairs:
            try:
                start = self.get_station(startname)
                target = self.get_station(targetname)
            except:
                raise NoSuchStation()
            if target in start.connections():
                yield (start, target)
            else:
                pass

    def __str__(self):
        s = ""
        for station in self.station_dict.values():
            s = s + str(station) + os.linesep
        return s

def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def shortest(station, trip):
    ''' make shortest trip from s.previous'''
    if station.previous:
        trip.append(station.previous.name)
        shortest(station.previous, trip)
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
     ['A', 'E', 'D'] ]
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
            sname = s.name
            tname = t.name
            print '( %s , %s, %3d)'  % ( sname, tname, s.distance_to(t))

    
if __name__ == '__main__':
    railway = example_railsystem()
    trips = example_trips()
    print_trip_distances(railway, trips)
    print "Output #6"
    print "Output #7"

    start = railway.get_station('A')
    target = railway.get_station('C')
    trip = [start.name, target.name]
    shortest(target, trip)
    print trip
    shortest_a_to_c = trip[::-1]
    print "Output #8: %s" % (str(shortest_a_to_c))

    trips = list(railway.find_trips_from('C', 30))
    # print trips
    trips_to_c = []
    for t in trips:
        if len(t) < 31:
            if t[-1] == 'C':
                trips_to_c.append(t)
    print "Output #9: %d" % ( len(trips_to_c) )

