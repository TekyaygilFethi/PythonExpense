from functools import wraps
from flask import request,jsonify
from IdeconOCRData.GenericResponseFolder.GenericResponse import GenericResponse

def auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            token = kwargs['token']
        except:
            token = request.args.get('token') or \
                request.form.get('token')

        if not token:
            return jsonify(GenericResponse("401","JWT is Invalid"))
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify(GenericResponse("401","JWT is Invalid"))

        return f(*args,**kwargs)
    
    return wrapper