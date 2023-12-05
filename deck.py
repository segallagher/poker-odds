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
    threeAces = 7
    royalFlush = 8

handInfo =[
    [handCategories.royalFlush, "AKQ (in any suit)", 250],
    [handCategories.straightFlush, "3 suited in sequence", 100],
    [handCategories.threeAces, "3 Aces (any combo of suits)", 100],
    [handCategories.threeOfAKind, "3 of the same rank", 30],
    [handCategories.straight, "3 in sequence (includes AKQ)", 15],
    [handCategories.flush, "3 suited", 5],
    [handCategories.pair, "2 of the same rank", 1],
    [handCategories.highCard, "None of the above", 0],
]

class holdInfo:
    def __init__(self, hold, ret, handTypes, numHands):
        self.hold = hold
        self.ret = ret
        self.handTypes = handTypes
        self.numHands = numHands

    def __str__(self) -> str:
        handStr = ""
        for card in self.hold:
            handStr += str(card) + ", "
        return "Return:" + str(self.ret) + "\tHold:" + handStr + "\tNum Hands:" + str(self.numHands) + "\tHand Types:" + str(self.handTypes)


# gets value of handCategory as described in handInfo
# input:    handCategory, a handCategories object
# returns:  corresponding value in handInfo
def getHandValue(handCategory):
    for entry in handInfo:
        if entry[0] == handCategory:
            return entry[2]
    return None

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
        
    # generates combinations of length "handSize" of self.cards, draws cards to reach handSize
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

    # removes cards passed to it from deck, does not modify self.cards
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
        handCount[getHandType(hand)] += 1
    return handCount

# returns type of hand
# inputs:   list of cards
# returns: handCategories type
def getHandType(hand):
    nValue = nKind(hand)
    straight = isStraight(hand)
    flush = isFlush(hand)
    royalFlush = isRoyalFlush(hand)

    if royalFlush:
        return handCategories.royalFlush
    elif flush and straight:
        return handCategories.straightFlush
    elif flush and not straight:
        return handCategories.flush
    elif straight:
        return handCategories.straight
    
    match nValue:
        case 2:
            return handCategories.pair
        case 3:
            if hand[0].rank == rank.ace:
                return handCategories.threeAces
            return handCategories.threeOfAKind
    return handCategories.highCard

# takes a hand and checks if it is a Pair
# inputs:   list of cards
# returns:  number of occurences of the most common card rank in the hand
def nKind(hand):
    if len(hand) == 0:
        return 0
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

# takes a hand and checks if its a royal flush
# inputs:   list of cards
# returns:  True if hand has the top n cards of a deck with  
#           ace included of the same suit, False otherwise
def isRoyalFlush(hand):
    if len(hand) == 0:
        return False
    # check if hand contains the top len(hand)-1 cards and ace
    sorted_hand = sorted(hand, key=lambda card: card.rank.value)
    if sorted_hand[0].rank != rank.ace:
        return False
    
    curValue = rank(len(rank))
    for i in range(len(sorted_hand) - 1):
        if sorted_hand[-1-i].rank != curValue:
            return False
        curValue = rank(curValue.value - 1)
    # check if all same suit
    if not isFlush(hand):
        return False
    return True


########################################################################
## additional functions
########################################################################

# prints the hand formatted
def printHand(hand, end = "\n"):
    for card in hand:
        print(card, end=", ")
    print(end, end="")

# writes an array of hands to a text file
# inputs: an array of hands
def handsToFile(hands):
    p = Path(__file__).with_name('hands.txt')
    with p.open("w") as file:
        for hand in hands:
            line = ""
            for card in hand:
                line += str(card) + ", "
            line += "\n"
            file.write(line)

# finds the total return of a hand, draws up to handSize from inHand
# inputs:   deck, deck object in use
#           handSize, number of cards to have in hand after drawing
#           inHand, list of cards currently in hand
#           inDiscard, list of cards discarded
# returns:  expected return of inHand cards
def totalReturn(handSize=3, inHand=[], inDiscard=[]):
    deck = Deck()
    hands = deck.generateHands(handSize, inHand, inDiscard)
    handTypeCount = countHandTypes(hands)
    
    sumHandValues = 0
    totalHands = 0
    for entry in handTypeCount:
        sumHandValues += getHandValue(entry) * handTypeCount[entry]
        totalHands += handTypeCount[entry]
    
    # if cards cannot be drawn
    if totalHands == 0:
        return 0
    return sumHandValues / totalHands, handTypeCount

# generates combinations of length "handSize" of self.cards
# inputs:   deck, deck object
#           handSize, integer size of hands
#           inHand, array of cards that are in hand
#           inDiscard, array of cards not in hand or in deck
# returns:  list of discard options and its total returns
def allHolds(handSize=3, inHand=[], inDiscard=[]):

    
    discardOptions = []
    # generate all ways to discard cards inHand
    for i in range(handSize + 1):
        discards = combinations(inHand, i)
        for combo in discards:
            discardOptions.append(combo)
    
    # 2D array of holds and their expected return
    holds = []
    # handTypes = []
    # numHands = []
    for toDiscard in discardOptions:
        currHand = []
        for card in inHand:
            if card not in toDiscard:
                currHand.append(card)

        ret, types = totalReturn(handSize, currHand, inDiscard+list(toDiscard))
        
        sum = 0
        for entry in types:
            # print(types[entry])
            sum += types[entry]

        holds.append(holdInfo(hold=currHand, ret=ret, handTypes=types, numHands=sum))

        # holds.append([currHand, ret])
        # # types = 1 #countHandTypes()
        # handTypes.append(types)
        # sum = 0
        # for entry in types:
        #     print(types[entry])
        #     sum += types[entry]
        # numHands.append(sum)
    # for i in range(len(holds)):
    #     print(holds[i], handTypes[i], numHands[i])
    # print()

    # holds = []

    # return correlated discards and options
    # sort based off expected return
    return sorted(holds, key=lambda h: h.ret, reverse=True)

# returns best hold from a 2D array of holds and their returns
# inputs:   holds, a 2D array of holds
# returns:  array of hold with return, returns the highest return 
def bestHold(holds):
    return max(holds, key=lambda x: x.ret)


holds = allHolds(3, [Card(rank.ace, suit.clubs),Card(rank.three, suit.diamonds), Card(rank.ace, suit.hearts)], [])
for hold in holds:
    print(hold)
    print()


print(len(holds))
best = bestHold(holds)
print(best.ret, best.hold)



# hands = a.generateHands(3,[Card(rank.ace, suit.clubs),Card(rank.ace, suit.diamonds)],[Card(rank.ace, suit.spades)])
# handsToFile(hands)