import sqlite3
import click
import json
from flask import current_app, g
from flask.cli import with_appcontext


def legality_logic(legality_dict):
	'''
	Takes the dictonary representation of legality and
	reduces it to a 12-digit 2-bit number. Each bit represents
	the legality, and here is an example for Force of Will with
	the number written column-wise, with the corresponding format.

	There is a better way to organize these that would naturally
	Let the formats "roll" into one another. Legacy / Vintage / 
	Commander should be the "first" numbers; then older formats
	to newer formats.

	Or would it be better to do all the old formats at the bottom?
	So once things "rotate" their number will go under a specific
	threshold that we can check against.
	1 Vintage
	1 Legacy
	1 Commander
	1 Modern
	0 Brawl
	1 Pioneer
	0 Explorer
	0 Standard
	0 Alchemy
	0 Penny


	0 Standard
	0 Pioneer
	0 Modern
	1 Legacy
	1 Vintage
	0 Pauper
	1 Commander
	0 Alchemy
	0 Explorer
	0 Brawl
	0 Historic
	0 Penny

	This would be written as:
		000110100000 -> 416 in integer representation.

	The basic lands have the code:
		111111111111 -> 4095

	The dictonary *only* has the keys for the formats that are
	legal. 
	'''

	format_list = [
		'standard',
		'alchemy',
		'pioneer',
		'explorer',
		'modern',
		'brawl',
		'historic',
		'legacy',
		'pauper',
		'commander',
		'vintage',
		'penny'
		]







	