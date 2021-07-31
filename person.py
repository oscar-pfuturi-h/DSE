class Person:
    def __init__(self,first_name,last_name,age,dni,cellphone,address):
        self.first_name=first_name
        self.last_name=last_name
        self.age=age
        self.dni=dni
        self.cellphone=cellphone
        self.address=address
    
    def greeting():
        print("Hello World!")

person=Person('Watm')
person.greeting()