"""Railway module, to contain each of the obvious abstractions.  In more 
   formal terms, I'd be breaking each class into it's matching module. 
   Trying to keep it simple for now.
   """

import sys
from itertools import tee, izip

class NoSuchRoute(Exception):
    pass
class NoSuchStation(Exception):
    pass

class Station:
    """Station is the local domain name of what is a vertex for our graph."""
    def __init__(self, name):
        self.name = name
        self.distances_by_station = {}
        self.distance = sys.maxint  # init to infinity

    def add_connection(self, connection, dist=0):
        self.distances_by_station[connection] = dist

    def connections(self):
        """Returns station instances."""
        return self.distances_by_station.keys()
    
    def connection_names(self):
        names = [station.name for station in self.connections()]
        return names

    def distance_to(self, connection):
        try:
            return self.distances_by_station[connection]
        except KeyError:
            raise NoSuchStation("No Such Route")

    def __str__(self):
        return ('<Station: ' + str(self.name) + ': ' + 
                str([x.name for x in self.distances_by_station]) +
                '>')

class TripStop:
    def __init__(self, station):
        """constructor requires a valid Station object."""
        self.station = station
        self.name = station.name
        self.prevstop = None
        self.nextstop = None
        self.visited = False
        self.first = False
        self.last = False

    def connections(self):
        return self.station.connections()

    def connection_names(self):
        return [s.name for s in self.connections()]

class Trip:
    def __init__(self, stations=[]):
        """construct a list of railway station stops using station objects."""
        self.stops =  []
        if stations:
            for s in stations:
                self.add_stop(s)
        for s in self.stops:
            stopindex = self.stops.index(s)
            if stopindex == 0:
                s.first = True
            elif stopindex == (len(self.stops)-1):
                s.last = True

    def add_stop(self, station):
        self.stops.append(TripStop(station))

    def segments(self):
        """return a list of pairs made of the steps of this trip."""
        starts, targets = tee(self.stops)
        next(targets, None)
        segments = izip(starts, targets)
        for start, target in segments:
            if target.name in start.connection_names():
                if start != target:
                    start.nextstop = target
                    target.prevstop = start
                    yield (start, target)
            else:
                raise NoSuchRoute()

    def distance(self):
        distances=[]
        for start, target in self.segments():
                distances.append(start.station.distance_to(target.station))
        return sum(distances) 

    def stops_count(self):
        """ThoughtWorks example lists a route of C-E-B-C as having three stops.
        Basically it excludes the starting point as a stop for our purposes.
        """
        return len(self.stops)-1

    def candidate_stop_names(self, non_visited_only=False):
        """Given the last stop in this trip, return candidate stop names."""
        return self.stops[-1].connection_names()

    def stop_names(self):
        """Simple characters as expected by the ThoughtWorks problem."""
        return "-".join([s.name for s in self.stops])

    def __str__(self):
        return ('<' + 
                str([s.name for s in self.stops]) +
                ' stops: ' + str(self.stops_count()) + 
                ' distance: ' + str(self.distance()) +
                '>')

class RailSystem:
    def __init__(self):
        self.stations_by_name = {}

    def __iter__(self):
        return iter(self.stations_by_name.values())

    def add_station(self, name):
        self.stations_by_name[name] = Station(name)

    def get_station(self, n):
        try:
            station = self.stations_by_name[n]
        except KeyError:
            raise NoSuchStation("No station matching name: %s" % n)
        return station

    def add_rail(self, frm, to, distance=0):
        if frm not in self.stations_by_name:
            self.add_station(frm)
        if to not in self.stations_by_name:
            self.add_station(to)
        self.stations_by_name[frm].add_connection(self.stations_by_name[to], distance)

    def trip_for_stopnames(self, stopnames=[]):
        matching_stations = [self.stations_by_name[name] for name in stopnames]
        return Trip(matching_stations)

    def distance_for_trip(self, stopnames=[]):
        trip = self.trip_for_stopnames(stopnames)
        return trip.distance()

    def _find_all_trips(self, tripnames, max_depth=0, max_stops=sys.maxint, max_distance=sys.maxint):
        if max_depth > 0:
            yield tripnames

            trip = self.trip_for_stopnames(tripnames)
            for x in trip.candidate_stop_names():
                for p in self._find_all_trips(tripnames + [x], max_depth - 1):
                    if len(p) <= max_stops: # dump out faster if we're over the max_stops
                        newtrip = self.trip_for_stopnames(p)
                        if newtrip.distance() <= max_distance:
                            yield p

    def find_trips_from(self, name, max_depth=10, max_stops=30, max_distance=50):
        all_trip_names = self._find_all_trips([name], max_depth, max_stops, max_distance)
        return all_trip_names

    def find_trips_from_to(self, startname, targetname, max_depth=10, max_stops=30, max_distance=50):
        all_trip_names = self.find_trips_from(startname, max_depth, max_stops, max_distance)
        matching_trips = []
        for tripnames in all_trip_names:
            if len(tripnames) > 1: # found that my algorithm includes a single match
                trip = self.trip_for_stopnames(tripnames)
                if trip.stops[-1].name == targetname:
                    matching_trips.append(trip)
        return matching_trips

    def trips_with_distance(self, trips):
        """Assumes trips is a list of trip tuples containing strings."""
        distance_trips = { }
        for t in trips:
            distance_trips[t.distance()] = t
        return distance_trips

    def trips_with_stops(self, startname, targetname, stops):
        trips = self.find_trips_from_to(startname, targetname, max_depth=15, max_stops=stops*2)
        # Odd, but the prev line doesn't get a full set of data to try unless max_stops is higher
        matching_trips = []
        for trip in trips:
            if trip.stops_count() == stops:
                matching_trips.append(trip)
        return matching_trips

    def trips_ordered_by_distance(self, trips):
        trips_dict = self.trips_with_distance(trips)
        ordered_distance = sorted(trips_dict.keys())
        for distance in ordered_distance:
            yield trips_dict[distance]

    def shortest_from_to(self, startname, targetname):
        all_trips = self.find_trips_from_to(startname, targetname, max_depth=15)
        ordered_trips = list( self.trips_ordered_by_distance(all_trips) )
        return ordered_trips[0]

    def __str__(self):
        station_strings = ", ".join([str(station) for station in self.stations_by_name.values()])
        return str("<Railway: " + station_strings + ">")

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
        except NoSuchStation:
            print "Surprise!"
        except NoSuchRoute:
            print "NO SUCH ROUTE"

        if distance:
            # print "Distance for %s : %d" % (str(trip), distance)
            print "%d" % (distance)
        distance = 0

def print_trip_stops(railway):
    trips = railway.find_trips_from_to('C', 'C', max_stops=4)
    print "Output #6:  %d" % len( list(trips) )
    trips = railway.trips_with_stops('A', 'C', 4)
    print "Output #7:  %d" % len( list(trips) )

def print_shortest_trips(railway):
    a_to_c = railway.shortest_from_to('A', 'C')
    print "Output #8:  %d" % a_to_c.distance()
    b_to_b = railway.shortest_from_to('B', 'B')
    print "Output #9:  %d" % b_to_b.distance()
    
def print_distance_trips(railway):
    trips = railway.find_trips_from_to('C', 'C', max_distance=30-1)
    print "Output #10: %d" % len( list(trips) )

    
if __name__ == '__main__':
    railway = example_railsystem()
    trips = example_trips()
    print_trip_distances(railway, trips)
    print_trip_stops(railway)
    print_shortest_trips(railway)
    print_distance_trips(railway)
