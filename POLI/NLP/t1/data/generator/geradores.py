import random
import re
import json
from typing import Dict, List, Tuple, Any, Optional
from templates import templates, variacoes

class GeradorFrases:
    def __init__(self, taxa_erro: float = 0.2):
        """
        Inicializa o gerador de frases
        
        Args:
            taxa_erro: Probabilidade de introduzir um erro em cada palavra (0.0 a 1.0)
        """
        self.templates = templates
        self.variacoes = variacoes
        self.taxa_erro = taxa_erro
        
    def gerar_frase(self, tipo_frase: Optional[str] = None) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Gera uma frase aleatória com base nos templates disponíveis
        
        Args:
            tipo_frase: Tipo específico de frase para gerar (se None, escolhe aleatoriamente)
            
        Returns:
            Tupla com (frase gerada, lista de entidades)
        """
        # Escolher o tipo de template se não for especificado
        if tipo_frase is None:
            tipo_frase = random.choice(list(self.templates.keys()))
            
        # Selecionar um template aleatório do tipo escolhido
        template = random.choice(self.templates[tipo_frase])
        
        # Identificar os placeholders no template
        placeholders = re.findall(r'\{([^}]+)\}', template)
        
        # Estrutura para armazenar as entidades extraídas
        entidades = []
        
        # Copiar o template para preenchimento
        frase = template
        
        # Para cada placeholder, substituir por uma variação e registrar a entidade
        for placeholder in placeholders:
            if placeholder in self.variacoes:
                variacao = random.choice(self.variacoes[placeholder])
                
                # Encontrar a posição do placeholder na frase atual
                posicao_placeholder = frase.find(f"{{{placeholder}}}")
                
                # Substituir o placeholder pela variação
                frase = frase.replace(f"{{{placeholder}}}", variacao, 1)
                
                # Registrar a entidade
                inicio = posicao_placeholder
                fim = inicio + len(variacao)
                
                # Determinar atributos da entidade
                atributos = self._gerar_atributos_entidade(placeholder, variacao)
                
                entidade = {
                    "entidade": variacao,
                    "tipo": placeholder.upper(),
                    "inicio": inicio,
                    "fim": fim,
                    **atributos
                }
                
                entidades.append(entidade)
        
        # Além da entidade explicitamente marcada pelo template,
        # também vamos identificar o tipo da frase como uma entidade
        modalidade = self._inferir_modalidade(frase)
        acao = self._identificar_acao(frase)
        
        entidade_principal = {
            "entidade": frase,
            "tipo": tipo_frase,
            "inicio": 0,
            "fim": len(frase),
            "orientacao": "positiva" if "não" not in frase.lower() else "negativa",
            "acao_relacionada": acao,
            "modalidade": modalidade,
            "referencia_temporal": self._inferir_referencia_temporal(frase),
            "explicito": True
        }
        
        # Aplicar erros de digitação à frase
        frase_com_erros = self._introduzir_erros_digitacao(frase)
        
        # Atualizar posições das entidades se a frase mudou
        if frase != frase_com_erros:
            # Aqui teríamos que recalcular as posições das entidades
            # Por simplicidade, vamos manter as posições originais por enquanto
            # Em uma implementação real, seria necessário um algoritmo mais complexo
            pass
        
        return frase_com_erros, entidades
    
    def _gerar_atributos_entidade(self, tipo: str, texto: str) -> Dict[str, Any]:
        """Gera atributos para uma entidade baseado no tipo e texto"""
        modalidade = self._inferir_modalidade(texto)
        orientacao = "positiva"
        
        # Inferir orientação
        if "não" in texto.lower() or "nao" in texto.lower():
            orientacao = "negativa"
        
        # Inferir ação relacionada
        acao = self._identificar_acao(texto)
        
        # Inferir referência temporal
        referencia_temporal = self._inferir_referencia_temporal(texto)
        
        return {
            "orientacao": orientacao,
            "acao_relacionada": acao,
            "modalidade": modalidade,
            "referencia_temporal": referencia_temporal,
            "explicito": True
        }
    
    def _inferir_modalidade(self, texto: str) -> str:
        """Infere a modalidade com base no texto"""
        texto_lower = texto.lower()
        
        # Palavras-chave para cada modalidade
        afirmado = ["vou", "irei", "farei", "pagarei", "mando"]
        planejado = ["quero", "pretendo", "planejo", "to pensando", "to querendo"]
        incerto = ["talvez", "pode ser", "quem sabe", "se der", "não sei"]
        negado = ["não", "nao", "nunca", "jamais", "nem"]
        condicional = ["se", "caso", "quando", "assim que", "desde que"]
        
        # Verificar cada conjunto de palavras-chave
        for palavras, modalidade in [
            (afirmado, "afirmado"),
            (planejado, "planejado"),
            (incerto, "incerto"),
            (negado, "negado"),
            (condicional, "condicional")
        ]:
            for palavra in palavras:
                if palavra in texto_lower:
                    return modalidade
        
        # Padrão se nenhuma modalidade for identificada
        return "afirmado"
    
    def _identificar_acao(self, texto: str) -> str:
        """Identifica a ação principal no texto"""
        acoes_comuns = {
            "pagar": ["pagar", "pagamento", "pago", "pagarei", "quitar", "pga"],
            "receber": ["receber", "recebimento", "recebo", "receberei"],
            "transferir": ["transferir", "transferencia", "transfiro", "pix", "ted"],
            "parcelar": ["parcelar", "parcelamento", "parcelo", "parcelas", "vezes"],
            "depositar": ["depositar", "deposito", "depositarei", "colocar"],
            "negociar": ["negociar", "negocio", "negociarei", "conversar", "acordo"],
            "emprestar": ["emprestar", "empresto", "emprestimo", "emprestimarei"]
        }
        
        texto_lower = texto.lower()
        
        for acao, palavras_chave in acoes_comuns.items():
            for palavra in palavras_chave:
                if palavra in texto_lower:
                    return acao
        
        return "pagar"  # ação padrão
    
    def _inferir_referencia_temporal(self, texto: str) -> str:
        """Infere a referência temporal do texto"""
        texto_lower = texto.lower()
        
        # Palavras-chave para cada referência temporal
        passado = ["paguei", "fiz", "transferi", "mandei", "já", "ja", "ontem", "semana passada"]
        presente = ["hoje", "hj", "agora", "agr", "nesse momento", "já já", "jaja"]
        futuro = ["amanhã", "amanha", "depois", "dps", "próxima", "proxima", "semana que vem", "q vem", "quando"]
        
        # Verificar cada conjunto de palavras-chave
        for palavras, tempo in [
            (passado, "passado"),
            (presente, "presente"),
            (futuro, "futuro")
        ]:
            for palavra in palavras:
                if palavra in texto_lower:
                    return tempo
        
        # Padrão se nenhuma referência for identificada
        return "futuro"
    
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
            # Decidir se aplica erro a esta palavra
            if len(palavra) > 3 and random.random() < self.taxa_erro:
                # Escolher tipo de erro
                tipo_erro = random.choice(["troca", "omissao", "insercao", "acentuacao"])
                
                if tipo_erro == "troca" and len(palavra) >= 3:
                    # Troca duas letras adjacentes de posição
                    pos = random.randint(0, len(palavra) - 2)
                    chars = list(palavra)
                    chars[pos], chars[pos + 1] = chars[pos + 1], chars[pos]
                    palavra = ''.join(chars)
                    
                elif tipo_erro == "omissao" and len(palavra) >= 4:
                    # Remove uma letra
                    pos = random.randint(1, len(palavra) - 2)  # Evita primeira e última letra
                    palavra = palavra[:pos] + palavra[pos+1:]
                    
                elif tipo_erro == "insercao":
                    # Insere uma letra repetida
                    pos = random.randint(0, len(palavra) - 1)
                    letra = palavra[pos]
                    palavra = palavra[:pos+1] + letra + palavra[pos+1:]
                    
                elif tipo_erro == "acentuacao" and any(c in "áàâãéèêíìîóòôõúùûç" for c in palavra):
                    # Remove acentuação
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
    
    def gerar_dataset(self, n_amostras: int = 100, output_file: str = "frases_sinteticas.jsonl") -> None:
        """
        Gera um conjunto de frases e salva em formato JSONL
        
        Args:
            n_amostras: Número de frases a gerar
            output_file: Arquivo de saída
        """
        dataset = []
        
        for _ in range(n_amostras):
            # Decidir aleatoriamente o tipo de frase
            tipo_frase = random.choice(list(self.templates.keys()))
            
            # Gerar frase e entidades
            frase, entidades = self.gerar_frase(tipo_frase)
            
            # Criar entrada no dataset
            entrada = {
                "texto": frase,
                "entidades": entidades
            }
            
            dataset.append(entrada)
        
        # Salvar em formato JSONL
        with open(output_file, 'w', encoding='utf-8') as f:
            for entrada in dataset:
                f.write(json.dumps(entrada, ensure_ascii=False) + '\n')
        
        print(f"Dataset gerado com {n_amostras} frases e salvo em {output_file}") 