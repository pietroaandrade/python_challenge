# Importante: Criar funcao de urgencia para triagem
# Importante: Criar funcao de temperatura para urgencia
# Importante: Criar funcao de Observar fila
# Importante: Criar funcao de Criar laudo
# importante: criar funcao de acessar laudo
# Importante: melhorar prints dic

from pydantic import BaseModel, ValidationError


class PatientData(BaseModel):
    name: str
    insurance: str
    symptoms: str
    temperature: int


next_id = 1

espera_cadastro = {
    "nome": "",
    "convenio": ""

}
patients = {
}

seguros = ["porto seguro", "bradesco", "amil", "sulamérica", "unimed"]

espera = []


def forca_opcao(msg, lista_opcoes, msg_erro='Inválido'):
    opcoes = '\n'.join(lista_opcoes).lower()
    opcao = input(f"{msg}\n{opcoes}\n->").lower()
    while opcao not in lista_opcoes:
        print(msg_erro)
        opcao = input(f"{msg}\n{opcoes}\n->").lower()
    return opcao


def forca_num(msg):
    num = input(msg)
    if not num.isnumeric():
        print("Deve ser um número!")
        num = forca_num(msg)
    return int(num)


def create_patient():
    global next_id
    for key in espera_cadastro.keys():
        if espera_cadastro[key] == "":
            print("Nenhum dado do paciente disponível. Aguarde o paciente preencher o nome e convênio.")
            return
    id_input = next_id
    next_id += 1
    name_input, insurance_input = espera_cadastro["nome"], espera_cadastro["convenio"]
    symptoms_input = input("Sintomas do paciente: ")
    temp_input = forca_num("Temperatura paciente:")

    try:
        patient_data = PatientData(
            name=name_input,
            insurance=insurance_input,
            symptoms=symptoms_input,
            temperature=temp_input
        )
        patients[id_input] = patient_data.model_dump()
        espera.append((patients[id_input]["name"], id_input))
        print("Patient added successfully!")
        print(patients)

        for key in espera_cadastro.keys():
            espera_cadastro[key] = ""

    except ValidationError as e:
        print("Invalid data:", e)

    return


def get_patient():
    while True:
        id = forca_num("Qual é o ID do paciente desejado?")
        if id not in patients:
            print("Paciente não encontrado")
            continue
        data = patients[id]
        print(f"ID: {id}, Name: {data['name']}, Insurance: {data['insurance']}, Symptoms: {data['symptoms']}, temperatura: {data['temperature']}ºC")
        break
    return


def retrieve_line_funcionario():
    if not espera:
        print("Não há pacientes na fila de espera.")
        return None
    proximo_paciente = espera.pop(0)
    nome, id = proximo_paciente
    print(f"Chamando o próximo paciente da fila:")
    print(f"🟢 Nome: {nome}\n🩺 Numero: {id}")
    print(f"Pacientes restantes na fila: {len(espera)}")

    return proximo_paciente

def retrieve_line_paciente():
    if not espera:
        print("Não Há pacientes cadastrados para a fila de espera. Aguarde ser chamado pela triagem.")
        return None

    else:
        proximo_paciente = espera
        nome, id = proximo_paciente
        print(f"🟢 Próximo paciente da fila \n --> Numero: {id}")
        print(f"Pacientes restantes na fila: {len(espera)}")

    return proximo_paciente


def menu_funcionario():
    while True:
        acao = forca_opcao("O que deseja fazer?", acoes_funcionario.keys())
        resultado = acoes_funcionario[acao]()
        if resultado == "sair":
            break


def menu_paciente():
    print("Bem vindo à CareLine, vamos coletar suas informações para acelerar o processo do seu atendimento")
    nome = input("Qual seu nome? \n -->")
    convenio = forca_opcao("Qual é o seu convênio?", seguros)
    espera_cadastro["nome"],espera_cadastro["convenio"] = nome, convenio
    print(f"Obrigado, {nome}. Aguarde, você será chamado pelo atendente.")
    while True:
        acao = forca_opcao("O que deseja fazer?", acoes_paciente.keys())
        resultado = acoes_paciente[acao]()
        if resultado == "sair":
            break
    return


def sair():
    print("Saindo do menu atual...\n")
    return "sair"


acoes_funcionario = {
    "cadastrar paciente": create_patient,
    "buscar paciente": get_patient,
    "chamar paciente": retrieve_line_funcionario,
    "sair": sair
}
acoes_paciente = {
    "ver fila": retrieve_line_paciente,
    "sair": sair
}
while True:
    print('Iniciando sistema CareLine')
    print(f"[DEBUG] Pacientes salvos: {patients}")
    user_type = forca_opcao("Qual seu papel?", ["funcionario", "paciente", "encerrar sistema"])
    if user_type == "funcionario":
        menu_funcionario()
    elif user_type == "paciente":
        menu_paciente()
    else:
        print("Encerrando sistema...")
        break

