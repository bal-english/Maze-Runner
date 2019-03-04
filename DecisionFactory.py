import random
import numpy
import MemoryMap
import TravelPath

class DecisionFactory:
    def __init__(self, name = 'Joe'):
        self.name = name
        self.directions = [ 'wait', 'left', 'up', 'right', 'down']#'up', 'down', 'right', 'left']
        self.last_result = 'success'
        self.last_direction = 'wait'
        self.memory = MemoryMap.MemoryMap()
        self.path = TravelPath.TravelPath()
        self.backtravelling = False

        # Note: we have relativisitic coordinates recorded here, since the map
        # is relative to the players first known recorded position:
        # self.state.pos = (0, 0)

    def get_decision(self, x, y, verbose = True):
        return self.smart_direction(x, y) #self.random_direction()

    def check_decision(self, dir):
        if dir == self.last_direction:
            if self.last_result is False:
                return False
        return True

    def random_direction(self):
        r = random.randint(1, 4)
        dir = self.directions[r]
        self.last_direction = dir
        return dir

    def smart_direction(self, x, y):
        options = list(self.directions)
        print("Available Decisions " + str(options))
        self.memory.remove_bad_choices(x, y, options)
        print("Moveable Decisions " + str(options))
        self.memory.remove_grayblack_choices(x, y, options)
        print("Smart Decisions " + str(options))
        print("Travel Path: " + str(self.path.path))
        size = len(options)
        if size == 1:
            self.backtravelling = True
            print("No White Spaces. Back-travelling...")
            dir = self.path.pop()
            print("Last Direction: " + dir)
            if dir == 'left':
                dir = 'right'
            elif dir == 'up':
                dir = 'down'
            elif dir == 'right':
                dir = 'left'
            elif dir == 'down':
                dir = 'up'
            self.last_direction = dir
        else:
            r = random.randint(1, size-1)
            dir = options[r]
            while self.check_decision(r) is False:
                r = random.randint(1, size-1)

            self.last_direction = dir

        print("Direction: " + dir + "\n")
        return dir

    def put_result(self, x, y, result):
        self.last_result = result
        self.memory.memorize(x, y, self.last_direction, self.last_result)
        if self.last_result is True and self.backtravelling is False:
            self.path.push(self.last_direction)
        elif self.backtravelling is True:
            self.backtravelling = False
