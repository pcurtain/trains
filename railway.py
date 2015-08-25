""" Railway module, to contain each of the obvious abstractions.  In more 
    formal terms, I'd be breaking each class into it's matching module. 
    Trying to keep it simple for now.
    """
import sys

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
        return self.adjacent.keys()

    def distance_to(self, neighbor):
        return self.adjacent[neighbor]

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
        return self.station_dict.get(n)

    def add_rail(self, frm, to, dist = 0):
        if frm not in self.station_dict:
            self.add_station(frm)
        if to not in self.station_dict:
            self.add_station(to)

        self.station_dict[frm].add_neighbor(self.station_dict[to], dist)
        # i think this creates a return route along any directed route.
        # self.station_dict[to].add_neighbor(self.station_dict[frm], dist)

    def get_stations(self):
        return self.station_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous

    def distance_for_trip(self, stops=[]):
        segments = trip_pairs_for_sequence(stops)
        total_distance = 0
        for segment in segments:
            startname, targetname = segment
            start = self.get_station(startname)
            if not start:
                print "We don't have a stop named" + str(startname)
                return 0
            target = self.get_station(targetname)
            if not target:
                print "We don't have a stop named" + str(targetname)
                return 0
            if target in start.connections():
                distance = start.distance_to(target)
                total_distance = total_distance + distance
            else:
                # print "There's no route between %s and %s" % segment
                return 0
        return total_distance

def trip_pairs_for_sequence(stops=[]):
    pairs = []
    stops_count = len(stops)
    for s in stops:
        sindex = stops.index(s)
        if sindex+1 < stops_count:
            pair = (s, stops[stops.index(s)+1])
            if len(pair) == 2:
                pairs.append( pair )
    return pairs

def shortest(station, path):
    ''' make shortest path from s.previous'''
    if station.previous:
        path.append(station.previous.stationname)
        shortest(station.previous, path)
    return

import heapq

def dijkstra(aRailSystem, start, target):
    print '''Dijkstra's shortest path'''
    # Set the distance for the start name to zero 
    start.set_distance(0)

    # Put tuple pair into the priority queue
    unvisited_queue = [(s.distance,s) for s in aRailSystem]
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        # Pops a station with the smallest distance 
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()

        #for next in s.adjacent:
        for next in current.adjacent:
            # if visited, skip
            if next.visited:
                continue
            new_dist = current.distance + current.distance_to(next)
            
            if new_dist < next.distance:
                next.set_distance(new_dist)
                next.set_previous(current)
                print 'updated : current = %s next = %s new_dist = %s' \
                        %(current.stationname, next.stationname, next.distance)
            else:
                print 'not updated : current = %s next = %s new_dist = %s' \
                        %(current.stationname, next.stationname, next.distance)

        # Rebuild heap
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Put all stations not visited into the queue
        unvisited_queue = [(s.distance,s) for s in aRailSystem if not s.visited]
        heapq.heapify(unvisited_queue)

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
        distance = railway.distance_for_trip(trip)
        if distance:
            # print "Distance for %s : %d" % (str(trip), distance)
            print "Output #%d: %d" % (trips.index(trip)+1, distance)
        else:
            print "Output #%d: NO SUCH ROUTE" % (trips.index(trip)+1)

def provided_example():
    railway = example_railsystem()

    print 'RailSystem data:'
    for s in railway:
        for t in s.connections():
            sstationname = s.stationname
            tstationname = t.stationname
            print '( %s , %s, %3d)'  % ( sstationname, tstationname, s.distance_to(t))

    dijkstra(railway, railway.get_station('A'), railway.get_station('C')) 

    target = railway.get_station('A')
    path = [target.stationname]
    shortest(target, path)
    print 'The shortest path : %s' %(path[::-1])
    
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


