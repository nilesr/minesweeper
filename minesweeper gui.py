# Data type
# master list          list             0          1                  2                  3
# master[x coordinate][y coordinate] = [is a mine, number to display, has been revealed, has been marked]
# Example map, in the format (x,y)
# (0,0) (0,1) (0,2)
# (0,1) (1,1) (1,2)
# (0,2) (1,2) (2,2)
# TODO
# nothing
# Imports
import random
import string
import math
import time
import os
import tkinter
import tkinter.messagebox
#import traceback
# Functions
def PrintBoard(final = False):
	global master
	# Print the header
	if TotalMarked > NumMines:
		TotalMarkedTemp = NumMines
	else:
		TotalMarkedTemp = TotalMarked
	str(int(time.time()) - int(TimerStart)) + " :) " + str(NumMines - TotalMarked)
	# Now go into the loop
	for x in range(0,MaxX):
		#frames[x].pack()
		for y in range(0,MaxY):
			#master[x][y][4].pack()
			if master[x][y][2] == 0: # If it's not revealed
				if final and master[x][y][0] == 1: # If it's not revealed, it is a mine and this is the game-over screen
					master[x][y][4]["text"] = "*"
				else:
					if master[x][y][3] == 0: # If it's not revealed and it's not marked
						master[x][y][4]["text"] = "#"
					else: # If it's not revealed and is marked
						if master[x][y][0] == 1 or not final: # If it's not revealed and is marked and was actually a mine, OR if it's not revealed and is marked and this is not the game-over screen
							master[x][y][4]["text"] = "*"
						else: # If it's not revealed and is marked but was marked incorrectly
							master[x][y][4]["text"] = "X" 
			else: # If it is revealed
				if master[x][y][0] == 1:
					master[x][y][4]["text"] = "+"
				else:
					if master[x][y][1] == 0:
						master[x][y][4]["text"] = " "
					else:
						master[x][y][4]["text"] = str(master[x][y][1]) # If it's revealed, and isn't a mine, print the number
		#print(row)
	if not final:
		CheckIfGameOver()
def reveal(x,y,manual = False):
	# Get master from the global scope
	global master
	if master[x][y][3] == 1: # If it's marked, never reveal it.
		if manual:
			tkinter.messagebox.showinfo("Nope","You cannot reveal a marked square. Unmark it first")
		return True
	if master[x][y][2] == 1 and not manual: # If this is already revealed, exit, otherwise the recursion will be infinite, and that's bad
		return True
	master[x][y][2] = 1 # Reveal it
	if master[x][y][0] == 1: # If it's a mine
		tkinter.messagebox.showinfo("Game over","Game over! Better luck next time")
		PrintBoard(True)
		return False
	surroundingMarkedMines = 0
	for i in [x+1,y],[x+1,y+1],[x+1,y-1],[x-1,y],[x-1,y+1],[x-1,y-1],[x,y+1],[x,y-1]: # For each of the 8 surrounding cells
		if i[0] == -1 or i[0] == MaxX or i[1] == -1 or i[1] == MaxY:
			continue
		if master[i[0]][i[1]][3] == 1: # If they are marked
			surroundingMarkedMines += 1 # Increase surroundingMarkedMines by 1
	if surroundingMarkedMines == master[x][y][1]: # If surroundingMarkedMines is equal to the number being displayed
		for i in [x+1,y],[x+1,y+1],[x+1,y-1],[x-1,y],[x-1,y+1],[x-1,y-1],[x,y+1],[x,y-1]: # For each of the 8 surrounding cells
			if i[0] == -1 or i[0] == MaxX or i[1] == -1 or i[1] == MaxY:
				continue
			if master[i[0]][i[1]][3] == 0: # If that cell has not been marked
				reveal(i[0],i[1]) # Reveal that square
	PrintBoard()
def mark(x,y):
	global TotalMarked
	if master[x][y][2] == 1:
		tkinter.messagebox.showinfo("Nope","Cannot mark a revealed square")
		return
	if master[x][y][3] == 0:
		master[x][y][3] = 1
		TotalMarked += 1
	else:
		TotalMarked -= 1
		master[x][y][3] = 0
	PrintBoard()
