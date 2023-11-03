
from deck import *

import tkinter as tk
from tkinter import ttk        

# populate the table
# input:    2D array of data to be displayed
# returns:  nothing
def populate_table(data):
    for i, row_data in enumerate(data):
        for j, cell_data in enumerate(row_data):
            width = 10
            if j == 1:
                width = 30
            cell = tk.Text(root, height=1, width=width)
            cell.insert("1.0", cell_data)
            cell.grid(row=i, column=j)
            cell.configure(state="disabled")

# creates a 2D array of information
# inputs:   handCounts, a dict with keys of handTypes and values of integer occurances
#           dispInfo, 2D array to set the order, description, and payout of each handCategory
# returns:  2D array to be displayed in cells
def generateTable(handCounts, dispInfo):
    data = [
        ["Hand", "Description", "Frequency", "Probability", "Payout", "Return"],
    ]

    totalHands = 0
    totalReturn = 0
    for category in handCounts:
        totalHands += handCounts[category]
    for i, entry in enumerate(dispInfo):
        prob = handCounts[entry[0]]/totalHands
        data.append([entry[0].name, entry[1],handCounts[entry[0]], prob, entry[2], prob * entry[2]])
        totalReturn += prob * entry[2]
    data.append(["","","","","Total Return:",totalReturn])
    
    return data

dispInfo =[
    [handCategories.straightFlush, "3 suited in sequence", 100],
    [handCategories.threeOfAKind, "3 of the same rank", 30],
    [handCategories.straight, "3 in sequence (includes AKQ)", 15],
    [handCategories.flush, "3 suited", 5],
    [handCategories.pair, "2 of the same rank", 1],
    [handCategories.highCard, "None of the above", 0],
]

deck = Deck()
# hands = deck.generateHands(inHand=[Card(rank.ace,suit.clubs),Card(rank.ace,suit.hearts)], inDiscard=[Card(rank.two,suit.hearts)])
hands = deck.generateHands()
handCounts = countHandTypes(hands)

data = generateTable(handCounts, dispInfo)

# Create the main window
root = tk.Tk()
root.title("Poker Probability")

# Populate the table with data
populate_table(data)

root.mainloop()
