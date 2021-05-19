## Importing Necessary Modules
import requests  # to get image from the web
import shutil  # to save it locally

def retreiver(coin):
    ## Set up the image URL and filename
    image_url = "https://cryptoicons.org/api/icon/" + coin + "/50"
    filename = coin + '.png'
    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(image_url, stream=True)
    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        print('Image sucessfully Downloaded: ', filename)
    else:
        print('Image Couldn\'t be retreived')


coins = ['btc','eth','bnb','ada','doge','xrp','dot','icp','bch','uni','ltc','link',
         'matic','sol','xlm','vet','etc','theta','eos','trx','fil','neo','crv']

for coin in coins:
    retreiver(coin)

# retreiver('bnb')
