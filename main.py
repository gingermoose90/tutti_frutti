import os
os.environ['KIVY_VIDEO']='ffpyplayer'
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.camera import Camera
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import pyrebase
import imageRecognition
import time


class Fruit(object):
    def __init__(self, name, image_path):
        self.name = name
        self.image_path = image_path
        self.id = time.strftime("%Y%m%d_%H%M%S")


class ViewListWindow(Screen):
    box = ObjectProperty(None)

    def displayList(self):
         config = {
           "apiKey": "AIzaSyCQ-mryRAVKKTpJnhmICLszdrTveqhLTtm",
            "authDomain": "tutti-frutti-ec817.firebaseapp.com",
            "databaseURL": "https://tutti-frutti-ec817.firebaseio.com/",
            "storageBucket": "tutti-frutti-ec817.appspot.com"
         }

         firebase = pyrebase.initialize_app(config)
         db = firebase.database()
         fruitDict = db.child('FruitList').get().val()

         for id, fruit in fruitDict.items():
             label = Label(text=fruit)
             storage = firebase.storage()
             imageRef = storage.child('FruitList').child(id)
             imageUrl = imageRef.get_url(token=None)
             print(imageUrl)
             asyncimage = AsyncImage(source=imageUrl, size=[100, 100])
             self.box.add_widget(label)
             self.box.add_widget(asyncimage)

    def back(self):
        sm.current = "home"


class HomePageWindow(Screen):

    def snapFruit(self):
        sm.current = "main"

    def viewList(self):
        sm.current = "list"


class MainWindow(Screen):
    box = ObjectProperty(None)
    camera = ObjectProperty(None)
    label = ObjectProperty(None)

    #cameraObject = Camera(play=False)
    #cameraObject.play = True
    #cameraObject.resolution = (100, 100)
    #box.add_widget(cameraObject)

    config = {
        "apiKey": "AIzaSyCQ-mryRAVKKTpJnhmICLszdrTveqhLTtm",
        "authDomain": "tutti-frutti-ec817.firebaseapp.com",
        "databaseURL": "https://tutti-frutti-ec817.firebaseio.com/",
        "storageBucket": "tutti-frutti-ec817.appspot.com"
    }

    firebase = pyrebase.initialize_app(config)
    newFruit = Fruit("null", "null")

    def discard(self):
        sm.current = "home"
        self.label.text="This is a : "

    def save(self, firebase, newFruit):

        db = firebase.database()
        #data = {'testEvent2': 'Pear'}
        print(newFruit.name)
        print(newFruit.image_path)

        #timeStamp = str(datetime.datetime.now().time())

        data = {newFruit.id: newFruit.name}
        db.child('FruitList').update(data)

        storage = firebase.storage()
        storage.child('FruitList').child(newFruit.id).put(newFruit.image_path)
        self.label.text="This is a : "
        #storage.child('FruitList').child('testEvent1').put('banana.jpg')
        #storage.child('FruitList').child('testEvent2').put('pear.jpg')


    def cameraClick(self, newFruit):

        timeStamp = time.strftime("%Y%m%d_%H%M%S")
        img_path = "{}_fruit_image.png".format(timeStamp)
        #img_path = 'apple.jpg'
        self.camera.export_to_png(img_path)
        #self.camera.export_to_png('{}_fruit_image.png'.format(timeStamp))
        input_data = imageRecognition.extract_features(img_path)
        predicted_fruit = imageRecognition.predict_output("weights2.npy", input_data, activation="sigmoid")
        self.label.text="This is a : " + predicted_fruit
        newFruit.name = predicted_fruit
        newFruit.image_path = img_path


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")

sm = WindowManager()

screens = [HomePageWindow(name="home"), ViewListWindow(name="list"),MainWindow(name="main")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "home"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()