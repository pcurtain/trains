""" problem.py
    
    To provide a runnable module that runs exactly the problems called-for 
    by the ThoughtWorks trains example program and provides those outputs 
    exactly as expected.

    More fun, and more correct, to run the provided unit tests module,
    trainstest.py  `python -m unittest trainstest`
    """

from railway import RailSystem, NoSuchRoute, NoSuchStation

"""
Problem one: Trains
 
The local commuter railroad services a number of towns in Kiwiland.
 Because of monetary concerns, all of the tracks are 'one-way.'  That
 is, a route from Kaitaia to Invercargill does not imply the existence
 of a route from Invercargill to Kaitaia.  In fact, even if both of
 these routes do happen to exist, they are distinct and are not
 necessarily the same distance!
 
The purpose of this problem is to help the railroad provide its
 customers with information about the routes.  In particular, you will
 compute the distance along a certain route, the number of different
 routes between two towns, and the shortest route between two towns.
 
Input:  A directed graph where a node represents a town and an edge
 represents a route between two towns.  The weighting of the edge
 represents the distance between the two towns.  A given route will
 never appear more than once, and for a given route, the starting and
 ending town will not be the same town.
 
"""
 
"""Data for the examples.

Test Input:
For the test input, the towns are named using the first few letters of
the alphabet from A to D.  A route between two towns (A to B) with a
distance of 5 is represented as AB5.
Graph: AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7
"""
def example_railsystem():
    railsystem = RailSystem()
    # Graph: AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7
    railsystem.add_rail('A', 'B', 5)  
    railsystem.add_rail('B', 'C', 4)
    railsystem.add_rail('C', 'D', 8)
    railsystem.add_rail('D', 'C', 8)
    railsystem.add_rail('D', 'E', 6)
    railsystem.add_rail('A', 'D', 5)
    railsystem.add_rail('C', 'E', 2)
    railsystem.add_rail('E', 'B', 3)
    railsystem.add_rail('A', 'E', 7)
    return railsystem


"""Distances for fixed routes.

1. The distance of the route A-B-C.
2. The distance of the route A-D.
3. The distance of the route A-D-C.
4. The distance of the route A-E-B-C-D.
5. The distance of the route A-E-D.

Output: For test input 1 through 5, if no such route exists, output
 'NO SUCH ROUTE'.  Otherwise, follow the route as given; do not make
 any extra stops!  For example, the first problem means to start at
 city A, then travel directly to city B (a distance of 5), then
 directly to city C (a distance of 4).
"""
def example_trips():
    trips = [
     ['A', 'B', 'C'],
     ['A', 'D'],
     ['A', 'D', 'C'],
     ['A', 'E', 'B', 'C', 'D'],
     ['A', 'E', 'D'] ]
    return trips

def print_trip_distances(railsystem):
    trips = example_trips()
    for trip in trips:
        print "Output #%d: " % (trips.index(trip)+1),
        try:
            distance = railsystem.distance_for_trip(trip)
        except NoSuchStation:
            print "Surprise!"
        except NoSuchRoute:
            print "NO SUCH ROUTE"

        if distance:
            print "%d" % (distance)
        distance = 0

"""Distinguishing by stops.

6. The number of trips starting at C and ending at C with a maximum of 
   3 stops.  In the sample data below, there are two such trips: 
       C-D-C (2 stops). 
       and C-E-B-C (3 stops).
7. The number of trips starting at A and ending at C with exactly 4 
   stops.  In the sample data below, there are three such trips: 
       A to C (via B,C,D); 
       A to C (via D,C,D); and 
       A to C (via D,E,B).
"""
def print_trip_stops(railsystem):
    trips = railsystem.find_trips_from_to('C', 'C', max_stops=4)
    print "Output #6:  %d" % len( list(trips) )
    trips = railsystem.trips_with_stops('A', 'C', 4)
    print "Output #7:  %d" % len( list(trips) )

"""Shortest route examples.

8. The length of the shortest route (in terms of distance to travel) from A to C.
9. The length of the shortest route (in terms of distance to travel) from B to B.
10.The number of different routes from C to C with a distance of less 
   than 30.  In the sample data, the trips are: 
       CDC, CEBC, CEBCDC, CDCEBC, CDEBC, CEBCEBC, CEBCEBCEBC.
"""
def print_shortest_trips(railsystem):
    a_to_c = railsystem.shortest_from_to('A', 'C')
    print "Output #8:  %d" % a_to_c.distance()
    b_to_b = railsystem.shortest_from_to('B', 'B')
    print "Output #9:  %d" % b_to_b.distance()
    
def print_distance_trips(railsystem):
    trips = railsystem.find_trips_from_to('C', 'C', max_distance=30-1)
    print "Output #10: %d" % len( list(trips) )
    
"""Outputs.

Expected Output:
Output #1: 9
Output #2: 5
Output #3: 13
Output #4: 22
Output #5: NO SUCH ROUTE
Output #6: 2
Output #7: 3
Output #8: 9
Output #9: 9
Output #10: 7
"""
 
if __name__ == '__main__':
    """Call each of the sections to answer the ThoughtWorks problem."""
    railsystem = example_railsystem()
    print_trip_distances(railsystem)
    print_trip_stops(railsystem)
    print_shortest_trips(railsystem)
    print_distance_trips(railsystem)

