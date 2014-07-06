#!/usr/bin/python

# Copyright 2014 Justin Cano
#
# This is a simple Python program of the game Blackjack
# (http://en.wikipedia.org/wiki/Blackjack), developed for
# a coding challenge from the 2014 Insight Data Engineering
# Fellows Program application.
#
# Licensed under the GNU General Public License, version 2.0
# (the "License"), this program is free software; you can
# redistribute it and/or modify it under the terms of the 
# License.
#
# You should have received a copy of the License along with this
# program in the file "LICENSE". If not, you may obtain a copy of 
# the License at
#	http://www.gnu.org/licenses/gpl-2.0.html
#
import random
import time

def shuffleDeck(numDecks):
	"""
	Builds, shuffles, and returns a deck of 52 * numDecks cards
	Deck is represented as a list of cards
	Cards are represented as strings labeled as their rank and suit
	Examples: '7H' - 7 Hearts
			  'TS' - 10 Spades
	"""
	deck = [r+s for r in '23456789TJQKA'*numDecks for s in 'SHDC']
	random.shuffle(deck)
	return deck

def changeNumDecks():
	"""
	Prompts user to change the number of decks to use
	Returns new number of decks to use
	"""
	numDecks = 0
	while numDecks <= 0:
		try:
			numDecks = int(raw_input("Enter number of decks to use:\n% "))
			assert numDecks > 0
		except (ValueError, AssertionError):
			print "Invalid input! Must be integer value greater than 0"
	return numDecks

def getBet(chips):
	"""
	Prompts user for bet value
	User input must be greater than 0 and less than chips
	Returns bet
	"""
	bet = 0
	while bet <= 0 or bet > chips:
		try:
			bet = float(raw_input("How much do you wanna bet?\n% "))
			assert bet > 0 and bet <= chips
		except ValueError:
			print "Invalid input! Must be integer or float value greater than 0 and less than the number of available chips"
		except AssertionError:
			print "You don't have that many chips!"
	return bet

menuChoices = ['',"PLAY","DECK","EXIT"]
def menu():
	"""
	Menu
	Prompts the user to choose menu option:
	1 - Play
	2 - Change # of decks
	3 - Exit
	Returns user selection
	"""
	choice = 0
	maxChoice = len(menuChoices)
	while choice <= 0 or choice >= maxChoice:
		try:
			choice = int(raw_input("Menu: 1 - Play | 2 - Change # of Decks | 3 - Exit\n% "))
			assert choice >= 1 and choice < maxChoice
		except (ValueError, AssertionError):
			print "Invalid choice! Must be [1-" + str(maxChoice-1) + "]"
	return menuChoices[choice]

blackjackChoices = ['',"HIT","STAND"]
def blackjackMenu():
	"""
	Prompts user to choose Blackjack option:
	1 - Hit
	2 - Stand
	Can be extended for advanced options, i.e. split, double
	Returns user selection
	"""
	choice = 0
	maxChoice = len(blackjackChoices)
	while choice <= 0 or choice >= maxChoice:
		try:
			choice = int(raw_input("Options: 1 - Hit | 2 - Stand\n% "))
			assert choice >= 1 and choice < maxChoice
		except (ValueError, AssertionError):
			print "Invalid choice! Must be [1-" + str(maxChoice-1) + "]"
	return blackjackChoices[choice]

def deal(deck):
	"""
	Pops and returns the first card in deck
	"""
	card = deck[0]
	del deck[0]
	return card

def rank(hand):
	"""
	Return the sum of the ranks in a hand
	Face cards are of rank 10
	Aces are of rank 11 or 1
	Example: rank(['7H','AS','JD']) => 18
	"""
	# Extract all ranks from hand
	ranks = [10 if r == 'T' or r == 'J' or r =='Q' or r == 'K' else
			11 if r == 'A' else
			int(r) for r,s in hand]

	# While there are 11-ranked Aces in hand and hand rank is greater than 21,
	while 11 in ranks and sum(ranks) > 21:
		"""
		Change rank of Aces to 1
		one Ace at a time
		until hand rank is less than 21
		or until there are no more 11-ranked Aces
		"""
		index = ranks.index(11)
		ranks[index] = 1
	return sum(ranks)

