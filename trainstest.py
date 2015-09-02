""" trainstest.py
    Standard python usage.  To run:  $python -m unittest trainstest
    """
import unittest
from railway import RailSystem, NoSuchRoute

class RailwayTestCase(unittest.TestCase):
    def setUp(self):
        self.railsystem = RailSystem()
        # Graph: AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7
        self.railsystem.add_rail('A', 'B', 5)  
        self.railsystem.add_rail('B', 'C', 4)
        self.railsystem.add_rail('C', 'D', 8)
        self.railsystem.add_rail('D', 'C', 8)
        self.railsystem.add_rail('D', 'E', 6)
        self.railsystem.add_rail('A', 'D', 5)
        self.railsystem.add_rail('C', 'E', 2)
        self.railsystem.add_rail('E', 'B', 3)
        self.railsystem.add_rail('A', 'E', 7)

        self.trips = [
            (['A', 'B', 'C'], 9),
            (['A', 'D'], 5),
            (['A', 'D', 'C'], 13),
            (['A', 'E', 'B', 'C', 'D'], 22),
            (['A', 'E', 'D'], NoSuchRoute) ]

    def test_distances(self):
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
        Output #1: 9
        Output #2: 5
        Output #3: 13
        Output #4: 22
        Output #5: NO SUCH ROUTE
        """
        for trip, expected in self.trips:
            try:
                distance = self.railsystem.distance_for_trip(trip)
                self.assertEqual(distance, expected) 
            except NoSuchRoute:
                self.assertEqual(trip, ['A', 'E', 'D'])
        
    def test_stops_c2c(self):
        """6. The number of trips starting at C and ending at C with a maximum of 
              3 stops.  In the sample data below, there are two such trips: 
               C-D-C (2 stops). 
               and C-E-B-C (3 stops).
       """
        startname = targetname = 'C'
        max_stop = 3
        expected_trips = ('C-D-C', 'C-E-B-C')
        trips = self.railsystem.find_trips_from_to(startname, targetname, max_stops=4)
        for trip in trips:
            self.assertLessEqual(trip.stops_count(), max_stop)
            info = str("didn't find the expected trip" +
                       trip.stop_names() + " not in " + str(expected_trips) )
            self.assertIn(trip.stop_names(), expected_trips, info)
 
    def test_stops_a2c(self):
        """7. The number of trips starting at A and ending at C with exactly 4 
              stops.  In the sample data below, there are three such trips: 
               A to C (via B,C,D); 
               A to C (via D,C,D); and 
               A to C (via D,E,B).
        """
        startname = 'A'
        targetname = 'C'
        expected_stops = 4
        expected_trips = ('A-B-C-D-C', 'A-D-C-D-C', 'A-D-E-B-C')
        trips = self.railsystem.trips_with_stops(startname, targetname, 4)
        for trip in trips:
            self.assertLessEqual(trip.stops_count(), expected_stops)
            info = str("didn't find the expected trip: " +
                       trip.stop_names() + " not in " + str(expected_trips) )
            self.assertIn(trip.stop_names(), expected_trips, info)

    def test_shortest_route(self):
        """8. The length of the shortest route (in terms of distance to travel) from A to C.
           9. The length of the shortest route (in terms of distance to travel) from B to B.
        """
        expected_trips = (('A', 'C', 9), ('B', 'B', 9))
        for startname, targetname, expected_distance in expected_trips:
            trip = self.railsystem.shortest_from_to(startname, targetname)
            self.assertEqual(trip.distance(), expected_distance)
        
    def test_routes_distance_c2c(self):
        """10. The number of different routes from C to C with a distance of less 
               than 30.  In the sample data, the trips are: 
                CDC, CEBC, CEBCDC, CDCEBC, CDEBC, CEBCEBC, CEBCEBCEBC.
        """
        startname = targetname = 'C'
        max_dist = 30
        expected_trips = ('C-D-C', 'C-E-B-C', 'C-E-B-C-D-C',
                          'C-D-C-E-B-C', 'C-D-E-B-C', 
                          'C-E-B-C-E-B-C', 'C-E-B-C-E-B-C-E-B-C')
        trips = self.railsystem.find_trips_from_to('C', 'C', max_distance=max_dist-1)
        for trip in trips:
            self.assertLessEqual(trip.distance(), max_dist)
            info = str("didn't find the expected trip: " +
                       trip.stop_names() + " not in " + str(expected_trips) )
            self.assertIn(trip.stop_names(), expected_trips, info)
        self.assertEqual(len(trips), len(expected_trips))
