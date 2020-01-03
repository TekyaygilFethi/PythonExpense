from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)
parser.add_argument('name', help = 'This field cannot be blank', required = True)
parser.add_argument('surname', help = 'This field cannot be blank', required = True)