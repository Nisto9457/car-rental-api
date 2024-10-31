from flask import Flask, jsonify, request

app= Flask(__name__)

cars =[] #bil data

bookings = [] #bookings liste

customers = []

employees = []

@app.route('/')
def home():
    return "This is the Car Rental API"


@app.route('/cars', methods=['POST'])
def create_car():
    car = request.get_json()
    cars.append(car)
    return jsonify(car), 201 

@app.route('/cars', methods=['GET'])
def get_cars():
    return jsonify(cars), 200  


@app.route('/cars/<int:index>', methods=['PUT'])
def update_car(index):
    if index < 0 or index >= len(cars):
        return jsonify({"error": "Car not found"}), 404
    car_data = request.get_json()
    cars[index] = car_data
    return jsonify(car_data), 200



@app.route('/cars/<int:index>', methods=['DELETE'])
def delete_car(index):
    if index < 0 or index >= len(cars):
        return jsonify({"error": "Car not found"}), 404
    deleted_car = cars.pop(index)
    return jsonify(deleted_car), 200


@app.route('/order-car', methods=['POST'])
def order_car():
    booking_data = request.get_json()
    customer_id = booking_data.get("customer_id")
    car_id = booking_data.get("car_id")

    # check if customer has booking
    if any(booking['customer_id'] == customer_id for booking in bookings):
        return jsonify({"error": "Customer already has booking."}), 400

    # check if car is available or not
    if car_id < 0 or car_id >= len(cars) or cars[car_id].get("status") != "available":
        return jsonify({"error": "Car is not available."}), 400

    # make booking
    bookings.append({"customer_id": customer_id, "car_id": car_id})
    cars[car_id]["status"] = "booked"  
    return jsonify({"message": "Car booked successfully."}), 201

#Cancel ordrer
@app.route('/cancel-order-car', methods=['POST'])
def cancel_order_car():
    booking_data = request.get_json()
    customer_id = booking_data.get("customer_id")
    car_id = booking_data.get("car_id")

    # check if booking exists or not
    for booking in bookings:
        if booking['customer_id'] == customer_id and booking['car_id'] == car_id:
            
            bookings.remove(booking)
            cars[car_id]["status"] = "available"  
            return jsonify({"message": "Booking was cancelled."}), 200

    return jsonify({"error": "no booking found."}), 404

# Rent car
@app.route('/rent-car', methods=['POST'])
def rent_car():

    rental_data = request.get_json()
    customer_id = rental_data.get("customer_id")
    car_id = rental_data.get("car_id")

    # check customer booking
    if not any(booking['customer_id'] == customer_id and booking['car_id'] == car_id for booking in bookings):
        return jsonify({"error": "No booking was found for specified car."}), 404

    cars[car_id]["status"] = "rented"
    return jsonify({"message": "Car sucessfulky rented."}), 200

# Returner car
@app.route('/return-car', methods=['POST'])
def return_car():
    return_data = request.get_json()
    customer_id = return_data.get("customer_id")
    car_id = return_data.get("car_id")
    car_status = return_data.get("status")

    if not any(booking['customer_id'] == customer_id and booking['car_id'] == car_id for booking in bookings):
        return jsonify({"error": "No rentals for this car was found."}), 404

    cars[car_id]["status"] = car_status 
    bookings[:] = [booking for booking in bookings if not (booking['customer_id'] == customer_id and booking['car_id'] == car_id)]
    return jsonify({"message": "Car returned."}), 200

# Customers
@app.route('/customers', methods=['GET'])
def get_customers():
    return jsonify(customers), 200  

# Lag ny customer
@app.route('/customers', methods=['POST'])
def create_customer():
    customer = request.get_json()
    customers.append(customer)
    return jsonify(customer), 201 

# Update customer
@app.route('/customers/<int:index>', methods=['PUT'])
def update_customer(index):
    if index < 0 or index >= len(customers):
        return jsonify({"error": "Customer not found"}), 404
    customer_data = request.get_json()
    customers[index] = customer_data
    return jsonify(customer_data), 200

# Delete customer
@app.route('/customers/<int:index>', methods=['DELETE'])
def delete_customer(index):
    if index < 0 or index >= len(customers):
        return jsonify({"error": "Customer not found"}), 404
    deleted_customer = customers.pop(index)
    return jsonify(deleted_customer), 200

# List eployees
@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(employees), 200  

# Create employee
@app.route('/employees', methods=['POST'])
def create_employee():
    employee = request.get_json()
    employees.append(employee)
    return jsonify(employee), 201 

# Update employee
@app.route('/employees/<int:index>', methods=['PUT'])
def update_employee(index):
    if index < 0 or index >= len(employees):
        return jsonify({"error": "Employee not found"}), 404
    employee_data = request.get_json()
    employees[index] = employee_data
    return jsonify(employee_data), 200

# Delet employee
@app.route('/employees/<int:index>', methods=['DELETE'])
def delete_employee(index):
    if index < 0 or index >= len(employees):
        return jsonify({"error": "Employee not found"}), 404
    deleted_employee = employees.pop(index)
    return jsonify(deleted_employee), 200

if __name__ == "__main__":
    app.run(debug=True)