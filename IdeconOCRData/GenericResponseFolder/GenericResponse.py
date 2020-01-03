class GenericResponse():
    def __init__(self,httpStatusCode,message,obj=None):
        self.httpStatusCode=httpStatusCode
        self.message=message
        self.object=obj