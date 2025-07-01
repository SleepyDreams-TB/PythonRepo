class Cars():
    colour = "black"  # class variable
    def __init__(self, name):
        print("Building car")
        self.name = name #variable in the init() of a class, all objects created from the class has access

    def drive(self): #method
        print("move")

class Trucks(Cars):
        def drive(self):
            super().drive()
            print(f"{self.name} is driving")

my_toyota = Trucks("Hilux") #create Object
my_toyota.drive()

print(my_toyota.colour)

