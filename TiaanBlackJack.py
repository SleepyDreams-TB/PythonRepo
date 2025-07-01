import random

deck = {
    'Hearts':   ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'],
    'Diamonds': ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'],
    'Clubs':    ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'],
    'Spades':   ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
}
playerCards = []
houseCards = []

def draw_random_card():
    suit = random.choice(list(deck.keys()))
    card = random.choice(deck[suit])
    deck[suit].remove(card)

    print(f"Random drawn card: {card} of {suit}")
    return card


def get_player_cards():
    card = draw_random_card()
    playerCards.append(card)

def get_house_cards():
    card = draw_random_card()
    houseCards.append(card)


def hand_total(isplayer):
    result = 0
    aces_found = 0

    if isplayer:
        for i in range(len(playerCards)):
            if playerCards[i] in ['J', 'Q', "K"]:
                    result += 10
            elif playerCards[i] == 'A':
                result += aces(is_player = True)
            else:
                result += int(playerCards[i])
        print("Player Hand Total:", result)
    else:
        for i in range(len(houseCards)):
            if houseCards[i] in ['J', 'Q', "K"]:
                result += 10
            elif houseCards[i] == 'A':
                aces_found += 1
            else:
                result += int(houseCards[i])

        if aces_found != 0:
            ace_value = 0
            if result + aces(is_player=False) >= 21:
                ace_value += 1
            else:
                ace_value += 11
            result += ace_value
            print("House chose Ace Value:", ace_value)
            print("House Hand Total:", result)

        else:
            print("House Hand Total:", result)
    return result

def aces(is_player):
    ace = 0

    if is_player:
        valid_input = False
        ace_str = input("You Drew a Ace, would you like it to count as 1 or 11?")
        while not valid_input:
            if ace_str in ['1', '11']:
                ace += int(ace_str)
                valid_input += True
            else:
                print("incorrect Input Received, Type either 1 or 11")
                valid_input += False
    return ace


def blackjack():
    get_player_cards()
    get_player_cards()
    hand_total(isplayer=True)
    get_house_cards()
    get_house_cards()
    hand_total(isplayer=False)


blackjack()

