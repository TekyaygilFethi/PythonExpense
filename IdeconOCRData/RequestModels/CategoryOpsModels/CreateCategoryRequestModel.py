from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument('categoryName', help = 'This field cannot be blank', required = True)