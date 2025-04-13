#Importante: Criar funcao de urgencia para triagem
#Importante: Criar funcao de temperatura para urgencia
#Importante: Criar funcao de Observar fila
#Importante: Criar funcao de Criar laudo
#importante: criar funcao de acessar laudo


from pydantic import BaseModel, ValidationError

class PatientData(BaseModel):
    name: str
    insurance: str
    symptoms: str
    temperature: int

next_id = 1
patients = {
}

seguros = ["Porto Seguro", "Bradesco", "Amil", "SulAmérica", "Unimed"]

espera = []

def forca_opcao(msg, lista_opcoes,msg_erro = 'Inválido'):
    opcoes = '\n'.join(lista_opcoes)
    opcao = input(f"{msg}\n{opcoes}\n->")
    while opcao not in lista_opcoes:
        print(msg_erro)
        opcao = input(f"{msg}\n{opcoes}\n->")
    return opcao


def forca_num(msg):
    num = input(msg)
    if not num.isnumeric():
        print("Deve ser um número!")
        num = forca_num(msg)
    return int(num)

def create_pacient():
    global next_id

    print(f"Patients in patients list: {patients}")

    id_input = next_id
    next_id += 1

    name_input = input("Qual seu nome?")
    insurance_input = forca_opcao("Qual é o seu convênio?", seguros)
    symptoms_input = input("Sintomas do paciente: ")
    temp_input = forca_num("Temperatura paciente:")

    try:
        patient_data = PatientData(
            name = name_input,
            insurance = insurance_input,
            symptoms = symptoms_input,
            temperature = temp_input
        )
        patients[id_input] = patient_data.model_dump()
        espera.append((patients[id_input]["name"], patients[id_input]["symptoms"]))
        print("Patient added successfully!")
        print(patients)
    except ValidationError as e:
        print("Invalid data:", e)
    acao = forca_opcao("O que deseja fazer?", acoes_funcionario.keys())
    acoes_funcionario[acao]()
    return



def get_patient():
    while True:
        id = forca_num("Qual é o ID do paciente desejado?")
        if id not in patients:
            print("Paciente não encontrado")
        data = patients[id]
        print(f"ID: {id}, Name: {data['name']}, Insurance: {data['insurance']}, Symptoms: {data['symptoms']}, temperatura: {data['temperature']}ºC")
        break
    return


def retrieve_line(espera):
    if not espera:
        print("Não há pacientes na fila de espera.")
        return None

    proximo_paciente = espera.pop(0)
    nome, sintomas = proximo_paciente

    print(f"Chamando o próximo paciente da fila:")
    print(f"🟢 Nome: {nome}\n🩺 Sintomas: {sintomas}")
    print(f"Pacientes restantes na fila: {len(espera)}")

    return proximo_paciente






acoes_funcionario = {
    "Cadastrar paciente" : create_pacient,
    "Buscar paciente" : get_patient,
    "Chamar paciente" : retrieve_line
}
acoes_paciente = {
    "Ver fila de espera" : retrieve_line
}
print('Iniciando sistema CareLine')



user_type = forca_opcao("Qual seu papel?", ["Funcionario", "Paciente"])
if user_type == "Funcionario":
    acao = forca_opcao("O que deseja fazer?", acoes_funcionario.keys())
    acoes_funcionario[acao]()
else:
    print("Bem vindo à CareLine, vamos coletar suas informações para acelerar o processo do seu atendimento")
    nome = input("Qual seu nome? \n -->")
    convenio = forca_opcao("Qual é o seu convênio?", seguros)

