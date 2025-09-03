# FARMTECH SOLUTIONS - APP

culturas = []
area = []                      # área em m²
area_ha = []                   # área em hectares
insumo_adubo = []              # nome do adubo mineral
insumo_defensivo = []          # nome do defensivo químico
insumo_adubo_quantidade = []   # dose de adubo (kg/ha) escolhida para o registro
insumo_defensivo_quantidade = []  # TOTAL de defensivo aplicado (L) neste registro (dose_ha * área_ha)
ruas = []                      # nº de ruas calculadas
planta_ruas = []               # nº de plantas por rua
plantas_total = []             # total de plantas (ruas * plantas_por_rua)


import os

HA_EM_M2 = 10000

# Espaçamentos por cultura: (entre ruas, entre plantas), em metros
espacamentos = {
    "açaí": (6, 6),
    "cupuaçu": (7, 7),
    "mandioca": (1, 1),
    "banana": (3, 2),
    "guaraná": (5, 5)
}

culturas_disponiveis = ['açaí', 'cupuaçu', 'mandioca', 'guaraná', 'banana']
adubos_disponiveis   = ['npk', 'calcário', 'potássio']
defensivos_disponiveis = ['fungicida', 'inseticida', 'nematicida']


# ---------- Utilitários ----------
def ler_opcao(msg, opcoes_validas):
    """Loop até o usuário digitar uma opção válida (strings minúsculas)."""
    while True:
        v = input(msg).strip().lower()
        if v in opcoes_validas:
            return v
        print(f"Entrada inválida. Opções: {opcoes_validas}")

def ler_float_pos(msg):
    """Lê um float > 0, com validação."""
    while True:
        try:
            v = float(input(msg).strip().replace(",", "."))
            if v > 0:
                return v
            print("Digite um número maior que zero.")
        except ValueError:
            print("Valor inválido. Tente novamente.")

def ler_indice_valido(tam):
    """Lê um índice de 0..tam-1 com validação."""
    while True:
        s = input(f"Informe o índice (0 a {tam-1}): ").strip()
        if s.isdigit():
            i = int(s)
            if 0 <= i < tam:
                return i
        print("Índice inválido.")

# ---------- Cálculos ----------
def calcular_area(lado_frontal_m, lado_lateral_m):
    """Retorna (area_m2, area_ha)."""
    a_m2 = lado_frontal_m * lado_lateral_m
    a_ha = a_m2 / HA_EM_M2
    return a_m2, a_ha

