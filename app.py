import json
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Soubor, kde budeme ukládat seznam aut
CAR_FILE = 'cars.json'

# Třída pro auta
class Car:
    def __init__(self, color, model, car_type):
        self.color = color
        self.model = model
        self.car_type = car_type

    def describe_car(self):
        return f"This car is {self.color}, model {self.model}, and a type {self.car_type}."

    def to_dict(self):
        # Pomocná metoda pro uložení auta jako slovník
        return {"color": self.color, "model": self.model, "car_type": self.car_type}

    @staticmethod
    def from_dict(data):
        # Pomocná metoda pro načtení auta ze slovníku
        return Car(data['color'], data['model'], data['car_type'])


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
    cars_with_index = [(index, car) for index, car in enumerate(cars)]
    return render_template('index.html', cars=cars_with_index)

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

# Route pro odstranění auta
@app.route('/delete_car', methods=['POST'])
def delete_car():
    index = int(request.form['index'])
    
    # Odstraníme auto ze seznamu podle indexu
    if 0 <= index < len(cars):
        del cars[index]
        save_cars(cars)

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=5006)
