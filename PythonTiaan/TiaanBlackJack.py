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
    f"{card} of {suit}"
    return card


def get_player_cards():
    card = draw_random_card()
    playerCards.append(card)

def get_house_cards():
    card = draw_random_card()
    houseCards.append(card)


def hand_total(isplayer = True):
    result = 0


    if isplayer:
        for i in range(len(playerCards)):
            if playerCards[i] in ['J', 'Q', "K"]:
                    result += 10
            elif playerCards[i] == 'A':
                result += aces(True)
                playerCards.pop(playerCards.index('A'))
                playerCards.append(str(aces(True)))
            else:
                result += int(playerCards[i])
    else:
        aces_found = 0
        for i in range(len(houseCards)):
            if houseCards[i] in ['J', 'Q', "K"]:
                result += 10
            elif houseCards[i] == 'A':
                aces_found += 1
            else:
                result += int(houseCards[i])

        for _ in range(aces_found):
            if result + 11 <= 21:
                result += 11
            else:
                result += 1
    return result

def aces(is_player):
    ace = 0

    if is_player:
        valid_input = False
        while not valid_input:
            ace_str = input("You Drew a Ace, would you like it to count as 1 or 11?")
            if ace_str in ['1', '11']:
                ace += int(ace_str)
                valid_input += True
            else:
                print("incorrect Input Received, Type either 1 or 11")
                valid_input += False
    return ace

def blackjack():
    playerCards.clear()
    houseCards.clear()


    get_player_cards()
    get_player_cards()
    get_house_cards()
    get_house_cards()
    print("--------------Welcome To Black Jack--------------")
    print(f"Your hand is: {playerCards}")
    print(f"House reveals: {houseCards[0]} & [Hidden]")


while True:
    blackjack()

    while hand_total(True) < 21:
        if hand_total(False) > 21:
            print(f"House has been busted.You win !\nPlayer Hand Total: {hand_total(True)}\nHouse Hand Total: {hand_total(False)}")
            break

        choice = input("Hit or Stand?").lower()
        if choice == 'hit':
            get_player_cards()
            print(f"Your hand is: {playerCards}")
        elif choice == 'stand':
            while hand_total(False) < 16:
                get_house_cards()
                print("House hits.")
            if hand_total(False) > 21:
                print(f"House busted! You win.\nPlayer Hand Total: {hand_total(True)}\nHouse Hand Total: {hand_total(False)}")
            elif hand_total(False) > hand_total(True):
                print("House wins.")
            elif hand_total(False) < hand_total(True):
                print(f"You win!\nPlayer Hand Total: {hand_total(True)}\nHouse Hand Total: {hand_total(False)}")
            else:
                print(f"It's a tie!\nPlayer Hand Total: {hand_total(True)}\nHouse Hand Total: {hand_total(False)}")
            break
        else:
            print("Invalid input. Please type 'Hit' or 'Stand'.")
    else:
        if hand_total(True) > 21:
            print(f"You busted! House wins.\nPlayer Hand Total: {hand_total(True)}\nHouse Hand Total: {hand_total(False)}")

    play_again = input("Play again? (yes/no): ").lower()
    deck = {
        'Hearts': ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'],
        'Diamonds': ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'],
        'Clubs': ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'],
        'Spades': ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    }
    if play_again != 'yes':
        print("Thanks for playing!")

        break
