import sys
import time
import webbrowser
import os
import platform
from datetime import datetime
import json
import hashlib
import psutil

ARQUIVO_USUARIOS = 'usuarios.json'
usuario_logado = None

# Configurações de acessibilidade globais
config_inclusao = {
    'modo_alto_contraste': False,
    'tamanho_fonte': 1,  # 1 = normal, 2 = grande, 3 = extra grande
    'leitor_tela': False,
    'libras': False,
    'descricao_audio': False,
    'dislexia': False,
    'daltonismo': False,
    'autismo': False
}

# Dicionário de cursos com links e informações adicionais
cursos = {
    1: {
        "nome": "Matemática Básica",
        "link": "https://www.youtube.com/watch?v=e78_5WIssSU&list=PLTPg64KdGgYhYpS5nXdFgdqEZDOS5lARB",
        "descricao": "Curso introdutório de matemática para iniciantes",
        "nivel": "Iniciante",
        "tags": ["matemática", "básico", "fundamentos"]
    },
    2: {
        "nome": "Física para Iniciantes",
        "link": "https://www.youtube.com/watch?v=wlTa_yTElGM&list=PLzjR7HXQnrcf84SMs9pE7XycU--cRAls4",
        "descricao": "Conceitos básicos de física para quem está começando",
        "nivel": "Iniciante",
        "tags": ["física", "ciências", "básico"]
    },
    3: {
        "nome": "Química do Zero",
        "link": "https://www.youtube.com/watch?v=XDBwYrWFZUQ&list=PLyuycNvl80SC6qg79NJuaY1W29ixvyPqG",
        "descricao": "Aprenda química desde os fundamentos",
        "nivel": "Iniciante",
        "tags": ["química", "elementos", "reações"]
    },
    4: {
        "nome": "Programação em Python",
        "link": "https://www.youtube.com/watch?v=GQpQha2Mfpg",
        "descricao": "Introdução à programação usando Python",
        "nivel": "Intermediário",
        "tags": ["programação", "python", "computação"]
    },
    5: {
        "nome": "Cybersegurança-comece",
        "link": "https://www.youtube.com/watch?v=oyR4hCJhwMU",
        "descricao": "Fundamentos de segurança digital para iniciantes",
        "nivel": "Intermediário",
        "tags": ["segurança", "hacking", "tecnologia"]
    },
    6: {
        "nome": "Ética e cidadania",
        "link": "https://www.youtube.com/watch?v=6tu8ERj7g-Y&list=PLxI8Can9yAHcT4o6AC7YynKNj1gM20U7R",
        "descricao": "Discussões sobre ética e cidadania na sociedade moderna",
        "nivel": "Todos",
        "tags": ["sociedade", "filosofia", "cidadania"]
    },
}

# Recursos de inclusão
recursos_inclusao = {
    'libras': {
        'descricao': 'Intérprete de LIBRAS em vídeos',
        'status': 'Disponível para todos os cursos'
    },
    'audiodescricao': {
        'descricao': 'Audiodescrição para conteúdo visual',
        'status': 'Disponível para 4 cursos'
    },
    'leitura_facil': {
        'descricao': 'Versão em leitura fácil para neurodivergentes',
        'status': 'Disponível para 3 cursos'
    },
    'alto_contraste': {
        'descricao': 'Modo alto contraste para baixa visão',
        'status': 'Disponível em toda plataforma'
    },
    'dislexia': {
        'descricao': 'Fonte especial para dislexia',
        'status': 'Disponível em toda plataforma'
    }
}

def limpar_tela():
    """Limpa a tela do console de forma multiplataforma"""
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def esperar(msg="Carregando"):
    """Exibe uma mensagem com animação de pontos"""
    print(msg, end="", flush=True)
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print("\n")

def cabecalho(titulo):
    """Exibe um cabeçalho formatado com inclusão visual"""
    largura = 60
    
    if config_inclusao['modo_alto_contraste']:
        print("\n" + "="*largura)
        print(f"{titulo.center(largura)}")
        print("="*largura)
    else:
        print("\n" + "═"*largura)
        print(f"║{titulo.center(largura-2)}║")
        print("╚" + "═"*(largura-2) + "╝")

def aplicar_estilo_inclusivo(texto):
    """Aplica formatação de inclusão com base nas configurações"""
    if config_inclusao['tamanho_fonte'] == 2:
        texto = f"\033[1m{texto}\033[0m"  # Negrito
    elif config_inclusao['tamanho_fonte'] == 3:
        texto = f"\033[1m\033[4m{texto}\033[0m"  # Negrito e sublinhado
        
    if config_inclusao['dislexia']:
        # Simula fonte para dislexia (apresentação diferente)
        texto = texto.upper()
        
    return texto

def exibir_mensagem_inclusiva(mensagem, tipo='info'):
    """Exibe mensagens com formatação inclusiva"""
    cores = {
        'erro': '\033[91m',  # Vermelho
        'sucesso': '\033[92m',  # Verde
        'aviso': '\033[93m',  # Amarelo
        'info': '\033[94m',  # Azul
        'alerta': '\033[95m'  # Magenta
    }
    
    if config_inclusao['modo_alto_contraste']:
        # Estilos para alto contraste
        estilo = {
            'erro': '\033[1;41;97m',  # Fundo vermelho, texto branco
            'sucesso': '\033[1;42;30m',  # Fundo verde, texto preto
            'aviso': '\033[1;43;30m',  # Fundo amarelo, texto preto
            'info': '\033[1;44;97m',  # Fundo azul, texto branco
            'alerta': '\033[1;45;97m'  # Fundo magenta, texto branco
        }[tipo]
    else:
        estilo = cores.get(tipo, '\033[94m')  # Azul como padrão
    
    reset = '\033[0m'
    
    if config_inclusao['leitor_tela']:
        print(f"[LEITOR DE TELA] {mensagem}")
    
    print(f"{estilo}{mensagem}{reset}")

