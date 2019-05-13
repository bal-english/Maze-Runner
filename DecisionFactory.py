import random
import numpy

import os
from enum import Enum

class TileType(Enum):
	white = 0
	gray = 1
	black = 2
	wall = 3

class MemoryMap:
	def __init__(self, name = 'Joe'):
		self.name = name
		self.sizeX = 10
		self.sizeY = 10
		self.forX = 0
		self.forY = 0
		self.recentlyExpanded = False
		self.map = []
		a = 0
		while a < self.sizeY:
			self.map.append([])
			b = 0
			while b < self.sizeX:
				self.map[a].append(TileType.white)
				b += 1
			a += 1
		self.print_tilemap()

	def isWithinBounds(self, x, y):
		return (x > 0 and x < self.sizeX and y > 0 and y < self.sizeY)

	def get(self, x, y):
		return self.map[y+self.forY][x+self.forX]

	def set(self, x, y, type):
		self.map[y+self.forY][x+self.forX] = type

	def expandMap(self):# var = 0):
		a = 0
		while a < self.sizeY:
			b = 0
			while b < self.sizeX/2:
				self.map[a].insert(0, TileType.white)
				self.map[a].append(TileType.white)
				b += 1
			a += 1

		a = 0
		while a < self.sizeY/2:
			b = 0
			self.map.insert(0, [])
			self.map.append([])

			while b < self.sizeX*2:
				self.map[0].append(TileType.white)
				self.map[self.sizeX+a*2+1].append(TileType.white)
				b += 1
			a += 1
		self.sizeX *= 2
		self.sizeY *= 2

	def doubleMap(self, var = 0):
		a = 0
		while a < self.sizeY:
			b = 0
			#self.map.append([])
			while b < self.sizeX:
				self.map[a].append(TileType.white)

				b += 1
			a += 1
		self.sizeX *= 2

		a = self.sizeY
		while a < self.sizeY*2:
			b = 0
			self.map.append([])
			while b < self.sizeX:
				self.map[a].append(TileType.white)
				b += 1
			a += 1

		self.sizeY *= 2

	def expand_if_needed(self, x, y):
		expanded = False
		nx = x + self.forX
		ny = y + self.forY
		if ((ny < 1) or (ny + 1 >= self.sizeY)) or ((nx < 1) or (nx + 1 >= self.sizeX)):
			expanded = True
			self.expandMap()
			self.forX += self.sizeX/4
			self.forY += self.sizeY/4
			self.expand_if_needed(x, y)
			self.recentlyExpanded = True
		return expanded

	def print_tilemap(self):
		y = 0
		while y < self.sizeY:
			x = 0
			row = ""
			while x < self.sizeX:
				#if x == 3 and y == 2:
				#	print("HELLO")
				row += (str(self.map[y][x].value) + "  ")
				x += 1
			print(row)
			y += 1
		print("")

	def auditTile(self, x, y):
		adjacents = [[y, x-1], [y-1, x], [y, x+1], [y+1,x]]#[self.map[y][x-1], self.map[y-1][x], self.map[y][x+1], self.map[y+1][x]]
		wallblackcount = 0
		if self.map[y][x] == TileType.gray or self.map[y][x] == TileType.white:
			for coord in adjacents:
				if self.isWithinBounds(coord[1], coord[0]):
					tile = self.map[coord[0]][coord[1]]
				 	if tile == TileType.wall or tile == TileType.black:
					 	wallblackcount += 1
		if (self.map[y][x] == TileType.gray and wallblackcount >= 3) or (self.map[y][x] == TileType.white and wallblackcount == 4):
			return True

		layouts = [[[y-1, x], [y, x-1], [y+1, x+1]], [[y-1, x], [y, x+1], [y+1, x-1]], [[y+1,x], [y,x-1], [y-1,x+1]], [[y+1, x], [y, x+1], [y-1, x-1]]]
		if self.map[y][x] == TileType.gray:
			for layout in layouts:
				if self.isWithinBounds(layout[0][1], layout[0][0]) and self.isWithinBounds(layout[1][1], layout[1][0]) and self.isWithinBounds(layout[2][1], layout[2][0]):
					if (self.map[layout[0][0]][layout[0][1]] == TileType.wall or self.map[layout[0][0]][layout[0][1]] == TileType.black) and (self.map[layout[1][0]][layout[1][1]] == TileType.wall or self.map[layout[1][0]][layout[1][1]] == TileType.black) and (self.map[layout[2][0]][layout[2][1]] == TileType.gray or self.map[layout[2][0]][layout[2][1]] == TileType.black):
						return True
		return False

	def auditAdjacents(self, x, y):
		adjCoords = [[y, x-1], [y-1, x], [y, x+1], [y+1,x]]
		for coord in adjCoords:
			self.auditAndMarkBlack(coord[1], coord[0])

	def auditAndMarkBlack(self, x, y):
		if self.auditTile(x, y) and self.isWithinBounds(x, y):
			self.map[y][x] = TileType.black
			#self.auditAdjacents(x, y)
			return True
		return False
	def reAuditMap(self):
		y = 1#0
		while y < len(self.map)-1:#for col in self.map:
			x = 1#0
			while x < len(self.map[0])-1:#for row in col:
				if self.auditAndMarkBlack(x, y):
					return True
				x += 1
			y += 1
		return False

	def memorize(self, x, y, direction, result, surroundings = []):
		self.expand_if_needed(x, y)
		#print(surroundings)
		#if result == True and (len(surroundings) == 3  ):# and len(surroundings[0]) != 3):
		#	a = 0
		#	while a < 3:
		#		b = 0
		#		while b < 3:
		#			if surroundings[a][b] == 1:
		#				self.map[y+self.forY-1+a][x+self.forX-1+b] = TileType.wall
		#			elif surroundings[a][b] == 0:
		#				self.map[y+self.forY-1+a][x+self.forX-1+b] = TileType.gray
		#			b += 1
		#		a += 1
		if result == True:
			if self.map[y+self.forY][x+self.forX] == TileType.white:
				self.map[y+self.forY][x+self.forX] = TileType.gray
