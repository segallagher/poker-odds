
import tkinter as tk
from tkinter import ttk        
import json
from deck import CardEncoder, CardDecoder

# populate the table
# input:    2D array of data to be displayed
# returns:  nothing
def populate_table(root, data):
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
#           handInfo, 2D array to set the order, description, and payout of each handCategory
# returns:  2D array to be displayed in cells
def generateProbabilityTable(handCounts, handInfo):
    data = [
        ["Hand", "Description", "Frequency", "Probability", "Payout", "Return"],
    ]

    totalHands = 0
    totalReturn = 0
    for category in handCounts:
        totalHands += handCounts[category]
    for i, entry in enumerate(handInfo):
        prob = handCounts[entry[0]]/totalHands
        data.append([entry[0].name, entry[1],handCounts[entry[0]], prob, entry[2], prob * entry[2]])
        totalReturn += prob * entry[2]
    data.append(["","",totalHands,"","Total Return:",totalReturn])
    
    return data

def makeTable(data):

    # Create the main window
    root = tk.Tk()
    root.title("Poker Probability")

    # Populate the table with data
    populate_table(root, data)

    root.mainloop()

def generateHandContributionTable(contributingHands, numContributingHands,sumExpectedReturn, handInfo):
    data = [
        ["Hand", "Description","Occurances", "Payout", "Return"],
    ]

    totalHands = 0
    for entry in handInfo:
        print(entry)
        if entry[0] not in contributingHands:
            continue
        print(contributingHands[entry[0]])
        totalHands += contributingHands[entry[0]]
        data.append([entry[0].name, entry[1], contributingHands[entry[0]], entry[2], (entry[2]/numContributingHands) * contributingHands[entry[0]] ])
    data.append(["","",totalHands,"Total Return:", sumExpectedReturn/numContributingHands])

    return data

def writeData(data):
    with open("data.json","w") as file:
        json.dump(data, file, cls=CardEncoder, indent=2)

def readData():
    data = None
    with open("data.json","r") as file:
        data = json.load(file, cls=CardDecoder)
    return data