def configurar_inclusao():
    """Menu de configuração do modo inclusão"""
    global config_inclusao  # Certifique-se de que está usando a variável global

    if usuario_logado:
        config_inclusao = carregar_configuracoes_usuario(usuario_logado['email'])
    else:
        exibir_mensagem_inclusiva("Você precisa estar logado.", "erro")
        time.sleep(1)
        return

    while True:
        limpar_tela()
        cabecalho("CONFIGURAÇÕES DE INCLUSÃO E ACESSIBILIDADE")
        
        print("\n1. " + aplicar_estilo_inclusivo("Modo Alto Contraste: ") + ("ATIVADO" if config_inclusao['modo_alto_contraste'] else "desativado"))
        print("2. " + aplicar_estilo_inclusivo("Tamanho da Fonte: ") + ("Normal" if config_inclusao['tamanho_fonte'] == 1 else "Grande" if config_inclusao['tamanho_fonte'] == 2 else "Extra Grande"))
        print("3. " + aplicar_estilo_inclusivo("Leitor de Tela: ") + ("ATIVADO" if config_inclusao['leitor_tela'] else "desativado"))
        print("4. " + aplicar_estilo_inclusivo("Intérprete de LIBRAS: ") + ("ATIVADO" if config_inclusao['libras'] else "desativado"))
        print("5. " + aplicar_estilo_inclusivo("Descrição em Áudio: ") + ("ATIVADO" if config_inclusao['descricao_audio'] else "desativado"))
        print("6. " + aplicar_estilo_inclusivo("Modo Dislexia: ") + ("ATIVADO" if config_inclusao['dislexia'] else "desativado"))
        print("7. " + aplicar_estilo_inclusivo("Modo Daltonismo: ") + ("ATIVADO" if config_inclusao['daltonismo'] else "desativado"))
        print("8. " + aplicar_estilo_inclusivo("Modo Autismo: ") + ("ATIVADO" if config_inclusao['autismo'] else "desativado"))
        print("\n0. Voltar ao menu principal")
        
        escolha = input("\nEscolha uma opção para modificar: ")

        match escolha:
            case "1":
                config_inclusao['modo_alto_contraste'] = not config_inclusao['modo_alto_contraste']
                exibir_mensagem_inclusiva("Modo Alto Contraste " + ("ativado" if config_inclusao['modo_alto_contraste'] else "desativado"), 'sucesso')
            case "2":
                config_inclusao['tamanho_fonte'] = config_inclusao['tamanho_fonte'] % 3 + 1
                exibir_mensagem_inclusiva(f"Tamanho da fonte alterado para: {'Normal' if config_inclusao['tamanho_fonte'] == 1 else 'Grande' if config_inclusao['tamanho_fonte'] == 2 else 'Extra Grande'}", 'sucesso')
            case "3":
                config_inclusao['leitor_tela'] = not config_inclusao['leitor_tela']
                exibir_mensagem_inclusiva("Leitor de tela " + ("ativado" if config_inclusao['leitor_tela'] else "desativado"), 'sucesso')
                if config_inclusao['leitor_tela']:
                    exibir_mensagem_inclusiva("Dica: Use o leitor de tela com fones de ouvido para melhor experiência.", 'info')
            case "4":
                config_inclusao['libras'] = not config_inclusao['libras']
                exibir_mensagem_inclusiva("Intérprete de LIBRAS " + ("ativado" if config_inclusao['libras'] else "desativado"), 'sucesso')
            case "5":
                config_inclusao['descricao_audio'] = not config_inclusao['descricao_audio']
                exibir_mensagem_inclusiva("Descrição em áudio " + ("ativada" if config_inclusao['descricao_audio'] else "desativada"), 'sucesso')
            case "6":
                config_inclusao['dislexia'] = not config_inclusao['dislexia']
                exibir_mensagem_inclusiva("Modo Dislexia " + ("ativado" if config_inclusao['dislexia'] else "desativado"), 'sucesso')
            case "7":
                config_inclusao['daltonismo'] = not config_inclusao['daltonismo']
                exibir_mensagem_inclusiva("Modo Daltonismo " + ("ativado" if config_inclusao['daltonismo'] else "desativado"), 'sucesso')
            case "8":
                config_inclusao['autismo'] = not config_inclusao['autismo']
                exibir_mensagem_inclusiva("Modo Autismo " + ("ativado" if config_inclusao['autismo'] else "desativado"), 'sucesso')
                if config_inclusao['autismo']:
                    exibir_mensagem_inclusiva("Dica: Este modo reduz elementos visuais complexos e animações.", 'info')
            case "0":
                break
            case _:
                exibir_mensagem_inclusiva("Opção inválida. Tente novamente.", 'erro')

        salvar_configuracoes_usuario(usuario_logado['email'], config_inclusao)
        time.sleep(1)


def pagina_inicio():
    """Página inicial com informações inclusivas"""
    limpar_tela()
    cabecalho("BEM-VINDO À PLATAFORMA EDTECH INCLUSIVA")
    
    print(aplicar_estilo_inclusivo("\nNossa missão é democratizar o acesso ao ensino de exatas e programação, oferecendo oportunidades para todos, independentemente de onde vivem, de suas condições ou de suas limitações."))
    
    if config_inclusao['modo_alto_contraste']:
        print("\n" + "*"*60)
        print("*" + "MODO ALTO CONTRASTE ATIVADO".center(58) + "*")
        print("*"*60)
    
    if config_inclusao['libras']:
        print(aplicar_estilo_inclusivo("\n[LIBRAS] Todos os vídeos possuem intérprete de LIBRAS disponível."))
    
    if config_inclusao['leitor_tela']:
        print(aplicar_estilo_inclusivo("\n[LEITOR DE TELA] Navegação por voz ativada."))
    
    print("\nRecursos disponíveis:")
    print("- Cursos adaptados para diferentes necessidades")
    print("- Material em múltiplos formatos (vídeo, áudio, texto)")
    print("- Suporte a diversas tecnologias assistivas")
    
    # Adicionando as novas opções
    print("\nOPÇÕES PRINCIPAIS:")
    print("1. Começar a Aprender")
    print("2. Seja Voluntário")
    
    escolha = input("\nEscolha uma opção (1-2) ou pressione Enter para voltar ao menu: ")
    
    match escolha:
        case "1":
            comecar_agora()
        case "2":
            seja_voluntario()
        case _:
            pass  # Volta ao menu principal

def pagina_sobre():
    """Página sobre a plataforma com foco em inclusão"""
    limpar_tela()
    cabecalho("SOBRE NÓS - PLATAFORMA INCLUSIVA")
    
    print(aplicar_estilo_inclusivo("\nQuem somos:"))
    print("Somos uma EdTech focada no ensino de exatas para todos, com ênfase em:")
    print("- Inclusão social e regional")
    print("- Acessibilidade para pessoas com deficiência")
    print("- Adaptação para diferentes estilos de aprendizagem")
    
    print(aplicar_estilo_inclusivo("\nNossos valores:"))
    print("1. Educação como direito fundamental")
    print("2. Tecnologia a serviço da inclusão")
    print("3. Respeito à diversidade humana")
    
    print(aplicar_estilo_inclusivo("\nEstatísticas de inclusão:"))
    print(f"- {len(cursos)} cursos adaptados")
    print(f"- {len(recursos_inclusao)} recursos de acessibilidade")
    print("- Mais de 100 horas de conteúdo com LIBRAS")
    
    input("\nPressione Enter para voltar ao menu.")

def pagina_cursos():
    """Lista de cursos com informações de acessibilidade"""
    limpar_tela()
    cabecalho("NOSSOS CURSOS INCLUSIVOS")
    
    print(aplicar_estilo_inclusivo("\nTodos os cursos possuem:"))
    print("- Legendas em português")
    print("- Transcrição do conteúdo")
    print("- Opção de áudio descrição")
    
    print("\nCursos disponíveis:")
    for i, dados in cursos.items():
        recursos = []
        if config_inclusao['libras']:
            recursos.append("LIBRAS")
        if config_inclusao['descricao_audio']:
            recursos.append("Áudio-descrição")
        if config_inclusao['dislexia']:
            recursos.append("Fonte dislexia")
            
        recursos_str = " | ".join(recursos) if recursos else "Padrão"
        
        print(f"\n{i}. {aplicar_estilo_inclusivo(dados['nome'])}")
        print(f"   Nível: {dados['nivel']}")
        print(f"   Recursos: {recursos_str}")
        print(f"   Tags: {', '.join(dados['tags'])}")
    
    input("\nPressione Enter para voltar.")

def pagina_acessibilidade():
    """Página detalhada sobre recursos de acessibilidade"""
    limpar_tela()
    cabecalho("ACESSIBILIDADE E INCLUSÃO")
    
    print(aplicar_estilo_inclusivo("\nRECURSOS DISPONÍVEIS:"))
    for recurso, info in recursos_inclusao.items():
        print(f"\n- {aplicar_estilo_inclusivo(info['descricao'])}")
        print(f"  Status: {info['status']}")
    
    print(aplicar_estilo_inclusivo("\nCOMO UTILIZAR:"))
    print("1. Acesse as Configurações de Inclusão")
    print("2. Ative os recursos que deseja utilizar")
    print("3. Navegue pela plataforma com os recursos adaptados")
    
    print(aplicar_estilo_inclusivo("\nDICAS DE ACESSIBILIDADE:"))
    print("- Tecla '+' aumenta o tamanho do texto")
    print("- Tecla '-' diminui o tamanho do texto")
    print("- Tecla 'L' ativa/desativa o leitor de tela")
    
    input("\nPressione Enter para voltar ao menu.")

