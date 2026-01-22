from . import tabelas
import numpy as np

class JogadorTabelaPosicoes():
  def __init__(self, indice_coeficientes, coordenadas_com_coeficiente, tabela_primeiro_jogador, tabela_segundo_jogador):
    self._lins = len(indice_coeficientes)
    self._cols = len(indice_coeficientes[0])
    self._idxcoef = indice_coeficientes
    self._tabela_1 = tabela_primeiro_jogador
    self._tabela_2 = tabela_segundo_jogador

  def nova_partida(self, jogo, jogador, id_oponente = None):
    self._jogador = jogador
    self._tabela = self._tabela_1 if self._jogador == 1 else self._tabela_2

  # Combinação linear de pesos e posições
  def _valor_pesos(self, jogo):
    val = 0.0
    for i in range(self._lins):
      for j in range(self._cols):
        val += jogo.posicao((i,j))*self._tabela[self._idxcoef[i][j]]
    return val*self._jogador

  # Tangente hiperbólica, mantém o valor entre -1 e 1
  def _avalia_posicao(self, jogo):
    return 2/(1+np.exp(-2*self._valor_pesos(jogo)))-1

  def _avalia_jogada(self, jogo, jogada):
    return self._avalia_posicao(jogo.joga(jogada))

  def escolhe_jogada(self, jogo):
    jogadas_possiveis = jogo.jogadas_legais()
    valores = [self._avalia_jogada(jogo, jogada) for jogada in jogadas_possiveis]
    return jogadas_possiveis[np.argmax(valores)]

  def informa_propria_jogada(self, tabuleiro_antes, jogada, tabuleiro_depois):
    pass

  def informa_jogada_oponente(self, tabuleiro_antes, jogada, tabuleiro_depois):
    pass

  def informa_fim(self, jogo_final):
    pass

def cria_jogador():
    return JogadorTabelaPosicoes(tabelas.indice_coeficientes, tabelas.coordenadas_com_coeficiente, tabelas.tabela_primeiro_jogador, tabelas.tabela_segundo_jogador)
