import random
import re
import json
from templates import templates, variacoes

class GeradorFrases:
    def __init__(self, taxa_erro: float = 0.2):
        self.templates = templates
        self.variacoes = variacoes
        self.taxa_erro = taxa_erro

    def gerar_frase(self, tipo_frase=None):
        """
        Gera uma frase aleatória com base nos templates disponíveis, simulando erros de digitação.
        Args:
            tipo_frase: Tipo específico de frase para gerar (se None, escolhe aleatoriamente)
        Returns:
            Frase gerada (string), possivelmente com erros de digitação
        """
        if tipo_frase is None:
            tipo_frase = random.choice(list(self.templates.keys()))
        template = random.choice(self.templates[tipo_frase])
        placeholders = re.findall(r'\{([^}]+)\}', template)
        frase = template
        for placeholder in placeholders:
            if placeholder in self.variacoes:
                variacao = random.choice(self.variacoes[placeholder])
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
        Gera um dataset de frases em formato JSON para Label Studio
        Args:
            n_amostras: Número de frases a serem geradas
            output_file: Caminho para o arquivo de saída
        """
        # Lista para armazenar todas as frases como objetos
        frases_json = []
        
        # Gerar frases e adicionar ao formato adequado para Label Studio
        for _ in range(n_amostras):
            frase = self.gerar_frase()
            # Cada frase é um objeto com a chave "text"
            frases_json.append({"text": frase})
        
        # Salvar como JSON (array de objetos)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(frases_json, f, ensure_ascii=False, indent=2)
        
        print(f"Dataset gerado com {n_amostras} frases e salvo em {output_file} (formato Label Studio)")

