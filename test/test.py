class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound."


class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)  # 调用父类构造函数
        self.breed = breed  # 子类特有的属性

    def speak(self):
        return f"{self.name} barks."

    def get_breed(self):
        return self.breed


class Cat(Animal):
    def __init__(self, name, color):
        super().__init__(name)
        self.color = color

    def speak(self):
        return f"{self.name} meows."

    def get_color(self):
        return self.color


# 使用父类引用存储子类对象
def main():
    animals = [
        Dog("Buddy", "Golden Retriever"),
        Cat("Whiskers", "Gray")
    ]

    for animal in animals:  # 父类引用指向子类对象
        print(animal.speak())  # 多态：调用子类的方法

        # 访问子类特有的属性或方法
        if isinstance(animal, Dog):
            print(f"Breed: {animal.get_breed()}")
        elif isinstance(animal, Cat):
            print(f"Color: {animal.get_color()}")

        print("-" * 20)


if __name__ == "__main__":
    main()