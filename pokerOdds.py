
from deck import *
from table import *
from tqdm import tqdm
import concurrent.futures

# Problem 1: generate probability table based off hand probability
deck = Deck()
hands = deck.generateHands()
handCounts = countHandTypes(hands)

data = generateProbabilityTable(handCounts, handInfo)

makeTable(data)

# Problem 2: generate best play for a hand

hands = [ 
    [Card(rank.ace, suit.clubs),Card(rank.ace, suit.diamonds),Card(rank.ace, suit.hearts)],
    [Card(rank.ace, suit.clubs),Card(rank.king, suit.diamonds),Card(rank.queen, suit.hearts)],
    [Card(rank.ace, suit.clubs),Card(rank.king, suit.hearts),Card(rank.ace, suit.hearts)],
    [Card(rank.ace, suit.clubs),Card(rank.king, suit.hearts),Card(rank.two, suit.spades)],
    [Card(rank.three, suit.clubs),Card(rank.three, suit.hearts),Card(rank.two, suit.spades)],
    [Card(rank.seven, suit.clubs),Card(rank.three, suit.hearts),Card(rank.five, suit.clubs)],
    [Card(rank.ace, suit.hearts),Card(rank.queen, suit.hearts),Card(rank.five, suit.clubs)],
    [Card(rank.three, suit.hearts),Card(rank.queen, suit.hearts),Card(rank.five, suit.clubs)],
    [Card(rank.queen, suit.hearts),Card(rank.ace, suit.diamonds),Card(rank.four, suit.hearts)],
    [Card(rank.jack, suit.hearts),Card(rank.ten, suit.diamonds),Card(rank.nine, suit.hearts)],
]

for hand in hands:
    holds = allHolds(inHand=hand)
    print("Hand:", end=" ")
    printHand(hand)
    print("Best hold:", end=" ")
    printHand(bestHold(holds).hold)
    print("All holds")
    for hold in holds:
        print("\t", end="")
        print(hold.ret, end="\t")
        printHand(hold.hold)
    print()

# Problem 3: Determine perfect play for all hands, Sum up expected value for perfect play

print("Start calculating perfect play")
deck = Deck()
hands = deck.generateHands()

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    pass

sumExpectedReturn = 0
for hand in tqdm(hands, desc="Calculating"):
    best = bestHold(allHolds(inHand=hand))
    sumExpectedReturn += best.ret
print("For Perfect Play")
print("Expected Return:", sumExpectedReturn/len(hands))
