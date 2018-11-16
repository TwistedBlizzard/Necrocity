import os, json

class Next(Exception):
    pass

class Skip(Exception):
    pass

class Stop(Exception):
    pass

def load(race):
    data = {}
    path = str(os.path.join('res', race.lower() + '_associations.json'))
    with open(path, 'r') as json_file:
        data = json.load(json_file)
    return data

def save(race, data):
    path = str(os.path.join('res', race.lower() + '_associations.json'))
    with open(path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def edit(race, associations):
    print('Editing Associations for', race)
    try:
        for root in associations:
            print('Please enter words relating to the word %s:' % (str(root)))
            print("Enter 'next' to go to the next word.")
            print("Enter 'skip' to skip to words that have no associations.")
            print("Enter 'stop' to stop editing.")
            if len(associations[root]) > 0:
                print('Current Associations:')
                for association in associations[root]:
                    print(' ', association)
            else:
                print('There are no current associations.')
            print('New Associations:')
            try:
                while True:
                    association = input('  ')
                    if association == '':
                        continue
                    elif association == 'next':
                        raise Next()
                    elif association == 'skip':
                        raise Skip()
                    elif association == 'stop':
                        raise Stop()
                    else:
                        associations[root].append(association)
                        save(race, associations)
            except Next:
                continue
            except Skip:
                break
        new_words = []
        for root in associations:
            for association in associations[root]:
                if association not in new_words and association not in associations:
                    new_words.append(association)
        for root in new_words:
            associations[root] = []
            print('Please enter words relating to the word %s:' % (root))
            print("Enter 'next' to go to the next word.")
            print("Enter 'skip' to skip to adding new words.")
            print("Enter 'stop' to stop editing.")
            print('There are no current associations')
            try:
                while True:
                    association = input('  ')
                    if association == '':
                        continue
                    elif association == 'next':
                        raise Next()
                    elif association == 'skip':
                        raise Skip()
                    elif association == 'stop':
                        raise Stop()
                    else:
                        associations[root].append(association)
                        save(race, associations)
            except Next:
                continue
            except Skip:
                break
        while True:
            print('Please enter a word to add to associations:' % (root))
            print("Enter 'next' to go to the next word.")
            print("Enter 'stop' to stop editing.")
            root = input()
            if root not in associations:
                associations[root] = []
            else:
                continue
            try:
                while True:
                    association = input('  ')
                    if association == '':
                        continue
                    elif association == 'next':
                        raise Next()
                    elif association == 'stop':
                        raise Stop()
                    else:
                        associations[root].append(association)
                        save(race, associations)
            except Next:
                continue
    except Stop:
        pass

if __name__ == '__main__':
    associations = load('Human')
    edit('Human', associations)
