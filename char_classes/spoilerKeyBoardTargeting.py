from functions import *
from bot import Bot
import random

class Spoiler(Bot):
	ATTACKS_LIMIT_BEFORE_TURN = 3

	__spoiled = False

	def loop(self, stop_event):

		attacks = 0
		while not stop_event.is_set():
			targeted_hp = self.get_targeted_hp()
			if targeted_hp > 0:
				print('target hp', targeted_hp, '%')
				self.useless_steps = 0

				self.spoil(targeted_hp)

				if attacks > self.ATTACKS_LIMIT_BEFORE_TURN and targeted_hp >= 100:
					print('turn')
					self.turn()
					time.sleep(0.2)
					print('go somewhere')
					self.go_somewhere()
					time.sleep(0.6)
					attacks = 0

				print("attack the target")
				self.autohot_py.F1.press()
				attacks += 1
				continue
			elif targeted_hp == 0:

				if self.__spoiled is True:
					self.__spoiled = False
					print("sweep")
					self.autohot_py.F3.press()
					time.sleep(0.2)
					self.autohot_py.F3.press()
					time.sleep(0.2)

				self.autohot_py.F5.press()
				time.sleep(0.3)
				self.autohot_py.F1.press()
				targeted_hp = self.get_targeted_hp()
				if targeted_hp:
					print('under attack!')
					self.spoil(targeted_hp)
					continue

				print("picking up drop")
				for i in range(5):
					self.autohot_py.F4.press()
					time.sleep(0.7)
				print("target is dead, find another")
				self.set_target()

				continue
			else:
				print("no target yet")
				# Find and click on the victim
				self.__spoiled = False
				self.useless_steps = 0
				print("define target")
				self.set_target()

				targeted_hp = self.get_targeted_hp()
				if targeted_hp:
					time.sleep(0.5)
					self.autohot_py.F1.press()
					continue
				elif self.useless_steps > 2:
					# We're stuck, go somewhere
					self.useless_steps = 0
					print("go_somewhere - we're stuck")
					self.go_somewhere()
				else:
					# Turn on 90 degrees
					self.useless_steps += 1
					self.turn()
					print("turn")

		print("loop finished!")

	def spoil(self, targeted_hp):

		if targeted_hp < 70 and not self.__spoiled:
			print("spoil")
			self.__spoiled = True
			self.autohot_py.F2.press()
			time.sleep(0.3)

	def set_target(self):
		random_target = int(random.randrange(0, 2))

		if random_target == 1:
			self.autohot_py.F6.press()
		elif random_target == 2:
			self.autohot_py.F8.press()
		else:
			self.autohot_py.F7.press()