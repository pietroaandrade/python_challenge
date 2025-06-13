from datetime import datetime
from pydantic import BaseModel, ValidationError
import json
import os
class PatientData(BaseModel):
    name: str          
    insurance: str
    symptoms: str
    temperature: int

espera_cadastro = {
    "nome": "",
    "convenio": ""
}

patients = {}
next_id = 1
chat = {}
seguros = ["porto seguro", "bradesco", "amil", "sulamérica", "unimed"]
espera_comum = []
espera_urgencia = []





def salvar_dados():
    chat_com_chaves_str = {str(k): v for k, v in chat.items()}
    with open('patients.json', 'w', encoding='utf-8') as f:
        json.dump(patients, f, ensure_ascii=False, indent=4)

    with open('fila_urgencia.json', 'w', encoding='utf-8') as f:
        json.dump(espera_urgencia, f, ensure_ascii=False, indent=4)

    with open('fila_comum.json', 'w', encoding='utf-8') as f:
        json.dump(espera_comum, f, ensure_ascii=False, indent=4)

    with open('chat.json', 'w', encoding='utf-8') as f:
         json.dump(chat_com_chaves_str, f, ensure_ascii=False, indent=4)

def carregar_dados():
    
    global patients, espera_urgencia, espera_comum, chat, next_id  

    if os.path.exists('patients.json'):
        with open('patients.json', 'r', encoding='utf-8') as f:
            patients = {int(k): v for k, v in json.load(f).items()}
        if patients:
            next_id = max(patients.keys()) + 1
        else:
            next_id = 1  
    
    if os.path.exists('fila_urgencia.json'):
        with open('fila_urgencia.json', 'r', encoding='utf-8') as f:
            espera_urgencia = [(nome, int(id_pac)) for nome, id_pac in json.load(f)]
    else:
        espera_urgencia = []
    
    if os.path.exists('fila_comum.json'):
        with open('fila_comum.json', 'r', encoding='utf-8') as f:
            espera_comum = [(nome, int(id_pac)) for nome, id_pac in json.load(f)]
    else:
        espera_comum = []
    
    if os.path.exists('chat.json'):
        with open('chat.json', 'r', encoding='utf-8') as f:
            chat = {int(k): v for k, v in json.load(f).items()}  
    else:
        chat = {}

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
def get_id(msg, dic):
    while True:
        print("\nIDs disponíveis:", ", ".join(map(str, dic.keys())))
        patient_id = forca_num(msg)
        
        
        if patient_id in dic:  
            return patient_id
            
        print(f"ID {patient_id} não encontrado.")
        if not continuar_loop():
            return None
def continuar_loop():
    while True:
        resposta = input("Deseja continuar? (s/n): ").lower()
        if resposta == 's':
            return True
        elif resposta == 'n':
            return False
        else:
            print("Resposta inválida. Digite 's' para sim ou 'n' para não.")


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

    if any(valor == "" for valor in espera_cadastro.values()):
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


        if urgencia == "urgente":
            espera_urgencia.append((patients[id_input]["name"], id_input))
        else:
            espera_comum.append((patients[id_input]["name"], id_input))

        print("Paciente adicionado com sucesso!")
        print_patient(id_input, patients)

        salvar_dados()
        for key in espera_cadastro.keys():
            espera_cadastro[key] = ""

    except ValidationError as e:
        print("Erro nos dados:", e)

    return

def delete_patient():
    global next_id
    if not patients:
        print("Nenhum paciente cadastrado.")
        return
    
    print("\n📋 Lista de Pacientes:")
    for patient_id, patient_data in patients.items():
        print(f"🆔 ID: {patient_id} | 👤 Nome: {patient_data['name']}")
    
    
    patient_id = get_id("\nQual o ID do paciente que deseja remover? ", patients)
    if patient_id is None:
        return
    
    confirm = forca_opcao(
        f"Tem certeza que deseja remover {patients[patient_id]['name']} (ID: {patient_id})?",
        ["sim", "nao"]
    )
    
    if confirm == "nao":
        print("Operação cancelada.")
        return
    
    
    patient_name = patients[patient_id]["name"]
    
    
    del patients[patient_id]
    if not patients:  
        next_id = 1  
        print("Todos os pacientes foram removidos. ID reiniciado para 1.")
    
    global espera_comum, espera_urgencia
    espera_comum = [(nome, id) for (nome, id) in espera_comum if id != patient_id]
    espera_urgencia = [(nome, id) for (nome, id) in espera_urgencia if id != patient_id]
    
    if patient_id in chat:
        del chat[patient_id]
    
    salvar_dados()
    print(f"Paciente {patient_name} (ID: {patient_id}) removido com sucesso!")
