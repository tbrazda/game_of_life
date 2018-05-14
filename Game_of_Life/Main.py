
from math import ceil
import random
import time
import os
from toolbox import get_integer, is_integer, get_string, get_boolean, yes_or_no, is_number, get_number, get_positive_number


class Cell(object):
    def __init__(self, row, column):
        self.living = False
        self.row = row
        self.column = column
        self.world = None
        self.neighbors = []
        self.livingNeighborCount = 0
        self.nextState = None
        #
        # single neighbors, used for testing and in self.get_neighbors_dish()
        #
        self.right = None
        self.left = None
        self.up = None
        self.down = None
        self.upRight = None
        self.upLeft = None
        self.downRight = None
        self.downLeft = None

    def set_neighbors(self):
        """Adds all neighbors to each cell's neighbor list. Done after each get_neighbors()."""
        neighbors = []
        neighbors.append(self.right)
        neighbors.append(self.left)
        neighbors.append(self.up)
        neighbors.append(self.down)
        neighbors.append(self.upRight)
        neighbors.append(self.upLeft)
        neighbors.append(self.downRight)
        neighbors.append(self.downLeft)
        self.neighbors = neighbors
        self.count_living_neighbors()
        return self.neighbors

    def get_neighbors_dish(self):
        """Assigns neighbors to each cell in the dish formation.
            Not the best way to assign neighbors, but functional. Very slow for large worlds."""
        cells = self.world.cellList
        for cell in cells:
            if cell.row == (self.row + 1) and cell.column == self.column:
                self.down = cell
            elif cell.row == (self.row - 1) and cell.column == self.column:
                self.up = cell
            elif cell.row == self.row and cell.column == (self.column + 1):
                self.right = cell
            elif cell.row == self.row and cell.column == (self.column - 1):
                self.left = cell
            elif cell.row == (self.row + 1) and cell.column == (self.column + 1):
                self.downRight = cell
            elif cell.row == (self.row - 1) and cell.column == (self.column + 1):
                self.upRight = cell
            elif cell.row == (self.row + 1) and cell.column == (self.column - 1):
                self.downLeft = cell
            elif cell.row == (self.row - 1) and cell.column == (self.column - 1):
                self.upLeft = cell

    def get_neighbors_torus(self):
        """Assigns neighbors to each cell in the torus formation.
            Not the best way to assign neighbors, but functional. Extremely slow for large worlds."""
        world = self.world
        rows = []
        for _ in range(world.rows):
            rows.append(_)
        columns = []
        for _ in range(world.columns):
            columns.append(_)
        cells = world.cellList
        for cell in cells:
            cell.get_neighbors_dish()
            #
            # top row
            #
            if cell.row == rows[0] and (cell.column != columns[-1] and cell.column != columns[0]):
                cell.up = world.find_cell(rows[-1], cell.column)
                cell.upRight = world.find_cell(rows[-1], (cell.column + 1))
                cell.upLeft = world.find_cell(rows[-1], (cell.column - 1))
            #
            # bottom row
            #
            elif cell.row == rows[-1] and (cell.column != columns[-1] and cell.column != columns[0]):
                cell.down = world.find_cell(rows[0], cell.column)
                cell.downRight = world.find_cell(rows[0], (cell.column + 1))
                cell.downLeft = world.find_cell(rows[0], (cell.column - 1))
            #
            # right column
            #
            elif cell.column == columns[-1] and (cell.row != rows[0] and cell.row != rows[-1]):
                cell.right = world.find_cell(cell.row, columns[0])
                cell.upRight = world.find_cell(cell.row-1, (columns[0]))
                cell.downRight = world.find_cell(cell.row+1, (columns[0]))
            #
            # left column
            #
            elif cell.column == columns[0] and (cell.row != rows[0] and cell.row != rows[-1]):
                cell.left = world.find_cell(cell.row, columns[-1])
                cell.upLeft = world.find_cell(cell.row + 1, (columns[-1]))
                cell.downLeft = world.find_cell(cell.row - 1, (columns[-1]))
            #
            # top left corner
            #
            if cell.row == rows[0] and cell.column == columns[0]:
                cell.up = world.find_cell(rows[-1],columns[0])
                cell.upRight = world.find_cell(rows[-1],columns[1])
                cell.upLeft = world.find_cell(rows[-1],columns[-1])
                cell.left = world.find_cell(rows[0],columns[-1])
                cell.downLeft = world.find_cell(rows[1],columns[-1])
            #
            # top right corner
            #
            elif cell.row == rows[0] and cell.column == columns[-1]:
                cell.up = world.find_cell(rows[-1],columns[-1])
                cell.upRight = world.find_cell(rows[-1],columns[0])
                cell.upLeft = world.find_cell(rows[-1],columns[-2])
                cell.right = world.find_cell(rows[0],columns[0])
                cell.downRight = world.find_cell(rows[1],columns[0])
            #
            # bottom left corner
            #
            elif cell.row == rows[-1] and cell.column == columns[0]:
                cell.down = world.find_cell(rows[0],columns[0])
                cell.downRight = world.find_cell(rows[0],columns[1])
                cell.downLeft = world.find_cell(rows[0],columns[-1])
                cell.left = world.find_cell(rows[-1],columns[-1])
                cell.upLeft = world.find_cell(rows[-2],columns[-1])
            #
            # bottom right corner
            #
            if cell.row == rows[-1] and cell.column == columns[-1]:
                cell.down = world.find_cell(rows[0],columns[-1])
                cell.downRight = world.find_cell(rows[0],columns[0])
                cell.downLeft = world.find_cell(rows[0],columns[1])
                cell.right = world.find_cell(rows[-1],columns[0])
                cell.upRight = world.find_cell(rows[1],columns[0])

    def assign_neighbors(self):
        """Determines which get_neighbors() to use."""
        if self.world.geometry == "dish":
            self.get_neighbors_dish()
        elif self.world.geometry == "torus":
            self.get_neighbors_torus()
        self.set_neighbors()

    def count_living_neighbors(self):
        """Counts the number of living neighbors for each cell. Used when determining next state of cell."""
        self.livingNeighborCount = 0
        for neighbor in self.neighbors:
            if neighbor != None:
                if neighbor.living == True:
                    self.livingNeighborCount += 1
        return self.livingNeighborCount

    def __str__(self):
        """Sets Unicode for living and dead cells."""
        if self.living == False:
            image = u"\u25A1"
        elif self.living == True:
            image = u"\u25A0"
        return image

    def __repr__(self):
        """Readable string showing cell's coordinates and it's living status."""
        string = f"""
		Coordinates = {self.row},{self.column}
		Cell.living = {self.living}
		"""
        return string


