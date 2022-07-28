from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from mtgBinderHelper.auth import login_required
from mtgBinderHelper.db import get_db

bp = Blueprint('collection', __name__, url_prefix = "/collection")


# we will be coming back to actually properly populate the table.
# for now we just want to make a table that will display our collection
# still work in progress
@bp.route('/')
def index():
	return render_template('/templates/collection/collection_screen.html')

@app.route('/api/data')
def data():
	db = get_db()
	

	# search
	# probably will have to aggregate all the
	# search/sort  options last if not using
	# a handler to load in memory - consider dfs?
	search = request.args.get('search')
	if search:
		yourCards = db.execute(
			'''
			SELECT * FROM collection c 
			WHERE c.userId = ? AND c.setCode LIKE ?
			''',
			(g.user['id'], search,)
			).fetchall()
	else:
		yourCards = db.execute(
			'SELECT * FROM collection c WHERE c.userId = ?' +
			' ORDER BY dateAcquired DESC', (g.user['id'],)
			).fetchall()


	sort = request.args.get('sort')
	#if sort:
	if False:
		order = []
		for s in sort.split(','):
			direction = s[0]
			name = s[1:]
			if name not in ['id', 'userId', 'setCode', 'setNumber', 'isFoil', 'isTradeable']:
				name = 'id'
			# on pause while I figure out sqlite tricks

	return {
		'data': [card for card in yourCards]
		'total': len(yourCards)
	}

# @app.route('/api/data', methods=['POST'])
# def update():
# 	data = 