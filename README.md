# MVP AutoTest

Um protótipo acadêmico de automação multiagente para orquestração de testes em Android.

Este projeto foi desenvolvido para a disciplina "Aplicações em Machine Learning" da pós-graduação do CIn-UFPE. O objetivo é demonstrar uma aplicação de agentes de IA no contexto de testes mobile e servir como exemplo prático para a criação de agentes de IA.

O repositório demonstra uma arquitetura de agentes Planner/Executor que usa um modelo LLM para gerar planos de teste e, em seguida, executá-los por meio de ferramentas de automação de dispositivos Android.

## O que faz

- `src/main.py` cria uma equipe de agentes com um Planner e um Executor.
- O Planner constrói um plano de teste passo a passo a partir das instruções do usuário.
- O Executor executa o plano usando ferramentas de automação Android e auxiliares locais `uiautomator`.
- Os agentes compartilham memória por meio de um banco de dados SQLite e podem carregar skills locais de `src/skills`.

## Componentes principais

- `src/main.py` – ponto de entrada da aplicação e camada de orquestração.
- `src/utils.py` – funções auxiliares para carregar arquivos de prompt, dados de teste JSON e localizar dispositivos Android.
- `src/uiautomator.py` – integração com ferramentas Android usada pelo Executor.
- `src/EXECUTOR_INSTRUCTIONS.md` / `src/PLANNER_INSTRUCTIONS.md` – instruções de prompt para cada agente.
- `src/test_instructions.json` – instruções de teste de exemplo usadas para conduzir a execução de automação.
- `src/skills/` – diretórios de skills locais usados pelo framework de agentes.
- `docs/` – material de referência de arquitetura para orquestração, skills e ferramentas.

## Requisitos

- Python 3.11+ (recomendado)
- `adb` instalado e configurado no PATH
- Dispositivo Android conectado e acessível via `adb devices`
- Modelo compatível com Ollama e chave de API

## Configuração

1. Ative o ambiente Python:

```bash
source src/.venv/bin/activate
```

2. Instale as dependências usando o arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

3. Crie um arquivo `.env` em `src/` com sua chave de API do Ollama:

```env
OLLAMA_API_KEY=sua_chave_aqui
```

> Você pode usar outros modelos seguindo a [documentação do agno](https://github.com/agno-agi/agno/tree/main/cookbook/90_models)

## Execução

A partir da raiz do repositório, execute:

```bash
python src/main.py
```

Isso irá carregar os agentes planner e executor, preparar o prompt de teste a partir de `src/test_instructions.json` e executar o fluxo de automação.

## Observações

- O projeto atualmente usa o modelo `gemma4:31b-cloud` via Ollama por padrão.
- O arquivo de banco de dados SQLite é criado em `src/db/agent_memory.db`.
- Agentes e skills são carregados de `src/skills` e de um framework de agentes local.

## Documentação útil

- `docs/orquestração.md` – princípios e padrões de orquestração
- `docs/skills.md` – design e estrutura de skills
- `docs/tools.md` – orientação sobre integração de ferramentas para agentes
