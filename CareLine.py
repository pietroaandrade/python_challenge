# Importante: Funcao mensagem com funcionario
# Importante: Funcao acessar mensagem paciente
# Importante: logar como paciente ou cadastrar
# Importante: Get_patient shows espera_list
# if else paciente na urgencia para display de pacientes restantes

from pydantic import BaseModel, ValidationError

class PatientData(BaseModel):
    name: str          
    insurance: str
    symptoms: str
    temperature: int

espera_cadastro = {
    "nome": "",
    "convenio": ""
}

patients = {
}

seguros = ["porto seguro", "bradesco", "amil", "sulamérica", "unimed"]

espera_comum = []

espera_urgencia = []

next_id = 1

def forca_opcao(msg, lista_opcoes, msg_erro='Inválido'):
    opcoes = '\n'.join(lista_opcoes)
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
def forca_input(msg):
    resposta = input(msg).strip()
    while not resposta:
        print("Campo obrigatório. Por favor, preencha.")
        resposta = input(msg).strip()
    return resposta


def print_patient(id, dic):
    data = dic[id]
    print(f"""
📄 Dados do Paciente:
🆔 ID: {id}
👤 Nome: {data['name']}
🏥 Convênio: {data['insurance']}
🤒 Sintomas: {data['symptoms']}
🌡️ Temperatura: {data['temperature']}ºC
""")

def avaliar_prioridade(temp):
    if temp <= 35 or temp >= 39:
        return "urgente"
    return "comum"

def create_patient():
    global next_id
    if any(valor == "" for valor in espera_cadastro.values()):
        print("Nenhum dado do paciente disponível.")
        resposta = forca_opcao("Gostaria de preencher o cadastro do paciente manualmente?", ["sim","nao"])
        if resposta == "nao":
            print("Aguarde o paciente preencher o nome e convênio.")
            return
        else:
            espera_cadastro["nome"] = input("Enter Name: ")
            espera_cadastro["convenio"] = forca_opcao("Qual é o seu convênio?", seguros)
                
    id_input = next_id
    next_id += 1

    name_input, insurance_input = espera_cadastro["nome"], espera_cadastro["convenio"]
    symptoms_input = input("Sintomas do paciente: ")
    temp_input = forca_num("Temperatura paciente: ")
    urgencia = forca_opcao("Qual é a situação do paciente?", ['urgente','comum'])
    urgencia = avaliar_prioridade(temp_input)
    print(f"Classificação automática: Paciente considerado '{urgencia.upper()}' com temperatura de {temp_input}°C.")

    
    try:
        patient_data = PatientData(
            name=name_input,
            insurance=insurance_input,
            symptoms=symptoms_input,
            temperature=temp_input
        )
        patients[id_input] = {
            **patient_data.model_dump(),
            "report" : {"Laudo": "", "Receita": "", "Mensagem": ""}
        }
        if urgencia == "urgente":
            espera_urgencia.append((patients[id_input]["name"], id_input))
        else:
            espera_comum.append((patients[id_input]["name"], id_input))
        print("Patient added successfully!")
        print_patient(id_input, patients)
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
        print_patient(id, patients)
    return

def create_report():
    id = forca_num("Qual é o ID do paciente desejado?")
    if id not in patients:
        print("Paciente não encontrado")
        create_report()
    else:
        print(f"\nPreenchendo relatório do paciente {patients[id]['name']}:")
        
        laudo = forca_input("Insira o laudo do paciente: \n -->")
        receita = forca_input("Insira a receita do paciente: \n -->")
        mensagem = forca_input("Insira a descrição: \n -->")

        patients[id]["report"]["Laudo"] = laudo
        patients[id]["report"]["Receita"] = receita
        patients[id]["report"]["Mensagem"] = mensagem
    return

def access_report():
    id = forca_num("Digite seu número de paciente para ver o relatório: ")
    if id not in patients:
        print("Paciente não encontrado.")
        return
    report = patients[id]["report"]
    if any(value =="" for value in patients[id][report].value()):
        print("O relatório ainda não foi preenchido. Aguarde o atendimento.")
        return
    print(f"""
📄 Relatório Médico do Paciente {patients[id]['name']}:
🧪 Laudo: {report['Laudo']}
💊 Receita: {report['Receita']}
📬 Mensagem do funcionário: {report['Mensagem']}
    """)
    return

def retrieve_line_funcionario():
    
    if not espera_comum and not espera_urgencia:
        print("Não há pacientes na fila de espera.")
        return
    if len(espera_urgencia) > 0:
        proximo_paciente = espera_urgencia.pop(0)
    else:
        proximo_paciente = espera_comum.pop(0)

    nome, id = proximo_paciente
    print(f"Chamando o próximo paciente da fila:")
    print(f"🟢 Nome: {nome}\n🩺 Numero: {id}")
    print(f"Pacientes restantes na fila: {len(espera_comum) + len(espera_urgencia)}")
    

    return proximo_paciente

def retrieve_line_paciente():
    if not espera_comum and not espera_urgencia:
        print("Não há pacientes cadastrados na fila de espera. Aguarde ser chamado pela triagem.")
        return None

    elif espera_urgencia:
        nome, id = espera_urgencia[0]
        fila = espera_urgencia
    else:
        nome, id = espera_comum[0]
        fila = espera_comum

    print(f"🟢 Próximo paciente da fila:\n --> Nome: {nome}\n --> Número: {id}")
    print(f"Pacientes restantes na fila: {len(fila)}")

    return (nome, id)



def sair():
    print("Saindo do menu atual...\n")
    return "sair"


def menu_funcionario():
    while True:
        acao = forca_opcao("\nO que deseja fazer?", acoes_funcionario.keys())
        resultado = acoes_funcionario[acao]()
        if resultado == "sair":
            break


def menu_paciente():
    print("Bem vindo à CareLine, vamos coletar suas informações para acelerar o processo do seu atendimento")
    nome = forca_input("Qual seu nome? \n -->")
    convenio = forca_opcao("Qual é o seu convênio?", seguros)
    espera_cadastro["nome"],espera_cadastro["convenio"] = nome, convenio
    print(f"Obrigado, {nome}. Aguarde, você será chamado pelo atendente.")
    while True:
        acao = forca_opcao("\nO que deseja fazer?", acoes_paciente.keys())
        resultado = acoes_paciente[acao]()
        if resultado == "sair":
            break
    return

acoes_funcionario = {
    "cadastrar paciente": create_patient,
    "buscar paciente": get_patient,
    "chamar paciente": retrieve_line_funcionario,
    "diagnostico" : create_report,
    "sair": sair
}
acoes_paciente = {
    "ver fila": retrieve_line_paciente,
    "ver diagnostico" : access_report,
    "sair": sair
}
while True:
    print('Iniciando sistema CareLine')
    user_type = forca_opcao("Qual seu papel?", ["funcionario", "paciente", "sair"])
    if user_type == "funcionario":
        menu_funcionario()
    elif user_type == "paciente":
        menu_paciente()
    else:
        print("Encerrando sistema...")
        break
