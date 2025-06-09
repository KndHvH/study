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
                "infelizmente {expressao_temporal_negativa}, mas {tempo_positivo} {acao_pagamento}"
            ],
            
            "SIMPLES": [
                "{valor} {expressao_valor}",
                "{tempo} {expressao_temporal}",
                "{acao_pagamento} {tempo}",
                "to com {valor} só",
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
                "com desconto", "se der um desconto", "com uma redução"
            ],
            
            "condicao_negativa": [
                "não tenho como", "não consigo", "não dá pra", "sem condição de",
                "sem condições de", "não vai dar pra", "impossível", "nem se eu quisesse",
                "não vai dar", "é impossível"
            ],
            
            "situacao_dificil": [
                "sem dinheiro", "duro", "liso", "ferrado", "no vermelho total",
                "desempregado", "apertado", "com as contas atrasadas", "sem grana",
                "devendo", "enrolado com outras contas"
            ],
            
            "situacao_financeira": [
                "bem apertado esse mês", "com dificuldade financeira", "sem margem nenhuma",
                "me virando como dá", "tentando arrumar grana", "vendo o que consigo fazer"
            ],
            
            "expressao_valor": ["eu consigo", "posso pagar", "tá ok", "dá pra fazer"],
            "expressao_valor_alto": ["puxado demais", "muito caro", "salgado pra mim", "demais"],
            "expressao_negativa": ["não dá", "não rola", "tá puxado", "é muito", "não consigo"],
            
            "expressao_temporal": ["eu resolvo", "vai dar", "consigo pagar", "acerto"],
            "expressao_temporal_negativa": ["não vai dar", "é impossível", "tá complicado", "já era pra mim"],
            
            "expressao_impossibilidade": [
                "nem fudendo que consigo", "nem rola", "sem chance de", "não tem como"
            ],
            
            "acao_negociacao": [
                "parcelar", "dar um desconto", "reduzir os juros", "fazer um acordo",
                "negociar esse valor", "reduzir essa multa"
            ],
            
            "conector_alternativa": ["mas", "porém", "só que", "então"],
            
            # Componentes para problemas identificados
            "consigo": ["consigo pagar", "consigo fazer", "consigo mandar", "consigo depositar"],
            "valor_menor": ["valor menor", "um valor mais baixo", "algo mais barato", "desconto"],
            "modificador_valor": ["demais", "muito", "puxado", "salgado"],
            
            "tempo_negativo": ["hoje", "agora", "esse mês", "essa semana"],
            "tempo_positivo": ["amanhã", "semana que vem", "mês que vem", "depois"],
            "valor_alto": ["R$ 800", "R$ 1000", "R$ 1500"],
            "valor_baixo": ["R$ 200", "R$ 300", "R$ 400"]
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
        """Mapeia nome do placeholder para tipo de entidade"""
        # Placeholders que não são entidades (modificadores, conectores)
        nao_entidades = ["conector_alternativa", "modificador_valor", "intensificador", 
                        "expressao_intensidade", "adverbio_negacao"]
        
        if placeholder in nao_entidades:
            return None  # Não são entidades relevantes
        elif "acao_pagamento" in placeholder or "consigo" in placeholder:
            return TipoEntidade.PAGAMENTO
        elif "tempo" in placeholder:
            return TipoEntidade.TEMPO
        elif "valor" in placeholder and "menor" not in placeholder:
            return TipoEntidade.VALOR
        elif "valor_menor" in placeholder or "desconto" in placeholder or "parcel" in placeholder:
            return TipoEntidade.CONDICAO  # "valor menor" é uma condição de negociação
        elif "condicao" in placeholder or "situacao" in placeholder or placeholder in ["acao_negociacao"]:
            return TipoEntidade.CONDICAO
        elif placeholder in ["expressao_impossibilidade", "expressao_negativa", "expressao_temporal_negativa"]:
            return TipoEntidade.CONDICAO
        else:
            return TipoEntidade.CONDICAO  # Default
    
    def determinar_atributos_por_categoria(self, categoria, entidade_texto, frase, posicao_entidade):
        """Determina orientação e modalidade baseada na CATEGORIA do template"""
        
        # PAGAMENTO_POSITIVO: todas entidades são positivas e afirmadas/planejadas
        if categoria == "PAGAMENTO_POSITIVO":
            orientacao = Orientacao.POSITIVA
            
            # Verifica se há condições na frase que tornam tudo CONDICIONAL
            palavras_condicionais = ["só", "apenas", "somente", "no máximo", "até", "quando muito", 
                                   "metade", "desconto", "parcel", "se", "quando", "caso", "consegui juntar"]
            if any(palavra in frase.lower() for palavra in palavras_condicionais):
                modalidade = Modalidade.CONDICIONAL
            elif re.search(r'\b(pago|quito|acerto|mando|deposito|transfiro|faço|pagar|quitar|fazer|consigo)\b', 
                        entidade_texto.lower()):
                modalidade = Modalidade.AFIRMADO
            else:
                modalidade = Modalidade.PLANEJADO
                
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
        # Verifica conectores que mudam o sentido
        pos_mas = -1
        for conector in ["mas", "porém", "só que", "então"]:
            if conector in frase.lower():
                pos_mas = frase.lower().find(conector)
                break
        
        if pos_mas != -1:
            # Se a entidade vem DEPOIS do conector, é positiva (mas condicional)
            if posicao_entidade > pos_mas:
                return Orientacao.POSITIVA, Modalidade.CONDICIONAL
            else:
                return Orientacao.NEGATIVA, Modalidade.NEGADO
        
        # Default se não achou conector
        return Orientacao.POSITIVA, Modalidade.CONDICIONAL
    
    def _analisar_simples(self, entidade_texto, frase):
        """Analisa frases simples baseado no contexto"""
        # Expressões fortemente negativas
        indicadores_negativos = ["impossível", "ferrado", "duro", "liso", "sem", "não", 
                               "nem se eu quisesse", "não vai dar", "é impossível", "fora da realidade"]
        palavras_limitadoras = ["só", "apenas", "somente", "no máximo", "até", "quando muito"]
        
        # Verifica se a entidade ou contexto tem expressões negativas
        if any(ind in entidade_texto.lower() for ind in indicadores_negativos) or \
           any(ind in frase.lower() for ind in indicadores_negativos):
            return Orientacao.NEGATIVA, Modalidade.NEGADO
        elif any(palavra in frase.lower() for palavra in palavras_limitadoras):
            return Orientacao.POSITIVA, Modalidade.CONDICIONAL
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
        if re.search(r'\b(hoje|agora|já)\b', entidade_texto.lower()):
            return ReferenciatTemporal.PRESENTE
        elif re.search(r'\b(amanhã|depois|semana que vem|mês que vem|ano que vem)\b', entidade_texto.lower()):
            return ReferenciatTemporal.FUTURO
        
        # Para outras entidades, analisa contexto temporal da frase
        indicadores_futuro = ["amanhã", "depois", "semana que vem", "mês que vem", "ano que vem", 
                             "vou", "vai", "quando", "futuro", "próxim"]
        indicadores_presente = ["hoje", "agora", "já", "neste momento"]
        
        # Prioriza indicadores de futuro
        if any(palavra in frase.lower() for palavra in indicadores_futuro):
            return ReferenciatTemporal.FUTURO
        elif any(palavra in frase.lower() for palavra in indicadores_presente):
            return ReferenciatTemporal.PRESENTE
        else:
            return ReferenciatTemporal.PRESENTE  # Default
    
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
        frase_final = self._aplicar_erros_naturais(frase)
        
        return frase_final, entidades
    
    def criar_entidades_com_atributos(self, entidades_mapeadas, categoria, frase):
        """Converte mapeamento de entidades para objetos Entidade com atributos corretos"""
        entidades = []
        
        for ent_map in entidades_mapeadas:
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
    for i in range(5):
        frase, entidades = gerador.gerar_frase()
        print(f"\n{i+1}. '{frase}'")
        for ent in entidades:
            print(f"   → '{ent.texto}' ({ent.tipo.value}) - {ent.orientacao.value} - {ent.modalidade.value} - {ent.referencia_temporal.value}") 