from PIL import Image
import random
random.seed(111)

from prototype import Planet, Natal_Chart, _generate
from constants import PLANET_NAMES, SIGNS

def create_mock_natal_chart(positions):
    assert len(positions) == len(Natal_Chart.required_objects)

    planets = []
    obj_names = ['Asc', 'Mc'] + list(PLANET_NAMES.keys())
    for name, pos in zip(obj_names, positions):
        sign = SIGNS[int(pos) // 30]
        planets.append(Planet(name, pos % 30, pos, sign))

    return Natal_Chart(planets)


def test_stelliums():
    # generate n stelliums

    def _generate_stellium(n):
        # n is number of planets in stellium
        # pick starting pos randomly
        theta = random.uniform(0, 360)
        positions = [random.uniform(theta - 4, theta + 4) for _ in range(n)]
        m = len(Natal_Chart.required_objects) - n
        positions += [random.uniform(0, 360) for _ in range(m)]
        return create_mock_natal_chart(positions)

    for _ in range(20):
        # generate conjunction/stellium with x planets
        # where x is randomly chosen between 2 and 
        print("GENERATING NEW CHART")
        chart = _generate_stellium(random.randint(2, len(Natal_Chart.required_objects)))
        load_image = lambda filename: Image.open("assets/images/" + filename)
        im = _generate(chart, load_image)
        im.show()

if __name__ == "__main__":
    test_stelliums()