#			self.auditAndMarkBlack(x+self.forX, y+self.forY)
			#if direction == 'left':
			#	self.auditAndMarkBlack(x+self.forX+1, y+self.forY)
			#elif direction == 'right':
			#	self.auditAndMarkBlack(x+self.forX-1, y+self.forY)
			#elif direction == 'up':
			#	self.auditAndMarkBlack(x+self.forX, y+self.forY+1)
			#elif direction == 'down':
			#	self.auditAndMarkBlack(x+self.forX, y+self.forY-1)
				#self.map[y+self.forY][x+self.forX] = TileType.black

		elif result == False:
			if direction == 'left':
				self.map[y+self.forY][x+self.forX-1] = TileType.wall
#				self.auditAdjacents(x+self.forX-1, y+self.forY)
			elif direction == 'right':
				self.map[y+self.forY][x+self.forX+1] = TileType.wall
#				self.auditAdjacents(x+self.forX+1, y+self.forY)
			elif direction == 'up':
				self.map[y+self.forY-1][x+self.forX] = TileType.wall
#				self.auditAdjacents(x+self.forX, y+self.forY-1)
			elif direction == 'down':
				self.map[y+self.forY+1][x+self.forX] = TileType.wall
#				self.auditAdjacents(x+self.forX, y+self.forY+1)
		#elif direction == 'wait':
		#	self.map[y+self.forY][x+self.forX] = TileType.gray

