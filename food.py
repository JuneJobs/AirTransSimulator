#import dinner
import random

class Dinner:
    def __init__(self):
        self.foodList = ['Beef', 'Pork', 'Souplantation', 'Straving', 'Vegemeal']


    def getDinnerMenu(self):
        return self.foodList[random.randint(0,4)]

def main():
    app = Dinner()
    print(app.getDinnerMenu())

if __name__ == '__main__':
    main()
