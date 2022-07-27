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
	return render_template('collection_table.html')

@app.route('/api/data')
def data():
	db = get_db()
	yourCards = db.execute(
		'SELECT * FROM collection c WHERE c.userId = ?' +
		' ORDER BY dateAcquired DESC', (g.user['id'],)
		).fetchall()

	# branch logic for when we return no rows

	