def StartGame():
	global master, MaxX, MaxY, NumMines, TimerStart
	while(True):
		try:
			MaxX = MaxXEntry.get()
			MaxY = MaxYEntry.get()
			NumMines = NumMinesEntry.get()
			if MaxX == "":
				MaxX = 10
			MaxX = int(MaxX)
			if MaxY == "":
				MaxY = 10
			MaxY = int(MaxY)
			if NumMines == "":
				NumMines = 10
			NumMines = int(NumMines)
			if NumMines > MaxX*MaxY-4:
				tkinter.messagebox.showinfo("Error", "Too many mines for " + str(MaxX*MaxY) + " spaces!")
				continue
			break
		except:
			tkinter.messagebox.showinfo("Error", "Input parse failed. That's probably not a number!")
	MaxXEntry.destroy()
	MaxXLabel.destroy()
	MaxXFrame.destroy()
	MaxYEntry.destroy()
	MaxYLabel.destroy()
	MaxYFrame.destroy()
	NumMinesEntry.destroy()
	NumMinesLabel.destroy()
	NumMinesFrame.destroy()
	SubmitButton.destroy()
	# Initialize timer
	TimerStart = time.time()
	# Initialize variables
	master = []
	for x in range(0,MaxX):
		master.append([])
		#frames.append(Tkinter.Frame(window))
		for y in range (0,MaxY):
			master[x].append([])
			master[x][y] = [0,0,0,0,tkinter.Button(window, command=lambda x=x,y=y: reveal(x,y,True))] # See line 2. That x=x,y=y is important, without it each button would think it's position was MaxX-1,MaxY-1
			master[x][y][4].grid(row=x,column=y)
			master[x][y][4].bind("<Button-3>",lambda event,x=x,y=y: mark(x=x,y=y))
	# Place mines
	#StartingCoords = str(int(math.floor(MaxX/2))) + str(int(math.floor(MaxY/2)))
	StartingX = int(math.floor(MaxX/2))
	StartingY = int(math.floor(MaxY/2))
	n = 0
	while n < NumMines:
		x=random.randrange(0,MaxX)
		y=random.randrange(0,MaxY)
		if master[x][y][0] == 1 or (abs(StartingX - x) <= 1 or abs(StartingY - y) <= 1): # Do not place a mine on a square where there is already a mine, on the starting position, or within the 8 squares surrounding the starting position
			continue
		master[x][y][0] = 1
		n = n + 1

	for x in range(0,MaxX):
		for y in range(0,MaxY):
			numberToStore = 0
			for i in [x+1,y],[x+1,y+1],[x+1,y-1],[x-1,y],[x-1,y+1],[x-1,y-1],[x,y+1],[x,y-1]:
				if i[0] == -1 or i[0] == MaxX or i[1] == -1 or i[1] == MaxY:
					continue
				if master[i[0]][i[1]][0] == 1:
					numberToStore += 1
			master[x][y][1] = numberToStore

	#window.bind("<Button-3>",mark)
	reveal(StartingX,StartingY) # Reveal it
	PrintBoard()
def CheckIfGameOver():
	# Check if the game is over here
	TotalRevealedTiles = 0
	for x in range(0,MaxX):
		for y in range(0,MaxY):
			if master[x][y][2] == 1:
				TotalRevealedTiles += 1
	if TotalRevealedTiles == MaxX*MaxY - NumMines:
		tkinter.messagebox.showinfo("Woohoo","You win! All mines found" + "\n\n" + "Your time: " + str(int(time.time() - TimerStart)))
		PrintBoard(True)
	MarkedCorrect = 0
	MarkedIncorrect = 0
	for x in range(0,MaxX):
		for y in range(0,MaxY):
			if master[x][y][3] == 1: # If it is marked
				if master[x][y][0] == 1:
					MarkedCorrect += 1
				else:
					MarkedIncorrect += 1
	if MarkedCorrect == NumMines and MarkedIncorrect == 0:
		tkinter.messagebox.showinfo("Woohoo","You win! All mines found" + "\n\n" + "Your time: " + str(int(time.time() - TimerStart)))
		PrintBoard(True)


# Variables
window = tkinter.Tk()
TotalMarked = 0
MaxXFrame = tkinter.Frame(window)
MaxXFrame.pack()
MaxXLabel = tkinter.Label(MaxXFrame, text="Height: ")
MaxXLabel.pack(side=tkinter.LEFT)
MaxXEntry = tkinter.Entry(MaxXFrame)
MaxXEntry.insert(0, "10")
MaxXEntry.pack(side=tkinter.RIGHT)
MaxYFrame = tkinter.Frame(window)
MaxYFrame.pack()
MaxYLabel = tkinter.Label(MaxYFrame, text="Width: ")
MaxYLabel.pack(side=tkinter.LEFT)
MaxYEntry = tkinter.Entry(MaxYFrame)
MaxYEntry.insert(0, "10")
MaxYEntry.pack(side=tkinter.RIGHT)
NumMinesFrame = tkinter.Frame(window)
NumMinesFrame.pack()
NumMinesLabel = tkinter.Label(NumMinesFrame, text="Mines: ")
NumMinesLabel.pack(side=tkinter.LEFT)
NumMinesEntry = tkinter.Entry(NumMinesFrame)
NumMinesEntry.insert(0, "10")
NumMinesEntry.pack(side=tkinter.RIGHT)
SubmitButton = tkinter.Button(window, text="Submit", command=StartGame)
SubmitButton.pack()
window.mainloop()
