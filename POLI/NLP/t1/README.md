# Extração de Entidades em Negociações Financeiras

Sistema de inteligência artificial para extração de entidades estruturadas de frases informais no contexto de negociação financeira, como mensagens de WhatsApp, SMS e e-mails.

## Visão Geral

Este projeto tem como objetivo desenvolver um sistema de inteligência artificial capaz de extrair entidades ricas e estruturadas de frases informais no contexto de negociação financeira, transformando-as em uma estrutura semântica interpretável no formato JSON.

O sistema identifica e classifica entidades como:

- **TEMPO**: expressões temporais como "amanhã", "nesse mês"
- **VALOR**: expressões monetárias como "R$500", "mil reais"
- **PAGAMENTO**: intenções de pagamento como "quero pagar", "vou pagar"
- **CONDIÇÃO**: condicionais como "se for à vista", "caso eu receba"
- **FORMA_PAGAMENTO**: métodos como "PIX", "12x sem juros"
- **LOCAL**: locais como "agência da Penha", "Banco do Brasil"

Para cada entidade, o sistema extrai atributos como:
- Orientação (positiva/negativa)
- Ação relacionada
- Modalidade (afirmado, planejado, incerto, negado, condicional)
- Referência temporal
- Explicitude

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
├── data/                  # Dados para treinamento e avaliação
│   ├── generator/         # Gerador de frases sintéticas
│   ├── frases_sinteticas/ # Frases geradas para treinamento
│   └── anotacoes/         # Anotações do Label Studio
├── src/                   # Código-fonte principal
├── modelos/               # Modelos treinados
└── notebooks/             # Notebooks para exploração e análise
```

## Componentes

1. **Gerador de Frases**: Cria frases sintéticas baseadas em templates parametrizáveis, incluindo mecanismos para simular erros de digitação comuns.

2. **Anotação com Label Studio**: Interface para anotação manual de entidades nas frases, com exportação em formato JSON contendo posições de início e fim de cada entidade.

3. **Pipeline de Extração**: Transformação de textos em representações vetoriais e classificação de atributos semânticos usando BERT e classificadores MLP.

## Como as Coisas Funcionarão

O fluxo de trabalho do projeto será:

1. Geração de frases sintéticas para criar dados de treinamento iniciais
2. Anotação manual das frases para marcar entidades e seus atributos
3. Transformação dos dados anotados em features vetoriais usando BERT
4. Treinamento de classificadores para cada tipo de atributo
5. Avaliação e refinamento do modelo com métricas de performance
6. Implantação do sistema como uma API para processamento de novas mensagens

## Roadmap Detalhado

### 1. Geração de Dados Sintéticos
- [x] Criar estrutura básica do gerador
- [x] Desenvolver templates informais para mensagens de WhatsApp
- [x] Implementar mecanismo de introdução de erros de digitação
- [x] Gerar conjunto inicial de frases sintéticas
- [ ] Adicionar maior variabilidade nos templates
- [ ] Implementar técnicas de data augmentation para aumentar diversidade
- [ ] Validar qualidade das frases geradas com avaliação humana

### 2. Preparação para Anotação
- [ ] Configurar ambiente Label Studio
  - [ ] Definir template de anotação customizado
  - [ ] Configurar exportação em formato compatível
  - [ ] Implementar validação de anotações
- [ ] Criar guia de anotação com exemplos
- [ ] Desenvolver sistema de avaliação de concordância entre anotadores
- [ ] Preparar interface para importação e exportação de dados

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
  - [ ] Ação relacionada
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
```

## Próximos Passos

- [ ] Expandir o conjunto de templates e variações
- [ ] Melhorar o algoritmo de geração de erros
- [ ] Implementar interface para anotação rápida
- [ ] Treinar modelo com dados reais anotados 