import random
import re
from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime, timedelta

# Classes base
class Orientacao(Enum):
    POSITIVA = "positiva"
    NEGATIVA = "negativa" 

class Modalidade(Enum):
    CONDICIONAL = "condicional"
    AFIRMADO = "afirmado"
    PLANEJADO = "planejado"
    NEGADO = "negado"
    INCERTO = "incerto"

class ReferenciatTemporal(Enum):
    PASSADO = "passado"
    PRESENTE = "presente"
    FUTURO = "futuro"

class TipoEntidade(Enum):
    VALOR = "VALOR"
    TEMPO = "TEMPO"
    CONDICAO = "CONDICAO"
    PAGAMENTO = "PAGAMENTO"

@dataclass
class Entidade:
    texto: str
    tipo: TipoEntidade
    orientacao: Orientacao
    modalidade: Modalidade
    referencia_temporal: ReferenciatTemporal
    start: int = 0
    end: int = 0

class GeradorFrases:
    def __init__(self):
        # Templates com atributos EXPLÍCITOS - MUITO EXPANDIDOS
        self.templates = {
            "AFIRMATIVO_POSITIVO": [
                # Frases básicas CONSIGO - positivas
                ("<PAGAMENTO>consigo</PAGAMENTO> <VALOR>{valor}</VALOR>", "positiva", "afirmado"),
                ("eu <PAGAMENTO>consigo</PAGAMENTO> <VALOR>{valor}</VALOR>", "positiva", "afirmado"),
                ("<PAGAMENTO>consigo</PAGAMENTO> <VALOR>{valor}</VALOR> <TEMPO>{tempo}</TEMPO>", "positiva", "afirmado"),
                ("eu <PAGAMENTO>consigo</PAGAMENTO> <VALOR>{valor}</VALOR> <TEMPO>{tempo}</TEMPO>", "positiva", "afirmado"),
                
                # Frases básicas POSSO - positivas
                ("<PAGAMENTO>posso</PAGAMENTO> <VALOR>{valor}</VALOR>", "positiva", "afirmado"),
                ("eu <PAGAMENTO>posso</PAGAMENTO> <VALOR>{valor}</VALOR>", "positiva", "afirmado"),
                ("<PAGAMENTO>posso</PAGAMENTO> <VALOR>{valor}</VALOR> <TEMPO>{tempo}</TEMPO>", "positiva", "afirmado"),
                ("<PAGAMENTO>posso</PAGAMENTO> fazer <VALOR>{valor}</VALOR>", "positiva", "afirmado"),
                
                # Frases básicas TENHO - positivas
                ("<PAGAMENTO>tenho</PAGAMENTO> <VALOR>{valor}</VALOR>", "positiva", "afirmado"),
                ("eu <PAGAMENTO>tenho</PAGAMENTO> <VALOR>{valor}</VALOR>", "positiva", "afirmado"),
                ("<PAGAMENTO>tenho</PAGAMENTO> <VALOR>{valor}</VALOR> guardado", "positiva", "afirmado"),
                ("<PAGAMENTO>tenho</PAGAMENTO> <VALOR>{valor}</VALOR> <TEMPO>{tempo}</TEMPO>", "positiva", "afirmado"),
                
                # Frases básicas DÁ - positivas
                ("<PAGAMENTO>dá</PAGAMENTO> pra <VALOR>{valor}</VALOR>", "positiva", "afirmado"),
                ("<PAGAMENTO>dá</PAGAMENTO> <VALOR>{valor}</VALOR>", "positiva", "afirmado"),
                ("<PAGAMENTO>dá</PAGAMENTO> pra fazer <VALOR>{valor}</VALOR>", "positiva", "afirmado"),
                ("<PAGAMENTO>dá</PAGAMENTO> <VALOR>{valor}</VALOR> <TEMPO>{tempo}</TEMPO>", "positiva", "afirmado"),
                
                # Pagamentos diretos
                ("<PAGAMENTO>pago</PAGAMENTO> <VALOR>{valor}</VALOR>", "positiva", "afirmado"),
                ("eu <PAGAMENTO>pago</PAGAMENTO> <VALOR>{valor}</VALOR>", "positiva", "afirmado"),
                ("<PAGAMENTO>pago</PAGAMENTO> <VALOR>{valor}</VALOR> <TEMPO>{tempo}</TEMPO>", "positiva", "afirmado"),
                ("<PAGAMENTO>faço</PAGAMENTO> <VALOR>{valor}</VALOR>", "positiva", "afirmado"),
                ("<PAGAMENTO>aceito</PAGAMENTO> <VALOR>{valor}</VALOR>", "positiva", "afirmado"),
                ("<PAGAMENTO>banco</PAGAMENTO> <VALOR>{valor}</VALOR>", "positiva", "afirmado"),
                ("<PAGAMENTO>mando</PAGAMENTO> <VALOR>{valor}</VALOR>", "positiva", "afirmado"),
                ("<PAGAMENTO>transfiro</PAGAMENTO> <VALOR>{valor}</VALOR>", "positiva", "afirmado"),
                ("<PAGAMENTO>quito</PAGAMENTO> <VALOR>{valor}</VALOR>", "positiva", "afirmado"),
                
                # Futuras/planejadas
                ("vou <PAGAMENTO>pagar</PAGAMENTO> <VALOR>{valor}</VALOR>", "positiva", "planejado"),
                ("vou <PAGAMENTO>conseguir</PAGAMENTO> <VALOR>{valor}</VALOR>", "positiva", "planejado"),
                ("vou <PAGAMENTO>mandar</PAGAMENTO> <VALOR>{valor}</VALOR> <TEMPO>{tempo}</TEMPO>", "positiva", "planejado"),
                ("vou <PAGAMENTO>quitar</PAGAMENTO> <VALOR>{valor}</VALOR> <TEMPO>{tempo}</TEMPO>", "positiva", "planejado"),
                
                # Com condições
                ("<PAGAMENTO>aceito</PAGAMENTO> <VALOR>{valor}</VALOR> <CONDICAO>{condicao}</CONDICAO>", "positiva", "afirmado"),
                ("<PAGAMENTO>faço</PAGAMENTO> <VALOR>{valor}</VALOR> <CONDICAO>{condicao}</CONDICAO>", "positiva", "afirmado"),
                ("no <CONDICAO>pix</CONDICAO> eu <PAGAMENTO>consigo</PAGAMENTO> <VALOR>{valor}</VALOR>", "positiva", "afirmado"),
                
                # Expressões coloquiais positivas
                ("<PAGAMENTO>rola</PAGAMENTO> <VALOR>{valor}</VALOR>", "positiva", "afirmado"),
                ("<PAGAMENTO>beleza</PAGAMENTO> <VALOR>{valor}</VALOR>", "positiva", "afirmado"),
                ("tá <PAGAMENTO>bom</PAGAMENTO> <VALOR>{valor}</VALOR>", "positiva", "afirmado"),
                ("<PAGAMENTO>fechado</PAGAMENTO> <VALOR>{valor}</VALOR>", "positiva", "afirmado"),
            ],
            
            "NEGATIVO": [
                # Frases básicas NÃO CONSIGO - negativas
                ("não <PAGAMENTO>consigo</PAGAMENTO> <VALOR>{valor}</VALOR>", "negativa", "negado"),
                ("eu não <PAGAMENTO>consigo</PAGAMENTO> <VALOR>{valor}</VALOR>", "negativa", "negado"),
                ("não <PAGAMENTO>consigo</PAGAMENTO> <VALOR>{valor}</VALOR> <TEMPO>{tempo}</TEMPO>", "negativa", "negado"),
                ("eu não <PAGAMENTO>consigo</PAGAMENTO> <VALOR>{valor}</VALOR> <TEMPO>{tempo}</TEMPO>", "negativa", "negado"),
                ("não <PAGAMENTO>consigo</PAGAMENTO> <VALOR>{valor}</VALOR> <TEMPO>esse mês</TEMPO>", "negativa", "negado"),
                
                # Frases básicas NÃO POSSO - negativas  
                ("não <PAGAMENTO>posso</PAGAMENTO> <VALOR>{valor}</VALOR>", "negativa", "negado"),
                ("eu não <PAGAMENTO>posso</PAGAMENTO> <VALOR>{valor}</VALOR>", "negativa", "negado"),
                ("não <PAGAMENTO>posso</PAGAMENTO> <VALOR>{valor}</VALOR> <TEMPO>{tempo}</TEMPO>", "negativa", "negado"),
                ("não <PAGAMENTO>posso</PAGAMENTO> fazer <VALOR>{valor}</VALOR>", "negativa", "negado"),
                
                # Frases básicas NÃO TENHO - negativas
                ("não <PAGAMENTO>tenho</PAGAMENTO> <VALOR>{valor}</VALOR>", "negativa", "negado"), 
                ("eu não <PAGAMENTO>tenho</PAGAMENTO> <VALOR>{valor}</VALOR>", "negativa", "negado"),
                ("não <PAGAMENTO>tenho</PAGAMENTO> nem <VALOR>{valor}</VALOR>", "negativa", "negado"),
                ("não <PAGAMENTO>tenho</PAGAMENTO> <VALOR>{valor}</VALOR> <TEMPO>{tempo}</TEMPO>", "negativa", "negado"),
                ("não <PAGAMENTO>tenho</PAGAMENTO> <VALOR>{valor}</VALOR> <TEMPO>esse mês</TEMPO>", "negativa", "negado"),
                ("não <PAGAMENTO>tenho</PAGAMENTO> <VALOR>{valor}</VALOR> <TEMPO>neste momento</TEMPO>", "negativa", "negado"),
                
                # Frases básicas NÃO DÁ - negativas
                ("não <PAGAMENTO>dá</PAGAMENTO> <VALOR>{valor}</VALOR>", "negativa", "negado"),
                ("não <PAGAMENTO>dá</PAGAMENTO> pra <VALOR>{valor}</VALOR>", "negativa", "negado"),
                ("não <PAGAMENTO>dá</PAGAMENTO> <VALOR>{valor}</VALOR> <TEMPO>{tempo}</TEMPO>", "negativa", "negado"),
                ("não <PAGAMENTO>dá</PAGAMENTO> pra <VALOR>{valor}</VALOR> <TEMPO>{tempo}</TEMPO>", "negativa", "negado"),
                ("não <PAGAMENTO>dá</PAGAMENTO> pra fazer <VALOR>{valor}</VALOR>", "negativa", "negado"),
                
                # Frases básicas NÃO ROLA - negativas
                ("não <PAGAMENTO>rola</PAGAMENTO> <VALOR>{valor}</VALOR>", "negativa", "negado"),
                ("não <PAGAMENTO>rola</PAGAMENTO> <PAGAMENTO>pagar</PAGAMENTO> <VALOR>{valor}</VALOR>", "negativa", "negado"),
                ("não <PAGAMENTO>rola</PAGAMENTO> <VALOR>{valor}</VALOR> <TEMPO>{tempo}</TEMPO>", "negativa", "negado"),
                
                # Negações de outros verbos
                ("não <PAGAMENTO>aceito</PAGAMENTO> <VALOR>{valor}</VALOR>", "negativa", "negado"),
                ("não <PAGAMENTO>faço</PAGAMENTO> por <VALOR>{valor}</VALOR>", "negativa", "negado"),
                ("não <PAGAMENTO>pago</PAGAMENTO> <VALOR>{valor}</VALOR>", "negativa", "negado"),
                
                # Expressões de impossibilidade
                ("impossível <PAGAMENTO>pagar</PAGAMENTO> <VALOR>{valor}</VALOR>", "negativa", "negado"),
                ("impossível <PAGAMENTO>bancar</PAGAMENTO> <VALOR>{valor}</VALOR>", "negativa", "negado"),
                ("sem condição de <PAGAMENTO>pagar</PAGAMENTO> <VALOR>{valor}</VALOR>", "negativa", "negado"),
                ("zero condição de <PAGAMENTO>arcar</PAGAMENTO> com <VALOR>{valor}</VALOR>", "negativa", "negado"),
                ("nem <PAGAMENTO>sonhando</PAGAMENTO> com <VALOR>{valor}</VALOR>", "negativa", "negado"),
                ("não tem como <PAGAMENTO>pagar</PAGAMENTO> <VALOR>{valor}</VALOR>", "negativa", "negado"),
                
                # Expressões de dificuldade financeira
                ("tô <CONDICAO>sem grana</CONDICAO> pra <VALOR>{valor}</VALOR>", "negativa", "negado"),
                ("tô <CONDICAO>duro</CONDICAO> <TEMPO>{tempo}</TEMPO>", "negativa", "negado"),
                ("tô <CONDICAO>quebrado</CONDICAO>", "negativa", "negado"),
                ("tô <CONDICAO>apertado</CONDICAO> <TEMPO>{tempo}</TEMPO>", "negativa", "negado"),
                ("sem <CONDICAO>grana</CONDICAO> pra <VALOR>{valor}</VALOR>", "negativa", "negado"),
                
                # Expressões sobre preços altos
                ("<VALOR>{valor}</VALOR> tá muito <CONDICAO>caro</CONDICAO>", "negativa", "negado"),
                ("<VALOR>{valor}</VALOR> tá <CONDICAO>salgado</CONDICAO> demais", "negativa", "negado"),
                ("<VALOR>{valor}</VALOR> tá fora da <CONDICAO>realidade</CONDICAO>", "negativa", "negado"),
                ("<VALOR>{valor}</VALOR> é muito <CONDICAO>puxado</CONDICAO>", "negativa", "negado"),
                ("<VALOR>{valor}</VALOR> tá <CONDICAO>pesado demais</CONDICAO>", "negativa", "negado"),
                ("<VALOR>{valor}</VALOR> tá <CONDICAO>impossível</CONDICAO>", "negativa", "negado"),
            ],
            
            "CONDICIONAL": [
                # Condicionais com SE
                ("se <CONDICAO>{condicao}</CONDICAO> eu <PAGAMENTO>pago</PAGAMENTO>", "positiva", "condicional"),
                ("se <CONDICAO>{condicao}</CONDICAO> eu <PAGAMENTO>consigo</PAGAMENTO>", "positiva", "condicional"),
                ("se <CONDICAO>{condicao}</CONDICAO> eu <PAGAMENTO>fecho</PAGAMENTO>", "positiva", "condicional"),
                ("se <CONDICAO>{condicao}</CONDICAO> eu <PAGAMENTO>aceito</PAGAMENTO>", "positiva", "condicional"),
                ("se der <CONDICAO>{condicao}</CONDICAO> eu <PAGAMENTO>aceito</PAGAMENTO>", "positiva", "condicional"),
                ("se der <CONDICAO>{condicao}</CONDICAO> eu <PAGAMENTO>pago</PAGAMENTO>", "positiva", "condicional"),
                ("se for <CONDICAO>{condicao}</CONDICAO> eu <PAGAMENTO>consigo</PAGAMENTO>", "positiva", "condicional"),
                ("se baixar pra <VALOR>{valor}</VALOR> eu <PAGAMENTO>levo</PAGAMENTO>", "positiva", "condicional"),
                ("se fizer <VALOR>{valor}</VALOR> eu <PAGAMENTO>pago</PAGAMENTO>", "positiva", "condicional"),
                
                # Condicionais com QUANDO
                ("quando <CONDICAO>receber</CONDICAO> <PAGAMENTO>mando</PAGAMENTO> <VALOR>{valor}</VALOR>", "positiva", "condicional"),
                ("quando <CONDICAO>cair na conta</CONDICAO> <PAGAMENTO>transfiro</PAGAMENTO> <VALOR>{valor}</VALOR>", "positiva", "condicional"),
                ("quando <CONDICAO>entrar dinheiro</CONDICAO> <PAGAMENTO>quito</PAGAMENTO> <VALOR>{valor}</VALOR>", "positiva", "condicional"),
                ("quando <CONDICAO>resolver uns problemas</CONDICAO> <PAGAMENTO>acerto</PAGAMENTO>", "positiva", "condicional"),
                ("quando <CONDICAO>aparecer um freela</CONDICAO> <PAGAMENTO>pago</PAGAMENTO> <VALOR>{valor}</VALOR>", "positiva", "condicional"),
                
                # Condicionais com COM
                ("com <CONDICAO>{condicao}</CONDICAO> eu <PAGAMENTO>fecho</PAGAMENTO>", "positiva", "condicional"),
                ("com <CONDICAO>{condicao}</CONDICAO> eu <PAGAMENTO>consigo</PAGAMENTO>", "positiva", "condicional"),
                ("com <CONDICAO>desconto</CONDICAO> eu <PAGAMENTO>aceito</PAGAMENTO>", "positiva", "condicional"),
                ("com <CONDICAO>prazo</CONDICAO> <PAGAMENTO>pago</PAGAMENTO> <VALOR>{valor}</VALOR>", "positiva", "condicional"),
            ],
            
            "NEGOCIACAO": [
                # Perguntas diretas - sempre positivas (tentativa)
                ("<PAGAMENTO>aceita</PAGAMENTO> <VALOR>{valor}</VALOR>?", "positiva", "condicional"),
                ("consegue fazer <VALOR>{valor}</VALOR>?", "positiva", "condicional"),
                ("dá pra fazer <VALOR>{valor}</VALOR>?", "positiva", "condicional"),
                ("<PAGAMENTO>rola</PAGAMENTO> <VALOR>{valor}</VALOR>?", "positiva", "condicional"),
                ("e <VALOR>{valor}</VALOR>?", "positiva", "condicional"),
                ("que tal <VALOR>{valor}</VALOR>?", "positiva", "condicional"),
                ("e <VALOR>{valor}</VALOR> <CONDICAO>{condicao}</CONDICAO>?", "positiva", "condicional"),
                
                # Propostas condicionais
                ("se fechar <VALOR>{valor}</VALOR> eu <PAGAMENTO>levo</PAGAMENTO> hoje", "positiva", "condicional"),
                ("por <VALOR>{valor}</VALOR> eu <PAGAMENTO>fecho</PAGAMENTO>", "positiva", "condicional"),
                ("se der <VALOR>{valor}</VALOR> <CONDICAO>{condicao}</CONDICAO> eu <PAGAMENTO>aceito</PAGAMENTO>", "positiva", "condicional"),
                ("última proposta: <VALOR>{valor}</VALOR>", "positiva", "condicional"),
                ("minha melhor oferta: <VALOR>{valor}</VALOR>", "positiva", "condicional"),
            ],
            
            "DUPLA_ORIENTACAO": [
                # Padrão NÃO CONSIGO hoje MAS amanhã SIM
                ("não <PAGAMENTO>consigo</PAGAMENTO> <TEMPO>hoje</TEMPO> mas <TEMPO>amanhã</TEMPO> <PAGAMENTO>pago</PAGAMENTO>",
                 {"consigo": "negativa", "hoje": "negativa", "amanhã": "positiva", "pago": "positiva"},
                 {"consigo": "negado", "hoje": "negado", "amanhã": "afirmado", "pago": "afirmado"}),
                
                ("não <PAGAMENTO>consigo</PAGAMENTO> <VALOR>{valor}</VALOR> <TEMPO>essa semana</TEMPO> mas <TEMPO>semana que vem</TEMPO> <PAGAMENTO>acerto</PAGAMENTO>",
                 {"consigo": "negativa", "valor": "negativa", "essa semana": "negativa", "semana que vem": "positiva", "acerto": "positiva"},
                 {"consigo": "negado", "valor": "negado", "essa semana": "negado", "semana que vem": "afirmado", "acerto": "afirmado"}),
                
                ("não <PAGAMENTO>consigo</PAGAMENTO> <VALOR>{valor}</VALOR> <TEMPO>esse mês</TEMPO> mas <TEMPO>mês que vem</TEMPO> <PAGAMENTO>pago</PAGAMENTO>",
                 {"consigo": "negativa", "valor": "negativa", "esse mês": "negativa", "mês que vem": "positiva", "pago": "positiva"},
                 {"consigo": "negado", "valor": "negado", "esse mês": "negado", "mês que vem": "afirmado", "pago": "afirmado"}),
                
                # Padrão NÃO TENHO agora MAS depois SIM
                ("não tenho <VALOR>{valor}</VALOR> <TEMPO>hoje</TEMPO> mas <TEMPO>amanhã</TEMPO> <PAGAMENTO>mando</PAGAMENTO>",
                 {"valor": "negativa", "hoje": "negativa", "amanhã": "positiva", "mando": "positiva"},
                 {"valor": "negado", "hoje": "negado", "amanhã": "afirmado", "mando": "afirmado"}),
                
                ("não tenho <VALOR>{valor}</VALOR> <TEMPO>esse mês</TEMPO> mas <TEMPO>mês que vem</TEMPO> <PAGAMENTO>acerto</PAGAMENTO>",
                 {"valor": "negativa", "esse mês": "negativa", "mês que vem": "positiva", "acerto": "positiva"},
                 {"valor": "negado", "esse mês": "negado", "mês que vem": "afirmado", "acerto": "afirmado"}),
                
                ("não tenho <VALOR>{valor}</VALOR> <TEMPO>agora</TEMPO> mas <TEMPO>{tempo}</TEMPO> <PAGAMENTO>transfiro</PAGAMENTO>",
                 {"valor": "negativa", "agora": "negativa", "tempo": "positiva", "transfiro": "positiva"},
                 {"valor": "negado", "agora": "negado", "tempo": "afirmado", "transfiro": "afirmado"}),
                
                # Padrão VALOR agora NÃO DÁ mas depois SIM
                ("<VALOR>{valor}</VALOR> <TEMPO>agora</TEMPO> não <PAGAMENTO>dá</PAGAMENTO> mas <TEMPO>{tempo}</TEMPO> <PAGAMENTO>resolvo</PAGAMENTO>",
                 {"valor": "negativa", "agora": "negativa", "dá": "negativa", "tempo": "positiva", "resolvo": "positiva"},
                 {"valor": "negado", "agora": "negado", "dá": "negado", "tempo": "afirmado", "resolvo": "afirmado"}),
                
                ("<VALOR>{valor}</VALOR> <TEMPO>hoje</TEMPO> não <PAGAMENTO>rola</PAGAMENTO> mas <TEMPO>{tempo}</TEMPO> <PAGAMENTO>quito</PAGAMENTO>",
                 {"valor": "negativa", "hoje": "negativa", "rola": "negativa", "tempo": "positiva", "quito": "positiva"},
                 {"valor": "negado", "hoje": "negado", "rola": "negado", "tempo": "afirmado", "quito": "afirmado"}),
                
                ("<VALOR>{valor}</VALOR> <TEMPO>já</TEMPO> não <PAGAMENTO>dá</PAGAMENTO> mas <TEMPO>na sexta</TEMPO> <PAGAMENTO>acerto</PAGAMENTO>",
                 {"valor": "negativa", "já": "negativa", "dá": "negativa", "na sexta": "positiva", "acerto": "positiva"},
                 {"valor": "negado", "já": "negado", "dá": "negado", "na sexta": "afirmado", "acerto": "afirmado"}),
                
                # Padrão IMPOSSÍVEL hoje MAS possível depois
                ("impossível <PAGAMENTO>pagar</PAGAMENTO> <VALOR>{valor}</VALOR> <TEMPO>hoje</TEMPO> mas <TEMPO>{tempo}</TEMPO> <PAGAMENTO>quito</PAGAMENTO>",
                 {"pagar": "negativa", "valor": "negativa", "hoje": "negativa", "tempo": "positiva", "quito": "positiva"},
                 {"pagar": "negado", "valor": "negado", "hoje": "negado", "tempo": "afirmado", "quito": "afirmado"}),
                
                ("sem condição <TEMPO>hoje</TEMPO> mas <TEMPO>{tempo}</TEMPO> <PAGAMENTO>deposito</PAGAMENTO> <VALOR>{valor}</VALOR>",
                 {"hoje": "negativa", "tempo": "positiva", "deposito": "positiva", "valor": "positiva"},
                 {"hoje": "negado", "tempo": "afirmado", "deposito": "afirmado", "valor": "afirmado"}),
                
                # Padrão situação atual DIFÍCIL MAS futura BOA
                ("tô <CONDICAO>duro</CONDICAO> <TEMPO>essa semana</TEMPO> mas <TEMPO>quando receber</TEMPO> <PAGAMENTO>mando</PAGAMENTO> <VALOR>{valor}</VALOR>",
                 {"duro": "negativa", "essa semana": "negativa", "quando receber": "positiva", "mando": "positiva", "valor": "positiva"},
                 {"duro": "negado", "essa semana": "negado", "quando receber": "afirmado", "mando": "afirmado", "valor": "afirmado"}),
                
                ("tô <CONDICAO>sem grana</CONDICAO> <TEMPO>hoje</TEMPO> mas <TEMPO>{tempo}</TEMPO> <PAGAMENTO>consigo</PAGAMENTO> <VALOR>{valor}</VALOR>",
                 {"sem grana": "negativa", "hoje": "negativa", "tempo": "positiva", "consigo": "positiva", "valor": "positiva"},
                 {"sem grana": "negado", "hoje": "negado", "tempo": "afirmado", "consigo": "afirmado", "valor": "afirmado"}),
                
                ("<TEMPO>hoje</TEMPO> não <PAGAMENTO>posso</PAGAMENTO> mas <TEMPO>amanhã</TEMPO> <PAGAMENTO>transfiro</PAGAMENTO> <VALOR>{valor}</VALOR>",
                 {"hoje": "negativa", "posso": "negativa", "amanhã": "positiva", "transfiro": "positiva", "valor": "positiva"},
                 {"hoje": "negado", "posso": "negado", "amanhã": "afirmado", "transfiro": "afirmado", "valor": "afirmado"}),
            ]
        }

    def gerar_valor(self):
        """Gerador de valores ENRIQUECIDO com múltiplas faixas e formatos"""
        # Define diferentes faixas de valores baseadas em contexto real
        faixa = random.choice([
            "pequeno",   # 50-300   (35%)
            "medio",     # 300-800  (30%) 
            "alto",      # 800-2000 (25%)
            "muito_alto" # 2000-5000 (10%)
        ])
        
        if faixa == "pequeno":
            valor = random.randint(50, 300)
            # 40% das vezes faz valores "redondos" pequenos
            if random.random() < 0.4:
                valor = random.choice([50, 80, 100, 120, 150, 200, 250, 300])
        elif faixa == "medio":
            valor = random.randint(300, 800)
            # 35% das vezes faz valores "redondos" médios
            if random.random() < 0.35:
                valor = random.choice([300, 350, 400, 450, 500, 600, 700, 800])
        elif faixa == "alto":
            valor = random.randint(800, 2000)
            # 30% das vezes faz valores "redondos" altos
            if random.random() < 0.3:
                valor = (valor // 100) * 100  # Arredonda para centenas
        else:  # muito_alto
            valor = random.randint(2000, 5000)
            # 25% das vezes faz valores "redondos" muito altos
            if random.random() < 0.25:
                valor = (valor // 500) * 500  # Arredonda para múltiplos de 500
        
        # Formatos mais diversificados e realistas
        formatos = [
            f"R$ {valor}",                      # R$ 150
            f"R$ {valor},00",                   # R$ 150,00  
            f"{valor} reais",                   # 150 reais
            f"{valor} real" if valor == 1 else f"{valor} reais",  # Singular/plural
            f"{valor}",                         # 150
            f"R${valor}",                       # R$150 (sem espaço)
            f"{valor} pila" if valor < 500 else f"R$ {valor}",     # Gíria para valores baixos
            f"{valor} mangos" if valor < 300 else f"R$ {valor}",   # Gíria alternativa
            f"{valor} conto" if valor >= 1000 else f"R$ {valor}",  # "Conto" para milhares
            f"uns {valor} reais" if valor < 1000 else f"R$ {valor}",  # "Uns X reais"
            f"{valor} pratas" if valor < 800 else f"R$ {valor}",   # Gíria "pratas"
        ]
        
        # Para valores muito baixos, adiciona formatos especiais
        if valor <= 100:
            formatos.extend([
                f"{valor} tempão" if valor < 80 else f"R$ {valor}",  # Gíria regional
                f"{valor} pau" if valor < 50 else f"R$ {valor}",     # Gíria muito coloquial
            ])
        
        return random.choice(formatos)
    
    def gerar_tempo(self):
        """Gerador de tempos ROBUSTO com múltiplas categorias"""
        # Categorias de tempo com pesos diferentes
        categoria = random.choices([
            "imediato",      # 25% - hoje, agora, já
            "proximo",       # 35% - amanhã, semana que vem
            "medio_prazo",   # 25% - mês que vem, daqui X dias  
            "longo_prazo",   # 10% - ano que vem, quando der
            "especifico"     # 5%  - datas específicas
        ], weights=[25, 35, 25, 10, 5])[0]
        
        if categoria == "imediato":
            return random.choice([
                "hoje", "agora", "já", "neste momento", "na hora",
                "rapidinho", "aqui agora", "de imediato", "urgente",
                "essa hora", "nesse instante", "sem demora"
            ])
        
        elif categoria == "proximo":
            return random.choice([
                "amanhã", "semana que vem", "próxima semana", "essa semana",
                "final de semana", "segunda que vem", "na sexta",
                "semana que vem", "daqui uns dias", "em breve",
                "logo logo", "logo", "brevemente", "quinta que vem",
                "final da semana", "início da semana", "terça que vem"
            ])
        
        elif categoria == "medio_prazo":
            opcoes_medio = [
                "mês que vem", "final do mês", "início do mês",
                "no outro mês", "daqui um mês", "mês seguinte",
                "quando receber", "depois do pagamento", "próximo mês"
            ]
            
            # 30% das vezes gera prazos específicos
            if random.random() < 0.3:
                dias = random.randint(3, 30)
                opcoes_medio.extend([
                    f"daqui {dias} dias",
                    f"em {dias} dias", 
                    f"depois de {dias} dias"
                ])
            
            return random.choice(opcoes_medio)
        
        elif categoria == "longo_prazo":
            return random.choice([
                "ano que vem", "ano seguinte", "quando der",
                "quando for possível", "no futuro", "mais pra frente",
                "quando melhorar", "quando aparecer", "futuramente",
                "quando tiver", "daqui uns meses", "quando resolver"
            ])
        
        else:  # especifico
            hoje = datetime.now()
            dias_futuro = random.randint(1, 45)
            data_futura = hoje + timedelta(days=dias_futuro)
            
            return random.choice([
                f"dia {data_futura.day}",
                f"no dia {data_futura.day}",
                f"até dia {data_futura.day}",
                f"dia {data_futura.day}/{data_futura.month:02d}",
                f"lá pro dia {data_futura.day}",
                f"por volta do dia {data_futura.day}"
            ])
    
    def gerar_condicao(self):
        """Gerador de condições ENRIQUECIDO com múltiplas categorias"""
        # Categorias de condições com pesos diferentes
        categoria = random.choices([
            "pagamento",     # 40% - pix, cartão, dinheiro
            "parcelamento",  # 25% - 2x, 3x, sem juros
            "desconto",      # 20% - descontos diversos
            "entrada",       # 10% - entradas e sinais
            "situacional"    # 5%  - condições específicas
        ], weights=[40, 25, 20, 10, 5])[0]
        
        if categoria == "pagamento":
            return random.choice([
                "no pix", "no cartão", "em dinheiro", "à vista",
                "transferência", "depósito", "pelo pix", "cartão de crédito",
                "cartão de débito", "dinheiro vivo", "cash", "via pix",
                "no débito", "no crédito", "transferência bancária",
                "ted", "doc", "pelo app", "pagamento digital"
            ])
        
        elif categoria == "parcelamento":
            # 70% usa parcelas fixas, 30% gera dinâmicas
            if random.random() < 0.7:
                return random.choice([
                    "parcelado", "em 2x", "em 3x", "em 4x", "em 5x", "em 6x",
                    "2x sem juros", "3x sem juros", "4x sem juros", "6x sem juros",
                    "10x sem juros", "12x sem juros", "parcelado sem juros",
                    "dividido", "em vezes", "sem juros", "juros zero"
                ])
            else:
                x_vezes = random.randint(2, 24)
                if x_vezes <= 6:
                    sem_juros = random.choice(["", " sem juros"])
                else:
                    sem_juros = ""  # Parcelas altas normalmente têm juros
                
                return random.choice([
                    f"em {x_vezes}x{sem_juros}",
                    f"em {x_vezes} vezes{sem_juros}",
                    f"parcelado em {x_vezes}x{sem_juros}",
                    f"{x_vezes}x{sem_juros}",
                    f"dividido em {x_vezes}x{sem_juros}"
                ])
        
        elif categoria == "desconto":
            # 60% usa descontos fixos, 40% gera dinâmicos
            if random.random() < 0.6:
                return random.choice([
                    "com desconto", "desconto à vista", "preço especial",
                    "promoção", "oferta", "desconto de amigo", "preço camarada",
                    "desconto bom", "preço diferenciado", "condição especial",
                    "preço melhor", "desconto razoável", "um desconto maneiro"
                ])
            else:
                percentual = random.choice([5, 10, 15, 20, 25, 30, 40, 50])
                valor_desc = random.randint(20, 200)
                return random.choice([
                    f"{percentual}% de desconto",
                    f"com {percentual}% off",
                    f"desconto de {percentual}%",
                    f"R$ {valor_desc} de desconto",
                    f"menos R$ {valor_desc}",
                    f"abatimento de R$ {valor_desc}"
                ])
        
        elif categoria == "entrada":
            # 50% usa entradas percentuais, 50% valores fixos
            if random.random() < 0.5:
                percentual = random.choice([20, 30, 40, 50, 60])
                return random.choice([
                    f"{percentual}% de entrada",
                    f"entrada de {percentual}%",
                    f"{percentual}% na hora",
                    f"sinal de {percentual}%"
                ])
            else:
                valor_entrada = random.choice([50, 100, 150, 200, 250, 300, 500])
                return random.choice([
                    f"entrada de R$ {valor_entrada}",
                    f"sinal de R$ {valor_entrada}",
                    f"R$ {valor_entrada} de entrada",
                    f"R$ {valor_entrada} na hora",
                    "sem entrada",
                    "entrada zero",
                    "sem sinal"
                ])
        
        else:  # situacional
            return random.choice([
                "se for hoje", "fechando agora", "condição especial",
                "só pra você", "preço de amigo", "condição diferenciada",
                "negócio fechado", "última oportunidade", "oferta única",
                "condição imperdível", "só desta vez", "preço final",
                "condição de ouro", "negócio da china", "preço bacana",
                "oferta especial", "condição única"
            ])

    def gerar_frase(self) -> Tuple[str, List[Entidade]]:
        """Gera frase com atributos explícitos"""
        # Escolhe categoria aleatória
        categoria = random.choice(list(self.templates.keys()))
        template_info = random.choice(self.templates[categoria])
        
        if categoria == "DUPLA_ORIENTACAO":
            # Tratamento especial para dupla orientação
            template, orientacoes_map, modalidades_map = template_info
            frase_com_marcacao = self._substituir_placeholders(template)
            frase_limpa, entidades = self._extrair_entidades_especiais(frase_com_marcacao, orientacoes_map, modalidades_map)
        else:
            # Tratamento normal
            template, orientacao_padrao, modalidade_padrao = template_info
            frase_com_marcacao = self._substituir_placeholders(template)
            frase_limpa, entidades = self._extrair_entidades_normais(frase_com_marcacao, orientacao_padrao, modalidade_padrao)
        
        return frase_limpa, entidades

    def _substituir_placeholders(self, template: str) -> str:
        """Substitui placeholders"""
        frase = template
        
        while "{valor}" in frase:
            frase = frase.replace("{valor}", self.gerar_valor(), 1)
        while "{tempo}" in frase:
            frase = frase.replace("{tempo}", self.gerar_tempo(), 1)
        while "{condicao}" in frase:
            frase = frase.replace("{condicao}", self.gerar_condicao(), 1)
            
        return frase

    def _extrair_entidades_normais(self, frase_marcada: str, orientacao_padrao: str, modalidade_padrao: str) -> Tuple[str, List[Entidade]]:
        """Extrai entidades com atributos fixos"""
        entidades = []
        frase_limpa = frase_marcada
        
        pattern = r'<(\w+)>(.*?)</\w+>'
        matches = list(re.finditer(pattern, frase_marcada))
        
        offset = 0
        for match in matches:
            tag = match.group(1).upper()
            texto = match.group(2)
            start_original = match.start()
            
            frase_limpa = frase_limpa.replace(match.group(0), texto, 1)
            start_ajustado = start_original - offset
            end_ajustado = start_ajustado + len(texto)
            offset += len(match.group(0)) - len(texto)
            
            if tag in ["VALOR", "TEMPO", "CONDICAO", "PAGAMENTO"]:
                tipo = TipoEntidade(tag)
                orientacao = Orientacao(orientacao_padrao)
                modalidade = Modalidade(modalidade_padrao)
                ref_temporal = self._determinar_referencia_temporal(texto)
                
                entidade = Entidade(
                    texto=texto, tipo=tipo, orientacao=orientacao,
                    modalidade=modalidade, referencia_temporal=ref_temporal,
                    start=start_ajustado, end=end_ajustado
                )
                entidades.append(entidade)
        
        return frase_limpa, entidades

    def _extrair_entidades_especiais(self, frase_marcada: str, orientacoes_map: dict, modalidades_map: dict) -> Tuple[str, List[Entidade]]:
        """Extrai entidades com mapeamento específico para dupla orientação"""
        entidades = []
        frase_limpa = frase_marcada
        
        pattern = r'<(\w+)>(.*?)</\w+>'
        matches = list(re.finditer(pattern, frase_marcada))
        
        offset = 0
        for match in matches:
            tag = match.group(1).upper()
            texto = match.group(2)
            start_original = match.start()
            
            frase_limpa = frase_limpa.replace(match.group(0), texto, 1)
            start_ajustado = start_original - offset
            end_ajustado = start_ajustado + len(texto)
            offset += len(match.group(0)) - len(texto)
            
            if tag in ["VALOR", "TEMPO", "CONDICAO", "PAGAMENTO"]:
                tipo = TipoEntidade(tag)
                
                # Busca mapeamento específico ou usa chave exata
                orientacao_str = orientacoes_map.get(texto, orientacoes_map.get(tag.lower(), "positiva"))
                modalidade_str = modalidades_map.get(texto, modalidades_map.get(tag.lower(), "afirmado"))
                
                orientacao = Orientacao(orientacao_str)
                modalidade = Modalidade(modalidade_str)
                ref_temporal = self._determinar_referencia_temporal(texto)
                
                entidade = Entidade(
                    texto=texto, tipo=tipo, orientacao=orientacao,
                    modalidade=modalidade, referencia_temporal=ref_temporal,
                    start=start_ajustado, end=end_ajustado
                )
                entidades.append(entidade)
        
        return frase_limpa, entidades

    def _determinar_referencia_temporal(self, texto: str) -> ReferenciatTemporal:
        """Determina referência temporal baseado no texto"""
        texto_lower = texto.lower()
        
        if any(f in texto_lower for f in ["amanhã", "semana que vem", "mês que vem", "ano que vem"]):
            return ReferenciatTemporal.FUTURO
        elif any(p in texto_lower for p in ["hoje", "agora", "neste momento"]):
            return ReferenciatTemporal.PRESENTE
        else:
            return ReferenciatTemporal.PRESENTE

    def gerar_dataset(self, n_amostras: int, output_file: str):
        """Gera dataset no formato correto"""
        dataset = []
        
        print(f"🔄 Gerando {n_amostras} amostras...")
        
        for i in range(n_amostras):
            frase, entidades = self.gerar_frase()
            
            entities_formatted = []
            orientacao_formatted = []
            modalidade_formatted = []
            referencia_temporal_formatted = []
            
            for ent in entidades:
                entities_formatted.append({
                    "start": ent.start,
                    "end": ent.end,
                    "text": ent.texto,
                    "labels": [ent.tipo.value]
                })
                
                orientacao_formatted.append({
                    "start": ent.start,
                    "end": ent.end,
                    "text": ent.texto,
                    "labels": [ent.orientacao.value]
                })
                
                modalidade_formatted.append({
                    "start": ent.start,
                    "end": ent.end,
                    "text": ent.texto,
                    "labels": [ent.modalidade.value]
                })
                
                referencia_temporal_formatted.append({
                    "start": ent.start,
                    "end": ent.end,
                    "text": ent.texto,
                    "labels": [ent.referencia_temporal.value]
                })
            
            amostra = {
                "text": frase,
                "id": i + 1,
                "entities": entities_formatted,
                "orientacao": orientacao_formatted,
                "modalidade": modalidade_formatted,
                "referencia_temporal": referencia_temporal_formatted
            }
            
            dataset.append(amostra)
            
            if (i + 1) % 100 == 0:
                print(f"  ✅ {i + 1}/{n_amostras} amostras geradas")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Dataset salvo em: {output_file}")
        self._imprimir_estatisticas(dataset)

    def _imprimir_estatisticas(self, dataset: List[Dict]):
        """Imprime estatísticas"""
        total_frases = len(dataset)
        total_entidades = sum(len(sample["entities"]) for sample in dataset)
        
        tipos = {}
        orientacoes = {}
        modalidades = {}
        
        for sample in dataset:
            for ent in sample["entities"]:
                tipos[ent["labels"][0]] = tipos.get(ent["labels"][0], 0) + 1
            for ent in sample["orientacao"]:
                orientacoes[ent["labels"][0]] = orientacoes.get(ent["labels"][0], 0) + 1
            for ent in sample["modalidade"]:
                modalidades[ent["labels"][0]] = modalidades.get(ent["labels"][0], 0) + 1
        
        print(f"\n📊 ESTATÍSTICAS:")
        print(f"  Total: {total_frases} frases, {total_entidades} entidades")
        print(f"  Média: {total_entidades/total_frases:.1f} entidades/frase")
        
        print(f"\n  🏷️ Tipos: {sorted(tipos.items())}")
        print(f"  🎯 Orientação: {sorted(orientacoes.items())}")
        print(f"  ⚡ Modalidade: {sorted(modalidades.items())}")

# Teste
if __name__ == "__main__":
    gerador = GeradorSimples()
    
    print("🧪 TESTANDO GERADOR SIMPLES E PRECISO:")
    print()
    
    for i in range(15):
        frase, entidades = gerador.gerar_frase()
        print(f"Frase: {frase}")
        for ent in entidades:
            print(f"  📍 {ent.texto} -> {ent.tipo.value} ({ent.orientacao.value}, {ent.modalidade.value})")
        print() 