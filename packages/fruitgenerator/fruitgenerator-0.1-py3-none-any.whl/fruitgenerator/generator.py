class FruitGenerator:
    def __init__(self):
        self.fruit_names = {
            1: "Mango",
            2: "Apple",
            3: "Banana",
            # Add more fruits as needed
        }

    def generate_fruit_name(self, num):
        if num in self.fruit_names:
            return self.fruit_names[num]
        else:
            return "Unknown Fruit"
