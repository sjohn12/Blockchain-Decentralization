# README

The programs run on Python version 3.11.1. During execution please make sure both programs are in the same directory.

## Installation
Open command prompt and make sure the following are installed:

```bash
pip install requests
pip install json
pip install time
pip install datetime
pip install sys
pip install os
pip install matplotlib
```

## Opensea_API_saan.py

This program collects NFT data from APIs to get specific infromation about an NFT collection and specific data per NFT. 

Please note that for this program the current Opensea API key will expire in approximately a year from now (2023/09/02). 
Visit here to request another one: [Get a key](https://docs.opensea.io/reference/api-keys)

This program has 3 functions : load_data(), nft_data() and price(). When the program is run directly, all the returned data will be printed.

### load_data(slug: str)
This function returns the dictionary "data" in the format {"token id": "smart contract address"} for a collection specified by user. The user will be prompted as follows:

```python
Slug: 
```
Enter the name of the NFT collection that you are looking for. 

### nft_data(data: dict, chain: str)
This function returns a list "nfts" with nft specific information by accepting a dictionary of id tokens and smart contracts as well as specification of what chain the nft uses. A text file will also be created in the same directory as the program with the same information as nft. The user will be prompted as follows:

```python:
Chain:
```
Enter the chain(the cryptocurrency) of the NFT collection that you specified earlier. To see supported chains, please look here : [Chains](https://docs.opensea.io/reference/supported-chains)

### price(data: dict)
This function takes a dictionary of token ids and contract addresses to obtain information about nft prices such as seller, protocol and royalty fee. The function calculates the fee in cryptocurrency and returns a dictionary with the token ids and the price of the last sale for that nft. It runs off a different API than the other functions in this module.

The user will not be prompted for this function.

## NFT Rarity Score Research
This program plots a graph of the rarity score vs the frequency based of calculations done with the trait types or values. User has the option to create new data within the program from calling API or use previously generated data in a text file that must be in the same directory as this program. All prompts are given with options that the user can type in to the console.

This program will output a graph of the rarity scores plotted against frequency, print a dictionary with the token ids and rarity scores, and print another dictionary with token ids and last sale of that NFT.

### Important variables
Here are some variables to take a closer look at the data of the program. Type the variable in the console. The list will be formatted as "variable: definition".

- traits: list of trait data per NFT in a collection. Includes trait types, trait values, trait counts and rarity information. Format is [[NFT #1 {trait #1}{trait#2}] [NFT #2{..}]]
- token_ids: a list of NFT token ids in the same order they were read from. 
- trait_data: a dictionary of NFT traits and trait values. Format is {Trait type #1: {Trait value #1: Amount of NFTS}{Trait value #2 ..}, Trait type #2: {..}}
- trez: a dictionary with the count of NFT trait types in the dataset. Format is {Trait type #1: Amount of NFTS, ..}
- no_trez: same as trez except this counts the missing trait types in each NFT.
- freq: a list of the frequency for each trait type/value of a NFT. Format is [NFT #1 [trait #1 frequency,trait #2 frequency], NFT #2 [..]]
- (mean type)_rar: list of calculated rarity scores using specified mean type (harmonic, arithmetic or geometric). This is per NFT.
- fre_(mean type first letter): dictionary that contains rarity score as key and frequency as value based on (mean type)_rar. 
- id_rar: dictionary that contains token id as key and a list of rarity scores. Format is printed in program. 
- price: dictionary of token ids as key and last sale of NFT as value. 


## Further Research

Opensea also offers information on rairty ranking which would be great to do further research in. Each rarity ranking system has unique criteria and it would be interesting to understand what criteria is most commonly used and why. Another way to approach this topic would be through understnading if the rarity ranking is a generalized system or special per NFT collection based on their data. There also may be a relationship when comparing the rarity ranking of different NFTS compared to their sales or current market demand. 

As per the "Rarity Metrics for Non-Fungible Tokens" research paper, independance trait testing is also explored to gain a deeper understanding of traits and rarity. It would be interesting to explore deeper as to figure out how this test is conducted. Further research on this topic may allow it to be implemented in the program for further analysis on different traits of NFTS to find new trends and it's implications to the current NFT market. 
