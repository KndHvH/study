#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script principal para geração de frases sintéticas para treinamento
de modelo de extração de entidades em negociações financeiras.
"""

import os
import argparse
from geradores import GeradorFrases

def main():
    """Função principal para execução do gerador de frases"""
    parser = argparse.ArgumentParser(description='Gerador de frases sintéticas para treinamento de NER')
    parser.add_argument('--amostras', type=int, default=1000, 
                        help='Número de frases a serem geradas')
    parser.add_argument('--saida', type=str, default='./frases_sinteticas.json',
                        help='Caminho para arquivo de saída JSON')
    parser.add_argument('--taxa-erro', type=float, default=0.2,
                        help='Taxa de erro de digitação (0.0 a 1.0)')
    args = parser.parse_args()
    
    # Criar diretório de saída se não existir
    os.makedirs(os.path.dirname(args.saida), exist_ok=True)
    
    # Inicializar gerador
    gerador = GeradorFrases(taxa_erro=args.taxa_erro)
    
    # Gerar dataset
    print(f"Gerando {args.amostras} frases sintéticas...")
    gerador.gerar_dataset(n_amostras=args.amostras, output_file=args.saida)
    
    print("✓ Geração concluída!")
    print(f"✓ Arquivo salvo em: {args.saida}")
    


if __name__ == "__main__":
    main() 