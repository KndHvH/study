import random
import json
import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Tuple

# Definindo as classes/atributos do projeto
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
    """Gerador usando templates genéricos ricos com orientação contextual corrigida"""
    
    def __init__(self, taxa_erro: float = 0.2):
        self.taxa_erro = taxa_erro
        
        # Templates genéricos baseados na riqueza dos templates originais
        self.templates_genericos = {
            "PAGAMENTO_POSITIVO": [
                "{acao_pagamento} {valor} {tempo}",
                "{condicao_positiva} {acao_pagamento} {valor}",
                "{acao_pagamento} {valor} pode ser?",
                "{tempo} {acao_pagamento} {valor}",
                "consegui juntar {valor} pra {acao_pagamento_infinitivo} {tempo}",
                "to com {valor} pra {acao_pagamento_infinitivo}",
                "{condicao_positiva} consigo {acao_pagamento_infinitivo} {valor} até {tempo}",
                "posso {acao_pagamento_infinitivo} {valor} {tempo}?",
                "vou fazer um pix de {valor} {tempo}",
                "{acao_pagamento} {valor} {tempo} certeza",
                "garanto que {tempo} {acao_pagamento} {valor}"
            ],
            
            "DIFICULDADE": [
                "{condicao_negativa} {acao_pagamento_infinitivo} {valor} agora",
                "{condicao_negativa} {acao_pagamento_infinitivo} agora",
                "to {situacao_dificil} até {tempo}",
                "{valor} {expressao_negativa}",
                "{situacao_dificil}, {expressao_temporal_negativa}",
                "não tenho da onde tirar {valor}",
                "{valor} tá {expressao_valor_alto}",
                "{expressao_impossibilidade} {acao_pagamento_infinitivo} isso agora",
                "to {situacao_financeira}, não consigo {acao_pagamento_infinitivo}",
                "{tempo} {expressao_temporal_negativa}",
                "{valor} tá fora da minha realidade agora",
                "não consigo lidar com {valor} agora"
            ],
            
            "NEGOCIACAO": [
                "pode ser {valor}?",
                "{valor} dá?",
                "{condicao_positiva} {acao_pagamento} {valor} {tempo}",
                "que tal {valor} {condicao_positiva}?",
                "dá pra ser {valor} {condicao_positiva}?",
                "aceita {valor} pra quitar tudo?",
                "tem como {acao_negociacao}?",
                "{acao_negociacao} {valor} {tempo}?",
                "posso fazer {condicao_positiva}?",
                "só consigo {condicao_positiva}",
                "{condicao_positiva} {acao_pagamento} tudo",
                "consegue fazer {valor_menor}?"
            ],
            
            "DUPLA_ORIENTACAO": [
                "{tempo_negativo} {expressao_negativa}, {conector_alternativa} {tempo_positivo} {acao_pagamento}",
                "{valor_alto} {expressao_negativa}, {conector_alternativa} {valor_baixo}",
                "{condicao_negativa} agora, apenas {condicao_positiva}",
                "{expressao_temporal_negativa}, mas {tempo_positivo} {acao_pagamento}"
            ],
            
            "SIMPLES": [
                "{valor} {expressao_valor}",
                "{tempo} {expressao_temporal}",
                "{acao_pagamento} {tempo}",
                "to com {valor} só",
                "quero {acao_pagamento_infinitivo}",
                "quero {acao_pagamento_infinitivo} {tempo}",
                "vou {acao_pagamento_infinitivo}",
                "vou {acao_pagamento_infinitivo} {tempo}",
                "{condicao_positiva}",
                "{situacao_dificil}"
            ]
        }
        
        # Componentes extraídos da riqueza dos templates originais
        self.componentes = {
            "acao_pagamento": ["pago", "quito", "acerto", "mando", "deposito", "transfiro", "faço"],
            "acao_pagamento_infinitivo": ["pagar", "quitar", "acertar", "mandar", "depositar", "transferir", "fazer"],
            
            "condicao_positiva": [
                "quando receber", "quando tiver dinheiro", "se der certo", "se conseguir",
                "quando entrar dinheiro", "se rolar pagamento", "quando meu salário cair",
                "se sobrar dinheiro", "assim que bater na conta", "quando resolver uns problemas",
                "em 2x", "em 3x", "parcelado em 6x", "50% agora", "metade agora", "30% de entrada",
                "com desconto", "se der um desconto", "com uma redução",
                "quando sair meu 13º", "no final do mês", "quando receber do cliente",
                "se vender umas coisas", "quando conseguir um freela", "se aparecer um trabalho",
                "quando minha mãe me ajudar", "se meu pai emprestar", "quando resolver umas pendências",
                "dividido em 4x", "parcelado em 12x", "25% de entrada", "70% agora",
                "se baixar um pouco", "com facilidade de pagamento", "se tiver prazo",
                "quando resolver minha situação", "se der uma força", "com jeitinho brasileiro",
                "quando cair o auxílio", "se conseguir um adiantamento", "quando vender o carro",
                "se alugar meu quarto", "quando receber uns trocados", "se der uma moral",
                "com cartão", "no cartão de crédito", "via pix", "em espécie",
                "quando sair minha rescisão", "se conseguir um empréstimo", "quando der",
                "se a vida melhorar", "quando as coisas se ajeitarem", "se Deus quiser"
            ],
            
            "condicao_negativa": [
                "não tenho como", "não consigo", "não dá pra", "sem condição de",
                "sem condições de", "não vai dar pra", "impossível", "nem se eu quisesse",
                "não vai dar", "é impossível", "nem pensar", "nem fodendo",
                "tá fora de cogitação", "não tem cabimento", "nem rola", "zero chance",
                "não tem jeito", "não dá mesmo", "sem chance nenhuma", "não há possibilidade",
                "tá fora da realidade", "nem com reza forte", "não consigo nem sonhando",
                "tá muito além das minhas possibilidades", "nem que eu quisesse muito",
                "não tenho de onde tirar", "não tenho nem pra comer", "tô zerado",
                "não sobra nem pro café", "tô no osso", "sem condição alguma",
                "nem vendendo o rim", "nem com milagre", "impossível total"
            ],
            
            "situacao_dificil": [
                "sem dinheiro", "duro", "liso", "ferrado", "no vermelho total",
                "desempregado", "apertado", "com as contas atrasadas", "sem grana",
                "devendo", "enrolado com outras contas", "quebrado", "lascado",
                "no sufoco", "apertadão", "na pior", "na merda", "fudido",
                "sem um centavo", "zerado", "raspando o tacho", "comendo pão dormido",
                "vivendo de milagre", "sobrevivendo", "me virando nos 30",
                "passando necessidade", "apertado financeiramente", "na lona",
                "sem perspectiva", "desgraçado", "numa situação difícil",
                "meio perdido", "bem complicado", "numa enrascada",
                "sem saída", "numa situação delicada", "bem apertado mesmo",
                "numa bad", "numa cilada", "em apuros", "numa sinuca",
                "batendo cabeça", "numa situação feia", "ralando muito"
            ],
            
            "situacao_financeira": [
                "bem apertado esse mês", "com dificuldade financeira", "sem margem nenhuma",
                "me virando como dá", "tentando arrumar grana", "vendo o que consigo fazer",
                "correndo atrás de dinheiro", "batalhando pra conseguir", "me esforçando muito",
                "fazendo malabarismo financeiro", "equilibrando os pratos", "dando um jeito",
                "improvisando bastante", "contando os centavos", "economizando no tudo",
                "cortando gastos", "vivendo no limite", "administrando a crise",
                "fazendo conta de cabeça", "pesando cada gasto", "priorizando o essencial",
                "tentando se organizar", "buscando alternativas", "correndo atrás de soluções",
                "fazendo das tripas coração", "dando duro pra conseguir", "batalhando muito"
            ],
            
            "expressao_valor": ["eu consigo", "posso pagar", "tá ok", "dá pra fazer"],
            "expressao_valor_alto": ["puxado demais", "muito caro", "salgado pra mim", "demais"],
            "expressao_negativa": ["não dá", "não rola", "tá puxado", "é muito", "não consigo"],
            
            "expressao_temporal": [
                "eu resolvo", "vai dar", "consigo pagar", "acerto", "dou um jeito",
                "me organizo", "providencio", "vou atrás", "corro atrás", "me viro",
                "faço acontecer", "dou conta", "resolvo essa", "quebro um galho",
                "me ajusto", "consigo dar conta", "vou conseguir", "vai dar certo",
                "tudo certo", "pode deixar", "tá garantido", "sem problema"
            ],
            "expressao_temporal_negativa": [
                "não vai dar", "é impossível", "tá complicado", "já era pra mim",
                "ferrou", "tá foda", "não tem jeito", "difícil demais", "pesado",
                "complicado demais", "muito apertado", "sem condição", "não rola",
                "impossível total", "nem pensando", "tá tenso", "muito difícil",
                "sem chance", "não consigo", "muito pesado", "tá osso"
            ],
            
            "expressao_impossibilidade": [
                "nem fudendo que consigo", "nem rola", "sem chance de", "não tem como",
                "nem fodendo", "nem pensando", "impossível total", "nem sonhando",
                "nem que a vaca tussa", "nem com reza forte", "nem que chova canivete",
                "nem amarrado", "nem com uma arma na cabeça", "nem que o mundo acabe",
                "nem vendendo o rim", "nem com milagre", "nem Jesus na causa"
            ],
            
            "acao_negociacao": [
                "parcelar", "dar um desconto", "reduzir os juros", "fazer um acordo",
                "negociar esse valor", "reduzir essa multa", "abater alguma coisa",
                "dar uma facilitada", "fazer um jeitinho", "dar uma moral",
                "fazer uma promoção", "dar uma condição especial", "facilitar pra mim",
                "fazer um preço camarada", "dar uma força", "ajudar com o preço",
                "fazer vista grossa", "relevar uns juros", "dar um desconto especial",
                "fazer um acordo bom", "negociar de boa", "chegar num meio termo",
                "fazer um trato", "dar uma oportunidade", "ser mais flexível"
            ],
            
            "conector_alternativa": [
                "mas", "porém", "só que", "então", "aí", "daí", "agora",
                "entretanto", "contudo", "todavia", "no entanto", "assim",
                "dessa forma", "desse jeito", "por outro lado", "em compensação"
            ],
            
            # Componentes para problemas identificados
            "consigo": [
                "consigo pagar", "consigo fazer", "consigo mandar", "consigo depositar",
                "consigo bancar", "consigo arcar", "consigo cobrir", "consigo honrar",
                "consigo dar conta", "consigo assumir", "consigo cumprir", "consigo tocar"
            ],
            "valor_menor": [
                "valor menor", "um valor mais baixo", "algo mais barato", "desconto",
                "preço melhor", "condição especial", "valor reduzido", "preço camarada",
                "algo mais acessível", "valor mais em conta", "preço promocional",
                "desconto especial", "valor facilitado", "preço de amigo"
            ],
            "modificador_valor": [
                "demais", "muito", "puxado", "salgado", "caro", "alto", "pesado",
                "exagerado", "absurdo", "surreal", "impossível", "fora de série",
                "nas alturas", "pela hora da morte", "astronômico", "abusivo"
            ],
            
            "tempo_negativo": [
                "hoje", "agora", "esse mês", "essa semana", "neste momento",
                "já", "ainda hoje", "hoje mesmo", "agora mesmo", "nesta semana",
                "neste final de semana", "até amanhã", "até sexta", "urgente"
            ],
            "tempo_positivo": [
                "amanhã", "semana que vem", "mês que vem", "depois", "mais tarde",
                "no futuro", "quando der", "daqui uns dias", "na próxima semana",
                "no próximo mês", "ano que vem", "em breve", "logo logo",
                "assim que possível", "quando tiver condição", "no tempo certo"
            ],
            "valor_alto": [
                "R$ 800", "R$ 1000", "R$ 1500", "R$ 2000", "R$ 2500", "R$ 3000",
                "R$ 1200", "R$ 1800", "R$ 900", "R$ 1100", "R$ 1300", "R$ 1600"
            ],
            "valor_baixo": [
                "R$ 200", "R$ 300", "R$ 400", "R$ 150", "R$ 250", "R$ 350",
                "R$ 100", "R$ 180", "R$ 220", "R$ 280", "R$ 320", "R$ 380"
            ],
            
            # Novos componentes adicionados
            "intensificador": [
                "muito", "bem", "super", "mega", "extremamente", "demais",
                "pra caramba", "pra caralho", "pra burro", "do caralho",
                "absurdamente", "completamente", "totalmente", "bastante"
            ],
            
            "grias_dinheiro": [
                "grana", "din-din", "trocados", "bufunfa", "tutu", "money",
                "cash", "graninha", "dinheirinho", "mosca", "pila", "real"
            ],
            
            "expressoes_tempo_coloquial": [
                "rapidinho", "na hora", "ligeiro", "voando", "correndo",
                "de uma vez", "sem demora", "já já", "num instante",
                "na velocidade da luz", "toca o sino", "sem enrolação"
            ],
            
            "formas_pagamento": [
                "no pix", "via pix", "no cartão", "em dinheiro", "à vista",
                "no débito", "no crédito", "via transferência", "por depósito",
                "em espécie", "via ted", "por boleto", "no app do banco"
            ],
            
            "expressoes_compromisso": [
                "palavra de homem", "juro por Deus", "te garanto", "pode confiar",
                "dou minha palavra", "prometo", "assumo o compromisso", "te asseguro",
                "pode acreditar", "é sério", "sem brincadeira", "de verdade",
                "na moral", "de coração", "com toda sinceridade"
            ]
        }
    
    def gerar_valor_dinamico(self):
        """Gera valores monetários dinamicamente"""
        faixas = {
            "micro": (10, 50),      # Mínimo 10 (nunca zero!)
            "baixo": (50, 300), 
            "medio": (300, 800),
            "alto": (800, 2500)
        }
        
        faixa = random.choices(
            ["micro", "baixo", "medio", "alto"],
            weights=[0.1, 0.4, 0.3, 0.2]
        )[0]
        
        min_val, max_val = faixas[faixa]
        valor = random.randint(min_val, max_val)
        
        # Valores "redondos" 30% das vezes
        if random.random() < 0.3:
            valor = (valor // 10) * 10
            if valor == 0:  # Garantia extra contra zero
                valor = 10
        
        formatos = ["R$ {}", "{} reais", "{}"]
        formato = random.choice(formatos)
        return formato.format(valor)
    
    def gerar_tempo_dinamico(self):
        """Gera expressões temporais dinamicamente"""
        # Componentes para gerar datas específicas
        dia = random.randint(1, 30)
        mes = random.randint(1, 12)
        ano = random.randint(2024, 2025)
        
        tempos = {
            "imediato": ["agora", "hoje", "já", "ainda hoje", "neste momento"],
            "curto_prazo": ["amanhã", "depois de amanhã", "essa semana", "até sexta", "segunda que vem", 
                           f"dia {dia}", f"no dia {dia}", f"até dia {dia}"],
            "medio_prazo": ["semana que vem", "mês que vem", "final do mês", "início do mês",
                           f"dia {dia}/{mes:02d}", f"no dia {dia}/{mes:02d}", f"até {dia}/{mes:02d}",
                           f"na próxima semana", f"daqui a {random.randint(2, 7)} dias"],
            "longo_prazo": ["ano que vem", "quando der", "daqui uns meses", f"em {dia}/{mes:02d}/{ano}",
                           f"no {random.randint(5, 30)} que vem", f"em {random.randint(1, 3)} semanas"]
        }
        
        categoria = random.choices(
            list(tempos.keys()),
            weights=[0.3, 0.4, 0.2, 0.1]
        )[0]
        
        return random.choice(tempos[categoria])
    
    def escolher_template_e_categoria(self):
        """Escolhe um template genérico e sua categoria"""
        categoria = random.choice(list(self.templates_genericos.keys()))
        template = random.choice(self.templates_genericos[categoria])
        return template, categoria
    
    def preencher_placeholders(self, template, categoria):
        """Preenche os placeholders do template e retorna frase + mapeamento de entidades"""
        frase_original = template
        entidades_mapeadas = []
        
        # Encontra todos os placeholders com suas posições ANTES de qualquer substituição
        placeholders_info = []
        for match in re.finditer(r'\{(\w+)\}', template):
            placeholder = match.group(1)
            pos_inicio = match.start()
            pos_fim = match.end()
            placeholders_info.append({
                'placeholder': placeholder,
                'pos_inicio': pos_inicio,
                'pos_fim': pos_fim,
                'texto_original': match.group(0)
            })
        
        # Gera valores para todos os placeholders
        substituicoes = {}
        for info in placeholders_info:
            placeholder = info['placeholder']
            
            if placeholder in self.componentes:
                valor_componente = random.choice(self.componentes[placeholder])
                substituicoes[info['texto_original']] = valor_componente
            elif placeholder == "valor":
                valor_gerado = self.gerar_valor_dinamico()
                substituicoes[info['texto_original']] = valor_gerado
            elif placeholder == "tempo":
                tempo_gerado = self.gerar_tempo_dinamico()
                substituicoes[info['texto_original']] = tempo_gerado
            elif placeholder == "valor_alto":
                valor_alto = f"R$ {random.randint(800, 1500)}"
                substituicoes[info['texto_original']] = valor_alto
            elif placeholder == "valor_baixo":
                valor_baixo = f"R$ {random.randint(100, 400)}"
                substituicoes[info['texto_original']] = valor_baixo
        
        # Aplica substituições e calcula posições corretas
        frase_final = frase_original
        offset_acumulado = 0
        
        for info in placeholders_info:
            placeholder = info['placeholder']
            texto_placeholder = info['texto_original']
            
            # Determina tipo de entidade
            tipo_entidade = self._mapear_placeholder_para_tipo(placeholder)
            
            # Pula conectores irrelevantes
            if tipo_entidade is None:
                valor_substituto = substituicoes[texto_placeholder]
                frase_final = frase_final.replace(texto_placeholder, valor_substituto, 1)
                offset_acumulado += len(valor_substituto) - len(texto_placeholder)
                continue
            
            # Calcula posições ajustadas pelo offset
            pos_inicio_ajustada = info['pos_inicio'] + offset_acumulado
            valor_substituto = substituicoes[texto_placeholder]
            pos_fim_ajustada = pos_inicio_ajustada + len(valor_substituto)
            
            # Aplica substituição
            frase_final = frase_final.replace(texto_placeholder, valor_substituto, 1)
            offset_acumulado += len(valor_substituto) - len(texto_placeholder)
            
            # Adiciona entidade com posições corretas
            entidades_mapeadas.append({
                "texto": valor_substituto,
                "tipo": tipo_entidade,
                "start": pos_inicio_ajustada,
                "end": pos_fim_ajustada,
                "placeholder_origem": placeholder
            })
        
        return frase_final, entidades_mapeadas
    
    def _mapear_placeholder_para_tipo(self, placeholder):
        """Mapeia nome do placeholder para tipo de entidade - MAIS ESPECÍFICO"""
        
        # 1. ENTIDADES CLARAS DE PAGAMENTO
        if "acao_pagamento" in placeholder or placeholder in ["consigo", "posso"]:
            return TipoEntidade.PAGAMENTO
        
        # 2. ENTIDADES CLARAS DE TEMPO
        elif placeholder == "tempo" or placeholder in ["tempo_positivo", "tempo_negativo"]:
            return TipoEntidade.TEMPO
        
        # 3. ENTIDADES CLARAS DE VALOR
        elif placeholder == "valor" or placeholder in ["valor_alto", "valor_baixo"]:
            return TipoEntidade.VALOR
        
        # 4. ENTIDADES CLARAS DE CONDIÇÃO
        elif placeholder in ["condicao_positiva", "condicao_negativa", "acao_negociacao", 
                            "valor_menor", "desconto", "parcelamento", "valor_reduzido"]:
            return TipoEntidade.CONDICAO
        
        # 5. NÃO SÃO ENTIDADES - EXPANDIDO
        elif placeholder in [
            "conector_alternativa", "modificador_valor", "intensificador", 
            "expressao_intensidade", "adverbio_negacao",
            # Expressões que são contexto, não entidades
            "expressao_valor", "expressao_valor_alto", "expressao_negativa",
            "expressao_temporal", "expressao_temporal_negativa", "expressao_impossibilidade",
            "situacao_dificil", "situacao_financeira",
            # Modificadores e conectores
            "conector", "modificador", "intensificador", "qualificador"
        ]:
            return None  # NÃO rotular - é melhor que rotular errado
        
        # 6. DEFAULT: NÃO ROTULAR
        else:
            return None  # Preferir não rotular a rotular errado
    
    def determinar_atributos_por_categoria(self, categoria, entidade_texto, frase, posicao_entidade):
        """Determina orientação e modalidade baseada na CATEGORIA do template"""
        
        # PAGAMENTO_POSITIVO: todas entidades são positivas, mas modalidade depende do contexto
        if categoria == "PAGAMENTO_POSITIVO":
            orientacao = Orientacao.POSITIVA
            
            # Verifica se há condições na frase que tornam tudo CONDICIONAL
            palavras_condicionais = ["pra", "para", "quando", "se", "caso", "assim que", 
                                   "depois que", "só", "apenas", "somente", "consegui juntar"]
            
            # Expressões que indicam PLANEJADO (intenção firme)
            palavras_planejadas = ["vou", "vai", "irei", "farei", "pagarei", "quitarei", 
                                 "garanto", "prometo", "assumo", "me comprometo"]
            
            if any(palavra in frase.lower() for palavra in palavras_planejadas):
                modalidade = Modalidade.PLANEJADO
            elif any(palavra in frase.lower() for palavra in palavras_condicionais):
                modalidade = Modalidade.CONDICIONAL
            elif re.search(r'\b(pago|quito|acerto|mando|deposito|transfiro|faço)\b', 
                        entidade_texto.lower()):
                modalidade = Modalidade.AFIRMADO
            else:
                modalidade = Modalidade.CONDICIONAL  # Default mais conservador
                
        # DIFICULDADE: todas entidades são negativas 
        elif categoria == "DIFICULDADE":
            orientacao = Orientacao.NEGATIVA
            modalidade = Modalidade.NEGADO
            
        # NEGOCIACAO: todas entidades são positivas e condicionais
        elif categoria == "NEGOCIACAO":
            orientacao = Orientacao.POSITIVA
            modalidade = Modalidade.CONDICIONAL
            
        # DUPLA_ORIENTACAO: analisa posição relativa ao conector
        elif categoria == "DUPLA_ORIENTACAO":
            orientacao, modalidade = self._analisar_dupla_orientacao(entidade_texto, frase, posicao_entidade)
            
        # SIMPLES: depende do contexto específico
        else:  # SIMPLES
            orientacao, modalidade = self._analisar_simples(entidade_texto, frase)
            
        return orientacao, modalidade
    
    def _analisar_dupla_orientacao(self, entidade_texto, frase, posicao_entidade):
        """Analisa entidades em frases com dupla orientação (antes/depois do conector)"""
        # Encontra conectores que mudam o sentido
        conectores = ["mas", "porém", "só que", "então", "dessa forma", "por outro lado", 
                     "entretanto", "contudo", "todavia", "no entanto", "apenas", "só"]
        
        pos_conector = -1
        conector_encontrado = ""
        for conector in conectores:
            if conector in frase.lower():
                pos_conector = frase.lower().find(conector)
                conector_encontrado = conector
                break
        
        if pos_conector != -1:
            # Se a entidade vem ANTES do conector, analisa se é negativa
            if posicao_entidade < pos_conector:
                # Expressões que indicam impossibilidade/negação forte
                expressoes_negativas = [
                    "nem que eu quisesse", "nem se eu quisesse", "nem que", "nem se",
                    "impossível", "não tem como", "não consigo", "não dá", "não vai dar",
                    "sem condição", "sem chance", "zero chance", "nem pensar", "nem rola",
                    "fora de cogitação", "nem fodendo", "nem pensando", "tá fora",
                    "não tenho como", "não há possibilidade", "tá impossível",
                    # ADICIONADO: expressões que indicam valor alto/impossível
                    "é muito", "tá muito", "muito caro", "muito alto", "não rola"
                ]
                
                # Verifica se a entidade ou contexto anterior tem expressões negativas
                texto_antes_conector = frase[:pos_conector].lower()
                entidade_lower = entidade_texto.lower()
                
                # Se a entidade contém expressão negativa OU está no contexto negativo
                if (any(expr in entidade_lower for expr in expressoes_negativas) or
                    any(expr in texto_antes_conector for expr in expressoes_negativas) or
                    any(neg in entidade_lower for neg in ["não", "sem", "impossível", "nem", "zero"])):
                    return Orientacao.NEGATIVA, Modalidade.NEGADO
                else:
                    # PARA VALORES: Se está antes do conector em dupla orientação, É NEGATIVO
                    # "R$ 800 não rola, mas R$ 200" - o primeiro valor é sempre negativo
                    return Orientacao.NEGATIVA, Modalidade.NEGADO
            else:
                # Se a entidade vem DEPOIS do conector, é positiva
                # Verifica se indica planejamento futuro
                if any(fut in entidade_texto.lower() for fut in ["logo", "depois", "amanhã", "próxim", "vou", "vai", "quando", "se"]):
                    return Orientacao.POSITIVA, Modalidade.CONDICIONAL  # Mudei de PLANEJADO para CONDICIONAL pois "quando conseguir" é condicional
                else:
                    return Orientacao.POSITIVA, Modalidade.CONDICIONAL
        
        # Default se não achou conector
        return Orientacao.POSITIVA, Modalidade.CONDICIONAL
    
    def _analisar_simples(self, entidade_texto, frase):
        """Analisa frases simples baseado no contexto - CORRIGIDO"""
        # Expressões fortemente negativas - mais específicas
        indicadores_negativos_fortes = [
            "impossível", "sem condição", "sem chance", "zero chance", 
            "nem pensar", "nem rola", "fora de cogitação", "nem fodendo", 
            "não tem como", "não há possibilidade", "não consigo", "não dá"
        ]
        
        # Expressões condicionais
        palavras_condicionais = ["pra", "para", "só", "apenas", "somente", "no máximo", "até", "quando muito"]
        
        # Expressões de planejamento
        palavras_planejadas = ["vou", "vai", "irei", "farei", "pagarei", "quitarei"]
        
        # Verifica se a entidade ou contexto tem expressões negativas
        entidade_lower = entidade_texto.lower()
        frase_lower = frase.lower()
        
        # 1. SE A ENTIDADE EM SI É NEGATIVA (ex: "não consigo")
        if any(ind in entidade_lower for ind in indicadores_negativos_fortes):
            return Orientacao.NEGATIVA, Modalidade.NEGADO
        
        # 2. SE A FRASE TEM NEGAÇÃO FORTE E ESPECÍFICA
        elif any(ind in frase_lower for ind in indicadores_negativos_fortes):
            return Orientacao.NEGATIVA, Modalidade.NEGADO
        
        # 3. VERIFICA MODALIDADES POSITIVAS
        elif any(palavra in frase_lower for palavra in palavras_planejadas):
            return Orientacao.POSITIVA, Modalidade.PLANEJADO
        elif any(palavra in frase_lower for palavra in palavras_condicionais):
            return Orientacao.POSITIVA, Modalidade.CONDICIONAL
        
        # 4. DEFAULT: AFIRMADO POSITIVO
        # Para frases simples como "pago semana que vem", assume positivo
        else:
            return Orientacao.POSITIVA, Modalidade.AFIRMADO
    
    def _determinar_ref_temporal(self, texto_tempo):
        """Determina referência temporal baseada no texto"""
        texto_lower = texto_tempo.lower()
        if any(palavra in texto_lower for palavra in ["hoje", "agora", "já"]):
            return ReferenciatTemporal.PRESENTE
        elif any(palavra in texto_lower for palavra in ["amanhã", "depois", "semana", "mês", "dia"]):
            return ReferenciatTemporal.FUTURO
        else:
            return ReferenciatTemporal.FUTURO  # Default
    
    def _determinar_ref_temporal_contextual(self, entidade_texto, frase):
        """Determina referência temporal considerando contexto da frase"""
        # Para entidades temporais, usa análise específica
        texto_lower = entidade_texto.lower()
        
        # PRESENTE - palavras que indicam tempo atual
        indicadores_presente = ["hoje", "agora", "já", "neste momento", "nesta semana", 
                               "esse mês", "esta semana", "atualmente", "no momento"]
        
        # FUTURO - palavras que indicam tempo futuro  
        indicadores_futuro = ["amanhã", "depois", "semana que vem", "mês que vem", "ano que vem",
                             "próxim", "final do mês", "início do mês", "logo", "em breve",
                             "daqui", "quando", "futuramente", "mais tarde", "depois de",
                             "na próxima", "no próximo", "logo logo", "em uns dias"]
        
        # PASSADO - palavras que indicam tempo passado
        indicadores_passado = ["ontem", "semana passada", "mês passado", "ano passado", 
                              "anteriormente", "antes", "já foi", "passou"]
        
        # Verifica primeiro a entidade específica
        if any(palavra in texto_lower for palavra in indicadores_presente):
            return ReferenciatTemporal.PRESENTE
        elif any(palavra in texto_lower for palavra in indicadores_futuro):
            return ReferenciatTemporal.FUTURO
        elif any(palavra in texto_lower for palavra in indicadores_passado):
            return ReferenciatTemporal.PASSADO
        
        # Se não encontrou na entidade, analisa contexto da frase
        frase_lower = frase.lower()
        
        # Verifica indicadores de futuro na frase (mais provável)
        if any(palavra in frase_lower for palavra in indicadores_futuro):
            return ReferenciatTemporal.FUTURO
        elif any(palavra in frase_lower for palavra in indicadores_presente):
            return ReferenciatTemporal.PRESENTE
        elif any(palavra in frase_lower for palavra in indicadores_passado):
            return ReferenciatTemporal.PASSADO
        
        # Análise contextual adicional
        # Se tem "pra + verbo", geralmente é futuro
        if re.search(r'\bpra\s+\w+', frase_lower) or re.search(r'\bpara\s+\w+', frase_lower):
            return ReferenciatTemporal.FUTURO
            
        # Se tem "vou/vai + verbo", é futuro
        if re.search(r'\b(vou|vai|irei|farei)\b', frase_lower):
            return ReferenciatTemporal.FUTURO
        
        # Default: presente
        return ReferenciatTemporal.PRESENTE
    
    def _escolher_modalidade(self) -> Modalidade:
        """Escolhe modalidade baseada na distribuição"""
        modalidades = [Modalidade.AFIRMADO, Modalidade.PLANEJADO, Modalidade.CONDICIONAL, 
                      Modalidade.INCERTO, Modalidade.NEGADO]
        pesos = [0.25, 0.20, 0.25, 0.10, 0.20]
        return random.choices(modalidades, weights=pesos)[0]
    
    def _escolher_referencia_temporal(self) -> ReferenciatTemporal:
        """Escolhe referência temporal baseada na distribuição"""
        referencias = [ReferenciatTemporal.PRESENTE, ReferenciatTemporal.FUTURO, ReferenciatTemporal.PASSADO]
        pesos = [0.3, 0.6, 0.1]
        return random.choices(referencias, weights=pesos)[0]
    
    def gerar_frase(self) -> Tuple[str, List[Entidade]]:
        """Método principal para gerar frases usando templates genéricos"""
        # Escolhe template e categoria
        template, categoria = self.escolher_template_e_categoria()
        
        # Preenche os placeholders E mapeia entidades
        frase, entidades_mapeadas = self.preencher_placeholders(template, categoria)
        
        # Converte mapeamento para objetos Entidade com atributos corretos
        entidades = self.criar_entidades_com_atributos(entidades_mapeadas, categoria, frase)
        
        # Aplica erros naturais
        #frase_final = self._aplicar_erros_naturais(frase)
        
        return frase, entidades
    
    def criar_entidades_com_atributos(self, entidades_mapeadas, categoria, frase):
        """Converte mapeamento de entidades para objetos Entidade com atributos corretos"""
        entidades = []
        
        for ent_map in entidades_mapeadas:
            # VALIDAÇÃO PÓS-GERAÇÃO: Filtra entidades inválidas
            if not self._validar_entidade(ent_map["texto"], ent_map["tipo"]):
                continue  # Pula entidades que não fazem sentido
            
            orientacao, modalidade = self.determinar_atributos_por_categoria(
                categoria, ent_map["texto"], frase, ent_map["start"]
            )
            
            entidade = Entidade(
                texto=ent_map["texto"],
                tipo=ent_map["tipo"],
                orientacao=orientacao,
                modalidade=modalidade,
                referencia_temporal=self._determinar_ref_temporal_contextual(ent_map["texto"], frase),
                start=ent_map["start"],
                end=ent_map["end"]
            )
            entidades.append(entidade)
        
        return entidades
    
    def _validar_entidade(self, texto, tipo):
        """Valida se uma entidade faz sentido semanticamente - CORRIGIDO"""
        texto_lower = texto.lower().strip()
        
        # Filtros por TIPO
        if tipo == TipoEntidade.VALOR:
            # VALOR deve ter números, "reais" ou porcentagem - RELAXADO
            if not (re.search(r'\d', texto) or 'real' in texto_lower or '%' in texto):
                return False
        
        elif tipo == TipoEntidade.TEMPO:
            # TEMPO deve ter indicadores temporais específicos OU datas - EXPANDIDO
            indicadores_tempo = [
                'hoje', 'amanhã', 'ontem', 'semana', 'mês', 'ano', 'dia',
                'agora', 'depois', 'antes', 'logo', 'breve', 'próxim',
                'final', 'início', 'manhã', 'tarde', 'noite', 'daqui',
                'momento', 'hora', 'tempo', 'quando'
            ]
            # Aceita datas no formato dd/mm/yyyy ou similares
            tem_data = re.search(r'\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}', texto)
            
            if not (any(ind in texto_lower for ind in indicadores_tempo) or tem_data):
                return False
        
        elif tipo == TipoEntidade.PAGAMENTO:
            # PAGAMENTO deve ter verbos de pagamento - EXPANDIDO
            verbos_pagamento = [
                'pag', 'quit', 'acer', 'mand', 'deposit', 'transf', 
                'consig', 'faz', 'envi', 'conseguir', 'posso'
            ]
            if not any(verbo in texto_lower for verbo in verbos_pagamento):
                return False
        
        elif tipo == TipoEntidade.CONDICAO:
            # CONDIÇÃO deve ter palavras relevantes
            palavras_condicao = [
                'desconto', 'parcel', 'entrada', 'prazo', 'facilidade',
                'condição', 'jeito', 'forma', 'maneira', 'quando', 'se',
                'fora de cogitação', 'cogitação', 'reduz', 'menor', 'baixar',
                'valor reduzido', '%', 'porcentagem'
            ]
            if not any(palavra in texto_lower for palavra in palavras_condicao):
                return False
        
        # Filtros GERAIS - palavras muito genéricas que não são entidades - REDUZIDO
        palavras_genericas = [
            'é', 'mas', 'né', 'ne', 'ai', 'aí', 'então', 'daí'
        ]
        
        if texto_lower in palavras_genericas:
            return False
        
        # Filtro de tamanho - entidades muito pequenas são suspeitas
        if len(texto_lower) <= 1:  # Mudei de 2 para 1 para aceitar números como "80"
            return False
            
        return True
    
    def _aplicar_erros_naturais(self, texto: str) -> str:
        """Aplica erros de digitação naturais"""
        if random.random() < 0.15:  # 15% chance de erro
            erros = {
                "você": "vc", "para": "pra", "porque": "pq", 
                "está": "tá", "estou": "to", "vou": "vo", "não": "nao"
            }
            
            for original, erro in erros.items():
                if original in texto and random.random() < 0.3:
                    texto = texto.replace(original, erro)
        
        return texto
    
    def gerar_dataset_balanceado(self, n_amostras: int, output_file: str):
        """Gera dataset balanceado no formato correto"""
        dataset = []
        
        for i in range(n_amostras):
            frase_texto, entidades = self.gerar_frase()
            
            # Converte para formato igual ao labeled_data.json
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
            
            dataset.append({
                "text": frase_texto,
                "id": i + 1,
                "entities": entities_formatted,
                "orientacao": orientacao_formatted,
                "modalidade": modalidade_formatted,
                "referencia_temporal": referencia_temporal_formatted
            })
            
            if (i + 1) % 100 == 0:
                print(f"Geradas {i + 1} frases...")
        
        # Salva o dataset
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Dataset salvo em: {output_file}")
        self._imprimir_estatisticas(dataset)
    
    def _imprimir_estatisticas(self, dataset: List[Dict]):
        """Imprime estatísticas do dataset gerado"""
        total_entidades = sum(len(item["entities"]) for item in dataset)
        
        orientacoes = {}
        modalidades = {}
        ref_temporais = {}
        tipos = {}
        
        for item in dataset:
            for ent in item["orientacao"]:
                orientacoes[ent["labels"][0]] = orientacoes.get(ent["labels"][0], 0) + 1
            for ent in item["modalidade"]:
                modalidades[ent["labels"][0]] = modalidades.get(ent["labels"][0], 0) + 1
            for ent in item["referencia_temporal"]:
                ref_temporais[ent["labels"][0]] = ref_temporais.get(ent["labels"][0], 0) + 1
            for ent in item["entities"]:
                tipos[ent["labels"][0]] = tipos.get(ent["labels"][0], 0) + 1
        
        print(f"\n📊 ESTATÍSTICAS DO DATASET:")
        print(f"📝 Total de frases: {len(dataset)}")
        print(f"🎯 Total de entidades: {total_entidades}")
        print(f"📈 Média de entidades por frase: {total_entidades/len(dataset):.2f}")
        
        print(f"\n🎭 ORIENTAÇÃO:")
        for orientacao, count in orientacoes.items():
            percentual = (count/total_entidades)*100
            print(f"  {orientacao}: {count} ({percentual:.1f}%)")
        
        print(f"\n🏷️ TIPOS DE ENTIDADE:")
        for tipo, count in tipos.items():
            percentual = (count/total_entidades)*100
            print(f"  {tipo}: {count} ({percentual:.1f}%)")


# Função principal para teste
if __name__ == "__main__":
    gerador = GeradorFrases()
    
    print("🧪 TESTANDO GERADOR CORRIGIDO:")
    for i in range(20):
        frase, entidades = gerador.gerar_frase()
        print(f"\n{i+1}. '{frase}'")
        for ent in entidades:
            print(f"   → '{ent.texto}' ({ent.tipo.value}) - {ent.orientacao.value} - {ent.modalidade.value} - {ent.referencia_temporal.value}") 