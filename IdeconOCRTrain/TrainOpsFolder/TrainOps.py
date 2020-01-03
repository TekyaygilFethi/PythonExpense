import random
import spacy
import sys
import os
import getpass
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from IdeconOCRData.TrainOpsDataFolder.TrainOpsDataTag import TrainOpsDataTag
from IdeconOCRData.GenericResponseFolder.GenericResponse import GenericResponse
from IdeconOCRData.TrainOpsDataFolder.TrainOpsData import TrainOpsData
from IdeconOCRTrain.TrainDocFolder.TrainDocOps import AIDoc

import json

aiDoc=AIDoc()

tDataList=[
TrainOpsData("GALAXY GAYRİMENKUL ÇETİN JEEPÇETİN BOZ TEMURORTAKÖY MH. MUALLIMNACİ CD. NO: 49/2BEŞİKTAŞ/I STANBULBEŞİKTAŞ VD47626300244 18-07-2019 FIS NO: 6 SAAT: 22:23OTOPARK %18 *50,00 KDV *7,63 TOP *50,00 NAKİT *50,00 EKÜ NO: 1 2 NO: 1817M ASOO00027675",(0,18,"COMPANY"),(166,171,"AMOUNT"),(121,131,"DATE"),(111,112,"NO"),(177,181,"KDV")),
TrainOpsData("ES BALABAN YUNUS USTA YASEMIN ORTACIKURTULUŞ MH. ZIYAPAŞA CD. N 29/BESK. V. D. BAŞKANLIGI 12173036496TEL: 221 14 06 ESKİŞEHİRTIC. SICNO:44265MERSİS N 1217303649600001 AFIYET OLSUN 23-04-20",(0,21,"COMPANY"),(242,247,"AMOUNT"),(180,190,"DATE"),(65,66,"NO"),(229,233,"KDV")),
TrainOpsData("Mehmet PAZAR Tutar 6.50 Fis No: 1234 Tarih: 22/03/2010",(0,12,"COMPANY"),(19,23,"AMOUNT"),(44,54,"DATE"),(32,36,"NO")),
TrainOpsData("GİRİN SALATA GIDA TURZ. TEKS. İNŞ.OTO. SAN. VE TİC.LTD.ŞTİ OVACIK MAH. D-100 KARAYOLU SOK. SYMBOL KOCAELİ AVM NO.34 BAŞİSKELE/KOCAELİ BAKIRKÖY V.D 3950849482 TARIH : 26/04/2019 SAAT : 17:32:08 FIS NO : 0036 YİYECEK %08 *47,80 - - TOPKDV *3,54 TOPLAM *47,80 - - KREDİ *47,80 GARANTİ BANKASI *********** MERSIS : 3950849482 EKÜ NO: 0001 Z NO:0136 1: 9173602 T: 02582992 B:000344 S: 004246 17:32 26/04/2019 KYNK :0810 VER:SBETS8D2 YURTICI KART TIPI:YIDK ************3599 EMRE SIMSEK SATIŞ TUTARI 47, 80 TL ONAY NUMARASI:521934 REF.NO:911660096508 ======================== İŞLEMINIZ SIFRENIZ İLE DOĞRULANMIŞTIR. ======================== Garanti T.GARANTI BANKASI A.S.",(0,23,"COMPANY"),(220,225,"AMOUNT"),(166,176,"DATE"),(202,206,"NO"),(238,242,"KDV")),
TrainOpsData("ULUDAG KEBAPÇISI 1.C.T.GIDA INS.LTD.STI. KENT HEYDANI A.V.M. N:23/0011 TL: 255 55 56 OSMANGAZI BURSA 4690488030 OSMANGAZI VERGI DAIRESI TARIH : 13/06/2019 SAAT : 13:59:42 FIS NO : 0013 YEMEK BED 308 89,00 TOPKDV *6,59 TOPLAM *89,00 KREDI *89,00 İŞ BANKASI *********6541 HERSIS : 0469048803000013 EKÜ NO: 0002 Z NO:1239 ISYERI NO 437237019 TERM. NO:13723703 BOLUN: 0001 BOLUN ! 13 06/2015 14:00 SATIS AID: A0000000031010 APP LABEL: Visa Credit **** **** **** 6541 AHMET SEUIL 89,00 TL # YURTICI VISA KREOL KARTI: ONAY KODU: 138643",(0,16,"COMPANY"),(199,204,"AMOUNT"),(144,154,"DATE"),(180,184,"NO"),(213,217,"KDV")),
TrainOpsData("LOKUM TANTUNI ORUCRE IS MAH. TEPE CAD. 6 B ESENLER 34220 ISTANBUL TEL: 212 4382525 1:295107 T: 02572980 B:000238 S:002484 02/05/2019 15:55 AID: A0000000041010 APP.LABEL: MASTERCARD VER:SBKTS502 KYNK:R C@10 K. N.: 5269********4302 MIKDAT DOGRU EMU SATIS TUTARI 46,00 TL KARSILIGI MAL VEYA HIZMET ALDIM. ONAY NUMARASI: 333233 REF.NO:912269870118 KART TIPI: YURTİÇİ GARANTİ BANKASI T. GARANTİ BANKASI A.S. MERSİS NO: 0879 0017 5660 0379 GENEL MÜDÜRLÜK:NISPETIYE MAH. AYTAR CAD. NO: 2. BESIKTAS. 34340. LEVENT. ISTANBUL WWW.GARANTI.COM.TR 1. NÜSHA (UYE İŞYERİNE AITTER.}) TC: E39D433DFC2ABC06",(0,13,"COMPANY"),(260,265,"AMOUNT"),(122,132,"DATE")),
TrainOpsData("KARUM ÇAY EVI MUALLA ALTIN HOŞNUDİYE MAHALLESİ KADİFE ÇİÇEĞİ SOK.NO:2/C ESKİŞEHİR 11461498510 ESK.V.D. BAŞK. TARİH : 24/04/2019 SAAT : 16:18:11 FİS NO : 0033 KSM7 %01 *34,00 - -------- TOPKDV *0,34 TOPLAM *34,00 KREDİ *34,00 AKBANK ********** ***** 3599 MERSIS : 1146149851000011 EKÜ NO: 0001 Z NO:0871 ISYERI NO:9001913300 TERMINAL : 01984878 Belge Ref No : 46091954 24/04/19 16:18 SATS **** **** **** 3599 EMRE SIMSEK Tutar: 34.00 TL KARŞILIGI MAL VEYA HIZMET ALINDI BU BELGEYI SAKLAYINIZ",(0,13,"COMPANY"),(168,173,"AMOUNT"),(117,127,"DATE"),(153,157,"NO"),(193,197,"KDV")),
TrainOpsData("CARREFOURSA Tekstilkent Mini CARREFOUR SABANCI TIC.MRK. A.Ş. Tekstilkent Koza Plaza A Blok Esenler/ İstanbul BUYUK MÜKELLEFLER VD. 2030017071 V.N. www.carrsfoursa.com Mersis Numarası. 4887254458388756 TARIH : 17.07.2019 SAAT : 07:26 FIS NO : 0001 4008496559749 LONGLIFE POWER AL %18 TOPKDV *2,58 TOPLAM *16,90 KREDY KARTI *16,90 Halkbank D.k.k Provizyon No : 582670 KDV Oranı KDV Dahil Tutar KDV %18 *2,58 Müsteri Kart Numarasi: Mersis No: 4887254458368756 BÜYÜK MÜKELLEFLER VD. 2030017071 V.N. 51120011707907630001 BANKACILIK İŞLEM BİLGİLERI Alışveriş Tutarı: 16,90 Kart Tipi:0 işlem Tipi:34 Onay Numarası: 582670 Terminal:PS601987 Kart No: 494314******7743 3 KASIYER: K**** S**** Z NO : 0892 YAB 15006143 EKO NO: 0001",(0,11,"COMPANY"),(304,309,"AMOUNT"),(209,219,"DATE"),(242,246,"NO"),(291,295,"KDV")),
TrainOpsData("EMPARK PARK YÖNETİMİ VE SİS. SAN. TİC. A.Ş. MIMARSINAN MH. SELMAN-I PAK CD. ABDÜLFEYYAZ SK.4 ÜSKÜDAR/İST 02124386318 ÜSKÜDAR V.D. 7210371396 TARIH 18/07/2019 SAAT : 15:16:42 FIŞ NO : 0038 HIZ BEDELİ %18 *10,00 34716387 3 Saat 46 Dakika Topl am : 4 Saat 35 Dakika TOPKDV *1,53 TOPLAM *10,00 NAKIT *10,00 MERSIS : 0721037139600010 TEKSTILKENT G KAPI EKU NO: 0001 Z NO:0585 MF JI 20060670",(0,20,"COMPANY"),(204,209,"AMOUNT"),(147,157,"DATE"),(183,187,"NO"),(271,275,"KDV")),
TrainOpsData("GALAXY GAYRİMENKUL ÇETİN JEEP ÇETİN BOZ TEMUR ORTAKÖY MH. MUALLIM NACİ CD. NO: 49/2 BEŞİKTAŞ/I STANBUL BEŞİKTAŞ VD47626300244 18-07-2019 FIS NO: 6 SAAT: 22:23 OTOPARK %18 *50,00 KDV *7,63 TOP *50,00 NAKİT *50,00 EKÜ NO: 1 2 NO: 1817 M ASOO00027675",(0,18,"COMPANY"),(172,177,"AMOUNT"),(126,136,"DATE"),(145,147,"NO"),(183,187,"KDV")),
TrainOpsData("NATAL www.nazalli.com Maslak V.D.: 630 039 9821 Ticaret Sicil No: 721679 Mersis No.: 0630039982100012 BERMUDA TEKNOLOJİ A.Ş SÜLEYMAN DEMİREL BLV.MALL OF İSTANBUL SIT OFIS APT.NO.7 E FATURA Seri A Sıra No. : 039366 22.07.2019 Tarih 026309 İrsaliye No İL KODU : 34 22.07.2019 İrsaliye Tarihi : İKİTELLİ ISTANBUL LIG BAKO Müşteri V.D.: IKITELLI 1660605020 Hesap No: MALIN CİNSİ TUTAR 6 ADET 450,00 BLA01 BELLA OFİS SANDALYESİ Nazalli Ofis Mobilyaları San.Tic.Ltd.Şti. Akbank Perpa Şubesi Şube Kodu:633 Hesap:51204 Tr 50 0004 6006 3388 8000 0512 04 2.700,00 YALNIZ TOPLAM 1- TTK'nun 23. md. gereğince iş bu faturaya 8 gün içinde itiraz edilmediği takdirde içeriği kabul edilmiş sayılır. K.D.V. % 2- Satilan mal müşterinin sorumluluğu altında seyahat eder. 3- Vadesinde ödenmeyen faturalara aylık % ....... vade farkı uygulanır. GENEL TOPLAM 3.186,00",(0,5,"COMPANY"),(837,844,"AMOUNT"),(263,272,"DATE"),(207,212,"NO")),
TrainOpsData("",("COMPANY"),("AMOUNT"),("DATE"),("NO"),("KDV"))
]

aiDoc.write_to_file(tDataList)
objectList=aiDoc.read_from_file()




def train_spacy(data, iterations):
    TRAIN_DATA = data
    nlp = spacy.blank('en')  # create blank Language class
    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)

    # add labels
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for itn in range(iterations):
            print("Statring iteration " + str(itn))
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                nlp.update(
                    [text],  # batch of texts
                    [annotations],  # batch of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    sgd=optimizer,  # callable to update weights
                    losses=losses)
            print(losses)
    return nlp

prdnlp = train_spacy([obj.trainData["trainData"] for obj in objectList],30)
prdnlp.to_disk("IdeconOCRTrainModelSets\\trainModel")