#		self.auditAdjacents(x+self.forX, y+self.forY)
			self.reAuditMap()

	def rememberWall(self, x, y, direction):
		self.expand_if_needed(x, y)
		if direction == 'left':
			if self.map[y+self.forY][x+self.forX-1] == TileType.wall:
				return False
			else:
				return True
		elif direction == 'up':
			if self.map[y+self.forY-1][x+self.forX] == TileType.wall:
				return False
			else:
				return True
		elif direction == 'right':
			if self.map[y+self.forY][x+self.forX+1] == TileType.wall:
				return False
			else:
				return True
		elif direction == 'down':
			if self.map[y+self.forY+1][x+self.forX] == TileType.wall:
				return False
			else:
				return True
		return True

	def rememberBadTiles(self, x, y, direction):
		self.expand_if_needed(x, y)
		if direction == 'left':
			if self.map[y+self.forY][x+self.forX-1] == TileType.black or self.map[y+self.forY][x+self.forX-1] == TileType.gray:
				return False
			else:
				return True
		elif direction == 'up':
			if self.map[y+self.forY-1][x+self.forX] == TileType.black or self.map[y+self.forY-1][x+self.forX] == TileType.gray:
				return False
			else:
				return True
		elif direction == 'right':
			if self.map[y+self.forY][x+self.forX+1] == TileType.black or self.map[y+self.forY][x+self.forX+1] == TileType.gray:
				return False
			else:
				return True
		elif direction == 'down':
			if self.map[y+self.forY+1][x+self.forX] == TileType.black or self.map[y+self.forY+1][x+self.forX] == TileType.gray:
				return False
			else:
				return True
		return True

	def remove_bad_choices(self, x, y, directions):
		#self.expand_if_needed(x, y)
		copy = list(directions)
		for d in copy:
			if d == 'left':
				if self.rememberWall(x, y, d) is False:
					directions.remove('left')
			elif d == 'up':
				if self.rememberWall(x, y, d) is False:
					directions.remove('up')
			elif d == 'right':
				if self.rememberWall(x, y, d) is False:
					directions.remove('right')
			elif d == 'down':
				if self.rememberWall(x, y, d) is False:
					directions.remove('down')
		return directions

	def remove_grayblack_choices(self, x, y, directions):
		#self.expand_if_needed(x, y)
		copy = list(directions)
		for d in copy:
			if d == 'left':
				if self.rememberBadTiles(x, y, d) is False:
					directions.remove('left')
			elif d == 'up':
				if self.rememberBadTiles(x, y, d) is False:
					directions.remove('up')
			elif d == 'right':
				if self.rememberBadTiles(x, y, d) is False:
					directions.remove('right')
			elif d == 'down':
				if self.rememberBadTiles(x, y, d) is False:
					directions.remove('down')
		if len(directions) - 1 == 0:
			directions = list(copy)
		return directions

class TravelPath:
	def __init__(self, name = 'Joe'):
		self.name = name
		self.path = []
		self.pathlength = 0
		self.adjacents = []

	def push(self, direction):
		self.path.append(direction)
		self.pathlength += 1

	def pop(self):
		if self.pathlength >= 1:
			self.pathlength -= 1
			return self.path.pop()
		else:
			print("Error: Path too short")
			return None

class PathMemory:
	def __init__(self, name = 'Joe', fp = 'paths', mem = 'last.txt'):
		self.name = name
		self.folder = fp
		self.file = mem
		self.dir = self.folder + "/" + self.file
		self.memoryExists = False
		self.lastPath = TravelPath()

		if not os.path.exists(self.folder):
			print("No memory directory found.")
			try:
				os.mkdir(self.folder)
				print("Directory: " + self.folder + " created")
			except OSError:
				print("Directory: " , self.folder ,  " could not be created. Exitting...")
				sys.exit()
		else:
			print("Memory directory found: " + self.folder)

		if not os.path.exists(self.dir):
			print("No memory file found.")
			try:
				open(self.dir, 'w+')
				print("File: " + self.file + " created")
			except OSError:
				print("File: " + self.file + " could not be created. Exitting...")
				sys.exit()
		else:
			self.memoryExists = True
			print("Memory file found: " + self.dir)
		if self.memoryExists:
			self.read()
			self.shorten()


	def update(self, tpath):
		f = open(self.dir, 'w')
		#f.write(str(x) + "\n")
		#f.write(str(y) + "\n")
		path = tpath.path
		while len(path) > 0:
			f.write(path[0] + "\n")
			path = path[1:]
		f.close()

	def read(self):
		path = TravelPath()
		f = open(self.dir, 'r')
		path.path = f.read().splitlines()
		f.close()

		path.pathlength = len(path.path)
		print(path.path)
		print(path.pathlength)
		path.path = path.path[::-1]
		self.lastPath = path
		if self.lastPath.pathlength == 0:
			self.memoryExists = False

	def shorten(self):
		def shortenable(a, b, c):
			print(a + " " + b + " " + c)
			if a == 'down' and c == 'up' and (b == 'left' or b == 'right'):
				return True
			elif a == 'up' and c == 'down' and (b == 'left' or b == 'right'):
				return True
			elif a == 'left' and c == 'right' and (b == 'up' or b == 'down'):
				return True
			elif a == 'right' and c == 'left' and (b == 'up' or b == 'down'):
				return True
			return
		shortcut = self.lastPath.path[:]
		a = 0
		while a < len(shortcut) - 2 and len(shortcut) >= 3:
			if shortenable(shortcut[a], shortcut[a+1], shortcut[a+2]):
				print(True)
				shortcut = shortcut[0:a] + shortcut[a+1:a+2] + shortcut[a+3:]
			else:
				a += 1
		print("Pre-shortened Previous Path: " + str(self.lastPath.path))
		self.lastPath.path = shortcut
		self.lastPath.pathlength = len(shortcut)
		print("Shortened: Path: " + str(self.lastPath.path))

