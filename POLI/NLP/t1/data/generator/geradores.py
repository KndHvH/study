import random
import re
import json
from templates import templates, variacoes
from num2words import num2words

class GeradorValorMonetario:
    def __init__(self):
        self.formatos = [
            "R$ {valor}",
            "{valor} reais",
            "{valor_extenso} reais",
            "{valor}",
            "{valor}",
            "{valor}",
        ]
        
    def gerar_valor_2d(self):
        """Gera um valor com 2 dígitos (10-99)"""
        return str(random.randint(10, 99))
    
    def gerar_valor_3d(self):
        """Gera um valor com 3 dígitos (100-999)"""
        return str(random.randint(100, 999))
    
    def gerar_valor_decimal(self):
        """Gera um valor decimal no formato XXX,YY"""
        inteiro = random.randint(10, 999)
        decimal = random.randint(0, 99)
        return f"{inteiro},{decimal:02d}"
    
    def valor_por_extenso(self, valor):
        """Converte um valor numérico para extenso em português"""
        try:
            return num2words(int(valor), lang='pt_BR')
        except:
            return valor
    
    def gerar_valor(self):
        """Gera um valor monetário em um formato aleatório"""
        formato = random.choice(self.formatos)
        
        # Decide qual tipo de valor gerar
        tipo_valor = random.choice(['2d', '3d', 'decimal'])
        if tipo_valor == '2d':
            valor = self.gerar_valor_2d()
        elif tipo_valor == '3d':
            valor = self.gerar_valor_3d()
        else:
            valor = self.gerar_valor_decimal()
            
        if formato == "{valor_extenso} reais":
            # Para valor por extenso, usamos apenas a parte inteira
            valor_base = valor.split(',')[0] if ',' in valor else valor
            return formato.replace("{valor_extenso}", self.valor_por_extenso(valor_base))
        else:
            return formato.replace("{valor}", valor)

