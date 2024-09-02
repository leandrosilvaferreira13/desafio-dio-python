import textwrap

def menu():
    menu = """\n
    ====================================
    BEM-VINDO AO SISTEMA DE BANCO DIGITAL
    ====================================
    Por favor, escolha uma das opções abaixo:
    
    [d]  Depósito - Adicionar dinheiro à sua conta
    [s]  Saque - Retirar dinheiro da sua conta
    [e]  Extrato - Ver todas as transações da sua conta
    [nc] Nova conta - Criar uma nova conta bancária
    [lc] Listar contas - Exibir todas as contas cadastradas
    [nu] Novo usuário - Cadastrar um novo usuário no sistema
    [q]  Sair - Encerrar o programa
    
    Digite a opção desejada: """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito realizado: R$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! Seu novo saldo é de R$ {:.2f} ===".format(saldo))
    else:
        print("\n@@@ Operação falhou! O valor do depósito deve ser positivo. Tente novamente. @@@")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Saldo insuficiente para realizar o saque. @@@")

    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite permitido de R$ {:.2f}. @@@".format(limite))

    elif excedeu_saques:
        print("\n@@@ Operação falhou! Você atingiu o limite máximo de {} saques diários. @@@".format(limite_saques))

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque realizado: R$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque de R$ {:.2f} realizado com sucesso! Seu novo saldo é de R$ {:.2f} ===".format(valor, saldo))

    else:
        print("\n@@@ Operação falhou! O valor do saque deve ser positivo. Tente novamente. @@@")

    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO DA CONTA ================")
    if not extrato:
        print("Nenhuma movimentação foi realizada na conta até o momento.")
    else:
        print(extrato)
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    print("==================================================")
    print("\n=== Extrato exibido com sucesso! ===")

def criar_usuario(usuarios):
    cpf = input("Por favor, informe o CPF (apenas números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe um usuário cadastrado com este CPF. @@@")
        return

    nome = input("Informe o nome completo do usuário: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço completo (logradouro, número - bairro - cidade/UF): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("\n=== Novo usuário cadastrado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário para associar à nova conta: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! Detalhes da conta abaixo: ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado. Certifique-se de que o CPF está correto ou cadastre um novo usuário. @@@")
    return None

def listar_contas(contas):
    if not contas:
        print("\n@@@ Nenhuma conta encontrada! Cadastre uma nova conta para visualizar aqui. @@@")
    else:
        print("\n=============== LISTA DE CONTAS CADASTRADAS ===============")
        for conta in contas:
            linha = f"""\
                Agência:\t{conta['agencia']}
                Número da Conta:\t{conta['numero_conta']}
                Titular:\t{conta['usuario']['nome']}
            """
            print("=" * 50)
            print(textwrap.dedent(linha))
        print("\n=== Todas as contas foram listadas com sucesso! ===")

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Digite o valor que deseja depositar: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Digite o valor que deseja sacar: "))
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
            else:
                print("\n@@@ Erro ao criar a conta. Por favor, verifique as informações e tente novamente. @@@")

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("\n=== Obrigado por utilizar nosso sistema bancário digital! Até logo! ===")
            break

        else:
            print("\n@@@ Opção inválida! Por favor, selecione uma opção válida do menu. @@@")

main()
