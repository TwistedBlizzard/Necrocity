import os, json

for file in os.listdir('buildings'):
    path = os.path.join('res', 'buildings', file)
    with open(path, 'r') as json_file:
        data = json.load(json_file)
        try:
            building = data['building']
        except:
            building = data
        level = 0
        while True:
            if str(level) in building:
                level -= 1
            else:
                level += 1
                break
        while True:
            if str(level) in building:
                print('\nLevel: ', level)
                for grid in building[str(level)]:
                    line = ''
                    for x in grid:
                        if x == 'X':
                            x = ' '
                        line += x
                    print(line)
                level += 1
            else:
                break
    print('\n\n')
