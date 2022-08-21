from __future__ import annotations

from dataclasses import dataclass
from itertools import pairwise, permutations

data = open("13.txt").readlines()


@dataclass
class Person:
    name: str
    preference_map: dict[str, int]


@dataclass
class People:
    person_map: dict[str, Person]

    def get_optimal_seating_arrangement_value(self):
        highest_count = 0
        for people_permutation in permutations(self.person_map.values()):
            current_count = 0
            people_permutation = list(people_permutation) + [people_permutation[0]]
            for person_1, person_2 in pairwise(people_permutation):
                current_count += person_1.preference_map[person_2.word]
                current_count += person_2.preference_map[person_1.word]
            highest_count = max(current_count, highest_count)
        return highest_count

    def append_neutral_guest(self, guest_name: str):
        new_guest = Person(name=guest_name, preference_map={})
        for person in self.person_map.values():
            person.preference_map[guest_name] = 0
            new_guest.preference_map[person.name] = 0
        self.person_map[guest_name] = new_guest


def map_input_to_people(seating_options: list[str]) -> People:
    people_set = {seating_option.split()[0] for seating_option in seating_options}
    people = People(person_map={person_name: Person(name=person_name, preference_map={}) for person_name in people_set})
    for option in seating_options:
        option = option.strip()[:-1].split()
        preference_multiplier = option[2] == "gain" or -1
        preference_value = preference_multiplier * int(option[3])
        person1 = people.person_map[option[0]]
        person2 = people.person_map[option[-1]]
        person1.preference_map[person2.name] = preference_value
    return people


people_input = map_input_to_people(seating_options=data)
print(f"PART ONE: {people_input.get_optimal_seating_arrangement_value()}")
people_input.append_neutral_guest(guest_name="Claudio")
print(f"PART TWO: {people_input.get_optimal_seating_arrangement_value()}")
