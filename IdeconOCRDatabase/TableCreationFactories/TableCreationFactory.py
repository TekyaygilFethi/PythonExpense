from IdeconOCRGeneric import db,app

def Create():
    db.create_all('__all__',app) #burayı düzeltince tüm tablolar oluşturuldu