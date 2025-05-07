# Templates para geração de frases informais sobre pagamentos
# Baseados em comunicações típicas via WhatsApp no Brasil

templates = {
    "PAGAMENTO": [
        "to querendo pagar {valor} {forma_pagamento}",
        "vou pagar {valor} {tempo}",
        "{condição} consigo pagar {valor}",
        "blz vou pagar {valor}",
        "quero quitar {valor} {forma_pagamento}",
        "vo te pagar {tempo} {valor} pode ser?",
        "consegui juntar {valor} pra pagar {tempo}",
        "to com {valor} pra te pagar",
        "da pra pagar {valor} hj?",
        "csg pagar {valor} {tempo}",
        "to pensando em pagar {valor}"
    ],
    "VALOR": [
        "são {valor} tá?",
        "o valor é {valor}",
        "to com {valor} só",
        "consegui juntar {valor}",
        "tenho {valor} agora",
        "ta {valor} no total",
        "o preço ficou {valor}",
        "ta saindo a {valor}",
        "fechou em {valor}"
    ],
    "TEMPO": [
        "quero pagar {tempo}",
        "{tempo} eu te pago",
        "consigo pagar {tempo}",
        "vou passar {tempo} pode ser?",
        "deixa q {tempo} resolvo",
        "me espera ate {tempo}",
        "pago {tempo} ctz",
        "{tempo} cai na sua conta"
    ],
    "CONDIÇÃO": [
        "{condição} consigo pagar {valor}",
        "{condição} te pago na hora",
        "{condição} pago td",
        "só consigo pagar {condição}",
        "vou pagar {condição} {valor}",
        "{condição} mando {valor}"
    ],
    "FORMA_PAGAMENTO": [
        "vou pagar no {forma_pagamento}",
        "te pago via {forma_pagamento}",
        "posso pagar de {forma_pagamento}?",
        "to pensando em pagar no {forma_pagamento}",
        "só consigo de {forma_pagamento}",
        "tem como pagar de {forma_pagamento}?",
        "aceita {forma_pagamento}?"
    ]
}

# Banco de variações para preenchimento dos templates
variacoes = {
    "valor": [
        "500 pila", "500 conto", "quinhentos", "500 reais", "meio k", "500", 
        "1000", "mil conto", "1k", "mil reais", "um milão", "1 mil",
        "pila", "dinheiro", "grana", "200", "duzentos", "100 reais", 
        "cinquentinha", "50 conto", "700 paus", "trezentos", "350"
    ],
    "tempo": [
        "amanhã", "amanha", "hj", "hoje", "agr", "agora", "dps", "depois",
        "na semana q vem", "semana q vem", "mes q vem", "no final do mes",
        "qnd cair meu salario", "dia 5", "sexta", "final de semana",
        "segunda", "qdo eu receber", "assim q cair o dinheiro", "ate dia 10",
        "qnd entrar meu pagamento", "qnd eu tiver a grana", "amanha cedinho"
    ],
    "forma_pagamento": [
        "pix", "transferência", "nubank", "picpay", "cartão", "cartao", 
        "credito", "debito", "boleto", "dinheiro", "especie", "mercado pago",
        "ted", "transferencia", "app", "aplicativo", "caixa tem", "iti",
        "12x", "parcelado", "a vista", "avista", "parcelado em 2x", "cc",
        "conta corrente"
    ],
    "condição": [
        "se eu receber", "se tiver", "qnd entrar dinheiro", "se me pagarem",
        "se rolar pagamento", "se der certo", "se conseguir", "caso eu pegue",
        "se eu puder", "se eu vender", "se eu conseguir emprestado",
        "se meu salario cair", "caso eu consiga", "se meu chefe pagar",
        "se eu tiver a grana", "se n ficar apertado"
    ]
}