class Mind:
	def __init__(self, name = 'Joe'):
		self.name = name
		self.map = MemoryMap()
		self.relX = (self.map.sizeX + 1)/2
		self.relY = (self.map.sizeY + 1)/2
		self.map.memorize(self.relX, self.relY, 'wait', True)
		self.path = TravelPath()
		self.pathMem = PathMemory()
		self.recentWhiteAdjacents = TravelPath()
		self.normalExit = False

	#def __del__(self):
	#	if self.normalExit:
	#		self.pathMem.update(self.path)

	def move(self, direction):
		if direction == 'left':
			self.relX -= 1
		elif direction == 'up':
			self.relY -= 1
		elif direction == 'right':
			self.relX += 1
		elif direction == 'down':
			self.relY += 1

	def learn(self, direction, result, surroundings = []):
		#if self.map.expand_if_needed(self.relX, self.relY):
		#	self.relX += self.map.sizeX/4
		#	self.relY += self.map.sizeY/4
		if result == True:
			self.move(direction)
		self.map.memorize(self.relX, self.relY, direction, result, surroundings)
		#if result == True:
		#	self.move(direction)

	def remove_bad_choices(self, directions):
		#if self.map.expand_if_needed(self.relX, self.relY):
		#	self.relX += self.map.sizeX/4
		#	self.relY += self.map.sizeY/4
		return self.map.remove_bad_choices(self.relX, self.relY, directions)

	def remove_grayblack_choices(self, directions):
		#if self.map.expand_if_needed(self.relX, self.relY):
		#	self.relX += self.map.sizeX/4
		#	self.relY += self.map.sizeY/4
		return self.map.remove_grayblack_choices(self.relX, self.relY, directions)

class DecisionFactory:
	def __init__(self, name = 'Joe'):
		self.name = name
		self.directions = [ 'wait', 'left', 'up', 'right', 'down']#'up', 'down', 'right', 'left']
		self.last_result = 'success'
		self.last_direction = 'wait'
		self.mind = Mind()
		self.backtravelling = False
		self.following = self.mind.pathMem.memoryExists
		# Note: we have relativisitic coordinates recorded here, since the map
		# is relative to the players first known recorded position:
		# self.state.pos = (0, 0)
		random.seed(random.randint(1, 5000))

	def get_decision(self, verbose = True):
		if self.following:
			#print(self.mind.pathMem.lastPath.path)
			dir = self.mind.pathMem.lastPath.pop()
		else:
			dir = self.smart_direction()
		self.last_direction = dir
		print("Direction: " + str(dir) + "\n")
		return dir

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

	def smart_direction(self):
		options = list(self.directions)
		print("Available Decisions " + str(options))
		self.mind.remove_bad_choices(options)
		print("Moveable Decisions " + str(options))
		self.mind.remove_grayblack_choices(options)
		print("Smart Decisions " + str(options))
		print("Travel Path: " + str(self.mind.path.path))
		size = len(options)
		if size == 1:
			if len(self.mind.path.path) > 0:
				self.backtravelling = True
				print("No White Spaces. Back-travelling...")
				dir = self.mind.path.pop()
				print("Last Direction: " + dir)
				if dir == 'left':
					dir = 'right'
				elif dir == 'up':
					dir = 'down'
				elif dir == 'right':
					dir = 'left'
				elif dir == 'down':
					dir = 'up'
			else:
				dir = self.random_direction()
		else:
			r = random.randint(1, size-1)
			dir = options[r]
			while self.check_decision(r) is False:
				r = random.randint(1, size-1)

		self.last_direction = dir

		print("Direction: " + dir)
		return dir

	def put_result(self, result, surroundings = []):
		if result == 'success':
			self.last_result = True
		else:
			self.last_result = False
		self.mind.learn(self.last_direction, self.last_result, surroundings)
		if self.following and self.last_result is False:
			self.following = False
		if self.last_result is True:
			if self.backtravelling is False:
				self.mind.path.push(self.last_direction)
			else:
				self.backtravelling = False