def carregar_usuarios():
    if not os.path.exists(ARQUIVO_USUARIOS):
        return []
    with open(ARQUIVO_USUARIOS, 'r', encoding='utf-8') as f:
        return json.load(f)

# Função para salvar usuários
def salvar_usuarios(lista):
    with open(ARQUIVO_USUARIOS, 'w', encoding='utf-8') as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)

def gerar_hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def salvar_configuracoes_usuario(email, config_atualizada):
    """Salva as configurações de inclusão do usuário no arquivo JSON"""
    try:
        with open(ARQUIVO_USUARIOS, 'r', encoding='utf-8') as f:
            usuarios = json.load(f)
    except FileNotFoundError:
        usuarios = []

    for usuario in usuarios:
        if usuario['email'] == email:
            usuario['config_inclusao'] = config_atualizada
            break

    with open(ARQUIVO_USUARIOS, 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)

# Página de login
def pagina_login():
    limpar_tela()
    global usuario_logado
    
    cabecalho("ACESSAR CONTA - LOGIN INCLUSIVO")

    print(aplicar_estilo_inclusivo("\nPreencha seus dados:"))
    if config_inclusao['leitor_tela']:
        print("[LEITOR DE TELA ATIVO] Por favor, preencha os campos a seguir:")

    usuario = input(aplicar_estilo_inclusivo("Usuário ou e-mail: "))
    senha = input(aplicar_estilo_inclusivo("Senha: "))

    if config_inclusao['leitor_tela']:
        print("[LEITOR DE TELA] Verificando credenciais...")

    esperar("Verificando login")

    usuarios = carregar_usuarios()
    senha_hash = gerar_hash_senha(senha)
    
    for u in usuarios:
        if (usuario == u['email'] or usuario == u['nome']) and senha_hash == u['senha']:
            usuario_logado = u
            # Inicializa estatísticas se não existirem
            if 'estatisticas' not in usuario_logado:
                usuario_logado['estatisticas'] = {
                    'primeiro_login': datetime.now().strftime("%d/%m/%Y %H:%M"),
                    'ultimo_login': datetime.now().strftime("%d/%m/%Y %H:%M"),
                    'total_sessoes': 1,
                    'tempo_total': 0,
                    'historico_logout': []
                }
            else:
                usuario_logado['estatisticas']['ultimo_login'] = datetime.now().strftime("%d/%m/%Y %H:%M")
                usuario_logado['estatisticas']['total_sessoes'] += 1
            
            # Atualiza o arquivo de usuários
            for user in usuarios:
                if user['email'] == usuario_logado['email']:
                    user.update(usuario_logado)
                    break
            salvar_usuarios(usuarios)
            
            exibir_mensagem_inclusiva("Login realizado com sucesso!", 'sucesso')
            break
    else:
        exibir_mensagem_inclusiva("Erro: Usuário ou senha inválidos.", 'erro')
        if config_inclusao['leitor_tela']:
            print("[LEITOR DE TELA] Erro no login. Por favor, tente novamente.")

    input("\nPressione Enter para voltar.")

def carregar_configuracoes_usuario(email):
    try:
        with open(ARQUIVO_USUARIOS, 'r', encoding='utf-8') as f:
            usuarios = json.load(f)
        for usuario in usuarios:
            if usuario['email'] == email:
                return usuario.get('config_inclusao', config_inclusao.copy())
    except FileNotFoundError:
        pass
    return config_inclusao.copy()


# Página de cadastro
def validar_senha_forte(senha):
    """Valida se a senha atende aos critérios de segurança"""
    if len(senha) < 8:
        return False, "A senha deve ter pelo menos 8 caracteres"
    
    if not any(c.isupper() for c in senha):
        return False, "A senha deve conter pelo menos 1 letra maiúscula"
    
    if not any(c.islower() for c in senha):
        return False, "A senha deve conter pelo menos 1 letra minúscula"
    
    if not any(c.isdigit() for c in senha):
        return False, "A senha deve conter pelo menos 1 número"
    
    caracteres_especiais = "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?"
    if not any(c in caracteres_especiais for c in senha):
        return False, "A senha deve conter pelo menos 1 caractere especial"
    
    return True, "Senha forte"

def pagina_cadastro():
    limpar_tela()
    cabecalho("CADASTRO INCLUSIVO")

    # Mostra dicas de segurança antes de começar
    mostrar_dicas_seguranca()
    cabecalho("CADASTRO INCLUSIVO")  # Mostra o cabeçalho novamente após limpar

    print(aplicar_estilo_inclusivo("\nCrie sua conta na plataforma mais acessível do Brasil!"))
    if config_inclusao['leitor_tela']:
        print("[LEITOR DE TELA] Por favor, preencha os campos para cadastro:")

    print("\nDados pessoais:")
    nome = input(aplicar_estilo_inclusivo("Nome completo: "))
    
    # Mostra alerta sobre e-mails antes do campo de e-mail
    exibir_mensagem_inclusiva("⚠️ Use um e-mail válido e que você tenha acesso regular", 'aviso')
    time.sleep(2)
    email = input(aplicar_estilo_inclusivo("Email: "))
    
    # Mostra dicas sobre senhas fortes
    exibir_mensagem_inclusiva("💡 Dica: Crie uma senha única para esta plataforma", 'info')
    time.sleep(2)
    
    while True:
        senha = input(aplicar_estilo_inclusivo("Senha (mínimo 8 caracteres, incluindo maiúsculas, minúsculas, números e símbolos): "))
        valido, mensagem = validar_senha_forte(senha)
        
        if valido:
            break
        else:
            exibir_mensagem_inclusiva(f"Senha fraca: {mensagem}", 'erro')
            print(aplicar_estilo_inclusivo("Exemplo de senha forte: Senha@1234"))

    # Mostra alerta sobre informações de acessibilidade
    exibir_mensagem_inclusiva("🔐 Suas informações de acessibilidade são armazenadas com segurança", 'info')
    time.sleep(2)
    
    print(aplicar_estilo_inclusivo("\nInformações de acessibilidade (opcional):"))
    print("1. Necessidades específicas")
    print("2. Preferências de aprendizado")
    print("3. Tecnologias assistivas utilizadas")
    acessibilidade = input(aplicar_estilo_inclusivo("Descreva, se quiser: "))

    # Mensagem de aceitação dos termos com alerta
    print("\n" + aplicar_estilo_inclusivo("Antes de prosseguir, você precisa aceitar os Termos de Uso e a Política de Privacidade."))
    exibir_mensagem_inclusiva("📄 Leia os termos cuidadosamente antes de aceitar", 'aviso')
    time.sleep(2)
    print("Leia com atenção os documentos disponíveis no site oficial ou solicite uma versão acessível.")

    aceite = input(aplicar_estilo_inclusivo("Você aceita os termos de uso e a política de privacidade? (s/n): ")).strip().lower()

    if aceite != 's':
        exibir_mensagem_inclusiva("Cadastro cancelado. É necessário aceitar os termos para criar uma conta.", 'aviso')
        input("\nPressione Enter para voltar.")
        return

    # Mostra mensagem final de segurança
    exibir_mensagem_inclusiva("🔒 Sua conta está sendo criada com medidas de segurança avançadas...", 'info')
    esperar("Criando sua conta EdTech")

    if nome and email and senha:
        usuarios = carregar_usuarios()

        # Verifica se email já está em uso
        if any(u['email'] == email for u in usuarios):
            exibir_mensagem_inclusiva("Erro: Este e-mail já está cadastrado.", 'erro')
        else:
            usuarios.append({
                'nome': nome,
                'email': email,
                'senha': gerar_hash_senha(senha),
                'acessibilidade': acessibilidade,
                'config_inclusao': config_inclusao.copy()
            })
            salvar_usuarios(usuarios)

            exibir_mensagem_inclusiva(f"Bem-vindo(a), {nome}! Cadastro concluído com sucesso.", 'sucesso')
            # Mostra dicas finais de segurança
            exibir_mensagem_inclusiva("💡 Dica: Ative a verificação em duas etapas nas configurações da conta", 'info')
            time.sleep(2)
            
            if acessibilidade:
                exibir_mensagem_inclusiva("Obrigado por compartilhar suas preferências de acessibilidade.", 'info')

            if config_inclusao['leitor_tela']:
                print(f"[LEITOR DE TELA] Cadastro concluído com sucesso. Bem-vindo, {nome}.")
    else:
        exibir_mensagem_inclusiva("Erro: Preencha todos os campos obrigatórios.", 'erro')

    input("\nPressione Enter para voltar.")

