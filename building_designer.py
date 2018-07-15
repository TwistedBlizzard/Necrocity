from tkinter import Tk, Frame, Label, Button, Entry, StringVar
import os, json

class Application(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.name = 'untitled'
        self.x = 0
        self.y = 0
        self.max_x = 0
        self.max_y = 0
        self.building = {}
        grid = []
        for x in range(10):
            col = []
            for y in range(10):
                col.append('X')
            grid.append(col)
        self.building['0'] = grid
        self.level = '0'
        self.sv_level = StringVar()
        self.sv_level.set('0')
        self.view = []
        for x in range(10):
            col = []
            for y in range(10):
                sv = StringVar()
                text = self.building[self.level][x][y]
                sv.set(text)
                col.append(sv)
            self.view.append(col)
        self.material = StringVar()
        self.material.set('O')
        self.create_widgets()
        
    def create_widgets(self):
        top_bar = Frame(self)
        top_bar.pack(side='top')
        exit_button = Button(top_bar, text='Exit', command=self.quit)
        exit_button.grid(column=0, row=0)
        save_button = Button(top_bar, text='Save', command=self.save)
        save_button.grid(column=1, row=0)
        load_button = Button(top_bar, text='Load', command=self.load)
        load_button.grid(column=2, row=0)
        material = Entry(top_bar, textvariable=self.material)
        material.grid(column=3, row=0)
        navigation = Frame(top_bar)
        navigation.grid(column=4, row=0)
        up_button = Button(navigation, text='^', command=self.view_up)
        up_button.grid(column=1, row=0)
        left_button = Button(navigation, text='<', command=self.view_left)
        left_button.grid(column=0, row=1)
        right_button = Button(navigation, text='>', command=self.view_right)
        right_button.grid(column=2, row=1)
        down_button = Button(navigation, text='v', command=self.view_down)
        down_button.grid(column=1, row=2)
        level_up_button = Button(navigation, text='Level Up', command=self.level_up)
        level_up_button.grid(column=3, row=0)
        level_indicator = Label(navigation, textvariable=self.sv_level)
        level_indicator.grid(column=3, row=1)
        level_down_button = Button(navigation, text='Level Down', command=self.level_down)
        level_down_button.grid(column=3, row=2)
        self.build_main_view()

    def build_main_view(self):
        self.main_view = Frame(self)
        self.main_view.pack(side='bottom')
        for x in range(10):
            for y in range(10):
                button = Button(self.main_view, textvariable=self.view[x][y], command=lambda x=x, y=y: self.set(x, y))
                button.grid(column=x, row=y)

    def set(self, x, y):
        self.building[self.level][x+self.x][y+self.y] = self.material.get()
        self.update()

    def view_right(self):
        self.x += 5
        height = len(self.building['0'][0])
        if self.x > self.max_x:
            for level, grid in self.building.items():
                for x in range(5):
                    col = []
                    for x in range(height):
                        col.append('X')
                    grid.append(col)
            self.max_x = self.x
        self.update()

    def view_left(self):
        if self.x != 0:
            self.x -= 5
            self.update()

    def view_down(self):
        self.y += 5
        if self.y > self.max_y:
            for level, grid in self.building.items():
                for col in grid:
                    for x in range(5):
                        col.append('X')
            self.max_y = self.y
        self.update()

    def view_up(self):
        if self.y != 0:
            self.y -= 5
            self.update()

    def level_up(self):
        width = len(self.building[self.level])
        height = len(self.building[self.level][0])
        self.level = int(self.level)
        self.level += 1
        self.level = str(self.level)
        self.sv_level.set(self.level)
        if self.level not in self.building:
            grid = []
            for x in range(width):
                col = []
                for y in range(height):
                    col.append('X')
                grid.append(col)
            self.building[self.level] = grid
        self.update()

    def level_down(self):
        width = len(self.building[self.level])
        height = len(self.building[self.level][0])
        self.level = int(self.level)
        self.level -= 1
        self.level = str(self.level)
        self.sv_level.set(self.level)
        if self.level not in self.building:
            grid = []
            for x in range(width):
                col = []
                for y in range(height):
                    col.append('X')
                grid.append(col)
            self.building[self.level] = grid
        self.update()

    def update(self):
        for x in range(10):
            for y in range(10):
                text = self.building[self.level][x+self.x][y+self.y]
                self.view[x][y].set(text)

    def invert_grid(self, building):
        temp_building = {}
        for level, grid in building.items():
            temp_grid = []
            y_range = len(grid)
            x_range = len(grid[0])
            for x in range(x_range):
                temp_col = []
                for y in range(y_range):
                    temp_col.append(grid[y][x])
                temp_grid.append(temp_col)
            temp_building[level] = temp_grid
        return temp_building

    def save(self):
        ## TODO: Make json files less 'stringy'
        if self.name == 'untitled':
            x = 1
            while True:
                temp_name = self.name + '_' + str(x)
                if os.path.isfile(os.path.join('buildings', temp_name + '.json')):
                    x += 1
                else:
                    self.name = temp_name
                    break
        path = os.path.join('buildings', self.name + '.json')
        try:
            os.remove(path)
        except OSError:
            pass
        with open(path, 'w') as json_file:
            data = {}
            data['name'] = self.name
            data['building'] = self.building
            json.dump(data, json_file, indent=4)

    def load(self):
        path = input('Enter Path: ')
        with open(path, 'r') as json_file:
            data = json.load(json_file)
            self.name = data['name']
            self.building = data['building']
            self.x = 0
            self.y = 0
            self.level = '0'
            self.update()

if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    app.mainloop()
