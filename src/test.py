import requests
import json

def retrieveData():
    #titre contient Earth, et image
    page_remaining = True
    page_counter=1
    while page_remaining:
        print(page_counter)
        parameters = {'title':'Earth,earth','media_type':'image','year_start':'2017','year_end':'2019','page':page_counter}
        url = 'https://images-api.nasa.gov/search'
        requestData = requests.get(url, params=parameters)
        # requestData = requests.get("https://images-api.nasa.gov/search?title=earth,Earth&year_start=2016&year_end=2019&media_type=image&page=100")
        responseDict = json.loads(requestData.content)
        print(responseDict['collection']['items'])
        if responseDict['collection']['items']:
            for collection in responseDict['collection']['items']:
                for index,element in enumerate(collection['data']):
                    #creer les attributs comme nullable
                    dateCliche = None
                    photograph = None
                    description = None
                    link = None
                    title = None
                    id = None
                    #on suppose que seuls les liens et une idee sont necessaires pour ajouter un element a la bdd, les autre
                    #parametres etant optionnels
                    try:
                        link = collection['links'][index]['href']
                        id = element['nasa_id']
                        try:
                            title = element['title']
                        except:
                            pass
                        try:
                            #parser la date en format compatible
                            dateCliche =  element['date_created'].replace('T', ' ').replace('Z','')
                        except:
                            pass
                        try:    
                            photograph = element['photographer']
                        except:
                            pass
                        try:
                            description = element['description']
                        except:
                            pass
                    except:
                        continue
            page_counter = page_counter+1
        else:
            page_remaining = False

if __name__ == '__main__':
    retrieveData()

