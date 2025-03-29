from pydantic import BaseModel, ValidationError

class PatientData(BaseModel):
    name: str
    insurance: str
    symptoms: str


patients = {
}

waiting_queue = []

def create_paciente():
    print(f"Patients in patients list: {patients}")

    while True:
        id_input = input("Enter ID (integer): ")
        if id_input.isnumeric():
            if id_input in patients:
                print("ID already exists. Try another.")
                continue
            break
        print("Invalid ID. Please enter a numeric value.")

    name_input = input("Enter Name: ")
    insurance_input = input("Enter Insurance: ")
    symptoms_input = input("Enter Symptoms: ")

    try:
        patient_data = PatientData(
            name=name_input,
            insurance=insurance_input,
            symptoms=symptoms_input
        )
        patients[id_input] = patient_data.model_dump()
        waiting_queue.append(id_input)
        print("Patient added successfully!")
        print(patients)
    except ValidationError as e:
        print("Invalid data:", e)

    return patients

def waiting_line():
    create_paciente()
    if not waiting_queue:
        print("No patients in the waiting line.")
        return

    next_patient_id = waiting_queue.pop(0)  # Use list pop(0) instead of deque.popleft()
    print(f"Next patient to be attended: {patients[next_patient_id]['name']}")
    del patients[next_patient_id]

def get_patient(patient_id):
    if patient_id not in patients:
        print("Patient not found")
    else:
        data = patients[patient_id]
        print(f"ID: {id}, Name: {data['name']}, Insurance: {data['insurance']}, Symptoms: {data['symptoms']}")

