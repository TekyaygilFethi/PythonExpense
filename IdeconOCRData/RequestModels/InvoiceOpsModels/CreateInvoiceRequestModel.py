from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument('rawText', help = 'This field cannot be blank', required = True)
parser.add_argument('date', help = 'This field cannot be blank', required = True)
parser.add_argument('invoiceNumber', help = 'This field cannot be blank', required = True)
parser.add_argument('companyName', help = 'This field cannot be blank', required = True)
parser.add_argument('vatTotal', help = 'This field cannot be blank', required = True)
parser.add_argument('invoiceTotal', help = 'This field cannot be blank', required = True)
parser.add_argument('userID', help = 'This field cannot be blank', required = True)
parser.add_argument('categoryID', help = 'This field cannot be blank', required = True)
parser.add_argument('isTest', help = 'This field cannot be blank', required = True)
parser.add_argument('vkn', help = 'This field cannot be blank', required = True)

