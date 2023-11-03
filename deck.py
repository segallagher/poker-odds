from enum import Enum
from itertools import combinations
from collections import defaultdict
from pathlib import Path

class suit(Enum):
    clubs = 1
    hearts = 2
    spades = 3
    diamonds = 4

class rank(Enum):
    ace = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10
    jack = 11
    queen = 12
    king = 13

class handCategories(Enum):
    straightFlush = 1
    threeOfAKind = 2
    straight = 3
    flush = 4
    pair = 5
    highCard = 6

class Card:
    def __init__(self, rank, suit) -> None:
        self.suit = suit
        self.rank = rank

    def __str__(self) -> str:
        return self.rank.name + " of " + self.suit.name
    
    def __eq__(self,other):
        if isinstance(other, Card):
            return (self.rank, self.suit) == (other.rank, other.suit)
        return False

    def getSuit(self):
        return self.suit
    
    def getValue(self):
        return self.rank

    suit = suit.spades
    rank = rank.ace

class Deck:
    def __init__(self, cards = []) -> None:
        if cards == []:
            self.cards = self.newDeck()
        else:
            self.cards = cards

    def __str__(self) -> str:
        deckString = ""
        for card in self.cards:
            deckString += str(card) + "\n"
        return deckString
    
    # creates a new deck 
    # inputs:   self
    # return:   a standard deck
    def newDeck(self):
        cards = []
        for suitValue in suit:
            for rankValue in rank:
                cards.append(Card(rankValue,suitValue))
        return cards
        
    # generates combinations of length "handSize" of self.cards
    # inputs:   handSize, integer size of hands
    #           inHand, array of cards that are in hand
    #           inDiscard, array of cards not in hand or in deck
    # returns:  itertools.combinations object of all combinations
    def generateHands(self, handSize=3, inHand=[], inDiscard=[]):
        tmpList = inDiscard
        for card in inHand:
            tmpList.append(card)
        remainingCards = self.discard(tmpList)
        hands = combinations(remainingCards,handSize-len(inHand))
        # put cards in hand back into each combination
        returnHands = []
        for hand in hands:
            hand += tuple(inHand)
            returnHands.append(hand)
        return returnHands

    # removes cards passed to it from deck
    # inputs:   array of cards to remove
    # returns:  deck without removed cards
    def discard(self, cardsToRemove):
        newCards = []
        for card in self.cards:
            if card not in cardsToRemove:
                newCards.append(card)
        return newCards
    
    # removes cards passed to it from deck and sets self.cards to the new deck
    # inputs:   array of cards to remove
    # returns:  nothing, modifies self.cards
    def setDiscard(self,cardsToRemove):
        self.cards = self.discard(cardsToRemove)

    cards = []



########################################################################
## Checks
########################################################################

# looks through hands and categorizes them
# inputs:   list of hands
# returns:  dict of handcategory and count
def countHandTypes(hands):
    handCount = defaultdict(int)

    for hand in hands:
        nValue = nKind(hand)
        straight = isStraight(hand)
        flush = isFlush(hand)

        if flush and straight:
            handCount[handCategories.straightFlush] += 1
            continue
        elif flush and not straight:
            handCount[handCategories.flush] += 1
            continue
        elif straight:
            handCount[handCategories.straight] += 1
            continue


        match nValue:
            case 2:
                handCount[handCategories.pair] += 1
                continue
            case 3:
                handCount[handCategories.threeOfAKind] += 1
                continue
        handCount[handCategories.highCard] += 1
    
    return handCount

# takes a hand and checks if it is a Pair
# inputs:   list of cards
# returns:  number of occurences of the most common card rank in the hand
def nKind(hand):
    ranks = defaultdict(int)
    for card in hand:
        ranks[card.rank] += 1

    return max(ranks.values())
# takes a hand and checks if it is a flush
# inputs:   list of cards
# returns:  True if hand is a flush or 0, False otherwise
def isFlush(hand):
    if len(hand) == 0:
        return True
    suit = hand[0].suit
    for card in hand:
        if card.suit != suit:
            return False
    return True

# takes a hand and checks if it is a straight
# inputs:   list of cards
# returns:  True if hand is straight or 0, False otherwise
def isStraight(hand):
    if len(hand) == 0:
        return True
    sorted_hand = sorted(hand, key=lambda card: card.rank.value)

    # loop = False
    if sorted_hand[0].rank == rank.ace and sorted_hand[-1].rank == rank(len(rank)):
        sorted_hand.append(sorted_hand[0])
        sorted_hand.pop(0)
        # loop = True

    curRank = sorted_hand[0].rank
    for i, card in enumerate(sorted_hand[1:]):
        if i+2 == len(sorted_hand) and sorted_hand[-2].rank == rank(len(rank)):
            if sorted_hand[-1].rank != rank.ace:
                return False
            return True
        if card.rank.value - 1 != curRank.value:
            return False
        curRank = card.rank
    return True


def handsToFile(hands):
    p = Path(__file__).with_name('hands.txt')
    with p.open("w") as file:
        for hand in hands:
            line = ""
            for card in hand:
                line += str(card) + ", "
            line += "\n"
            file.write(line)