def mostrar_dicas_seguranca():
    """Exibe dicas de segurança contra phishing"""
    dicas = [
        "⚠️ ATENÇÃO: Nunca compartilhe sua senha com ninguém!",
        "🔒 Dica: A plataforma nunca pedirá sua senha por e-mail ou telefone",
        "📧 Cuidado com e-mails falsos que imitam nosso serviço",
        "🌐 Sempre verifique se o site é oficial antes de digitar suas credenciais",
        "🛡️ Use autenticação de dois fatores quando disponível",
        "🔍 Verifique sempre o remetente de e-mails suspeitos",
        "🚫 Desconfie de promoções ou ofertas que pareçam boas demais"
    ]
    
    limpar_tela()
    cabecalho("DICAS IMPORTANTES DE SEGURANÇA")
    
    for dica in dicas:
        print(aplicar_estilo_inclusivo(f"\n{dica}"))
        time.sleep(2)  # Mostra cada dica por 2 segundos
    
    print(aplicar_estilo_inclusivo("\nLembre-se: Sua segurança é nossa prioridade!"))
    time.sleep(2)
    limpar_tela()

def explorar_cursos():
    """Exploração de cursos com filtros de acessibilidade"""
    limpar_tela()
    cabecalho("EXPLORAR CURSOS INCLUSIVOS")
    
    print(aplicar_estilo_inclusivo("\nFiltrar por:"))
    print("1. Todos os cursos")
    print("2. Cursos com LIBRAS")
    print("3. Cursos com áudio-descrição")
    print("4. Cursos para dislexia")
    print("5. Cursos iniciantes")
    
    filtro = input(aplicar_estilo_inclusivo("\nEscolha um filtro (ou Enter para todos): "))
    
    cursos_filtrados = []
    
    match filtro:
        case "1" | "":
            cursos_filtrados = cursos.items()
            print(aplicar_estilo_inclusivo("\nTodos os cursos disponíveis:"))
        case "2":
            cursos_filtrados = [(i, c) for i, c in cursos.items() if "matemática" in c['tags'] or "ética" in c['tags']]
            print(aplicar_estilo_inclusivo("\nCursos com LIBRAS disponível:"))
        case "3":
            cursos_filtrados = [(i, c) for i, c in cursos.items() if "física" in c['tags'] or "química" in c['tags']]
            print(aplicar_estilo_inclusivo("\nCursos com áudio-descrição:"))
        case "4":
            cursos_filtrados = [(i, c) for i, c in cursos.items() if c['nivel'] == "Iniciante"]
            print(aplicar_estilo_inclusivo("\nCursos adaptados para dislexia:"))
        case "5":
            cursos_filtrados = [(i, c) for i, c in cursos.items() if c['nivel'] in ["Iniciante", "Todos"]]
            print(aplicar_estilo_inclusivo("\nCursos para iniciantes:"))
        case _:
            exibir_mensagem_inclusiva("Filtro inválido. Mostrando todos os cursos.", 'alerta')
            cursos_filtrados = cursos.items()
    
    for i, dados in cursos_filtrados:
        print(f"\n{i}. {aplicar_estilo_inclusivo(dados['nome'])}")
        print(f"   {dados['descricao']}")
        print(f"   Nível: {dados['nivel']}")
        print(f"   Tags: {', '.join(dados['tags'])}")
    
    escolha = input(aplicar_estilo_inclusivo("\nEscolha um curso para ver detalhes (ou Enter para voltar): "))
    
    if escolha.isdigit() and int(escolha) in cursos:
        curso = cursos[int(escolha)]
        pagina_aula(curso["nome"], curso["link"])
    elif escolha:
        exibir_mensagem_inclusiva("Curso inválido.", 'erro')
        time.sleep(1)

def pagina_aula(nome_curso, link):
    """Página de aula com todos recursos de inclusão"""
    while True:  # Adicionei loop para manter na página até escolher voltar
        limpar_tela()
        cabecalho(f"AULA - {nome_curso.upper()}")
        
        print(aplicar_estilo_inclusivo(f"\nConteúdo da aula de {nome_curso}"))
        
        # Verificar se o curso já foi concluído
        curso_concluido = False
        if usuario_logado and 'cursos_concluidos' in usuario_logado:
            curso_concluido = nome_curso in usuario_logado['cursos_concluidos']
        
        if curso_concluido:
            exibir_mensagem_inclusiva("✅ Você já completou este curso!", 'sucesso')
        
        print("\n" + aplicar_estilo_inclusivo("RECURSOS INCLUSIVOS DISPONÍVEIS:"))
        print("- [✅] Intérprete de LIBRAS" if config_inclusao['libras'] else "- [ ] Intérprete de LIBRAS")
        print("- [✅] Transcrição textual" if True else "- [ ] Transcrição textual")
        print("- [✅] Legendas em português" if True else "- [ ] Legendas")
        print(f"- [{'✅' if config_inclusao['descricao_audio'] else ' '}] Áudio-descrição")
        print(f"- [{'✅' if config_inclusao['dislexia'] else ' '}] Fonte para dislexia")
        
        print(aplicar_estilo_inclusivo("\nFORMAS DE ACESSAR O CONTEÚDO:"))
        print("1. Assistir ao vídeo diretamente")
        print("2. Ler a transcrição (texto completo)")
        print("3. Ouvir o áudio da aula")
        print("4. Baixar material em PDF acessível")
        print("5. Marcar curso como concluído" if not curso_concluido else "5. ✅ Curso já concluído")
        print("\nPressione ENTER para voltar")
        
        escolha = input(aplicar_estilo_inclusivo("\nEscolha uma opção (1-5): ")).strip()
        
        if escolha == "":
            return  # Volta ao menu anterior
            
        if escolha == "5":
            if usuario_logado:
                if not curso_concluido:
                    marcar_curso_concluido(nome_curso)
                    exibir_mensagem_inclusiva(f"Curso {nome_curso} marcado como concluído!", 'sucesso')
                    input("\nPressione Enter para continuar...")
                    continue  # Recarrega a página para mostrar novo status
                else:
                    exibir_mensagem_inclusiva("Este curso já está concluído!", 'info')
                    input("\nPressione Enter para continuar...")
            else:
                exibir_mensagem_inclusiva("Faça login para marcar cursos como concluídos.", 'aviso')
                input("\nPressione Enter para continuar...")
            continue  # Recarrega a página
        
        match escolha:
            case "1":
                print(aplicar_estilo_inclusivo(f"\nAbrindo vídeo aula de {nome_curso}..."))
                webbrowser.open(link)
            case "2":
                print(aplicar_estilo_inclusivo("\nPreparando transcrição acessível..."))
                esperar("Gerando texto adaptado")
                print(aplicar_estilo_inclusivo("\n[TRANSCRIÇÃO DA AULA]"))
                print(f"Aula: {nome_curso}\n")
            case "3":
                print(aplicar_estilo_inclusivo("\nPreparando versão em áudio..."))
                esperar("Convertendo para áudio")
                print(aplicar_estilo_inclusivo("\n[VERSÃO EM ÁUDIO]"))
                webbrowser.open(link.replace("watch?v=", "embed/"))
            case "4":
                print(aplicar_estilo_inclusivo("\nPreparando PDF acessível..."))
                esperar("Gerando documento")
                print(aplicar_estilo_inclusivo("\n[PDF ACESSÍVEL]"))
            case _:
                exibir_mensagem_inclusiva("Opção inválida.", 'erro')
        
        input("\nPressione Enter para continuar...")

