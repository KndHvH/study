import dill
import os
import builtins  
import re
import dateparser
from text_to_num import text2num
from datetime import datetime, timedelta
import calendar

class NERBertDillWrapper:
    """Wrapper para usar a pipeline original do notebook com dill"""
    
    def __init__(self, caminho_dill_pickle):
        caminho_dill_pickle = os.path.join(os.path.dirname(__file__), caminho_dill_pickle)
        if not os.path.exists(caminho_dill_pickle):
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_dill_pickle}")
            
        print(f"Carregando pipeline com dill de {caminho_dill_pickle}...")
        
        with open(caminho_dill_pickle, 'rb') as f:
            components = dill.load(f)
            
        # Carregar componentes
        for key, value in components.items():
            if key == 'ohe_encoder':
                self.ohe = value
            elif key == 'label_encoders':
                self.encoders = value
            elif key == 'pipeline_function':
                self.pipeline_inf = value
            elif key == 'helper_functions':
                self.helper_functions = value
            else:
                setattr(self, key, value)
        
        self._configurar_contexto()
        print("Pipeline carregada com sucesso!")
    
    def _configurar_contexto(self):
        """Configura o contexto global uma única vez"""
        # Todas as variáveis que as funções precisam
        contexto = {
            'tokenizer': self.tokenizer,
            'model': self.model, 
            'ohe': self.ohe,
            'encoders': self.encoders,
            'classifiers': self.classifiers,
            'pca': self.pca,
            'scaler': self.scaler
        }
        
        # Aplicar tudo de uma vez
        for nome, valor in {**contexto, **self.helper_functions}.items():
            globals()[nome] = valor
            setattr(builtins, nome, valor)


    def _limpar_entidades(self, texto, entidade):
        """
        Limpa o texto de acordo com o tipo de entidade:
        - PAGAMENTO: mantém apenas dígitos, vírgulas e pontos; converte para número (ponto decimal).
        - TEMPO: tenta extrair data com dateparser; retorna 'YYYY-MM-DD' ou o texto original se não parsear.
        - outros: remove vírgulas, interrogações e múltiplos espaços.
        """
        # remover aspas simples e duplas
        texto = texto.replace('"', "").replace("'", "").strip()
        
        if entidade == "VALOR":
            # Primeiro tentar converter números por extenso em português
            try:
                numero_convertido = text2num(texto.lower().strip(), "pt")
                return str(float(numero_convertido))
            except:
                pass
                
            # manter só dígitos, vírgula e ponto
            limpado = re.sub(r"[^0-9,\.]", "", texto)
            # converter vírgula decimal para ponto
            try:
                num = float(limpado.replace(",", "."))
                return str(num)
            except:
                return limpado

        elif entidade == "TEMPO":
            # Verificar casos especiais primeiro (antes do dateparser)
            resultado_manual = self._verificar_casos_especiais(texto)
            if resultado_manual != texto:
                return resultado_manual
                
            # tentar parse de data em pt-BR
            dt = dateparser.parse(texto, languages=["pt"], settings={"DATE_ORDER": "DMY"})
            if dt:
                # Validar se o resultado do dateparser faz sentido
                from datetime import datetime
                hoje = datetime.now()
                # Se a data é no passado, provavelmente é um erro
                if dt < hoje - timedelta(days=2):
                    # Tentar função manual
                    return self._processar_tempo_manual(texto)
                return dt.strftime("%Y-%m-%d")
            else:
                # Se dateparser falhou, tentar lógica manual para casos específicos
                return self._processar_tempo_manual(texto)

        limpado = re.sub(r"[?,]", "", texto)
        limpado = re.sub(r"\s+", " ", limpado).strip()
        return limpado

    def _verificar_casos_especiais(self, texto):
        """
        Verifica casos especiais que devem ser processados antes do dateparser
        """
        from datetime import datetime, timedelta
        
        texto_lower = texto.lower().strip()
        
        # Padrões para número de dias específico (ex: "15 dias", "em 30 dias")
        padrao_dias = re.search(r'(\d+)\s*dias?', texto_lower)
        if padrao_dias:
            num_dias = int(padrao_dias.group(1))
            hoje = datetime.now()
            data_futura = hoje + timedelta(days=num_dias)
            return data_futura.strftime("%Y-%m-%d")
        
        # Se não é caso especial, retorna texto original
        return texto

    def _processar_tempo_manual(self, texto):
        """
        Processa expressões de tempo que o dateparser não consegue interpretar
        """
        
        texto_lower = texto.lower().strip()
        hoje = datetime.now()
        
        # Mapeamento de dias da semana em português
        dias_semana = {
            'segunda': 0, 'seg': 0, 'segunda-feira': 0,
            'terca': 1, 'terça': 1, 'ter': 1, 'terça-feira': 1, 'terca-feira': 1,
            'quarta': 2, 'qua': 2, 'quarta-feira': 2,
            'quinta': 3, 'qui': 3, 'quinta-feira': 3,
            'sexta': 4, 'sex': 4, 'sexta-feira': 4,
            'sabado': 5, 'sábado': 5, 'sab': 5, 'sábado-feira': 5,
            'domingo': 6, 'dom': 6
        }
        
        # Padrões para próximo dia da semana
        for dia_nome, dia_num in dias_semana.items():
            padroes = [
                f'proxima {dia_nome}', f'próxima {dia_nome}', f'{dia_nome} que vem',
                f'para a proxima {dia_nome}', f'para a próxima {dia_nome}',
                f'no proximo {dia_nome}', f'no próximo {dia_nome}'
            ]
            
            if any(padrao in texto_lower for padrao in padroes):
                # Calcular próximo dia da semana
                dias_ate_dia = (dia_num - hoje.weekday()) % 7
                if dias_ate_dia == 0:  # Se hoje é o mesmo dia
                    dias_ate_dia = 7
                proximo_dia = hoje + timedelta(days=dias_ate_dia)
                return proximo_dia.strftime("%Y-%m-%d")
        
        # Padrões para semanas específicas
        if 'primeira semana' in texto_lower:
            if 'mes que vem' in texto_lower or 'mês que vem' in texto_lower or 'proximo mes' in texto_lower or 'próximo mês' in texto_lower:
                # Primeira semana do próximo mês
                proximo_mes = hoje.replace(day=1) + timedelta(days=32)
                primeiro_dia_mes = proximo_mes.replace(day=1)
                # Encontrar a primeira segunda-feira do mês
                dias_ate_segunda = (0 - primeiro_dia_mes.weekday()) % 7
                primeira_segunda = primeiro_dia_mes + timedelta(days=dias_ate_segunda)
                return primeira_segunda.strftime("%Y-%m-%d")
        
        if 'segunda semana' in texto_lower:
            if 'mes que vem' in texto_lower or 'mês que vem' in texto_lower:
                # Segunda semana do próximo mês
                proximo_mes = hoje.replace(day=1) + timedelta(days=32)
                primeiro_dia_mes = proximo_mes.replace(day=1)
                dias_ate_segunda = (0 - primeiro_dia_mes.weekday()) % 7
                segunda_semana = primeiro_dia_mes + timedelta(days=dias_ate_segunda + 7)
                return segunda_semana.strftime("%Y-%m-%d")
        
        # Padrões para mês que vem (genérico)
        if 'mes que vem' in texto_lower or 'mês que vem' in texto_lower or 'proximo mes' in texto_lower or 'próximo mês' in texto_lower:
            proximo_mes = hoje.replace(day=1) + timedelta(days=32)
            primeiro_dia_mes = proximo_mes.replace(day=1)
            return primeiro_dia_mes.strftime("%Y-%m-%d")
        
        # Padrões para semana que vem
        if 'semana que vem' in texto_lower or 'proxima semana' in texto_lower or 'próxima semana' in texto_lower:
            # Próxima segunda-feira (início da semana)
            dias_ate_segunda = (0 - hoje.weekday()) % 7
            if dias_ate_segunda == 0:
                dias_ate_segunda = 7
            proxima_semana = hoje + timedelta(days=dias_ate_segunda)
            return proxima_semana.strftime("%Y-%m-%d")
        
        # Padrões para número de dias específico (ex: "15 dias", "em 30 dias")
        import re as regex_module
        padrao_dias = regex_module.search(r'(\d+)\s*dias?', texto_lower)
        if padrao_dias:
            num_dias = int(padrao_dias.group(1))
            data_futura = hoje + timedelta(days=num_dias)
            return data_futura.strftime("%Y-%m-%d")
        
        # Tentar parseamentos mais simples extraindo palavras-chave
        palavras = texto_lower.split()
        for palavra in palavras:
            # Limpar palavra de pontuação
            palavra_limpa = re.sub(r'[^\w]', '', palavra)
            if palavra_limpa:
                dt = dateparser.parse(palavra_limpa, languages=["pt"])
                if dt:
                    return dt.strftime("%Y-%m-%d")
        
        # Tentar alguns parseamentos alternativos
        alternativas = [
            texto_lower.replace('para a ', '').replace('para o ', ''),
            texto_lower.replace('?', '').replace('!', ''),
            texto_lower.replace('que vem', '').strip()
        ]
        
        for alt in alternativas:
            if alt.strip():
                dt = dateparser.parse(alt.strip(), languages=["pt", "en"])
                if dt:
                    return dt.strftime("%Y-%m-%d")
        
        # Se nada funcionar, retornar texto original
        return texto
        
    def _inferir(self, frase):
        """Usa a função pipeline_inf original do notebook"""
        return self.pipeline_inf(frase, self.model, self.tokenizer, 
                                self.classifiers, self.pca, self.scaler, 
                                self.ohe, self.encoders)
    
    def inferir(self, frase):
        entidades = self._inferir(frase)
        for ent in entidades:
            ent['texto'] = self._limpar_entidades(ent['texto'], ent['entidade'])
        return entidades
    
    def relatorio(self, frase, entidades=None):
        """Gera relatório usando a função original"""
        if entidades is None:
            entidades = self.inferir(frase)
        return gerar_relatorio(frase, entidades) # type: ignore