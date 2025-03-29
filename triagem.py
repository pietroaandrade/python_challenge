from pydantic import BaseModel

class patient_data(BaseModel):
    name: str
    health_insurance: str

patients = {

}


def create_pacient( ):
    print(f"Patients in patients list: {patients}")
    id_input = input("Enter ID (integer): ")
    while not (id_input.isnumeric()):
        print("invalid id")
        id_input = input("Enter ID (integer): ")
    if id_input.isnumeric():
        id_input = int(id_input)
        patients[f"{id_input}"] = ''
        print(patients)
    name_input = input("Enter Name: ")