def marcar_curso_concluido(nome_curso):
    """Registra um curso como concluído pelo usuário"""
    usuarios = carregar_usuarios()
    
    for usuario in usuarios:
        if usuario['email'] == usuario_logado['email']:
            if 'cursos_concluidos' not in usuario:
                usuario['cursos_concluidos'] = []
            
            if nome_curso not in usuario['cursos_concluidos']:
                usuario['cursos_concluidos'].append(nome_curso)
                usuario_logado['cursos_concluidos'] = usuario['cursos_concluidos']
                salvar_usuarios(usuarios)
            break

def pagina_play():
    """Página de início rápido para aprendizado"""
    limpar_tela()
    cabecalho("COMEÇAR A APRENDER AGORA")
    
    print(aplicar_estilo_inclusivo("\nCaminhos de aprendizagem inclusivos:"))
    
    print("\n1. Rota Rápida - Aprenda o essencial em 7 dias")
    print("   (Conteúdo condensado com foco no fundamental)")
    
    print("\n2. Rota Acessível - Conteúdo com todos recursos inclusivos")
    print("   (LIBRAS, áudio-descrição, texto adaptado)")
    
    print("\n3. Rota Personalizada - Baseado em suas preferências")
    print("   (Usa suas configurações de acessibilidade)")
    
    print("\n4. Rota Tradicional - Conteúdo padrão")
    
    escolha = input(aplicar_estilo_inclusivo("\nEscolha uma rota de aprendizagem (1-4): "))
    
    match escolha:
        case "1":
            print(aplicar_estilo_inclusivo("\nIniciando Rota Rápida..."))
            print("Dia 1: Conceitos básicos")
            print("Dia 2: Fundamentos essenciais")
            print("...")
            print("Dia 7: Revisão e aplicação")
        case "2":
            print(aplicar_estilo_inclusivo("\nIniciando Rota Acessível..."))
            config_inclusao.update({
                'libras': True,
                'descricao_audio': True,
                'leitor_tela': True
            })
            print("Todos os recursos de acessibilidade ativados!")
        case "3":
            print(aplicar_estilo_inclusivo("\nIniciando Rota Personalizada..."))
            print(f"Configurações aplicadas:")
            print(f"- Tamanho fonte: {config_inclusao['tamanho_fonte']}")
            print(f"- LIBRAS: {'Sim' if config_inclusao['libras'] else 'Não'}")
            print(f"- Leitor de tela: {'Sim' if config_inclusao['leitor_tela'] else 'Não'}")
        case "4":
            print(aplicar_estilo_inclusivo("\nIniciando Rota Tradicional..."))
            print("Conteúdo padrão sem adaptações específicas.")
        case _:
            exibir_mensagem_inclusiva("Opção inválida. Iniciando rota personalizada por padrão.", 'alerta')
    
    input("\nPressione Enter para continuar para os cursos.")

def comecar_agora():
    """Página de chamada para ação com inclusão"""
    limpar_tela()
    cabecalho("COMEÇAR AGORA - EDUCAÇÃO INCLUSIVA")
    
    print(aplicar_estilo_inclusivo("\nPor que começar agora?"))
    print("- Acesso imediato a todos os cursos")
    print("- Configurações de acessibilidade salvas")
    print("- Progresso acompanhado de forma inclusiva")
    
    print(aplicar_estilo_inclusivo("\nComo funciona para PCDs:"))
    print("1. Cadastro rápido com informações de acessibilidade")
    print("2. Configuração automática baseada em suas necessidades")
    print("3. Acesso prioritário a suporte especializado")
    
    print(aplicar_estilo_inclusivo("\nBenefícios inclusivos:"))
    print("- Certificado acessível")
    print("- Material didático adaptado")
    print("- Suporte em LIBRAS disponível")
    
    resposta = input(aplicar_estilo_inclusivo("\nQuer criar sua conta agora? (S/N): ")).lower()
    
    if resposta == 's':
        pagina_cadastro()
    else:
        exibir_mensagem_inclusiva("Você pode criar sua conta a qualquer momento pelo menu principal.", 'info')
        input("\nPressione Enter para voltar.")

def quero_fazer_parte():
    """Página de participação com inclusão"""
    limpar_tela()
    cabecalho("FAÇA PARTE DA NOSSA COMUNIDADE INCLUSIVA")
    
    print(aplicar_estilo_inclusivo("\nPara alunos:"))
    print("- Participe de grupos de estudo acessíveis")
    print("- Conecte-se com outros alunos PCDs")
    print("- Ajude a melhorar nossa plataforma")
    
    print(aplicar_estilo_inclusivo("\nPara educadores:"))
    print("- Crie conteúdo acessível")
    print("- Participe de nosso programa de formação")
    print("- Desenvolva materiais inclusivos")
    
    print(aplicar_estilo_inclusivo("\nPara instituições:"))
    print("- Parcerias para inclusão digital")
    print("- Licenças para grupos")
    print("- Cursos customizados")
    
    input("\nPressione Enter para voltar.")

def seja_voluntario():
    """Página de voluntariado com acessibilidade"""
    limpar_tela()
    cabecalho("VOLUNTARIADO INCLUSIVO")
    
    print(aplicar_estilo_inclusivo("\nÁreas de atuação:"))
    print("1. Tradutores para LIBRAS")
    print("2. Revisores de conteúdo acessível")
    print("3. Testadores de acessibilidade")
    print("4. Tutores para alunos com necessidades especiais")
    
    print(aplicar_estilo_inclusivo("\nRequisitos:"))
    print("- Disponibilidade de 4h semanais")
    print("- Compromisso com a inclusão")
    print("- Conhecimento básico em acessibilidade (treinaremos)")
    
    print(aplicar_estilo_inclusivo("\nBenefícios:"))
    print("- Certificado de voluntariado inclusivo")
    print("- Formação em educação acessível")
    print("- Experiência em projetos reais")
    
    resposta = input(aplicar_estilo_inclusivo("\nQuer se candidatar? (S/N): ")).lower()
    
    if resposta == 's':
        print(aplicar_estilo_inclusivo("\nFormulário de candidatura:"))
        nome = input("Seu nome: ")
        email = input("Seu email: ")
        area = input("Área de interesse (1-4): ")
        
        esperar("Enviando candidatura")
        exibir_mensagem_inclusiva(f"Obrigado, {nome}! Sua candidatura foi recebida.", 'sucesso')
        print("Entraremos em contato em até 5 dias úteis.")
    else:
        exibir_mensagem_inclusiva("Você pode se candidatar a qualquer momento.", 'info')
    
    input("\nPressione Enter para voltar.")

