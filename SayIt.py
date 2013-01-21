#!/usr/bin/env python
# -*- coding: utf8 -*-

from Tkinter import *
import tkMessageBox
import objc
import AppKit

list = None
names = []
ids = []
textEntry = None

def getNames():
	# Get the list of the names of the avaible voices
	global names
	global ids
	NSSpeechSynthesizer = objc.lookUpClass("NSSpeechSynthesizer")
	array = NSSpeechSynthesizer.availableVoices()
	for voice in array:
		dict = NSSpeechSynthesizer.attributesForVoice_(voice)
		name = dict["VoiceName"]
		names.append(name)
		currid = dict["VoiceIdentifier"]
		ids.append(currid)
	return names

def ButtonPressed():
	global list
	global textEntry
	# Get the currently selected voice
	currentSelected = list.curselection()
	if not currentSelected:
		tkMessageBox.showinfo("Error!", "You haven't selected a voice! Please select one")
	else:
		currentID = ids[int(currentSelected[0])]
		NSSpeechSynthesizer = objc.lookUpClass("NSSpeechSynthesizer")
		# Get the content of the text widget and then erase it
		strToSay = textEntry.get('1.0', 'end')
		textEntry.delete('1.0', 'end')
		# Say the text with the given voice
		synth = NSSpeechSynthesizer.alloc().initWithVoice_(currentID)
		synth.startSpeakingString_(strToSay)

def main():
	global names
	global textEntry
	global list
	names = getNames()
	mainWindow = Tk()

	mainWindow.title("SayIt by Rickye")

	textEntry = Text(mainWindow, height = 6, width = 40, borderwidth = 1, relief = SUNKEN)
	textEntry.focus_set()
	list = Listbox(mainWindow)
	# Add the names to the listbox's list
	for string in names:
		list.insert(END, string)
	button = Button(mainWindow, text ="Say It", command = ButtonPressed)
	textEntry.grid(row =1, column =2, rowspan = 2, padx = 10)
	button.grid(row =3, column =2)
	list.grid(row =1, column =1, rowspan =3, padx =10, pady =5)
	# Get the index of Alex and set it to the default selection
	list.select_set(names.index("Alex"))
	mainWindow.mainloop()

if __name__ == "__main__":
	main()