import json
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

#Folder, kde budeme ukládat seznam aut
CAR_FILE  = "cars.json"

# class for cars
class Car:
    def __init__(self, color, model, car_type):
        self.color = color
        self.model = model
        self.car_type = car_type

    def describe_car(self):
        return f"This car is {self.color}, model {self.model}, and a type {self.car_type}."
    
    #Pomocná metoda pro uložení aut ze slovníku
    def to_dict(self):
        return {"color": self.color, "model": self.model, "car_type": self.car_type}
    
    #Pomocná metoda pro načtení aut ze slovníku
    @staticmethod
    def from_dict(data):
        return Car(data["color"], data["model"], data["car_type"])

# Funkce pro načtení seznamu aut ze souboru JSON
def load_cars():
    try:
        with open(CAR_FILE, 'r') as f:
            cars_data = json.load(f)
            return [Car.from_dict(car) for car in cars_data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []   

# Funkce pro uložení seznamu aut do souboru JSON
def save_cars(cars):
    with open(CAR_FILE, 'w') as f:
        json.dump([car.to_dict() for car in cars], f)


# Načti auta při spuštění aplikace
cars = load_cars()

# Route pro hlavní stránku
@app.route('/')
def index():
    return render_template('index.html', cars=cars)


# Route pro přidání auta
@app.route('/add_car', methods=['POST'])
def add_car():
    color = request.form['color']
    model = request.form['model']
    car_type = request.form['car_type']

    # Vytvoř nové auto a přidej ho do seznamu
    new_car = Car(color, model, car_type)
    cars.append(new_car)

    # Ulož seznam aut do souboru
    save_cars(cars)

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=5006)