def showCards(dealer,player,turn="player"):
	"""
	Print cards on screen
	If player's turn, hide dealer's second card and rank
	"""
	print "*" * 20
	print "Dealer Cards:", rank([dealer[0]]) if turn is "player" else rank(dealer)
	for card in dealer:
		if card is dealer[1] and turn is "player":
			card = "--"
		print card,
	print 
	print "Player Cards:", rank(player)
	for card in player:
		print card,

	print
	print "*" * 20

def blackjack(dealer, player, chips, bet):
	"""
	Evaluates and compares dealer and player hands
	Calculates winnings and adds to chips
	Returns chips
	"""
	# Player bust
	if rank(player) > 21:
		print "Bust!"

	# Push
	elif rank(dealer) == rank(player):
		chips += bet
		print "Push"

	# Player gets Blackjack
	elif rank(player) == 21 and len(player) == 2:
		chips += 2.5*bet
		print "You got Blackjack!"

	# Dealer bust or player beats dealer
	elif rank(dealer) > 21 or rank(player) > rank(dealer):
		chips += 2*bet
		print "You win!"

	# Dealer beats player
	else:
		print "You lose!"

	return chips
	
def main():
	chips = 100
	numDecks = changeNumDecks()
	choice = ''

	# while there are still chips available to bet
	while chips > 0:
		print "Chips:", chips

		# Display menu
		while choice != "PLAY":
			choice = menu()
			if choice == "DECK":
				numDecks = changeNumDecks()
				print "Changed # of decks to:", numDecks
			elif choice == "EXIT":
				print "\nCashing out with", chips, "chips..."
				print "Thanks for playing!\n"
				return

		print
		bet = getBet(chips)
		print
		chips = chips - bet
		print "Chips:", chips
		print "Bet:", bet
		deck = shuffleDeck(numDecks)
		dealerCards, playerCards = [], []
		dealerRank, playerRank = 0, 0

		# Deal cards by appending the first card from deck to list
		playerCards.append(deal(deck))
		dealerCards.append(deal(deck))
		playerCards.append(deal(deck))
		dealerCards.append(deal(deck))

		# Player goes first
		blackjack.turn = "player"

		# Check for dealer Blackjack
		if rank(dealerCards) == 21:
			print "\nDealer got blackjack!"
			showCards(dealerCards,playerCards,"dealer")
			blackjack.turn = None

		# Check player for Blackjack
		elif rank(playerCards) == 21:
			showCards(dealerCards,playerCards)
			blackjack.turn = None

		# Else show cards
		else:
			showCards(dealerCards,playerCards)

		# Player's turn
		while blackjack.turn is "player":
			choice = blackjackMenu()

			if choice == "HIT": 
				playerCards.append(deal(deck))
			elif choice == "STAND":
				blackjack.turn = "dealer"
				break

			showCards(dealerCards,playerCards)
			playerRank = rank(playerCards)

			# Bust
			if playerRank > 21:
				blackjack.turn = None
			# Twenty-One
			elif playerRank == 21:
				print "\nYou got 21!"
				# Pause so player notices 21
				time.sleep(1)
				blackjack.turn = "dealer"

		print

		# Dealer's turn
		while blackjack.turn is "dealer":
			showCards(dealerCards,playerCards,blackjack.turn)
			dealerRank = rank(dealerCards)

			if dealerRank > 21:
				print "\nDealer busts!"
				blackjack.turn = None
			elif dealerRank < 17:
				print "\nDealer hits"
				dealerCards.append(deal(deck))
			else:
				blackjack.turn = None
			
			# Pause between dealer moves so player can see dealer's actions
			time.sleep(1)

		# Compare hands and update available chips
		chips = blackjack(dealerCards, playerCards, chips, bet)
		choice = ''
		print
			

	print "No more chips available"
	print "Thanks for playing!\n"






if __name__ == "__main__":
	main()

