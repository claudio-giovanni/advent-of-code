import re
from dataclasses import dataclass
from itertools import product


@dataclass
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int


@dataclass
class CookieMaker:
    ingredients: list[Ingredient] = None

    def __call__(self, ingredient: Ingredient):
        self.ingredients = self.ingredients or []
        self.ingredients.append(ingredient)

    def get_highest_scoring_mix(self, target_cal: int = None) -> int:
        permutations = product(range(100), repeat=len(self.ingredients))
        valid_permutations = (permutation for permutation in permutations if sum(permutation) == 100)
        max_score = 0
        for permutation in valid_permutations:
            max_score = max(max_score, self._get_mix_score(ingredient_permutation=permutation, target_cal=target_cal))
        return max_score

    def _get_mix_score(self, ingredient_permutation: tuple[int], target_cal: int = None) -> int:
        capacity = durability = flavor = texture = calories = 0
        for i, quantity in enumerate(ingredient_permutation):
            capacity += self.ingredients[i].capacity * quantity
            durability += self.ingredients[i].durability * quantity
            flavor += self.ingredients[i].flavor * quantity
            texture += self.ingredients[i].texture * quantity
            calories += self.ingredients[i].calories * quantity
        if target_cal and target_cal != calories:
            return 0
        capacity, durability, flavor, texture = max(capacity, 0), max(durability, 0), max(flavor, 0), max(texture, 0)
        return capacity * durability * flavor * texture


def get_cookie_maker(ingredients_data: list[str]) -> CookieMaker:
    maker = CookieMaker()
    for ingredient_data in ingredients_data:
        capacity, durability, flavor, texture, calories = map(int, re.findall(r"-?\d+", ingredient_data))
        name = re.findall(r"\w+", ingredient_data)[0]
        maker(ingredient=Ingredient(name, capacity, durability, flavor, texture, calories))
    return maker


data = open("15.txt").read().splitlines()
cookie_maker = get_cookie_maker(ingredients_data=data)
print(f"PART ONE: {cookie_maker.get_highest_scoring_mix()}")
print(f"PART TWO: {cookie_maker.get_highest_scoring_mix(target_cal=500)}")
