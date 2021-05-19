from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import numpy as np
from numpy import random
import ast

app = Flask(__name__)
api = Api(app)


class Users(Resource):
    data = pd.read_csv('users.csv')

    def get(self, data=data):
        data = data.to_dict()
        return {'data': data}, 200  # return data and 200 OK code

    def post(self, data=data):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('name', required=True)
        parser.add_argument('city', required=True)
        userId = random.randint(low=0, high=9, size=5)
        if userId in data['userID']:
            userId = random.randint(low=0, high=9, size=5)
        else:
            pass
        args = parser.parse_args()
        args['userId'] = userId
        data.assign(**args)
        data.to_csv('users.csv', index=False)
        return {'data': data.loc[-1].to_dict()}, 200

    def put(self, data=data):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('userId', required=True)
        parser.add_argument('favourite_pokemon', required=True)
        args = parser.parse_args()

        if args['userId'] in list(data['userId']):
            user_index = data.loc[data[args['userId']]]
            data.favourite_pokemon.iloc[user_index] = args['favourite_pokemon']
            data.to_csv('users.csv', index=False)
            return {'data': data.to_dict()}, 200

        else:
            return {
                       'message': f"'{args['userId']}' user not found."
                   }, 404

    def delete(self, data=data):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('userId', required=True)
        args = parser.parse_args()
        if args['userId'] in list(data['userId']):
            user_index = data.loc[data[args['userId']]]
            data = data.drop(index=user_index)
            data.to_csv('users.csv', index=False)
            return {'data': data.to_dict()}, 200

        else:
            return {
                       'message': f"'{args['userId']}' user not found."
                   }, 404


class Pokemon(Resource):
    df = pd.read_csv('pokemon.csv')

    def get(self, data=df):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('name', required=True)
        pokemon = (parser.add_argument('name', required=True)).lower
        pokemon = pokemon.capitalize()
        poke_index = data[data['name'] == pokemon].index.values
        general = data.iloc[poke_index[0]]
        return {
                   'name': general[29:31],

                   'basic stats': general['pokedex_number', 'generation', 'is_legendary', 'classfication',
                                          'type1', 'type2', 'abilities',
                                          'attack', 'defense', 'capture_rate'],
                   'fight stats': general[1:19],

                   'nerd stats': general['experience_growth', 'base_egg_steps', 'base_happiness',
                                         'base_total', 'height_m', 'hp', 'percentage_male', 'sp_attack',
                                         'sp_defense', 'weight_kg'],

               }, 200


# Resources (entry points)
api.add_resource(Users, '/users')
api.add_resource(Pokemon, '/pokemon')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
