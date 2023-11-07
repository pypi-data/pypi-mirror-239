def config(word):
    from urllib.parse import quote
    ref = "collegiate"
    key = getApiKey()
    
    # Perform the API call
    uri = f"https://dictionaryapi.com/api/v3/references/{ref}/json/{quote(word)}?key={quote(key)}"
    return uri

def getApiKey():
    import os, sys
    try:
        os.environ['MW_API_KEY']
    except KeyError:
        print ('[error]: `MW_API_KEY` environment variable is required')
        print('Set this API key using export command e.g. `export MW_API_KEY=<API_KEY>`')
        exit()
    return os.environ['MW_API_KEY']

def callApi(uri):
    import requests
    try:
        response=requests.get(uri)
        return response.json()
    except ValueError:
        print("We are unable to get the definition now. Please try again later")


def getData(word):
    uri=config(word)
    result=callApi(uri)

    if len(result):
        data=result.pop(0)
        if isinstance(data, dict):
            printDefinition(data)
        else:
            print("Oops: The word you've entered isn't in the dictionary. Try again with the spelling suggestions from the following list:")
            index=1
            for suggestion in result:
                print("[{}]: {}".format(index, suggestion))
                index+=1
    else:
        print("Invalid Data. Please check the spelling of the word you are trying.")


def printDefinition(result):
    import json
    print("{} ({}): {}".format(getPronunciation(result),getType(result),getMeaning(result)))
    
def getPronunciation(data):
    result=''
    try:
        result= data['hwi']['prs'][0]['mw']
    except (KeyError, IndexError):
       pass 
    return result

        
def getType(data):
    result=''
    try:
        if 'fl' in data:
            result=data['fl']
    except (KeyError, IndexError):
        pass
    return result

def getMeaning(data):
    import json
    result=''
    try:
        if 'shortdef' in data:
            if len(data['shortdef']):
                if data['shortdef'][0].count(':') > 0:
                    meaning = data['shortdef'][0].split(':')
                    result=meaning[0]
    except (KeyError, IndexError):
        pass
    return result
    