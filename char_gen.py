import random, json, os
from urllib.request import urlopen
from decimal import Decimal as dec

class human:
    def __init__(self):
        # Here we do all of the character generation.
        self.gender = random.choice(['male', 'female'])
        self.name = self.generate_name()
        self.stats = self.generate_stats()
        self.skills = self.generate_skills()
        self.unique_id = self.generate_id()
        self.save()
        print(self.name, self.stats, self.skills)
    def generate_name(self):
        name = []
        with open(self.gender + '_names.json', 'r') as json_file:
            first_names = json.load(json_file)
            name.append(random.choice(first_names))
        with open('last_names.json', 'r') as json_file:
            last_names = json.load(json_file)
            name.append(random.choice(last_names))
        return name
    def generate_stats(self):
        stats = {}
        categories = ['str', 'con', 'def', 'dex', 'int', 'cha', 'wis', 'wil', 'per', 'luck']
        for category in categories:
            stats[category] = 0
        i = 0
        while i < 75:
            category = random.choice(categories)
            modifier = random.randint(1, 3)
            stats[category] += modifier
            i += modifier
        return stats
    def generate_skills(self):
        weights = {}
        with open('skill_weights.json', 'r') as json_file:
            weights = json.load(json_file)
        char_skills = {}
        for category, skills in weights.items():
            char_skills[category] = {}
            for skill, stats in skills.items():
                char_skills[category][skill] = 0
                for stat, weight in stats.items():
                    char_skills[category][skill] += self.stats[stat]*weight

        return char_skills
    def generate_id(self):
        try:
            os.makedirs('humans')
        except OSError:
            pass
        x = 1
        while True:
            unique_id = self.name[0] + '_' + self.name[1] + '_' + str(x)
            if os.path.isfile(os.path.join('humans', unique_id + '.json')):
                x += 1
            else:
                return unique_id
    def save(self):
        path = os.path.join('humans', self.unique_id + '.json')
        data = {
            'gender': self.gender,
            'name': self.name,
            'stats': self.stats,
            'skills': self.skills,
            'unique_id': self.unique_id
        }
        with open(path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    def calculate_attribs(self):
        attributes = {}
    def step(self, category, skill):
        self.skills[category][skill] += 0.1

def populate_names():
    male_names = []
    female_names = []
    last_names = []
    url = 'http://uinames.com/api/?amount=500&region=england&gender=male'
    for name in get_data(url):
        # Hotfix for api
        if name['name'] == 'OwenLeo':
            male_names.append(random.choice(['Owen', 'Leo']))
        else:
            male_names.append(name['name'])
        last_names.append(name['surname'])
    url = 'http://uinames.com/api/?amount=500&region=england&gender=female'
    for name in get_data(url):
        female_names.append(name['name'])
        last_names.append(name['surname'])
    path = os.path.join('res', 'male_names.json')
    try:
        os.remove(path)
    except OSError:
        pass
    with open(path, 'w') as json_file:
        json.dump(male_names, json_file)
    path = os.path.join('res', 'female_names.json')
    try:
        os.remove(path)
    except OSError:
        pass
    with open(path, 'w') as json_file:
        json.dump(female_names, json_file)
    path = os.path.join('res', 'last_names.json')
    try:
        os.remove(path)
    except OSError:
        pass
    with open(path, 'w') as json_file:
        json.dump(last_names, json_file)
def get_data(url):
    response = urlopen(url)
    return json.load(response)

if __name__ == '__main__':
    populate_names()
    for i in range(10):
        test_human = human()