def get_patient():
    if not patients:
        print("Nenhum paciente cadastrado ainda.")
        return
    
    print("\n📋 Pacientes cadastrados:")
    for patient_id, patient_data in patients.items():
        print(f"🆔 ID: {patient_id} | 👤 Nome: {patient_data['name']}")
    
    patient_id = get_id("\nQual o ID do paciente que quer buscar?", patients)
    if patient_id is None:
        return
    
    print_patient(patient_id, patients)
def create_report():
    patient_id = get_id("Qual o ID do paciente que quer fazer o laudo?", patients)
    if patient_id is None:
        return
    print(f"\nPreenchendo relatório do paciente {patients[patient_id]['name']}:")
        
    laudo = forca_input("Insira o laudo do paciente: \n -->")
    receita = forca_input("Insira a receita do paciente: \n -->")
    mensagem = forca_input("Insira a descrição: \n -->")

    patients[patient_id]["report"]["Laudo"] = laudo
    patients[patient_id]["report"]["Receita"] = receita
    patients[patient_id]["report"]["Mensagem"] = mensagem
    notify_msg = f"Seu laudo médico está pronto! Acesse seu relatório para ver os detalhes."
    notify_patient(patient_id, notify_msg)
    
    print("Relatório salvo e paciente notificado com sucesso!")
    salvar_dados()
    return
def notify_patient(patient_id, message):
    
    if patient_id not in patients:
        return False
    
    if 'notifications' not in patients[patient_id]:
        patients[patient_id]['notifications'] = []
    
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    patients[patient_id]['notifications'].append({
        'message': message,
        'timestamp': timestamp,
        'read': False
    })
    salvar_dados()
    return True
def check_notifications():
    patient_id = get_id("Qual seu ID de paciente?", patients)
    if patient_id is None:
        return
    
    if 'notifications' not in patients[patient_id] or not patients[patient_id]['notifications']:
        print("\n📭 Você não tem novas notificações.")
        return
    
    unread = sum(1 for n in patients[patient_id]['notifications'] if not n['read'])
    print(f"\n📬 Você tem {unread} nova(s) notificação(ões)!")
    
    for idx, notification in enumerate(patients[patient_id]['notifications']):
        status = "🆕" if not notification['read'] else "📭"
        print(f"\n{status} Notificação {idx+1} - {notification['timestamp']}")
        print(notification['message'])
        patients[patient_id]['notifications'][idx]['read'] = True
    
    salvar_dados()
def access_report():
    patient_id = get_id("Qual o seu ID de paciente para acessar o relatório?", patients)
    if patient_id is None:
        return
    
    
    if patient_id not in patients:
        print("Paciente não encontrado.")
        return
    
    report = patients[patient_id]["report"]
    
    
    if not any(report.values()):
        print("O relatório ainda não foi preenchido. Aguarde o atendimento.")
        return
    
    print(f"""
📄 Relatório Médico do Paciente {patients[patient_id]['name']}:
🧪 Laudo: {report['Laudo']}
💊 Receita: {report['Receita']}
📬 Mensagem do funcionário: {report['Mensagem']}
""")
    return