def logout():
    """Desloga o usuário da sessão atual"""
    global usuario_logado
    
    if usuario_logado:
        # Registrar dados da sessão
        agora = datetime.now()
        logout_data = {
            'data_hora': agora.strftime("%d/%m/%Y %H:%M"),
            'duracao': 0  # Poderia calcular se tivéssemos registro do horário de login
        }
        
        # Atualizar estatísticas no arquivo
        usuarios = carregar_usuarios()
        for u in usuarios:
            if u['email'] == usuario_logado['email']:
                if 'estatisticas' not in u:
                    u['estatisticas'] = {}
                if 'historico_logout' not in u['estatisticas']:
                    u['estatisticas']['historico_logout'] = []
                u['estatisticas']['historico_logout'].append(logout_data)
                salvar_usuarios(usuarios)
                break
    
    usuario_logado = None
    exibir_mensagem_inclusiva("Logout realizado com sucesso. Retornando ao menu principal...", 'info')
    time.sleep(2)
    
def sair():
    """Opção de sair ou fazer logout"""
    limpar_tela()
    cabecalho("SAIR - PLATAFORMA INCLUSIVA")
    
    print(aplicar_estilo_inclusivo("\nDeseja realizar logout ou apenas encerrar a aplicação?"))
    print("1. Logout e voltar ao menu principal")
    print("2. Encerrar a aplicação")
    
    escolha = input("\nEscolha uma opção (1-2): ")

    if escolha == "1":
        logout()
    elif escolha == "2":
        if usuario_logado:
            # Registrar logout antes de sair
            logout()
        
        limpar_tela()
        cabecalho("ENCERRANDO - PLATAFORMA INCLUSIVA")

        print(aplicar_estilo_inclusivo("\nObrigado por usar nossa plataforma acessível!"))
        print("\nLembre-se, você pode:")
        print("- Retornar a qualquer momento")
        print("- Sugerir melhorias de acessibilidade")
        print("- Compartilhar com quem precisa de recursos inclusivos")

        agora = datetime.now().strftime("%d/%m/%Y %H:%M")
        print(f"\nSessão encerrada em: {agora}")
        
        sys.exit()
    else:
        exibir_mensagem_inclusiva("Opção inválida. Retornando ao menu principal...", 'erro')
        time.sleep(2)

def menu_principal():
    """Menu principal com verificação de acessibilidade"""
    while True:
        limpar_tela()
        
        # Barra de status de acessibilidade
        status = []
        if config_inclusao['modo_alto_contraste']:
            status.append("ALTO CONTRASTE")
        if config_inclusao['leitor_tela']:
            status.append("LEITOR DE TELA")
        if config_inclusao['libras']:
            status.append("LIBRAS")
        if config_inclusao['dislexia']:
            status.append("DISLEXIA")
        
        if status:
            print(aplicar_estilo_inclusivo(" | ".join(status)) + "\n")
        
        cabecalho("PLATAFORMA EDTECH INCLUSIVA - MENU PRINCIPAL")
        
        if usuario_logado:
            print(aplicar_estilo_inclusivo(f"\nSeja bem-vindo(a), {usuario_logado['nome']}!"))
        
        # Opções fixas (1-3)
        print("1. Início")
        print("2. Sobre")
        print("3. Acessibilidade")
        
        # Opções condicionais (não logado - 4-5)
        if not usuario_logado:
            print("4. Entrar / Login")
            print("5. Cadastro")
        
        # Opções principais (numeração condicional)
        opcao = 4 if usuario_logado else 6
        print(f"{opcao}. Explorar Cursos"); opcao += 1
        print(f"{opcao}. Começar a Aprender"); opcao += 1
        print(f"{opcao}. Quero Fazer Parte"); opcao += 1
        print(f"{opcao}. Seja Voluntário"); opcao += 1
        print(f"{opcao}. Configurações de Inclusão"); opcao += 1
        print(f"{opcao}. Perfil"); opcao += 1
        print("13. Sistema")  
        print(f"14. Sair")    
        
        escolha = input(aplicar_estilo_inclusivo("\nEscolha uma opção: "))
        
        # Mapeamento das opções
        opcoes_disponiveis = {
            "1": pagina_inicio,
            "2": pagina_sobre,
            "3": pagina_acessibilidade
        }
        
        if not usuario_logado:
            opcoes_disponiveis.update({
                "4": pagina_login,
                "5": pagina_cadastro
            })
            base = 6
        else:
            base = 4
            
        opcoes_disponiveis.update({
            str(base): explorar_cursos,
            str(base+1): pagina_play,
            str(base+2): quero_fazer_parte,
            str(base+3): seja_voluntario,
            str(base+4): configurar_inclusao,
            str(base+5): mostrar_perfil,
            "13": pagina_sistema,  
            "14": sair             
        })
        
        if escolha in opcoes_disponiveis:
            opcoes_disponiveis[escolha]()
        else:
            exibir_mensagem_inclusiva("Opção inválida. Tente novamente.", 'erro')
            time.sleep(1)
            
def editar_perfil():
    """Permite ao usuário editar suas informações pessoais"""
    limpar_tela()
    cabecalho("EDITAR PERFIL")
    
    if usuario_logado is None:
        exibir_mensagem_inclusiva("Você precisa estar logado para editar o perfil.", 'aviso')
        input("\nPressione Enter para voltar.")
        return
    
    usuarios = carregar_usuarios()
    usuario_atual = None
    
    # Encontra o usuário atual na lista
    for i, usuario in enumerate(usuarios):
        if usuario['email'] == usuario_logado['email']:
            usuario_atual = i
            break
    
    if usuario_atual is None:
        exibir_mensagem_inclusiva("Erro ao carregar perfil.", 'erro')
        input("\nPressione Enter para voltar.")
        return
    
    print(aplicar_estilo_inclusivo("\nInformações atuais:"))
    print(f"1. Nome: {usuario_logado['nome']}")
    print(f"2. Email: {usuario_logado['email']}")
    print("3. Senha: ********")
    
    print(aplicar_estilo_inclusivo("\nO que deseja alterar?"))
    print("1. Nome")
    print("2. Email")
    print("3. Senha")
    print("4. Voltar ao menu do perfil")
    
    escolha = input(aplicar_estilo_inclusivo("\nEscolha uma opção (1-4): "))
    
    if escolha == "1":
        novo_nome = input(aplicar_estilo_inclusivo("Novo nome: ")).strip()
        if novo_nome:
            usuarios[usuario_atual]['nome'] = novo_nome
            usuario_logado['nome'] = novo_nome
            salvar_usuarios(usuarios)
            exibir_mensagem_inclusiva("Nome alterado com sucesso!", 'sucesso')
        else:
            exibir_mensagem_inclusiva("Nome não pode estar vazio.", 'erro')
    
    elif escolha == "2":
        novo_email = input(aplicar_estilo_inclusivo("Novo email: ")).strip()
        if novo_email:
            # Verifica se o novo email já está em uso
            if any(u['email'] == novo_email for u in usuarios if u['email'] != usuario_logado['email']):
                exibir_mensagem_inclusiva("Este e-mail já está em uso.", 'erro')
            else:
                usuarios[usuario_atual]['email'] = novo_email
                usuario_logado['email'] = novo_email
                salvar_usuarios(usuarios)
                exibir_mensagem_inclusiva("Email alterado com sucesso!", 'sucesso')
        else:
            exibir_mensagem_inclusiva("Email não pode estar vazio.", 'erro')
    
    elif escolha == "3":
        senha_atual = input(aplicar_estilo_inclusivo("Senha atual: "))
        if gerar_hash_senha(senha_atual) != usuario_logado['senha']:
            exibir_mensagem_inclusiva("Senha atual incorreta.", 'erro')
        else:
            while True:
                nova_senha = input(aplicar_estilo_inclusivo("Nova senha (mínimo 8 caracteres, incluindo maiúsculas, minúsculas, números e símbolos): "))
                valido, mensagem = validar_senha_forte(nova_senha)
                
                if valido:
                    confirmacao = input(aplicar_estilo_inclusivo("Confirme a nova senha: "))
                    if nova_senha == confirmacao:
                        usuarios[usuario_atual]['senha'] = gerar_hash_senha(nova_senha)
                        usuario_logado['senha'] = gerar_hash_senha(nova_senha)
                        salvar_usuarios(usuarios)
                        exibir_mensagem_inclusiva("Senha alterada com sucesso!", 'sucesso')
                        break
                    else:
                        exibir_mensagem_inclusiva("As senhas não coincidem.", 'erro')
                else:
                    exibir_mensagem_inclusiva(f"Senha fraca: {mensagem}", 'erro')
                    print(aplicar_estilo_inclusivo("Exemplo de senha forte: Senha@1234"))
    
    elif escolha == "4":
        return
    
    else:
        exibir_mensagem_inclusiva("Opção inválida.", 'erro')
    
    input("\nPressione Enter para continuar...")

