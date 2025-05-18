# Extração de Entidades em Negociações Financeiras

Sistema de inteligência artificial para extração de entidades estruturadas de frases informais no contexto de negociação financeira, como mensagens de WhatsApp, SMS e e-mails.

## Visão Geral

Este projeto tem como objetivo desenvolver um sistema de inteligência artificial capaz de extrair entidades ricas e estruturadas de frases informais no contexto de negociação financeira, transformando-as em uma estrutura semântica interpretável no formato JSON.

O sistema identifica e classifica entidades como:

- **TEMPO**: expressões temporais como "amanhã", "essa semana", "depois do almoço"
- **VALOR**: expressões monetárias como "R$500", "mil reais", "50%"
- **PAGAMENTO**: intenções de pagamento como "vou pagar", "não consigo pagar", "comprometo"
- **CONDIÇÃO**: condicionais como "quando receber o adiantamento", "com juros", "se sobrar dinheiro"
- **FORMA_PAGAMENTO**: métodos como "boleto", "transferência", "dinheiro"

Para cada entidade, o sistema extrai atributos como:
- **Orientação**: positiva, negativa ou neutra
- **Modalidade**: afirmado, planejado, incerto, negado, condicional
- **Referência temporal**: presente, passado, futuro
- **Explicitude**: explícito ou implícito

## Abordagem Técnica

Em vez de usar modelos de linguagem baseados em instruções (como T5 ou GPT), o projeto utiliza modelos encoder-only como BERT, operando por meio de:

1. **Rotulagem BIO**: Identificação dos spans das entidades usando tags Begin, Inside, Outside
2. **Extração de Embeddings**: Vetores extraídos diretamente das camadas do BERT para cada entidade
3. **Classificação Supervisionada**: Redes neurais densas (MLPs) treinadas para classificar os atributos semânticos

O pipeline de processamento funciona da seguinte forma:
- A frase é processada pelo BERT para detectar spans de entidades
- Para cada entidade, são extraídos embeddings (vetor médio da entidade, vetor da frase, contexto local)
- Esses vetores são concatenados e alimentam classificadores que determinam os atributos semânticos
- O resultado final é estruturado em JSON, com informações completas sobre cada entidade

## Estrutura do Projeto

```
.
├── data/                      # Dados para treinamento e avaliação
│   ├── generator/             # Gerador de frases sintéticas
│   ├── frases_sinteticas.json # Frases geradas para treinamento
│   ├── labeled_data.json      # Dados anotados para treinamento
│   └── label.xml              # Template de anotação para Label Studio
├── src/                       # Código-fonte principal
├── modelos/                   # Modelos treinados
└── notebooks/                 # Notebooks para exploração e análise
```

## Componentes

1. **Gerador de Frases**: Cria frases sintéticas baseadas em templates parametrizáveis, incluindo mecanismos para simular erros de digitação comuns.

2. **Anotação com Label Studio**: Interface para anotação manual de entidades nas frases, com exportação em formato JSON contendo posições de início e fim de cada entidade e seus atributos.

3. **Pipeline de Extração**: Transformação de textos em representações vetoriais e classificação de atributos semânticos usando BERT e classificadores MLP.

## Esquema de Anotação

O esquema de anotação atual define:

1. **Cinco tipos principais de entidades**:
   - TEMPO: quando ocorre uma ação ("amanhã", "depois do almoço")
   - VALOR: quantias monetárias ("R$ 1.111,11", "600 reais")
   - PAGAMENTO: ações relacionadas a pagamento ("vou pagar", "não tenho como")
   - CONDIÇÃO: pré-condições e qualificadores ("quando receber", "se sobrar dinheiro")
   - FORMA_PAGAMENTO: método de pagamento ("boleto", "transferência")