class GeradorTempo:
    def __init__(self):
        self.formatos_dia = [
            "dia {dia}",
            "no dia {dia}",
            "até dia {dia}",
            "depois do dia {dia}",
            "antes do dia {dia}",
        ]
        
        self.formatos_dia_mes_atual = [
            "dia {dia} desse mês",
            "no dia {dia} desse mês",
            "até dia {dia} desse mês",
            "dia {dia} ainda esse mês",
        ]
        
        self.formatos_dia_proximo_mes = [
            "dia {dia} do próximo mês",
            "dia {dia} mês que vem",
            "no dia {dia} do mês que vem",
            "até dia {dia} do próximo mês",
        ]
        
        self.formatos_mes_especifico = [
            "em {mes}",
            "no {mes}",
            "até {mes}",
            "quando chegar {mes}",
            "lá pro {mes}",
            "só em {mes}",
        ]
        
        self.formatos_dia_mes_especifico = [
            "dia {dia} de {mes}",
            "no dia {dia} de {mes}",
            "até dia {dia} de {mes}",
            "lá pro dia {dia} de {mes}",
        ]
        
        self.formatos_prazo_dias = [
            "em {numero} dias",
            "daqui {numero} dias",
            "dentro de {numero} dias",
            "até {numero} dias",
        ]
        
        self.formatos_prazo_horas = [
            "em {numero} horas",
            "daqui {numero} horas",
            "até {numero} horas",
        ]
        
        self.formatos_prazo_meses = [
            "mês que vem",
            "no próximo mês",
            "em {numero} meses",
            "daqui {numero} meses",
        ]
        
        self.meses = [
            "janeiro", "fevereiro", "março", "abril", "maio", "junho",
            "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
        ]
        
        self.tempos_fixos = [
            "amanhã", "hoje", "agora", "depois",
            "semana que vem", "mês que vem", "no final do mês",
            "quando receber meu salário", "sexta", "final de semana",
            "segunda", "quando eu receber", "assim que cair o dinheiro",
            "quando entrar meu pagamento", "quando eu tiver o dinheiro", "amanhã cedo",
            "ainda hoje", "mais tarde", "daqui a pouco", "essa semana", "esse mês",
            "terça que vem", "quarta-feira", "quinta", "sábado", 
            "na hora do almoço", "depois do expediente", "antes das 18h",
            "dia do pagamento", "na próxima semana",
            "depois de amanhã", "antes do fim do mês",
            "depois do expediente", "fim do dia", "começo do mês", "depois do almoço"
        ]
    
    def gerar_dia_mes(self):
        """Gera um dia do mês realista (1-28, com foco nos dias de pagamento comuns)"""
        # Dias mais comuns para pagamentos: 1, 5, 10, 15, 20, 25, 30
        dias_comuns = [1, 5, 10, 15, 20, 25, 30]
        # 70% chance de ser um dia comum, 30% qualquer dia até 28
        if random.random() < 0.7:
            return str(random.choice(dias_comuns))
        else:
            return str(random.randint(1, 28))
    
    def gerar_prazo_dias(self):
        """Gera um prazo em dias realista (1-45 dias, mais comum até 30)"""
        # 80% chance de ser até 30 dias, 20% até 45 dias
        if random.random() < 0.8:
            return str(random.randint(1, 30))
        else:
            return str(random.randint(31, 45))
    
    def gerar_prazo_horas(self):
        """Gera um prazo em horas realista (1-72 horas)"""
        # Horas comuns: 24, 48, 72, ou números menores
        horas_comuns = [24, 48, 72]
        if random.random() < 0.4:
            return str(random.choice(horas_comuns))
        else:
            return str(random.randint(1, 24))
    
    def gerar_prazo_meses(self):
        """Gera um prazo em meses realista (1-6 meses)"""
        return str(random.randint(1, 6))
    
    def gerar_tempo(self):
        """Gera uma expressão temporal variada e realista"""
        # Pesos ajustados para incluir as novas opções
        tipo_tempo = random.choices(
            ['fixo', 'dia', 'dia_mes_atual', 'dia_proximo_mes', 'mes_especifico', 
             'dia_mes_especifico', 'prazo_dias', 'prazo_horas', 'prazo_meses'],
            weights=[20, 15, 12, 12, 8, 8, 7, 2, 1]
        )[0]
        
        if tipo_tempo == 'fixo':
            return random.choice(self.tempos_fixos)
        elif tipo_tempo == 'dia':
            formato = random.choice(self.formatos_dia)
            dia = self.gerar_dia_mes()
            return formato.replace("{dia}", dia)
        elif tipo_tempo == 'dia_mes_atual':
            formato = random.choice(self.formatos_dia_mes_atual)
            dia = self.gerar_dia_mes()
            return formato.replace("{dia}", dia)
        elif tipo_tempo == 'dia_proximo_mes':
            formato = random.choice(self.formatos_dia_proximo_mes)
            dia = self.gerar_dia_mes()
            return formato.replace("{dia}", dia)
        elif tipo_tempo == 'mes_especifico':
            formato = random.choice(self.formatos_mes_especifico)
            mes = random.choice(self.meses)
            return formato.replace("{mes}", mes)
        elif tipo_tempo == 'dia_mes_especifico':
            formato = random.choice(self.formatos_dia_mes_especifico)
            dia = self.gerar_dia_mes()
            mes = random.choice(self.meses)
            return formato.replace("{dia}", dia).replace("{mes}", mes)
        elif tipo_tempo == 'prazo_dias':
            formato = random.choice(self.formatos_prazo_dias)
            numero = self.gerar_prazo_dias()
            return formato.replace("{numero}", numero)
        elif tipo_tempo == 'prazo_horas':
            formato = random.choice(self.formatos_prazo_horas)
            numero = self.gerar_prazo_horas()
            return formato.replace("{numero}", numero)
        else:  # prazo_meses
            if random.random() < 0.5:
                return random.choice(["mês que vem", "no próximo mês"])
            else:
                formato = random.choice(["em {numero} meses", "daqui {numero} meses"])
                numero = self.gerar_prazo_meses()
                return formato.replace("{numero}", numero)

