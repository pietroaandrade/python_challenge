# Importante: Funcao mensagem com funcionario
# Importante: Funcao acessar mensagem paciente


from datetime import datetime
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
next_id = 1



chat = {

}



seguros = ["porto seguro", "bradesco", "amil", "sulamérica", "unimed"]

espera_comum = []

espera_urgencia = []




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



def create_patient():
    global next_id
    cadastro_manual = False



    if any(valor == "'" for valor in espera_cadastro.values()):
        print("Nenhum dado do paciente disponível.")
        resposta = forca_opcao("Gostaria de preencher o cadastro do paciente manualmente?", ["sim", "nao"])
        if resposta == "nao":
            print("Aguarde o paciente preencher o nome e convênio.")
            return
        else:
            espera_cadastro["nome"] = input("Digite o nome do paciente: ")
            espera_cadastro["convenio"] = forca_opcao("Qual é o convênio do paciente?", seguros)
            cadastro_manual = True


    name_input = espera_cadastro["nome"]
    insurance_input = espera_cadastro["convenio"]
    id_input = next_id
    next_id += 1

    if not cadastro_manual:
        print("\nPaciente aguardando na fila de cadastro:")
        print(f"👤 Nome: {name_input}")
        print(f"🏥 Convênio: {insurance_input}")


    symptoms_input = input("Descreva os sintomas do paciente: ")
    temp_input = forca_num("Temperatura do paciente (°C): ")
    urgencia = forca_opcao("Classificação de urgência do paciente:", ['urgente', 'comum'])

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
            "report": {"Laudo": "", "Receita": "", "Mensagem": ""}
        }

        # Adiciona na fila correta
        if urgencia == "urgente":
            espera_urgencia.append((patients[id_input]["name"], id_input))
        else:
            espera_comum.append((patients[id_input]["name"], id_input))

        print("Paciente adicionado com sucesso!")
        print_patient(id_input, patients)

        # Limpa o cadastro temporário para o próximo paciente
        for key in espera_cadastro.keys():
            espera_cadastro[key] = ""

    except ValidationError as e:
        print("Erro nos dados:", e)

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
    if any(value =="" for value in report.values()):
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


def message():
    tipo_mensagem = forca_opcao("Sobre o que sua mensagem está recorrendo?", ["urgencia", "espera", "feedback"])

    if tipo_mensagem == "urgencia":
        print("Você selecionou URGÊNCIA.")
    elif tipo_mensagem == "espera":
        print("Você selecionou ESPERA.")
    else:
        print("Você selecionou FEEDBACK.")

        while True:
            patient_id = forca_num("Qual seu ID para enviar a mensagem? ")
            if patient_id not in patients:
                print("Paciente não encontrado. Tente novamente.")
                continue
            break

        descricao = forca_input("Descreva sua situação:\n--> ")

        if patient_id not in chat:
            chat[patient_id] = []

        chat[patient_id].append({
            "tipo": tipo_mensagem,
            "descricao": descricao,
            "hora": datetime.now().strftime("%H:%M")
        })

        print("Mensagem enviada com sucesso para avaliação!")
        print(f"\nResumo da mensagem:\nTipo: URGÊNCIA\nDescrição: {descricao}\nHorário: {chat[patient_id][-1]['hora']}")

    return


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
    paciente_user = forca_opcao("O que deseja fazer?", ["cadastro", "outro"])
    if paciente_user == "cadastro":
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
    "enviar mensagem" : message,
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