def retrieve_line_funcionario():
    todas_filas = []
    
    if espera_urgencia:
        print("\n🟥 Fila de Urgência:")
        for nome, id_p in espera_urgencia:
            print(f"ID: {id_p} | Nome: {nome}")
            todas_filas.append(id_p)
    
    if espera_comum:
        print("\n🟩 Fila Comum:")
        for nome, id_p in espera_comum:
            print(f"ID: {id_p} | Nome: {nome}")
            todas_filas.append(id_p)
    
    if not todas_filas:
        print("Não há pacientes na fila de espera.")
        return None
    
    while True:
        id_paciente = forca_num("\nDigite o ID do paciente que deseja chamar: ")
        
        
        if id_paciente in todas_filas:
            break
        print(f"ID {id_paciente} não encontrado nas filas. IDs disponíveis: {', '.join(map(str, todas_filas))}")
    
    
    for fila in [espera_urgencia, espera_comum]:
        for i, (nome, id_p) in enumerate(fila):
            if id_p == id_paciente:
                fila.pop(i)
                print(f"\n✅ Paciente {nome} (ID: {id_p}) chamado com sucesso!")
                print_patient(id_p, patients)
                salvar_dados()
                return id_p

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
    tipo_mensagem = forca_opcao("Sobre o que sua mensagem está recorrendo?", ["urgencia", "pergunta", "feedback"])

    if tipo_mensagem == "urgencia":
        print("Você selecionou URGÊNCIA.")
    elif tipo_mensagem == "espera":
        print("Você selecionou PERGUNTA.")
    else:
        print("Você selecionou FEEDBACK.")

    patient_id = get_id("Qual seu ID de paciente para enviar a mensagem?", patients)
    if patient_id is None:
        return
    descricao = forca_input("Descreva sua situação:\n--> ")

    if patient_id not in chat:
        chat[patient_id] = []

    chat[patient_id].append({
            "tipo": tipo_mensagem,
            "descricao": descricao,
            "hora": datetime.now().strftime("%H:%M")
    })
    salvar_dados()
    print("Mensagem enviada com sucesso para avaliação!")
    print(f"\nPaciente: {patients[patient_id]['name']}\nTipo: {tipo_mensagem}\nDescrição: {descricao}\nHorário: {chat[patient_id][-1]['hora']}")
    
    return


def retrieve_messages():
    print("\n📨 Acessar Mensagens")
    print("-" * 30)
    patient_id = get_id("Qual seu ID de paciente para ver suas mensagens?", chat)
    if patient_id is None:
        print("\nNenhuma mensagem para exibir. Voltando ao menu...")
        return

    if not chat[patient_id]:
        print("\nNenhuma mensagem enviada ainda.")
        return

    print(f"\n📋 Chat do paciente ID {patient_id}:")
    for i in range(len(chat[patient_id])):
        message = chat[patient_id][i]
        print(f"""
📝 Mensagem {i+1}
• Tipo: {message['tipo']}
• Descrição: {message['descricao']}
• Horário: {message['hora']}
        """)
    return

def retrieveMessage_funcionario():
    if not chat:
        print("📨 Não há mensagens no sistema.")
        return
    
    total = sum(len(mensagens) for mensagens in chat.values())
    print(f"📨 Você tem {total} mensagem(ns) no sistema.")

    filtro = forca_opcao("Qual o tipo de mensagem deseja ver?", ["urgencia", "pergunta", "feedback", "todos"])
    
    encontrou = False
    for id_paciente, mensagens in chat.items():
        
        if id_paciente not in patients:
            nome_paciente = "[Paciente Removido]"
        else:
            nome_paciente = patients[id_paciente]['name']
            
        for mensagem in mensagens:
            if filtro == "todos" or mensagem["tipo"] == filtro:
                encontrou = True
                print(f"""
📬 Nova mensagem de {nome_paciente} (ID {id_paciente})
🕒 Hora: {mensagem['hora']}
📌 Tipo: {mensagem['tipo'].capitalize()}
📝 Conteúdo: {mensagem['descricao']}
""")
    
    if not encontrou:
        print(f"Nenhuma mensagem do tipo '{filtro}' encontrada.")
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
    "remover paciente": delete_patient,
    "chamar paciente": retrieve_line_funcionario,
    "diagnostico" : create_report,
    "ver mensagens" : retrieveMessage_funcionario,
    "sair": sair
}
acoes_paciente = {
    "ver fila": retrieve_line_paciente,
    "ver diagnostico" : access_report,
    "enviar mensagem" : message,
    "ver mensagem" : retrieve_messages,
    "ver notificacoes": check_notifications,
    "sair": sair
}
carregar_dados()
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