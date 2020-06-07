import configparser
import pyimgur

config = configparser.ConfigParser()
config.read('auth.ini')

def uploadImage(imgPath, name):
    client_id = config.get('credentials', 'client_id')
    client_secret = config.get('credentials', 'client_secret')

    client = pyimgur.Imgur(client_id)
    uploaded_image = client.upload_image(imgPath, title=name)
    # print(uploaded_image.title)
    # print(uploaded_image.link)
    # print(uploaded_image.size)
    # print(uploaded_image.type)

    return uploaded_image.link
