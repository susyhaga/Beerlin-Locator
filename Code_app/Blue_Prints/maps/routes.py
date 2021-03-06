import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from beerlin import app, db, bcrypt
from beerlin.models import User, Local, Ranking
from beerlin.maps.forms import PostForm
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
from flask import jsonify
import pandas as pd

maps = Blueprint('maps', __name__)

@ maps.route("/map")
def map():
    local = Local.query.all()
    #print(local)
    return render_template('map.html', title='Map', local=local)


# JSON Api routes
# ----------------
@maps.route("/api/get_stores_in_radius")
def get_stores_in_radius():
    latitude = float(request.args.get('lat'))
    longitude = float(request.args.get('lng'))
    radius = int(request.args.get('radius'))

    # TODO: Validate the input? 

    stores = Local.get_stores_within_radius(lat=latitude, lng=longitude, radius=radius)
    
    result_raking = []

    result = []
    for s in stores:
        result.append(s.toDict())
        result_raking.append(s.toRankDict())

    #print(result_raking)
    
    result_raking_final = []

    for r in result_raking:
        ranking = Ranking.values_ranking(r)

        for i in ranking:
            for j in i:
                result_raking_final.append(j.toDictfromRank())

    list_store_name = []
    list_ranking = []

    for i in range(len(result_raking_final)):
        list_store_name.append(result_raking_final[i].get('place'))
        list_ranking.append(result_raking_final[i].get('ranking'))

    df = pd.DataFrame(list(zip(list_store_name,list_ranking)),columns=['place','rank'])
    df1 = df.groupby('place').mean()

    list_ranking_final = []
    list_store_name_final = list(set(list_store_name))

    for i in list_store_name_final:
        list_ranking_final.append(float(df1.loc[i]))

    dictionary_ranking = dict(zip(list_store_name_final, list_ranking_final))

    for i in range(len(result)):

        store_from_result = str(result[i].get('name'))

        if store_from_result in list_store_name_final:
            rank_to_add = dictionary_ranking.get(str(result[i].get('name')))
            result[i]['ranking'] = rank_to_add
        else:
            pass

    #print(result)


    return jsonify(result)

@maps.route("/api/beer_ranking")
def beer_ranking():
    
    #test
    store = int(request.args.get('storeId'))
    print(store)
    return_beer_rank = Ranking.beer_rank(store)

    #print(return_beer_rank)

    return jsonify(return_beer_rank)

@maps.route("/ranking", methods=['GET', 'POST'])
@login_required
def new_rank():
    form = PostForm()
    if form.validate_on_submit():
        
        store_id=form.bar.data
        beercode=form.beer.data
        ranking =form.rank.data

        list_bar = PostForm.list_bar
        list_bar_dict = dict((x, y) for x, y in list_bar)
        list_beer = PostForm.list_beer
        list_beer_dict = dict((x, y) for x, y in list_beer)

        beerbrand = list_beer_dict[beercode]
        place = list_bar_dict[store_id]

        user_id = current_user
        user_id_int = int(str(user_id))

        rank = Ranking(beercode = beercode, beerbrand = beerbrand, place = place, ranking = ranking, user_id = user_id_int, store_id = store_id)

        db.session.add(rank)
        db.session.commit()
        flash('Your review has been saved! Thank you!', 'success')
        return redirect(url_for('maps.map'))
    return render_template('ranking.html',
                           form=form, legend='Rank how cold is your beer')