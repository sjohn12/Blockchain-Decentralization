
import requests
import json
import time
import datetime 

def load_data(slug: str) -> dict:
    """
    This function returns a dictionary of token ids and smart contracts of a collection identified by the variable slug.
    Example call:
    load_data("boredapeyachtclub")
    """
    url = "https://api.opensea.io/v2/collection/"+slug+"/nfts"
    headers = {
        "accept": "application/json",
        "X-API-KEY": "156234b9509b44838606984599692fdd"
        }
    try:  
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_data = json.loads(response.text)
        raw_data = response_data.get("nfts")
        
        if raw_data is None:
            print("No data received from the API at this time. Try again later") 
            return {}        

        data = {"identifier": "smart_contract"}
        for dictionary in raw_data:
            x = dictionary.get("identifier")
            y = dictionary.get("contract")
            data[x] = y
        return data
    
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print("An error occurred:", e)
            return {}    

def nft_data(data: dict, chain: str) -> list:
    """
    Generate a list of nft data based on token ids and smart contracts provided by function load_data.
    Data is stored in a list and also creates a txt file with the information.
    Chain is chain on which the contract is deployed.
    Example call:
    nft_data({identifier: smart_contract}, cryptocurrency}), 
    """
    nft_data = []
    counter = 0
    formatted_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = "Opensea_data" + formatted_datetime + ".txt"
    with open(file_name, 'w') as file:
        for i in data:
            if counter != 0:
                identifier = i
                address = data.get(i)
            
                url = "https://api.opensea.io/v2/chain/"+chain+"/contract/"+address+"/nfts/"+ identifier
            
                headers = {
                "accept": "application/json",
                "X-API-KEY": "156234b9509b44838606984599692fdd"
                }
            
                response = requests.get(url, headers=headers)
            
                dicti = json.loads(response.text) # if there are more than 50 traits, null will be returned for traits
            
                if dicti.get("detail"):
                    time.sleep(1)
                    response = requests.get(url, headers=headers)
                    dicti = json.loads(response.text)                
                if dicti.get("nft"):
                    nft_data += [dicti]
                    file.write(response.text + "\n")
            counter += 1
    return nft_data

def price(data: dict) -> dict:
    """
    Generate a dictionary of token ids and last sold prices.
    Example call:
    price({identifier: smart contract..})
    """
    counter = 0
    price = {}
    royalityFee = 0.0
    protocolFee = 0.0
    for i in data: 
        if counter > 2:
            token = i
            address = data.get(i)
            url = "https://eth-mainnet.g.alchemy.com/nft/v2/tSx2jCfMOms4tUVYZh-s7OzjZNlJyvdV/getNFTSales?fromBlock=0&toBlock=latest&order=desc&contractAddress="+address+"&tokenId="+token+"&limit=1"
            headers = {"accept": "application/json"}
            response = requests.get(url, headers=headers)
            
            price_data = json.loads(response.text).get("nftSales") 
            
            if price_data != []:
                sellerFee = float(price_data[0].get("sellerFee").get("amount"))*10**-18
                if price_data[0].get("royaltyFee") == {}:
                    royalityFee = 0.0
                else:
                    royalityFee = float(price_data[0].get("royaltyFee").get("amount"))*10**-18
                if price_data[0].get("protocolFee") == {}:
                    protocolFee = 0.0
                else:
                    protocolFee = float(price_data[0].get("protocolFee").get("amount"))*10**-18
                fees = sellerFee + royalityFee + protocolFee
                if fees >=1 and (fees - int(fees)) > 0.1:
                    fees = fees - 1
                
                price [token] = str(fees) + " " + price_data[0].get("sellerFee").get("symbol")
        counter +=1
    return price

if __name__ == "__main__":
    slug = input("Slug:")
    data = load_data(slug)
    while data == {}:
        data = load_data()
    chain = input("Chain:")
    nfts = nft_data(data, chain)
    prices = price(data)
    print("Nft token ids and smart contract addresses:")
    print(data)
    print("Nft specific data:")
    print(nfts)
    print("Nft token id and last sale price:")
    print(prices)

  
   

    



