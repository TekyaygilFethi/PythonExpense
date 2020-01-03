import IdeconOCRVision.Regex.DateRegex as dateRegex
import IdeconOCRVision.Regex.AmountRegex as amountRegex
import IdeconOCRVision.Regex.VKNRegex as vknRegex

def findRegexes(text):
    vkn=vknRegex.get(text)
    date=dateRegex.get(text)
    amount=amountRegex.get(text)


    responseDict= {"VKN":vkn,"DATE":date}
    responseDict.update(amount)

    return responseDict