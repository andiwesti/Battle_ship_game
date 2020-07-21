import random
import os

class Field(object):
	def __init__(self, number_of_ships=0):
		self.number_of_ships = number_of_ships
		self.ships = []  #list of player's ships
		self.field = ['_' for i in range(100)]
		self.coordinates_field = []  # list of coordinates, creating below
		self.statuses = [False for i in self.field]

		self.len_one_ships = []
		self.len_two_ships = []
		self.len_three_ships = []
		self.len_four_ships = []

		''' Making list with coordinates
		like a0, b0, c0, etc'''
		letters = 'a b c d e f g h i j'.split()
		self.coordinates_field += letters * 10
		nums = '0123456789'
		nums_list = ''
		for i in nums:
			nums_list += i * 10
		for i, j in enumerate(nums_list):
			self.coordinates_field[i] += str(j)

	def print_field_with_ships(self): 
		print('  a b c d e f g h i j')
		for i in range(0, 100, 10):
			print(str(i)[0], 'I'.join(self.field[i:i + 10]))

	def print_field_with_known_ships(self):
		field_with_known_ships = []
		# Checking statuses list for the cell is known by opponent
		for index, cell in enumerate(self.field):
			if cell == '_' and self.statuses[index]:
				field_with_known_ships.append('•')
			elif cell == '_':
				field_with_known_ships.append(cell)
			if cell == 'X' and self.statuses[index]:
				for ship in self.ships:
					for element in ship:
						if element == self.coordinates_field[index]:
							field_with_known_ships.append(ship[element])
			elif cell == 'X':
				field_with_known_ships.append('_')

		print('  a b c d e f g h i j')
		for i in range(0, 100, 10):
			print(str(i)[0], 'I'.join(field_with_known_ships[i:i + 10]), end='\n')

	# TODO make it to check if it is possible to place new ship
	def get_ships_from_player(self, current_player):
		while self.number_of_ships < 2:
			os.system("clear")
			ship = {}
			print(current_player.name.capitalize(), "'s field: ")
			self.print_field_with_ships()


			while True:
				text = 'abcdefghij0123456789'
				try:
					x, y = input(current_player.name.capitalize() + ', please input coordinates of the ship: ')
					if x not in text or y not in text:    # raise error if where is no correct characters in coordinates
						raise ValueError
					if x.isalpha() and y.isalpha():    # raise error if two letters in coordinates
						raise ValueError
					if x.isdecimal() and y.isdecimal():   # raise error if two numbers in coordinates
						raise ValueError
					break
				except:
					print('Incorrect coordinates, try again')
					continue

			while True:
				try:
					lenght = int(input('Please, choose lenght of the ship: '))
					break
				except:
					print('Incorrect input')
					continue

			while not lenght or lenght > 4:
				try:
					lenght = int(input('Try again, lenght can not be more then 4: '))
				except:
					print('Incorrect input')
					continue

			while len(self.len_one_ships) >= 4 and lenght == 1 or len(self.len_two_ships) >= 3 and lenght == 2 or len(self.len_three_ships) >= 2 and lenght == 3 or len(self.len_four_ships) >= 1 and lenght == 4:
				print('You can add only:\n'
					'4 ships of lenght 1\n'
					'3 ships of lenght 2\n'
					'2 ships of lenght 3\n'
					'1 ships of lenght 4')
				while True:
					try:
						lenght = int(input('Try again: '))
						break
					except:
						print('Incorrect input')
						continue

			self.len_one_ships.append(1) if lenght == 1 else None
			self.len_two_ships.append(1) if lenght == 2 else None
			self.len_three_ships.append(1) if lenght == 3 else None 
			self.len_four_ships.append(1) if lenght == 4 else None

			orientation = input('Please, choose orientation of the ship horizontal[h] or vertical[v]')

			for i in self.coordinates_field:
				if x in i and y in i:
					ship[i] = '_'
					first_element_index = self.coordinates_field.index(i)  # index of i (the first element of the ship)
					if orientation == 'h':
						for i in range(1, lenght):
							ship[self.coordinates_field[first_element_index + i]] = '_'
						self.number_of_ships += 1
					elif orientation == 'v':
						for i in range(1, lenght):
							ship[self.coordinates_field[first_element_index + i * 10]] = '_'
						self.number_of_ships += 1
					else:
						os.system('clear')
						print('You can choose only vertical or horizontal orientation! [v/h]')
						current_player.field.get_ships_from_player(current_player)
					for i in ship:
						self.field[self.coordinates_field.index(i)] = 'X'
					self.ships.append(ship)