class GeradorFrases:
    def __init__(self, taxa_erro: float = 0.2):
        self.templates = templates
        self.variacoes = variacoes
        self.taxa_erro = taxa_erro
        self.gerador_valor = GeradorValorMonetario()
        self.gerador_tempo = GeradorTempo()
        
        # Sistema de pesos para templates
        # Pesos maiores = mais frequentes na geração
        self.pesos_templates = {
            # Templates principais (mais importantes para o modelo)
            "PAGAMENTO": 3.0,    # Frases sobre pagamentos são muito importantes
            "VALOR": 3.0,        # Frases sobre valores são muito importantes  
            "TEMPO": 3.0,        # Frases sobre tempo são muito importantes
            "CONDIÇÃO": 3.0,     # Frases sobre condições são muito importantes
            
            # Templates secundários (menos frequentes)
            "DIFICULDADE": 1.0,  # Frases sobre dificuldades
            "NEGOCIAÇÃO": 1.0,   # Frases sobre negociação
        }

    def escolher_tipo_frase_com_peso(self):
        """Escolhe um tipo de frase baseado nos pesos definidos"""
        tipos = list(self.pesos_templates.keys())
        pesos = list(self.pesos_templates.values())
        
        # Normalizar pesos para que somem 1
        total_peso = sum(pesos)
        pesos_normalizados = [p / total_peso for p in pesos]
        
        return random.choices(tipos, weights=pesos_normalizados)[0]

    def gerar_frase(self, tipo_frase=None):
        """
        Gera uma frase aleatória com base nos templates disponíveis, simulando erros de digitação.
        Args:
            tipo_frase: Tipo específico de frase para gerar (se None, escolhe com base nos pesos)
        Returns:
            Frase gerada (string), possivelmente com erros de digitação
        """
        if tipo_frase is None:
            tipo_frase = self.escolher_tipo_frase_com_peso()
        
        template = random.choice(self.templates[tipo_frase])
        placeholders = re.findall(r'\{([^}]+)\}', template)
        frase = template
        
        for placeholder in placeholders:
            if placeholder == "valor":
                variacao = self.gerador_valor.gerar_valor()
            elif placeholder == "tempo":
                variacao = self.gerador_tempo.gerar_tempo()
            elif placeholder in self.variacoes:
                variacao = random.choice(self.variacoes[placeholder])
            else:
                # Se não encontrar o placeholder, mantém o texto original
                variacao = f"{{{placeholder}}}"
            frase = frase.replace(f"{{{placeholder}}}", variacao, 1)
            
        frase_com_erros = self._introduzir_erros_digitacao(frase)
        return frase_com_erros

    def _introduzir_erros_digitacao(self, texto: str) -> str:
        """
        Introduz erros de digitação comuns em mensagens informais
        Args:
            texto: Texto original
        Returns:
            Texto com erros típicos de digitação
        """
        palavras = texto.split()
        novas_palavras = []
        for palavra in palavras:
            if len(palavra) > 3 and random.random() < self.taxa_erro:
                tipo_erro = random.choice(["troca", "omissao", "insercao", "acentuacao"])
                if tipo_erro == "troca" and len(palavra) >= 3:
                    pos = random.randint(0, len(palavra) - 2)
                    chars = list(palavra)
                    chars[pos], chars[pos + 1] = chars[pos + 1], chars[pos]
                    palavra = ''.join(chars)
                elif tipo_erro == "omissao" and len(palavra) >= 4:
                    pos = random.randint(1, len(palavra) - 2)
                    palavra = palavra[:pos] + palavra[pos+1:]
                elif tipo_erro == "insercao":
                    pos = random.randint(0, len(palavra) - 1)
                    letra = palavra[pos]
                    palavra = palavra[:pos+1] + letra + palavra[pos+1:]
                elif tipo_erro == "acentuacao" and any(c in "áàâãéèêíìîóòôõúùûç" for c in palavra):
                    acentos = {
                        'á': 'a', 'à': 'a', 'â': 'a', 'ã': 'a',
                        'é': 'e', 'è': 'e', 'ê': 'e',
                        'í': 'i', 'ì': 'i', 'î': 'i',
                        'ó': 'o', 'ò': 'o', 'ô': 'o', 'õ': 'o',
                        'ú': 'u', 'ù': 'u', 'û': 'u',
                        'ç': 'c'
                    }
                    for acento, sem_acento in acentos.items():
                        palavra = palavra.replace(acento, sem_acento)
            novas_palavras.append(palavra)
        return ' '.join(novas_palavras)
    
    def gerar_dataset(self, n_amostras: int, output_file: str):
        """
        Gera um dataset de frases com entidades identificadas
        Args:
            n_amostras: Número de frases a serem geradas
            output_file: Caminho para o arquivo de saída
        """
        frases = []
        for _ in range(n_amostras):
            frase = self.gerar_frase()
            frases.append({"text": frase})
            
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(frases, f, ensure_ascii=False, indent=2)
    
    def configurar_pesos(self, novos_pesos: dict):
        """
        Permite configurar pesos personalizados para os templates
        Args:
            novos_pesos: Dicionário com os novos pesos {tipo_template: peso}
        """
        self.pesos_templates.update(novos_pesos)

