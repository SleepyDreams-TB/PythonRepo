class Person:

    totalPeople = ""

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")

    def update_age(self, new_age):
        self.age = new_age

    def is_adult(self):
        return self.age >= 18


Member1 = Person("Tiaan", 21)
Member1.update_age(22)
print(Member1.is_adult())
Member1.greet()
