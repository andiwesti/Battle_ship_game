import random
import os


class Field(object):
	def __init__(self, size=100, number_of_ships=0):
		self.size = size
		self.number_of_ships = number_of_ships
		self.ships = []
		self.field = ['[ ]' for i in range(100)]
		self.coordinates_field = []  # list of coordinates, creating below
		self.statuses = [False for i in self.field]

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

	def print_field_with_ships(self):  # TODO make better field appearence
		print('     a      b      c      d      e      f      g      h      i      j')
		for i in range(0, 100, 10):
			print(str(i)[0], self.field[i:i + 10])

	def print_field_with_known_ships(self):
		field_with_known_ships = []
		# Checking statuses list for the cell is known by opponent
		for index, cell in enumerate(self.field):
			if cell == '[ ]' and self.statuses[index]:
				field_with_known_ships.append('[-]')
			elif cell == '[ ]':
				field_with_known_ships.append(cell)
			if cell == '[X]' and self.statuses[index]:
				#field_with_known_ships.append(cell)
				for ship in self.ships:
					for element in ship:
						if element == self.coordinates_field[index]:
							field_with_known_ships.append(ship[element])
			elif cell == '[X]':
				field_with_known_ships.append('[ ]')

		'''for j, i in enumerate(self.field):
			if i == '[X]':
				field_with_known_ships.append('[ ]')
			elif i == '[X]' and self.statuses[j]:#i == '[O]':
				for ship in self.ships:
					for element in ship:
						print(element)
						if element == self.coordinates_field[self.field.index(i)]:
							print(ship[element])
							print(self.coordinates_field[self.field.index(i)])
							field_with_known_ships.append('[O]')
			elif i == '[ ]':
				field_with_known_ships.append(i)
			elif i == '[ ]' and self.statuses[j]:
				print('ok')
				field_with_known_ships.append(['[-]'])'''
		print('     a      b      c      d      e      f      g      h      i      j')
		for i in range(0, 100, 10):
			print(str(i)[0], field_with_known_ships[i:i + 10], end='\n')

	# TODO make it to check if inputs and position of new ship are correct
	# and it is possible before placing it to the field
	def get_ships_from_player(self, current_player):
		while self.number_of_ships < 3:
			os.system("clear")
			print(self.number_of_ships)
			ship = {}
			print(current_player.name.capitalize(), "'s field: ")
			self.print_field_with_ships()
			'''one_deck_ships = []
			two_decks_ships = []
			three_decks_ships = []
			four_decks_ship = []
			
			def print_no_more_ships_text():'''
				#print('You can add only:\n'
				#	'4 ships of lenght 1\n'
					#'3 ships of lenght 2\n'
					#'2 ships of lenght 3\n'
					#'1 ships of lenght 4

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
			lenght = int(input('Please, choose lenght of the ship: '))
			while not lenght or lenght > 4:
				lenght = int(input('Try again, length can not be more then 4: '))
			orientation = input('Please, choose orientation of the ship horizontal[h] or vertical[v]')

			for i in self.coordinates_field:
				if x in i and y in i:
					ship[i] = '[ ]'
					first_element_index = self.coordinates_field.index(i)  # index of i (the first element of the ship)
					if orientation == 'h':
						for i in range(1, lenght):
							ship[self.coordinates_field[first_element_index + i]] = '[ ]'
						self.number_of_ships += 1
					elif orientation == 'v':
						for i in range(1, lenght):
							ship[self.coordinates_field[first_element_index + i * 10]] = '[ ]'
						self.number_of_ships += 1
					else:
						os.system('clear')
						print('You can choose only vertical or horizontal orientation! [v/h]')
						current_player.field.get_ships_from_player(current_player)
					for i in ship:
						self.field[self.coordinates_field.index(i)] = '[X]'
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
		if self.opponent.field.field[self.opponent.field.coordinates_field.index(position)] == '[X]':
			for ship in self.opponent.field.ships:
				for element in ship:
					if element == position:
						ship[position] = '[X]'
			#self.opponent.field.field[self.opponent.field.coordinates_field.index(position)] = '[O]'
			self.opponent.field.statuses[self.opponent.field.coordinates_field.index(position)] = True
			if shot.is_ship_dead():
				self.opponent.field.number_of_ships -= 1
				#print(self.opponent.field.number_of_ships)
			if not is_game_finished(player1, player2):
				shot.shot(shot, player1, player2)
		elif self.opponent.field.field[self.opponent.field.coordinates_field.index(position)] == '[ ]':
			#self.opponent.field.field[self.opponent.field.coordinates_field.index(position)] = '[-]'
			self.opponent.field.statuses[self.opponent.field.coordinates_field.index(position)] = True
		'''elif self.opponent.field.field[self.opponent.field.coordinates_field.index(position)] == '[O]' or self.opponent.field.field[self.opponent.field.coordinates_field.index(position)] == '[-]':
			print('You have already shot here!')
			input('Press Enter to continue')
			shot.shot(shot, player1, player2)'''

	def is_ship_dead(self):
		dead = 0
		for ship in self.opponent.field.ships:
			if list(ship.values()).count('[X]') == len(ship):
				for element in ship:
					ship[element] = '[Ж]'
					dead += 1
		if dead > 0:
			return True
		else:
			return False

				#return True
			#else:
				#return False
#
				#dead = True
	#	if dead:
		#	self.opponent.field.number_of_ships -= 1




class Player(object):
	def __init__(self, name, field):
		self.name = name
		self.field = field
		self.win = False

	def print_clear_field(self):
		print('     a      b      c      d      e      f      g      h      i      j')
		for i in range(0, 100, 10):
			print(str(i)[0], self.clear_field[i:i + 10])


'''class Ships(object):
	def __init__(self):
		self.ships = []
	def get_ships_from_player(self, player):
		counter = 0
		while counter <= 2:
			ship = []
			player.field.print_field_with_ships()
			x, y = input('Please input coordinates of the ship: ')
			lenght = int(input('Please, choose lenght of the ship: '))
			orientation = input('Please, choose orientation of the ship horizontal[h] or vertical[v]')
			# какая то херня, надо все переделать(
			for i in player.field.coordinates_field:
				if x in i and y in i:
					ship.append(i)
					cell = player.field.coordinates_field.index(i) #index of i (the first element of the ship)
					if orientation == 'h':
						for i in list(enumerate(range(1, lenght +1))):

							

						for index, value in enumerate(list(range(1, lenght + 1))):
							cell = player.field.coordinates_field.index(i) + value
							ship.append(cell)
							self.ships.append(ship)
							counter += 1'''

# '''корабли буду хранить в виде списка списков, где каждый список это корабль,
# этот список будет состоять из н элементов где колличество н это длинна корабля, а
# каждый элемент будет в виде а1, как в поле координат, и собстевнно обозначать координату
# каждой ячейки корабля'''

'''Main game logic and some functions'''


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