def mostrar_perfil():
    """Exibe as informações do usuário logado com menu de opções"""
    while True:
        limpar_tela()
        cabecalho("MEU PERFIL")
        
        if usuario_logado is None:
            exibir_mensagem_inclusiva("Você não está logado. Faça login para acessar seu perfil.", 'aviso')
            input("\nPressione Enter para voltar.")
            return
        
        print(aplicar_estilo_inclusivo("\nSelecione o que deseja visualizar:"))
        print("1. Informações do usuário")
        print("2. Configurações de acessibilidade")
        print("3. Estatísticas de uso")
        print("4. Progresso nos cursos")
        print("5. Editar perfil")  # Nova opção adicionada
        print("6. Voltar ao menu principal")
        
        escolha = input(aplicar_estilo_inclusivo("\nEscolha uma opção (1-6): "))
        
        if escolha == "1":
            mostrar_informacoes_usuario()
        elif escolha == "2":
            mostrar_configuracoes_acessibilidade()
        elif escolha == "3":
            mostrar_estatisticas_uso()
        elif escolha == "4":
            mostrar_progresso_cursos()
        elif escolha == "5":
            editar_perfil()  # Chama a nova função de edição
        elif escolha == "6":
            return
        else:
            exibir_mensagem_inclusiva("Opção inválida. Tente novamente.", 'erro')
            time.sleep(1)
            
def mostrar_progresso_cursos():
    """Exibe o progresso do usuário nos cursos"""
    limpar_tela()
    cabecalho("PROGRESSO NOS CURSOS")
    
    if 'cursos_concluidos' not in usuario_logado or not usuario_logado['cursos_concluidos']:
        print("\nNenhum curso concluído ainda.")
        input("\nPressione Enter para voltar ao menu do perfil.")
        return
    
    total_cursos = len(cursos)
    concluidos = len(usuario_logado['cursos_concluidos'])
    progresso = (concluidos / total_cursos) * 100
    
    print("\nSeu progresso:")
    print(f"Cursos concluídos: {concluidos}/{total_cursos}")
    print(f"Progresso geral: {progresso:.1f}%")
    
    # Barra de progresso visual
    barra = "[" + "■" * int(progresso/5) + " " * (20 - int(progresso/5)) + "]"
    print(barra)
    
    print("\nCursos completados:")
    for i, curso in enumerate(usuario_logado['cursos_concluidos'], 1):
        print(f"{i}. {curso}")
    
    input("\nPressione Enter para voltar ao menu do perfil.")

def mostrar_estatisticas_uso():
    """Exibe as estatísticas de uso da plataforma"""
    limpar_tela()
    cabecalho("ESTATÍSTICAS DE USO")
    
    if 'estatisticas' not in usuario_logado:
        print("\nNenhum dado estatístico disponível.")
        input("\nPressione Enter para voltar ao menu do perfil.")
        return
    
    estat = usuario_logado['estatisticas']
    
    print("\nResumo de uso:")
    print(f"Primeiro login: {estat.get('primeiro_login', 'Não registrado')}")
    print(f"Último login: {estat.get('ultimo_login', 'Não registrado')}")
    print(f"Total de sessões: {estat.get('total_sessoes', 0)}")
    
    if 'historico_logout' in estat and estat['historico_logout']:
        print("\nÚltimos logouts:")
        for i, logout in enumerate(reversed(estat['historico_logout'][-5:]), 1):
            print(f"{i}. {logout['data_hora']}")
    else:
        print("\nNenhum registro de logout encontrado.")
    
    input("\nPressione Enter para voltar ao menu do perfil.")
    
def mostrar_informacoes_usuario():
    """Exibe as informações básicas do usuário"""
    limpar_tela()
    cabecalho("INFORMAÇÕES DO USUÁRIO")
    
    print(aplicar_estilo_inclusivo("\nDados cadastrais:"))
    print(f"Nome: {usuario_logado['nome']}")
    print(f"E-mail: {usuario_logado['email']}")
    
    input("\nPressione Enter para voltar ao menu do perfil.")

def mostrar_configuracoes_acessibilidade():
    """Exibe as configurações de acessibilidade ativas"""
    limpar_tela()
    cabecalho("CONFIGURAÇÕES DE ACESSIBILIDADE")
    
    print("\nConfigurações ativas:")
    configs_ativas = [k for k, v in usuario_logado.get('config_inclusao', {}).items() if v]
    
    if configs_ativas:
        for config in configs_ativas:
            print(f"- {config.replace('_', ' ').title()}")
    else:
        print("Nenhuma configuração especial ativada")
    
    input("\nPressione Enter para voltar ao menu do perfil.")

def mostrar_estatisticas_uso():
    """Exibe as estatísticas de uso da plataforma"""
    limpar_tela()
    cabecalho("ESTATÍSTICAS DE USO")
    
    if 'estatisticas' not in usuario_logado:
        print("\nNenhum dado estatístico disponível.")
        input("\nPressione Enter para voltar ao menu do perfil.")
        return
    
    estat = usuario_logado['estatisticas']
    
    print("\nResumo de uso:")
    print(f"Primeiro login: {estat.get('primeiro_login', 'Não registrado')}")
    print(f"Último login: {estat.get('ultimo_login', 'Não registrado')}")
    print(f"Total de sessões: {estat.get('total_sessoes', 0)}")
    
    # Mostrar progresso nos cursos
    if 'cursos_concluidos' in usuario_logado:
        total_cursos = len(cursos)  # Assumindo que 'cursos' é um dicionário com todos os cursos
        concluidos = len(usuario_logado['cursos_concluidos'])
        progresso = (concluidos / total_cursos) * 100
        
        print("\nProgresso nos cursos:")
        print(f"Cursos concluídos: {concluidos}/{total_cursos}")
        print(f"Progresso: {progresso:.1f}%")
        
        # Barra de progresso visual
        barra = "[" + "■" * int(progresso/5) + " " * (20 - int(progresso/5)) + "]"
        print(barra)
        
        if concluidos > 0:
            print("\nCursos completados:")
            for i, curso in enumerate(usuario_logado['cursos_concluidos'], 1):
                print(f"{i}. {curso}")
    else:
        print("\nProgresso nos cursos: Nenhum curso concluído ainda")
    
    if 'historico_logout' in estat and estat['historico_logout']:
        print("\nÚltimos logouts:")
        for i, logout in enumerate(reversed(estat['historico_logout'][-5:]), 1):
            print(f"{i}. {logout['data_hora']}")
    else:
        print("\nNenhum registro de logout encontrado.")
    
    input("\nPressione Enter para voltar ao menu do perfil.")
    
