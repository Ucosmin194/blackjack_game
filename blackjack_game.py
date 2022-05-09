import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f'{self.rank} of {self.suit}'


class Deck:

    def __init__(self):
        self.deck = []  # starts with an emty list

        for rank in ranks:
            for suit in suits:
                self.deck.append(Card(suit, rank))

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def deal_one(self):
        return self.deck.pop()

    def __str__(self):
        return f"{[x.rank + ' of ' + x.suit for x in self.deck]}"


class Hand:

    def __init__(self):
        self.cards = []  # start with and empty list
        self.value = 0  # start with zero value
        self.aces = 0  # add an attribute to keep track of aces

    def add_card(self, card):

        # card passed in
        # from Deck.deal() --> single Card(suit, rank)
        self.cards.append(card)
        self.value += values[card.rank]

        # track aces
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        # If total value > 21 and i still have an ace
        # than change my ace to be a 1 instead of an 11

        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user imput
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))

        except ValueError:
            print("Sorry, please provide an integer")

        else:
            if chips.bet > chips.total:
                print(f"Sorry, you don't have enough chips! You have {chips.total}")
            else:
                break


def hit(deck, hand):
    single_card = deck.deal_one()
    hand.add_card(single_card)
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing  # to control an upcoming while loop

    while True:
        x = input('Hit or stand? Enter h or s: ')

        if x[0].lower() == 'h':
            hit(deck, hand)
        elif x[0].lower() == 's':
            print("Player Stands Dealer's Turn")
            playing = False
        else:
            print('Sorry, wrong input. Please enter h or s only!')
            continue
        break


def show_some(player, dealer):
    # dealer.cards[1]
    # Show only one of the dealer's cards
    print("\n Dealer's Hand: ")
    print("First card hidden!")
    print(dealer.cards[1])

    # Show all (2 cards) of the player's hand/cards
    print("\n Player's hand:")
    for card in player.cards:
        print(card)


def show_all(player, dealer):
    # show all the dealer's cards
    print("\n Dealer's hand:")
    for card in dealer.cards:
        print(card)

    # calculate and display value (j+k == 20)
    print(f"Value of dealer's hand is: {dealer.value}")

    # show all the players cards
    print("\n Player's hand:")
    for card in player.cards:
        print(card)
    print(f"Value of player's hand is: {player.value}")


def player_busts(player, dealer, chips):
    print("Bust player!")
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print("Player wins!")
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    print("Player wins! Dealer busted!")
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    print("Bust player. Dealer wins!")
    chips.lose_bet()


def push(player, dealer):
    print("Dealer and player tie! Push!")


player_chips = Chips()
while True:

    # Print an opening statement
    print("Welcome to Blackjack! Let's play")

    # create and shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle_deck()

    player_hand = Hand()
    player_hand.add_card(deck.deal_one())
    player_hand.add_card(deck.deal_one())


    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal_one())
    dealer_hand.add_card(deck.deal_one())

    # Set up the player's chips


    # Prompt the player for their bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)
    playing = True
    while playing:  # the variable from hit_or_stand function

        # Prompt for player to hit or stand
        hit_or_stand(deck, player_hand)
        # Show cards(but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

    # If player hasn't busted, player dealer's hand until dealer reaches the value of player's hand
    if player_hand.value <= 21:

        while dealer_hand.value < player_hand.value:
            hit(deck, dealer_hand)

        # Show all cards
        show_all(player_hand, dealer_hand)

        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)

        else:
            push(player_hand, dealer_hand)

    # Inform the player of their remaining chips
    print(f"\n Player total chips are: {player_chips.total}")

    # Ask to play again
    new_game = input("Would you like to play another game? y / n")

    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Thank you for playing!")
        playing = False
        break