class World(object):
    deadASCII = '.'
    aliveASCII = 'x'
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.genNumber = 0
        self.name = None
        self.percentAlive = 0
        self.geometry = 'dish'
        #
        # list of rows(lists of cells)
        #
        self.cells = self.create_cells()
        #
        # list of all cells not organized into rows or columns
        #
        self.cellList = []
        for row in self.cells:
            for cell in row:
                self.cellList.append(cell)
        #
        # sets cell.world
        # needed in cell.get_neighbors() methods
        #
        for cell in self.cellList:
            cell.world = self
        self.liveCells = 0
        self.toLetLive = [2, 3]
        self.toMakeAlive = 3
        self.previousGenerations = []

    def create_cells(self):
        """helper method for __init__. Creates all cells in world based on rows and columns, and adds them to world."""
        self._cells = []
        for row in range(self.rows):
            self._cells.append([])
            for column in range(self.columns):
                self._cells[row].append(Cell(row, column))
        return self._cells

    def find_cell(self, row, column):
        """Used to find an existing cell in a world. Used in cell.get_neighbors_torus()"""
        coordinates = (row, column)
        found = None
        for cell in self.cellList:
            if (cell.row, cell.column) == coordinates:
                found = cell
                break
        return found

    def get_living_cells(self):
        """Calculates total amount of living cells in world."""
        total = 0
        for cell in self.cellList:
            if cell.living == True:
                total += 1
        self.liveCells = total
        return self.liveCells

    def __str__(self):
        """String method for world. Used to display the world during simulation.play()."""
        string = ""
        for row in self.cells:
            string += "\n"
            for cell in row:
                string += (" " + str(cell))
        return string

    def __repr__(self):
        """String format of world. Used when saving and opening files. Also used when reading previous generations."""
        string = ''
        for row in self._cells:
            string += '\n'
            for cell in row:
                if cell.living == True:
                    string += self.aliveASCII
                else:
                    string += self.deadASCII
        return string

    def populate_cells(self, percentAlive):
        """"Creates initial population of cells in world. Used in change_population_rate()."""
        numToMakeAlive = (percentAlive / 100) * len(self.cellList)
        numToMakeAlive = ceil(numToMakeAlive)
        cellsChosen = []
        cells = []
        for cell in self.cellList:
            cells.append(cell)
        for number in range(0, numToMakeAlive):
            cell = random.choice(cells)
            cellsChosen.append(cell)
            cells.remove(cell)
        for cell in self.cellList:
            if cell in cellsChosen:
                cell.living = True
                self.liveCells += 1
        percentAlive = self.calculate_percent_living()
        self.percentAlive = percentAlive
        self.previousGenerations.append(repr(self))
        return str(self)

    def calculate_percent_living(self):
        """Calculates percent of world that is alive. Used in status bar."""
        percent = (self.get_living_cells() / len(self.cellList)) * 100
        percent = ceil(percent)
        self.percentAlive = percent
        return percent

    def next_generation(self):
        """Creates next generation based on previous world's cells."""
        nextGen = self.cellList
        for cell in nextGen:
            cell.count_living_neighbors()
            if cell.living == True and cell.livingNeighborCount in self.toLetLive:
                cell.nextState = True
            elif cell.living == False and cell.livingNeighborCount == self.toMakeAlive:
                cell.nextState = True
            else:
                cell.nextState = False
        for cell in nextGen:
            cell.living = cell.nextState
        self.liveCells = 0
        for cell in nextGen:
            if cell.living == True:
                self.liveCells += 1
        self.cellList = nextGen
        self.genNumber += 1
        self.previousGenerations.append(repr(self))
        return nextGen

    def steady_state(self):
        """Checks if world is in a steady state based on previous 3 generations."""
        past5 = self.previousGenerations[:-3]
        steadyState = False
        for _ in past5:
            if repr(self) == _:
                steadyState = True
        return steadyState


