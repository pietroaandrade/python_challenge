from pydantic import BaseModel, ValidationError

class PatientData(BaseModel):
    name: str
    insurance: str
    symptoms: str


patients = {
}

seguros = {
    1 : "Porto Seguro",
    2 : "Bradesco",
    3 : "Amil",
    4 : "SulAmérica",
    5 : "Unimed"
}

def forca_opcao(msg, dic):
    print("Seguros que aceitamos:" "\n")
    for key in dic.keys():
        data = dic[key]
        print(f"- {data}" )
    
    opcao = input(f"{msg}\n\n->")
    while opcao not in dic.values():
         print("Opção inválida! Por favor, escolha um nome de seguro válido.")
         opcao = input(f"{msg}\n\n->")

    return opcao


def forca_opcaoooo(msg,opcoes):
    possibilidades = '\n'.join(opcoes)
    opcao = input(f"{msg}\n{possibilidades}\n->")
    while opcao not in opcoes:
        print("Opção inválida!")
        opcao = input(f"{msg}\n{possibilidades}\n->")
    return opcao

def create_pacient():
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
    insurance_input = forca_opcao("Qual é o seu seguro?", seguros)
    symptoms_input = input("Enter Symptoms: ")

    try:
        patient_data = PatientData(
            name=name_input,
            insurance=insurance_input,
            symptoms=symptoms_input
        )
        patients[id_input] = patient_data.model_dump()
        print("Patient added successfully!")
        print(patients)
    except ValidationError as e:
        print("Invalid data:", e)

    return patients


def get_patient(patient_id):
    if patient_id not in patients:
        print("Patient not found")
    else:
        data = patients[patient_id]
        print(f"ID: {id}, Name: {data['name']}, Insurance: {data['insurance']}, Symptoms: {data['symptoms']}")

create_pacient()