class ShotAt(object):
	def __init__(self, current_player, opponent):
		self.current_player = current_player
		self.opponent = opponent

	def shot(self, shot, player1, player2):
		os.system("clear")
		self.opponent.field.print_field_with_known_ships()
		while True:
			text = 'abcdefghij0123456789'
			try:
				x, y = input(self.current_player.name.capitalize() + ', please, enter coordinates to shot: ')
				if x not in text or y not in text:  # raise error if where is no correct characters in coordinates
					raise ValueError
				if x.isalpha() and y.isalpha():  # raise error if two letters in coordinates
					raise ValueError
				if x.isdecimal() and y.isdecimal():  # raise error if two numbers in coordinates
					raise ValueError
				break
			except:
				print('Incorrect coordinates, try again')
				continue
		position = None
		for i in self.opponent.field.coordinates_field:
			if x in i and y in i:
				position = i
		if self.opponent.field.statuses[self.opponent.field.coordinates_field.index(position)]:
			print('You have already shoot here, try again')
			input('Press Enter to continue')
			shot.shot(shot, player1, player2)
		if self.opponent.field.field[self.opponent.field.coordinates_field.index(position)] == 'X':
			for ship in self.opponent.field.ships:
				for element in ship:
					if element == position:
						ship[position] = 'X'
			self.opponent.field.statuses[self.opponent.field.coordinates_field.index(position)] = True
			if shot.is_ship_dead():
				self.opponent.field.number_of_ships -= 1
			if not is_game_finished(player1, player2):
				shot.shot(shot, player1, player2)
		elif self.opponent.field.field[self.opponent.field.coordinates_field.index(position)] == '_':
			self.opponent.field.statuses[self.opponent.field.coordinates_field.index(position)] = True

	def is_ship_dead(self):
		dead = 0
		for ship in self.opponent.field.ships:
			if list(ship.values()).count('X') == len(ship):
				for element in ship:
					ship[element] = 'Ж'
					dead += 1
		if dead > 0:
			return True
		else:
			return False

class Player(object):
	def __init__(self, name, field):
		self.name = name
		self.field = field
		self.win = False


# This will check is where all opponents ships were killed
def is_game_finished(player1, player2):
	if player2.field.number_of_ships == 0:
		player1.win = True
		return True
	elif player1.field.number_of_ships == 0:
		player2.win = True
		return True
	else:
		return False

# This is switching playes and if it's first turn setting who will make first shot
def switch_player(current_player, player1, player2):
	if current_player == player1:
		current_player = player2
		return current_player
	elif current_player == player2:
		current_player = player1
		return current_player
	else:
		choise_or_coin = input('Do you want to [c]hoose who will be the first or you can [f]lip a coin: ')
		while choise_or_coin not in 'cf':
			choise_or_coin = input('Try again! Only c/f allowed: ')
		if choise_or_coin == 'c':
			choise = input('Who will be the first to shoot, enter the name: ')
			if choise.lower() == player1.name.lower():
				print('Ok!')
				return player1
			if choise.lower() == player2.name.lower():
				print('Ok!')
				return player2
		if choise_or_coin.lower() == 'f':
			current_player = random.choice([player1, player2])
			print(current_player.name.capitalize(), 'is the first!')
			input('Press Enter to start placing ships')
			return current_player


def game():
	os.system("clear")
	name1 = name2 = input('Player 1, please, enter your name: ')
	while name1 == name2:
		name2 = input('Player 2, please, enter your name: ')
	player1_field, player2_field = Field(), Field()
	player1, player2 = Player(name1, player1_field), Player(name2, player2_field)
	current_player = None
	current_player = switch_player(current_player, player1, player2)
	opponent = player1 if current_player == player2 else player2
	player1.field.get_ships_from_player(player1)
	player2.field.get_ships_from_player(player2)

	# Start of the main loop
	while True:
		shot = ShotAt(current_player, opponent)
		shot.shot(shot, player1, player2)
		if is_game_finished(player1, player2):
			break

		current_player = switch_player(current_player, player1, player2)
		opponent = player1 if current_player == player2 else player2

	if player2.win:
		print(player2.name.capitalize() + ' has won!')
	if player1.win:
		print(player1.name.capitalize() + ' has won!')



if __name__ == '__main__':
	game()