2. **Quatro dimensões de atributos**:
   - **Orientação**: atitude/sentimento associado à entidade
     - positiva: indica disposição para pagar
     - negativa: indica recusa ou dificuldade
     - neutra: sem carga emocional clara
   
   - **Modalidade**: status factual da entidade
     - afirmado: fato concreto ("fiz o pagamento")
     - planejado: intenção futura ("vou pagar")
     - incerto: dúvida ou incerteza ("é 500 com juros?")
     - negado: recusa ou impossibilidade ("não consigo pagar")
     - condicional: dependente de condição ("se eu vender")
   
   - **Referência temporal**: quando ocorre
     - presente: ocorrendo agora ou em tempo indefinido
     - passado: já ocorreu ("paguei")
     - futuro: ocorrerá ("amanhã")
   
   - **Explicitude**: quão direta é a informação
     - explícito: claramente declarado
     - implícito: indiretamente sugerido

## Estado Atual do Projeto

Já realizamos:
- [x] Criação de templates de mensagens informais
- [x] Implementação de mecanismo de simulação de erros de digitação
- [x] Definição completa do esquema de anotação de entidades
- [x] Configuração do ambiente Label Studio com template personalizado
- [x] Anotação de conjunto inicial com ~50 exemplos de mensagens
- [x] Estruturação dos dados anotados em formato JSON

## Roadmap Detalhado

### 1. Geração de Dados Sintéticos
- [x] Criar estrutura básica do gerador
- [x] Desenvolver templates informais para mensagens de WhatsApp
- [x] Implementar mecanismo de introdução de erros de digitação
- [x] Gerar conjunto inicial de frases sintéticas
- [x] Adicionar maior variabilidade nos templates


### 3. Pré-processamento dos Dados
- [ ] Implementar tokenização com BERT
- [ ] Desenvolver algoritmo para mapear spans anotados para tokens BERT
- [ ] Extrair embeddings das camadas do modelo
- [ ] Criar pipeline de transformação de dados anotados para features
- [ ] Implementar divisão estratificada em treino/validação/teste

### 4. Detecção de Entidades (NER)
- [ ] Implementar modelo de rotulagem BIO usando BERT
- [ ] Treinar detector de spans de entidades
- [ ] Avaliar performance com métricas de precisão/recall/F1
- [ ] Otimizar hiperparâmetros do modelo
- [ ] Implementar mecanismos para lidar com erros ortográficos

### 5. Classificação de Atributos
- [ ] Desenvolver arquitetura MLP para classificação
- [ ] Treinar classificadores para cada tipo de atributo:
  - [ ] Tipo de entidade
  - [ ] Orientação
  - [ ] Modalidade
  - [ ] Referência temporal
  - [ ] Explicitude
- [ ] Avaliar desempenho de cada classificador
- [ ] Realizar análise de erros e refinamento

### 6. Integração e Pipeline Completo
- [ ] Desenvolver pipeline unificado de processamento
- [ ] Implementar geração de saída JSON estruturada
- [ ] Otimizar desempenho e latência
- [ ] Criar testes automatizados para o sistema completo
- [ ] Documentar API e interfaces

### 7. Avaliação e Refinamento
- [ ] Desenvolver métricas de avaliação específicas para o domínio
- [ ] Realizar testes com dados reais de conversas
- [ ] Identificar e corrigir casos problemáticos
- [ ] Realizar nova rodada de treinamento com dados ampliados
- [ ] Comparar desempenho com baseline e alternativas

### 8. Implantação
- [ ] Desenvolver API REST para o serviço
- [ ] Criar documentação técnica e de usuário
- [ ] Implementar monitoramento e logging
- [ ] Desenvolver mecanismos de feedback para melhoria contínua
- [ ] Preparar exemplos de integração

## Desenvolvedores

Para configurar o ambiente de desenvolvimento:

```bash
# Instalar dependências de desenvolvimento
uv add -d black isort flake8 pytest

# Instalar dependências do projeto
uv add pandas numpy spacy torch transformers
uv add "label-studio[data-sdk]"
```

## Próximos Passos

- [x] Expandir o conjunto de templates e variações
- [x] Melhorar o algoritmo de geração de erros
- [x] Implementar interface para anotação no Label Studio
- [ ] Aumentar o conjunto de dados anotados (meta: 200+ exemplos)
- [ ] Treinar modelo BERT customizado para NER
- [ ] Implementar classificadores para atributos de entidades
- [ ] Desenvolver API para processamento de novas mensagens 