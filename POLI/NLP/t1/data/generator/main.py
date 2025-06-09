#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script principal para o gerador melhorado de frases sintéticas.
Melhorias:
- Frases mais reais e ricas com múltiplas entidades
- Classes balanceadas com distribuição natural  
- Valores e parcelamentos gerados dinamicamente
- Formato de saída compatível com labeled_data.json
"""

import os
import argparse
from gerador import GeradorFrases

def main():
    """Função principal para execução do gerador melhorado"""
    parser = argparse.ArgumentParser(
        description='Gerador melhorado de frases sintéticas para treinamento de NER',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py --amostras 1000
  python main.py --amostras 500 --saida ./frases_v2.json
  python main.py --test  # Para testar apenas algumas frases
        """
    )
    
    parser.add_argument('--amostras', type=int, default=2000, 
                        help='Número de frases a serem geradas (padrão: 2000)')
    parser.add_argument('--saida', type=str, default='./frases_rotuladas.json',
                        help='Caminho para arquivo de saída JSON (padrão: ./frases_rotuladas.json)')
    parser.add_argument('--test', action='store_true',
                        help='Modo teste: gera apenas 10 frases para validação')
    parser.add_argument('--seed', type=int, default=None,
                        help='Seed para reprodutibilidade (opcional)')
    
    args = parser.parse_args()
    
    # Configurar seed se fornecido
    if args.seed:
        import random
        random.seed(args.seed)
        print(f"🔧 Seed definido: {args.seed}")
    
    # Criar diretório de saída se não existir
    os.makedirs(os.path.dirname(os.path.abspath(args.saida)), exist_ok=True)
    
    # Inicializar gerador
    print("🚀 Inicializando gerador melhorado...")
    gerador = GeradorFrases()
    
    if args.test:
        # Modo teste - apenas mostrar algumas frases
        print("\n🧪 MODO TESTE - Gerando frases de exemplo:")
        print("=" * 60)
        
        for i in range(10):
            frase, entidades = gerador.gerar_frase()
            print(f"\n{i+1:2d}. 💬 {frase}")
            
            for j, ent in enumerate(entidades):
                print(f"    {j+1}. 🏷️  '{ent.texto}'")
                print(f"        Tipo: {ent.tipo.value}")
                print(f"        Orientação: {ent.orientacao.value}")
                print(f"        Modalidade: {ent.modalidade.value}")
                print(f"        Ref. Temporal: {ent.referencia_temporal.value}")
        
        print("\n✅ Teste concluído! O gerador está funcionando corretamente.")
        print("💡 Para gerar dataset completo, execute sem --test")
        
    else:
        # Modo produção - gerar dataset completo
        print(f"📝 Gerando {args.amostras} frases sintéticas...")
        print(f"💾 Arquivo de saída: {args.saida}")
        print("⏳ Processando...")
        
        gerador.gerar_dataset_balanceado(
            n_amostras=args.amostras, 
            output_file=args.saida
        )
        
        print("\n✅ Geração concluída com sucesso!")
        print(f"📁 Arquivo salvo em: {os.path.abspath(args.saida)}")
        

if __name__ == "__main__":
    main() 