def calcular_ruas_plantas(cultura, lado_frontal_m, lado_lateral_m):
    """Usa o dicionário 'espacamentos' para calcular ruas, plantas/rua e total."""
    esp_rua, esp_planta = espacamentos[cultura]  # metros
    qtd_ruas = int(lado_frontal_m // esp_rua)
    qtd_plantas_rua = int(lado_lateral_m // esp_planta)
    total_plantas = qtd_ruas * qtd_plantas_rua
    return qtd_ruas, qtd_plantas_rua, total_plantas


# ---------- CRUD ----------
def inserir_registro():
    print("\n=== INSERIR REGISTRO ===")

    cultura = ler_opcao(
        "Escolha a cultura (açaí, cupuaçu, mandioca, guaraná, banana): ",
        culturas_disponiveis
    )

    # Área (m² e ha)
    lado_frontal = ler_float_pos("Informe a medida frontal (em metros): ")
    lado_lateral = ler_float_pos("Informe a medida lateral (em metros): ")
    a_m2, a_ha = calcular_area(lado_frontal, lado_lateral)

    # Ruas e plantas
    qtd_ruas, qtd_plantas_rua, total_plantas = calcular_ruas_plantas(
        cultura, lado_frontal, lado_lateral
    )

    # Insumos (adubo e defensivo)
    print("\nDefina o adubo mineral e o defensivo químico.")
    adubo = ler_opcao("Adubo (npk, calcário, potássio): ", adubos_disponiveis)
    # Padrão pedagógico: kg/ha
    adubo_qtd_ha = ler_float_pos("Quantidade de adubo (kg/ha) para essa área: ")

    defensivo = ler_opcao("Defensivo (fungicida, inseticida, nematicida): ", defensivos_disponiveis)
    # Padrão pedagógico: L/ha (ex.: fungicida 300 L/ha)
    defensivo_dose_ha = ler_float_pos("Dose do defensivo (L/ha) para essa cultura: ")
    defensivo_total_L = defensivo_dose_ha * a_ha  # total aplicado na área

    # Empilhar nos vetores (alinhados)
    culturas.append(cultura)
    area.append(a_m2)
    area_ha.append(a_ha)

    insumo_adubo.append(adubo)
    insumo_adubo_quantidade.append(adubo_qtd_ha)  # guardando dose em kg/ha

    insumo_defensivo.append(defensivo)
    insumo_defensivo_quantidade.append(defensivo_total_L)  # total L aplicado

    ruas.append(qtd_ruas)
    planta_ruas.append(qtd_plantas_rua)
    plantas_total.append(total_plantas)

    # Feedback
    print("\nRegistro inserido com sucesso!")
    print(f"Área: {a_m2:.2f} m² ({a_ha:.4f} ha)")
    print(f"Ruas: {qtd_ruas} | Plantas/rua: {qtd_plantas_rua} | Total plantas: {total_plantas}")
    print(f"Adubo: {adubo} | Dose: {adubo_qtd_ha} kg/ha")
    print(f"Defensivo: {defensivo} | Total aplicado: {defensivo_total_L:.2f} L\n")


def listar_registros():
    print("\n=== LISTAR REGISTROS ===")
    if len(culturas) == 0:
        print("Não há registros.\n")
        return

    for i in range(len(culturas)):
        print("-" * 50)
        print(f"Índice: {i}")
        print(f"Cultura: {culturas[i]}")
        print(f"Área: {area[i]:.2f} m² | {area_ha[i]:.4f} ha")
        print(f"Ruas: {ruas[i]} | Plantas/rua: {planta_ruas[i]} | Total plantas: {plantas_total[i]}")
        print(f"Adubo: {insumo_adubo[i]} | Dose: {insumo_adubo_quantidade[i]} kg/ha")
        print(f"Defensivo: {insumo_defensivo[i]} | Total aplicado: {insumo_defensivo_quantidade[i]:.2f} L")
    print("-" * 50 + "\n")


def atualizar_registro():
    print("\n=== ATUALIZAR REGISTRO ===")
    if len(culturas) == 0:
        print("Não há registros para atualizar.\n")
        return

    listar_registros()
    i = ler_indice_valido(len(culturas))

    print("\nO que deseja atualizar?")
    print("1 - Cultura")
    print("2 - Medidas do terreno (recalcula área/ruas/plantas e defensivo total)")
    print("3 - Adubo e dose (kg/ha)")
    print("4 - Defensivo e dose (L/ha)  [recalcula total aplicado]")
    print("5 - Cancelar")
    op = input("Escolha: ").strip()

    if op == "1":
        nova_cultura = ler_opcao("Nova cultura: ", culturas_disponiveis)
        culturas[i] = nova_cultura
        # Recalcular ruas/plantas com mesma geometria? Precisa das medidas originais.
        # Como não salvamos lado_frontal/lateral, vamos recalcular com base nas RUAS/PLANTAS atuais NÃO é possível.
        # Solução simples: perguntar novamente as medidas (garante consistência).
        print("Para recalcular ruas/plantas, informe novamente as medidas do terreno.")
        lado_frontal = ler_float_pos("Medida frontal (m): ")
        lado_lateral = ler_float_pos("Medida lateral (m): ")
        a_m2, a_ha = calcular_area(lado_frontal, lado_lateral)
        area[i] = a_m2
        area_ha[i] = a_ha
        qtd_ruas, qtd_plantas_rua, total_plant = calcular_ruas_plantas(nova_cultura, lado_frontal, lado_lateral)
        ruas[i] = qtd_ruas
        planta_ruas[i] = qtd_plantas_rua
        plantas_total[i] = total_plant
        # Como o total de defensivo depende de ha, precisamos da dose L/ha novamente:
        dose_ha = ler_float_pos("Dose de defensivo (L/ha) para recalcular total: ")
        insumo_defensivo_quantidade[i] = dose_ha * a_ha
        print("Registro atualizado.\n")

    elif op == "2":
        # Atualiza medidas → recalcula área, ruas/plantas e defensivo total
        lado_frontal = ler_float_pos("Nova medida frontal (m): ")
        lado_lateral = ler_float_pos("Nova medida lateral (m): ")
        a_m2, a_ha = calcular_area(lado_frontal, lado_lateral)
        area[i] = a_m2
        area_ha[i] = a_ha
        qtd_ruas, qtd_plantas_rua, total_plant = calcular_ruas_plantas(culturas[i], lado_frontal, lado_lateral)
        ruas[i] = qtd_ruas
        planta_ruas[i] = qtd_plantas_rua
        plantas_total[i] = total_plant
        # Para recalcular o total de defensivo, precisamos da dose L/ha atual (pergunte):
        dose_ha = ler_float_pos("Informe novamente a dose do defensivo (L/ha) para recalcular total: ")
        insumo_defensivo_quantidade[i] = dose_ha * a_ha
        print("Medidas e cálculos atualizados.\n")

    elif op == "3":
        novo_adubo = ler_opcao("Novo adubo (npk, calcário, potássio): ", adubos_disponiveis)
        nova_dose = ler_float_pos("Nova dose de adubo (kg/ha): ")
        insumo_adubo[i] = novo_adubo
        insumo_adubo_quantidade[i] = nova_dose
        print("Adubo atualizado.\n")

    elif op == "4":
        novo_def = ler_opcao("Novo defensivo (fungicida, inseticida, nematicida): ", defensivos_disponiveis)
        nova_dose_ha = ler_float_pos("Nova dose (L/ha): ")
        insumo_defensivo[i] = novo_def
        insumo_defensivo_quantidade[i] = nova_dose_ha * area_ha[i]
        print("Defensivo atualizado.\n")

    else:
        print("Cancelado.\n")


def deletar_registro():
    print("\n=== DELETAR REGISTRO ===")
    if len(culturas) == 0:
        print("Não há registros para deletar.\n")
        return

    listar_registros()
    i = ler_indice_valido(len(culturas))

    # Remover a MESMA posição em todos os vetores
    culturas.pop(i)
    area.pop(i)
    area_ha.pop(i)
    insumo_adubo.pop(i)
    insumo_adubo_quantidade.pop(i)
    insumo_defensivo.pop(i)
    insumo_defensivo_quantidade.pop(i)
    ruas.pop(i)
    planta_ruas.pop(i)
    plantas_total.pop(i)

    print("Registro deletado com sucesso.\n")


def exportar_csv():
    print("\n=== EXPORTAR CSV ===")
    if len(culturas) == 0:
        print("Não há dados para exportar.\n")
        return

    os.makedirs("data", exist_ok=True)
    caminho = os.path.join("data", "farmtech_dados.csv")

    with open(caminho, "w", encoding="utf-8") as f:
        f.write("cultura,area_m2,area_ha,adubo,adubo_kg_ha,defensivo,defensivo_total_L,ruas,plantas_por_rua,plantas_total\n")
        for i in range(len(culturas)):
            linha = [
                culturas[i],
                f"{area[i]:.2f}",
                f"{area_ha[i]:.4f}",
                insumo_adubo[i],
                str(insumo_adubo_quantidade[i]),
                insumo_defensivo[i],
                f"{insumo_defensivo_quantidade[i]:.2f}",
                str(ruas[i]),
                str(planta_ruas[i]),
                str(plantas_total[i]),
            ]
            f.write(",".join(linha) + "\n")

    print(f"CSV exportado para: {os.path.abspath(caminho)}\n")



# ---------- Menu ----------
def menu():
    while True:
        print("==== FARMTECH ====")
        print("1 - Inserir dados")
        print("2 - Listar dados")
        print("3 - Atualizar dados")
        print("4 - Deletar dados")
        print("5 - Exportar CSV (para usar no R)")
        print("6 - Sair")
        op = input("Escolha: ").strip()

        if op == "1":
            inserir_registro()
        elif op == "2":
            listar_registros()
        elif op == "3":
            atualizar_registro()
        elif op == "4":
            deletar_registro()
        elif op == "5":
            exportar_csv()
        elif op == "6":
            print("Encerrando... Até logo!")
            break
        else:
            print("Opção inválida.\n")


# ---------- Execução ----------
if __name__ == "__main__":
    menu()

Guaraná
Medida frontal (m): 80
Medida lateral (m): 60
Área: 4800 m² → 0,4800 ha
Espaçamento: 5 × 5 m
Ruas: 80 // 5 = 16
Plantas por rua: 60 // 5 = 12
Total plantas: 192
Adubo: Calcário
Dose adubo: 160 kg/ha
Defensivo: Fungicida
Dose defensivo: 300 L/ha → Total aplicado = 300 × 0,48 = 144 L