def obter_info_sistema():
    """Obtém informações detalhadas do sistema"""
    sistema = platform.system()
    arquitetura = platform.architecture()[0]
    compativel = False
    ram_gb = 0
    
    # Obter memória RAM (funciona no Windows e Linux)
    try:
        if sistema == "Windows":
            import psutil
            ram = psutil.virtual_memory().total / (1024**3)  # Em GB
            ram_info = f"{ram:.1f} GB RAM"
            ram_gb = ram
        elif sistema == "Linux":
            with open('/proc/meminfo') as f:
                mem = f.readline()
            ram_kb = int(mem.split()[1])
            ram = ram_kb / (1024**2)  # Em GB
            ram_info = f"{ram:.1f} GB RAM"
            ram_gb = ram
        else:
            ram_info = "Informação de RAM não disponível"
    except:
        ram_info = "Informação de RAM não disponível"
    
    # Verificar compatibilidade (mínimo 2GB RAM)
    compativel = ram_gb >= 2 if ram_gb > 0 else False
    
    return sistema, arquitetura, ram_info, compativel, ram_gb

def obter_info_energia():
    """Obtém informações sobre o estado de energia do sistema"""
    try:
        sistema = platform.system()
        
        if sistema == "Windows":
            import psutil
            bateria = psutil.sensors_battery()
            if bateria:
                return {
                    'plugada': bateria.power_plugged,
                    'porcentagem': bateria.percent,
                    'modo_energia': "Alto desempenho" if bateria.power_plugged else "Economia de energia"
                }
        
        elif sistema == "Linux":
            # Tentativa de ler informações de bateria no Linux
            try:
                with open('/sys/class/power_supply/BAT0/status') as f:
                    status = f.read().strip()
                with open('/sys/class/power_supply/BAT0/capacity') as f:
                    porcentagem = int(f.read().strip())
                
                return {
                    'plugada': status == "Charging",
                    'porcentagem': porcentagem,
                    'modo_energia': "Alto desempenho" if status == "Charging" else "Economia de energia"
                }
            except FileNotFoundError:
                pass
        
        return None
    except:
        return None

def configurar_economia_energia(ativar):
    """Ativa ou desativa o modo de economia de energia"""
    sistema = platform.system()
    try:
        if sistema == "Windows":
            import ctypes
            # Constantes do Windows para configuração de energia
            GUID_VIDEO_SUBGROUP = "7516b95f-f776-4464-8c53-06167f40cc99"
            GUID_VIDEO_POWERDOWN_TIMEOUT = "3c0bc021-c8a8-4e07-a973-6b14cbcb2b7e"
            
            if ativar:
                # Configurações para economia de energia
                print("Ativando modo de economia de energia...")
                # (Aqui você implementaria as mudanças reais)
            else:
                # Configurações para alto desempenho
                print("Desativando modo de economia de energia...")
                # (Aqui você implementaria as mudanças reais)
            
            return True
        
        elif sistema == "Linux":
            if ativar:
                print("Ativando modo de economia de energia...")
                # Comandos para ativar economia de energia no Linux
                # os.system("sudo cpufreq-set -g powersave")
            else:
                print("Desativando modo de economia de energia...")
                # Comandos para desativar economia de energia no Linux
                # os.system("sudo cpufreq-set -g performance")
            
            return True
        
        return False
    except:
        return False

def pagina_sistema():
    """Exibe informações detalhadas do sistema"""
    while True:
        limpar_tela()
        cabecalho("INFORMAÇÕES DO SISTEMA")
        
        sistema, arquitetura, ram_info, compativel, ram_gb = obter_info_sistema()
        info_energia = obter_info_energia()
        
        print(aplicar_estilo_inclusivo("\nDetalhes do sistema operacional:"))
        print(f"Sistema: {sistema}")
        print(f"Arquitetura: {arquitetura}")
        print(f"Memória: {ram_info}")
        
        # Mensagem de compatibilidade
        if ram_gb > 0:
            status = "COMPATÍVEL" if compativel else "NÃO COMPATÍVEL"
            cor = 'sucesso' if compativel else 'erro'
            exibir_mensagem_inclusiva(f"\nStatus do sistema: {status} (Mínimo 2GB RAM requeridos)", cor)
        else:
            exibir_mensagem_inclusiva("\nNão foi possível verificar a compatibilidade do sistema", 'aviso')
        
        # Informações de energia
        print(aplicar_estilo_inclusivo("\nConfigurações de Energia:"))
        if info_energia:
            print(f"Estado: {'Conectado' if info_energia['plugada'] else 'Bateria'}")
            print(f"Nível de bateria: {info_energia['porcentagem']}%")
            print(f"Modo atual: {info_energia['modo_energia']}")
        else:
            print("Informações de energia não disponíveis")
        
        # Opções de economia de energia
        print(aplicar_estilo_inclusivo("\nOpções de economia de energia:"))
        print("1. Ativar modo economia de energia")
        print("2. Desativar modo economia de energia")
        print("3. Voltar ao menu principal")
        
        escolha = input(aplicar_estilo_inclusivo("\nEscolha uma opção (1-3): "))
        
        if escolha == "1":
            if configurar_economia_energia(True):
                exibir_mensagem_inclusiva("Modo de economia de energia ativado", 'sucesso')
            else:
                exibir_mensagem_inclusiva("Não foi possível ativar o modo de economia", 'erro')
            input("\nPressione Enter para continuar...")
        elif escolha == "2":
            if configurar_economia_energia(False):
                exibir_mensagem_inclusiva("Modo de economia de energia desativado", 'sucesso')
            else:
                exibir_mensagem_inclusiva("Não foi possível desativar o modo de economia", 'erro')
            input("\nPressione Enter para continuar...")
        elif escolha == "3":
            return
        else:
            exibir_mensagem_inclusiva("Opção inválida", 'erro')
            time.sleep(1)
            
if __name__ == "__main__":
    # Mensagem inicial de acessibilidade
    print(aplicar_estilo_inclusivo("\nIniciando Plataforma Edtech Inclusiva..."))
    
    # Verificação do sistema operacional e compatibilidade
    sistema, arquitetura, ram_info, compativel, ram_gb = obter_info_sistema()
    
    if sistema == "Windows":
        mensagem_sistema = "Windows - Recursos de acessibilidade nativos disponíveis."
    elif sistema == "Linux":
        mensagem_sistema = "Linux - Algumas ferramentas podem requerer configuração adicional."
    else:
        mensagem_sistema = "Sistema não identificado - Alguns recursos podem não funcionar corretamente."
    
    print(f"Sistema operacional: {sistema}")
    print(aplicar_estilo_inclusivo(mensagem_sistema))
    print(f"Memória RAM detectada: {ram_info}")
    
    # Mensagem de compatibilidade inicial
    if ram_gb > 0:
        if compativel:
            exibir_mensagem_inclusiva("✅ Sistema compatível com a plataforma (2GB RAM ou mais)", 'sucesso')
        else:
            exibir_mensagem_inclusiva("⚠️ Sistema pode ter desempenho limitado (Recomendado 2GB RAM ou mais)", 'aviso')
    else:
        exibir_mensagem_inclusiva("⚠️ Não foi possível verificar a memória RAM do sistema", 'aviso')
    
    print("\nCarregando recursos de acessibilidade")
    esperar()
    
    # Inicia com leitor de tela se configurado
    if config_inclusao['leitor_tela']:
        print("[LEITOR DE TELA] Plataforma carregada. Bem-vindo ao menu principal.")
    
    menu_principal()