class Simulation(object):
    def __init__(self):
        self.world = World(10, 10)
        self.initialWorldState = self.world
        self.percentAlive = 30
        self.enterCommand = "n"
        self.delay = 0.3
        self.lastCommand = None
        self.world.populate_cells(self.percentAlive)
        self.world.get_living_cells()
        for cell in self.world.cellList:
            cell.assign_neighbors()

    def intro(self):
        """Prints introductory string for user."""
        myPath = './'
        filename = os.path.join(myPath, 'Intro.txt')
        myFile = open(filename, 'r')
        text = myFile.read()
        myFile.close()
        print(text)
        print("------------------------------------------------------------------------------------------------------------------------")
        print("To play, enter one of the letters surrounded by brackets in the Menu. For more help, enter 'h'. Enjoy playing!")
    #
    # forwards
    #
    def multiple_generations(self, generations):
        """Creates x generations based on user input and displays them."""
        for _ in range(0, generations):
            self.world.next_generation()
            print(self.world)
            time.sleep(self.delay)
        return self.world

    def skip_x_generations(self, generations):
        """Creates x generations, but only displays last generation created."""
        for _ in range(0, generations):
            self.world.next_generation()
        print(self.world)
        return self.world
    #
    # backwards
    #
    def back_x_generations(self, generations):
        """Reads and displays former generations saved in world.previousGenerations. Displays each former generation."""
        #
        # so it doesn’t count current generation (added to previousGenerations during world.next_generation())
        #
        generations += 1
        previousGenerations = self.world.previousGenerations
        if generations > len(previousGenerations):
            print("Error: could not go back that far in previous generations.")
            while generations > len(previousGenerations) and generations >=0:
                generations = (get_integer(f"Enter a number less than {len(previousGenerations)}. "))+1
        newGenList = previousGenerations[0:-(generations)]
        #
        # list of selected generation to end of previousGenerations
        #
        goBack = previousGenerations[-generations:]
        goBack.reverse()
        goBack.remove(goBack[0])
        for generation in goBack:
            textGeneration = generation.split('\n')[1:]
            rows = len(textGeneration)
            columns = len(textGeneration[0])
            fullText = ''
            for _ in textGeneration:
               fullText += _
            world = World(rows, columns)
            for cell in world.cellList:
                index = world.cellList.index(cell)
                correspondingText = fullText[index]
                if correspondingText == World.aliveASCII:
                    cell.living = True
                else:
                    cell.living = False
            print(world)
        self.world = world
        for cell in self.world.cellList:
            cell.assign_neighbors()
        self.world.get_living_cells()
        self.world.previousGenerations = newGenList
        self.world.genNumber = len(newGenList) + 1

    def skip_back(self, generations):
        if generations > len(self.world.previousGenerations):
            print("Error: could not go back that far in previous generations.")
            while generations > len(self.world.previousGenerations) and generations >=0:
                generations = (get_integer(f"Enter a number less than {len(self.world.previousGenerations)}. "))+1
        genCount = self.world.genNumber
        newGenCount = genCount - generations
        generations += 1
        selected = self.world.previousGenerations[-generations]
        textGeneration = selected.split('\n')[1:]
        rows = len(textGeneration)
        columns = len(textGeneration[0])
        fullText = ''
        for _ in textGeneration:
            fullText += _
        # makes it a new world to display
        world = World(rows, columns)
        for cell in world.cellList:
            index = world.cellList.index(cell)
            correspondingText = fullText[index]
            if correspondingText == World.aliveASCII:
                cell.living = True
            else:
                cell.living = False
        self.world = world
        for cell in self.world.cellList:
            cell.assign_neighbors()
        self.world.get_living_cells()
        self.world.genNumber = newGenCount
        print(world)

    def reset_timeline(self):
        """Resets world to initial generation."""
        previousGenerations = self.world.previousGenerations
        firstWorld = previousGenerations[0]
        textGeneration = firstWorld.split('\n')[1:]
        rows = len(textGeneration)
        columns = len(textGeneration[0])
        fullText = ''
        for _ in textGeneration:
            fullText += _
        world = World(rows, columns)
        for cell in world.cellList:
            index = world.cellList.index(cell)
            correspondingText = fullText[index]
            if correspondingText == World.aliveASCII:
                cell.living = True
            else:
                cell.living = False
        self.world = world
        for cell in self.world.cellList:
            cell.assign_neighbors()
        self.world.get_living_cells()
        self.world.previousGenerations = [firstWorld]
        self.world.genNumber = 0
        print(self.world)
    #
    # edit world
    #
    def change_world_size(self):
        """Creates new world with user input for rows and columns."""
        rows = get_integer(input("rows: "))
        columns = get_integer(input("columns: "))
        newWorld = World(rows, columns)
        self.rows = rows
        self.columns = columns
        self.world = newWorld
        self.world.populate_cells(self.percentAlive)
        self.world.get_living_cells()
        for cell in self.world.cellList:
            cell.assign_neighbors()
        print(self.world)
        return self.world

    def change_population_rate(self, newRate):
        """Creates new world with new population rate."""
        self.percentAlive = newRate
        newWorld = World(self.world.rows, self.world.columns)
        self.world = newWorld
        self.world.populate_cells(newRate)
        self.world.get_living_cells()
        for cell in self.world.cellList:
            cell.assign_neighbors()
        print(self.world)
        return self.world

    def change_speed(self, newSpeed):
        """Changes speed of displaying generations in simulation."""
        self.delay = newSpeed
        return self.delay

    def toggle_geometry(self):
        """Switches world Geometry between dish and torus. Does not create new world."""
        if self.world.geometry == "dish":
            self.world.geometry = "torus"
        elif self.world.geometry == "torus":
            self.world.geometry = "dish"
        for cell in self.world.cellList:
            cell.neighbors = []
            cell.assign_neighbors()
        print(str(self.world))

    def change_rules(self,toLetLive,toMakeAlive):
        """Allows user to recreate the rules.
            Can have up to 8 numbers for toLetLive, but only one number for toMakeAlive."""
        self.world.toLetLive = toLetLive
        self.world.toMakeAlive = toMakeAlive
        print(f"""
------------------------------------------------------------------------------------------------------------------------
The rules have been changed:
    All living cells continue living if they have {self.world.toLetLive} neighbors.
    All dead cells with {self.world.toMakeAlive} neighbors will become alive.
------------------------------------------------------------------------------------------------------------------------""")
        self.multiple_generations(1)
    #
    # save/open
    #
    def save(self, filename='', myPath='./'):
        """Save the current generation of the current world as a text file."""
        filename = self.get_filename_for_saving(filename, myPath)
        text = repr(self.world)
        myFile = open(filename, 'w')
        myFile.write(text)
        myFile.close()
        self.world.name = filename
        self.message = f'saved {filename}'
        print(self.message)
        print(self.world)

    def get_filename_for_saving(self, filename, myPath='./'):
        """Make sure that the filename exists, that it has the right extension and that it goes into the correct directory."""
        if filename == '':
            filename = get_string('What do you want to call the file? ')
        #
        # Make sure the file has the correct file extension.
        #
        if filename[-5:] != '.life':
            filename = filename + '.life'
        #
        # Check if the file already exists.
        #
        if not os.path.isdir(myPath):
            mkdir(myPath)
        if filename in os.listdir(myPath):
            prompt = f"A file named '{filename}' already exists! Do you want to replace it?"
            replaceFile = get_boolean(prompt)
            if replaceFile == False:
                filename = self.get_filename_for_saving('')
        #
        # Add on the correct path for saving files.
        #
        if filename[0:len(myPath)] != myPath:
            filename = os.path.join(myPath, filename)
        return filename

    def open(self, filename='', myPath='./'):
        """Open a previously saved world."""
        filename = self.get_filename_for_opening(filename, myPath)
        #
        # get_filename_for_opening return '' if there are no files available
        #
        if filename == '':
            self.message = '404 -No files found. Try saving one first.'
        else:
            myFile = open(filename, 'r')
            textGeneration = myFile.read()
            myFile.close()
            textGeneration = textGeneration.split('\n')[1:]
            rows = len(textGeneration)
            columns = len(textGeneration[0])
            self.world = World(rows, columns)  # self.geometry, self.rules
            self.world.name = filename
            for cell in self.world.cellList:
                correspondingText = textGeneration[cell.row][cell.column]
                if correspondingText == World.aliveASCII:
                    cell.living = True
                else:
                    cell.living = False
            self.message = f'opened {filename}'
            self.generationCount = 0
            self.world.get_living_cells()
            for cell in self.world.cellList:
                cell.assign_neighbors()
            print(self.message)
            print(self.world)
            self.world.previousGenerations.append(repr(self))

    def get_filename_for_opening(self, filename, myPath='./'):
        """Make sure the filename has the right extension, goes in the right directory and, if no name is given, provides a list of worlds."""
        #
        # Find the files that are available.
        #
        filesAvailable = False
        files = os.listdir(myPath)
        availableFiles = 'Available files: '
        for file in files:
            splitFile = file.split('.')
            if splitFile[-1] == 'life':
                availableFiles += splitFile[0] + ', '
                filesAvailable = True
        availableFiles = availableFiles[:-2]
        if filesAvailable:
            #
            # Make sure the file has the correct file extension.
            #
            if filename[-5:] != '.life':
                filename = filename + '.life'
                while filename not in files:
                    print(availableFiles)
                    filename = get_string('Which file do you want to open?')
                    if filename[-5:] != '.life':
                        filename = filename + '.life'
                    if filename not in files:
                        print('404: File not found...')
                #
                # Add on the correct path for saving files.
                #
                if filename[0:9] != myPath:
                    filename = os.path.join(myPath, filename)
        else:
            filename = ''
        return filename

    def enter(self, command):
        """Sets whether world progresses forwards or backwards based on previous commands."""
        if command == "n":
            self.multiple_generations(1)
        elif command == "p":
            self.back_x_generations(1)
        self.play()

    def get_command(self, parameter):
        """Gets user command from Main Menu. Does not get commands for sub menus."""
        prompt = "Enter command: "
        commands = {
            "n": "next",  # sub-menu
            "p": "previous",  # sub-menu
            "e": "edit world",  # sub-menu
            "o": "open",
            "s": "save",
            "h": "help",
            "q": "quit"}
        print()
        userString = input(prompt)
        valid = ''.join(commands.keys())
        while userString[0].lower() not in valid:
            prompt = 'Please enter one of these letters: ' + valid + ' '
            userString = input(prompt).lower()
        try:
            command = userString[0]
            parameter = userString[1:].strip()
            self.lastCommand = (commands[command])
            commandList = []
            commandList.append(command)
        except:
            command = None
        return commandList

    def get_command_forward(self, parameter):
        """Gets command for Progress Forward Menu. Opened by calling 'n' in Main Menu."""
        commands = {
            "n": "[n]ext generation",
            "m": "[m]ultiple generations",
            "s": "[s]kip x generations"}
        menu = "[n]ext generation [m]ultiple generations [s]kip x generations"
        print(menu)
        prompt = "Enter command: "
        print()
        userString = input(prompt)
        if len(userString) == 0:
            command = 'next generation'
            perameter = 1
        else:
            valid = ''.join(commands.keys())
            while userString[0].lower() not in valid:
                prompt = 'Please enter one of these letters: ' + valid + ' '
                userString = input(prompt).lower()
            command = userString[0]
            parameter = userString[1:].strip()
            self.lastCommand = (commands[command])
        if parameter == '':
            parameter = None
        commandList = []
        commandList.append(command)
        try:
            commandList.append(int(parameter))
        except:
            parameter = None
        return commandList

    def get_command_back(self, parameter):
        """Gets command for Previous Generations Menu. Opened by calling 'p' in Main Menu."""
        commands = {
            "p": "[p]revious generation",
            "b": "[b]ack x generations",
            "s": "[s]kip back x generations",
            "r": "[r]eset timeline"}
        menu = "[p]revious generation [b]ack x generations [s]kip back x generations [r]eset timeline"
        print(menu)
        prompt = "Enter command: "
        print()
        userString = input(prompt)
        if len(userString) == 0:
            self.skip_back(1)
            self.play()
        else:
            valid = ''.join(commands.keys())
            while userString[0].lower() not in valid:
                prompt = 'Please enter one of these letters: ' + valid + ' '
                userString = input(prompt).lower()
            command = userString[0]
            parameter = userString[1:].strip()
            self.lastCommand = (commands[command])
        if parameter == '':
            parameter = None
        commandList = []
        commandList.append(command)
        try:
            commandList.append(int(parameter))
        except:
            parameter = None
        return commandList

    def get_command_edit_world(self, parameter):
        """Gets command for Edit World Menu. Opened by calling 'e' in Main Menu."""
        prompt = 'Enter command: '
        commands = {
            "w": "change world size",
            "p": "change population rate",
            "s": "change simulation speed",
            "t": "toggle geometry",
            "r": "change rules"}
        menu = "Edit: [w]orld size [p]opulation rate [s]peed [t]oggle geometry [r]ules"
        print(menu)
        print()
        userString = input(prompt)
        if len(userString) == 0:
            command = 'next generation'
            parameter = 1
        else:
            valid = ''.join(commands.keys())
            while userString[0].lower() not in valid:
                prompt = 'Please enter one of these letters: ' + valid + ' '
                userString = input(prompt).lower()
            command = userString[0]
            parameter = userString[1:].strip()
            self.lastCommand = (commands[command])
        if parameter == '':
            parameter = None
        commandList = []
        commandList.append(command)
        try:
            commandList.append(int(parameter))
        except:
            parameter = None
        return commandList
    #
    #main event methods
    #
    def display_status_bar(self):
        """Creates and displays status bar."""
        progress = "forwards"
        if self.enterCommand == "n":
            progress = "forwards"
        elif self.enterCommand == "p":
            progress = "backwards"
        world = self.world
        string = f"""Progressing {progress}
Size:{world.rows}x{world.columns}, Generation {world.genNumber+1}, Name:{world.name}, Percent Alive:{world.calculate_percent_living()}%, Geometry:{world.geometry}, speed:{self.delay}, Last Command: {self.lastCommand}"""
        print('------------------------------------------------------------------------------------------------------------------------')
        print(string)
        print('------------------------------------------------------------------------------------------------------------------------')
        return string

    def play(self):
        """Main Event Loop. Calls former simulation methods for user to play Life."""
        mainMenu = """[h]elp [n]ext [p]revious [e]dit world [o]pen [s]ave [q]uit"""
        self.display_status_bar()
        print(mainMenu)
        command = ''
        try:
            command = self.get_command('Enter command: ')
        except:
            #
            #if command == '', next code
            #
            if self.world.steady_state()== True:
                print("""
========================================================================================================================
World is currently in a steady state.
========================================================================================================================
""")
                self.enterCommand = "p"
            self.enter(self.enterCommand)
        try:
            #
            #selects action based on command from Main Menu
            #placed in try/except due to an error with the 'q' method.
            #
            if command[0][0] == 'h':
                print("""=======================================""")
                myPath = './'
                filename = os.path.join(myPath, 'Help.txt')
                myFile = open(filename, 'r')
                text = myFile.read()
                myFile.close()
                print(text)
                print("""=======================================""")
                print(self.world)
                self.play()
            elif command[0][0] == 'n':
                if self.world.steady_state() == True:
                    #
                    #prohibits player from progressing forwards with Progress Forwards Menu.
                    #
                    print("""
========================================================================================================================                 
World is in a steady state.
========================================================================================================================
""")
                    self.play()
                else:
                    #
                    #if not prohibited...
                    #
                    self.enterCommand = 'n'
                    command = self.get_command_forward('Enter command: ')
                    if len(command) == 0:
                        command = 'n'
                    if command[0][0] == 'n':
                        self.multiple_generations(1)
                        self.play()
                    elif command[0][0] == 'm':
                        if len(command) == 1:
                            generations = get_integer(input("How many generations? "))
                        else:
                            generations = command[1]
                        self.multiple_generations(generations)
                        self.play()
                    elif command[0][0] == 's':
                        if len(command) == 1:
                            generations = get_integer(input("How many generations do you want to skip? "))
                        else:
                            generations = command[1]
                        self.skip_x_generations(generations)
                        self.play()
            elif command[0][0] == 'p':
                #
                #Determines action based on Progress Backwards Menu
                #
                self.enterCommand = 'p'
                command = self.get_command_back('Enter command: ')
                if command[0][0] == 'p':
                    self.back_x_generations(1)
                    self.play()
                elif command[0][0] == 'b':
                    if len(command) == 1:
                        generations = get_integer(input("How many generations? "))
                    else:
                        generations = command[1]
                    self.back_x_generations(generations)
                    self.play()
                elif command[0][0] == 's':
                    if len(command) == 1:
                        generations = get_integer(input("How many generations do you want to skip? "))
                    else:
                        generations = command[1]
                    self.skip_back(generations)
                    self.play()
                elif command[0][0] == 'r':
                    self.reset_timeline()
                    self.enterCommand = 'n'
                    self.play()
            elif command[0][0] == 'e':
                #
                #Determines action based on Edit World Menu
                #
                command = self.get_command_edit_world('Enter command: ')
                if command[0][0] == 's':
                    if len(command) == 1:
                        newSpeed = get_positive_number(input("New speed: "))
                    else:
                        newSpeed = command[1:]
                    self.change_speed(newSpeed)
                    self.play()
                elif command[0][0] == 'p':
                    if len(command) == 1:
                        newRate = get_integer(input("New rate: "))
                    else:
                        newRate = command[1]
                    self.change_population_rate(newRate)
                    self.play()
                elif command[0][0] == 'w':
                    self.change_world_size()
                    self.play()
                elif command[0][0] == 't':
                    self.toggle_geometry()
                    self.play()
                elif command[0][0] == 'r':
                    toLetLive = []
                    anotherNum = True
                    while anotherNum != False and len(toLetLive) <= 8:
                        num = get_integer("Enter a number of neighbors that cells can live with: ")
                        if num > 8 or num < 0:
                            anotherNum = True
                        else:
                            toLetLive.append(num)
                            anotherNum = yes_or_no("Enter another number? ")
                    toMakeAlive = -1
                    while toMakeAlive < 0 or toMakeAlive> 8:
                        toMakeAlive = get_integer("With what number of neighbors should cells become alive? ")
                    self.change_rules(toLetLive,toMakeAlive)
                    self.play()
            elif command[0][0] == 'o':
                self.open()
                self.play()
            elif command[0][0] == 's':
                self.save()
                self.play()
            elif command[0][0] == 'q':
                print("""========================================================================================================================""")
                print('End of Life Simulation. Thanks for playing!')
                print("""========================================================================================================================""")
                pass
        except:
            pass


def main():
    """Main event loop. Creates a simulation and calls simulation.play()."""
    sim = Simulation()
    sim.intro()
    print()
    print('Initial World:')
    print(sim.world)
    sim.play()


main()
