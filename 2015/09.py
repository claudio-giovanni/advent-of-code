from dataclasses import dataclass

data = open("09.txt").readlines()


@dataclass
class City:
    name: str
    destinations: dict[str, int]


class SantaMap:
    def __init__(self, cities: list[City]):
        self.cities = cities
        self.trip_lengths: list[int] = []

    def find_shortest_trip(self):
        for city in self.cities:
            remaining_cites = self.cities[::]
            remaining_cites.remove(city)
            self._calculate_remaining_distance(city=city, remaining_cities=remaining_cites)

    def _calculate_remaining_distance(self, city: City, remaining_cities: list[City], distance_traveled: int = 0):
        if destinations := [destination for destination in remaining_cities if destination.name in city.destinations]:
            for destination in destinations:
                total_traveled = distance_traveled + city.destinations[destination.name]
                remaining_cities = [city for city in destinations if city.name != destination.name]
                self._calculate_remaining_distance(
                    city=destination, remaining_cities=remaining_cities, distance_traveled=total_traveled
                )
        elif remaining_cities:
            return
        else:
            self.trip_lengths.append(distance_traveled)


city_names = list(city.split("to")[0].strip() for city in data)
city_names = set(list(city.split("to")[1].split("=")[0].strip() for city in data) + city_names)
city_map = {name: City(name=name, destinations={}) for name in city_names}
for datum in data:
    start_city, end_city = map(str.strip, datum.split("to"))
    end_city, distance = map(str.strip, end_city.split("="))
    city_map[start_city].destinations.update({end_city: int(distance)})
    city_map[end_city].destinations.update({start_city: int(distance)})

santa_map = SantaMap(cities=list(city_map.values()))
santa_map.find_shortest_trip()
print(f"PART ONE: {min(santa_map.trip_lengths)}")
print(f"PART TWO: {max(santa_map.trip_lengths)}")
