# Ferramentas para Agentes de IA

## 1. O que são ferramentas de agentes?

Ferramentas de agentes são interfaces que permitem que modelos de linguagem (LLMs) interajam com sistemas externos. Sozinho, um LLM consegue apenas gerar texto com base no conhecimento aprendido durante o treinamento. Já as ferramentas dão ao modelo a capacidade de acessar informações em tempo real, executar ações e interagir com o mundo externo.

Na prática, elas funcionam como os “braços e pernas” de um agente de IA.

### Conhecimento vs. ação

De forma geral, as ferramentas podem ser divididas em dois grupos:

* **Ferramentas de percepção** → servem para buscar ou ler informações.
  Exemplos: pesquisa na web, consultas em banco de dados, leitura de arquivos.

* **Ferramentas de ação** → permitem modificar sistemas externos.
  Exemplos: enviar e-mails, editar arquivos, executar código ou realizar pagamentos.

### Por que isso importa?

As ferramentas transformam LLMs de simples geradores de texto em **agentes autônomos**, capazes de:

* executar tarefas completas,
* lidar com ambiguidades,
* tomar decisões ao longo de um fluxo,
* interagir com ambientes dinâmicos.

---

# 2. Arquitetura básica

Sistemas de agentes modernos funcionam a partir de um ciclo contínuo entre **raciocínio** e **execução**.

## Tool Calling

O fluxo geralmente segue estes passos:

1. o modelo identifica um objetivo,
2. escolhe a ferramenta mais adequada,
3. gera uma chamada estruturada.

Exemplo:

```json
{
  "tool": "weather_api",
  "arguments": {
    "location": "São Paulo, SP"
  }
}
```

---

## Schemas de ferramentas

Toda ferramenta deve possuir uma estrutura bem definida.

Os elementos mais importantes são:

| Componente     | Função                                                 |
| -------------- | ------------------------------------------------------ |
| `name`         | Nome único da ferramenta                               |
| `description`  | Explica o que a ferramenta faz e quando deve ser usada |
| `input_schema` | Define os parâmetros esperados                         |

Exemplo:

```json
{
  "name": "get_weather",
  "description": "Retorna o clima atual de uma cidade.",
  "input_schema": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string"
      }
    },
    "required": ["location"]
  }
}
```

---

## O padrão ReAct

O padrão mais utilizado em agentes modernos é o **ReAct** (*Reasoning + Acting*), uma abordagem que combina raciocínio e execução dentro do mesmo ciclo.

Antes do ReAct, muitos sistemas utilizavam o modelo tradicional de *Chain-of-Thought*, no qual o LLM apenas raciocinava internamente para gerar uma resposta final. O problema é que esse tipo de abordagem funciona bem para perguntas estáticas, mas falha quando o agente precisa interagir com o mundo externo.

O ReAct surgiu justamente para resolver essa limitação.

Em vez de apenas “pensar”, o agente passa a:

1. raciocinar sobre o problema,
2. executar uma ação,
3. observar o resultado,
4. adaptar o próximo passo.

Ou seja, o agente deixa de operar como um sistema puramente textual e passa a funcionar como um ciclo contínuo de tomada de decisão.

Na prática, praticamente todo sistema moderno de agentes, seja usando ferramentas, navegadores, APIs ou workflows multiagentes, utiliza alguma variação do padrão ReAct.

### **Estrutura**

```text
Pensamento → Ação → Observação
```

### Exemplo

```text
Pensamento:
O usuário quer o preço atual da ação.

Ação:
Executar stock_price_api("AAPL")

Observação:
AAPL = $214.32

Pensamento:
Agora resumir o resultado.
```

Esse ciclo permite que o agente:

* acompanhe o próprio plano,
* lide com erros,
* adapte decisões com base em novas informações.

---

# 3. Tipos de ferramentas

| Tipo de ferramenta                     | Função                                                              | Exemplos                                                                                      |
| -------------------------------------- | ------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Ferramentas de percepção e recuperação | Coletam contexto e informações para o agente                        | Sistemas de arquivos, bancos vetoriais, mecanismos de busca, APIs externas                    |
| Ferramentas de ação                    | Modificam ambientes ou sistemas externos                            | Envio de e-mails, commits em repositórios, processamento de pagamentos, automação de sistemas |
| Ferramentas de raciocínio              | Executam tarefas analíticas ou computacionais fora do LLM principal | Análise de dados, matemática simbólica, geração de planos, mapeamento conceitual              |
| Ferramentas de ambiente                | Padronizam a comunicação entre agentes e ecossistemas externos      | MCP, Slack, Google Calendar, sistemas locais, softwares corporativos                          |

### MCP (Model Context Protocol)

O MCP funciona como um “USB-C para agentes de IA”.

A ideia é criar um protocolo padronizado para conectar agentes a ferramentas, aplicações e fontes de dados sem precisar desenvolver integrações específicas para cada sistema.

Sem MCP, cada framework normalmente precisa criar conectores próprios para serviços como Slack, Google Drive, GitHub ou bancos de dados. Isso gera duplicação de trabalho, acoplamento entre plataformas e dificuldade de manutenção.

O MCP resolve esse problema criando uma camada universal de comunicação.

Na prática, um servidor MCP expõe ferramentas, contexto e recursos de forma padronizada, enquanto o agente atua como cliente consumindo essas capacidades.

Isso permite que diferentes modelos e frameworks reutilizem as mesmas integrações.

---

# 4. O que faz uma boa ferramenta?

Uma boa ferramenta não é feita pensando em humanos, mas no modelo que irá utilizá-la.

Ela precisa ser:

* previsível,
* fácil de interpretar,
* bem documentada,
* segura.

## Princípios fundamentais

| Princípio              | Descrição                                                   |
| ---------------------- | ----------------------------------------------------------- |
| Responsabilidade única | Cada ferramenta deve resolver apenas um problema específico |
| Descrições claras      | A descrição funciona como um manual para o modelo           |
| Schemas estritos       | Use parâmetros fortemente tipados                           |
| Contexto relevante     | Retorne apenas informações úteis para a próxima decisão     |
| Limites de permissão   | Deixe explícito quando a ferramenta executa ações sensíveis |

---

## Comparação de exemplos

| Característica | Mau exemplo            | Bom exemplo                                                      |
| -------------- | ---------------------- | ---------------------------------------------------------------- |
| Descrição      | `"Atualiza o sistema"` | `"Atualiza o endereço de entrega do usuário após validar o CEP"` |
| Parâmetros     | `data: string`         | `new_address: string`, `user_id: integer`                        |
| Saída          | `"Concluído"`          | `{ "status": "success", "updated_fields": [...] }`               |

---

# 5. Padrões de design

## Separação entre leitura e escrita

Evite usar a mesma ferramenta tanto para consultar quanto para modificar dados.

### Exemplo

Em vez de:

```text
user_profile_tool()
```

Prefira:

```text
get_user_profile()
update_user_profile()
```

Isso reduz alterações acidentais e torna o comportamento do agente mais previsível.

---

## Abstração semântica

Ferramentas devem representar a intenção do usuário, e não detalhes técnicos da implementação.

### Ruim

```text
Clique no seletor CSS .nav-item-4
```

### Melhor

```text
Abrir o menu de Pedidos
```

A segunda opção é mais estável, compreensível e independente da interface.

---

## Human-in-the-Loop (HITL)

Ações críticas devem exigir aprovação humana antes da execução.

Exemplos:

* pagamentos,
* reembolsos,
* cancelamentos,
* exclusão de contas.

Fluxo típico:

```text
Pendente → Aprovação Humana → Execução
```

---

## Ferramentas hierárquicas

Em sistemas maiores, é comum existir:

* um agente gerente,
* vários agentes especialistas.

Exemplo:

```text
Agente Gerente
 ├── Ferramentas Financeiras
 ├── Ferramentas de Código
 └── Ferramentas de Pesquisa
```

Esse modelo melhora escalabilidade e precisão na seleção das ferramentas.

---

# 6. Falhas comuns

## Explosão de ferramentas

Disponibilizar ferramentas demais costuma piorar a seleção, principalmente em modelos menores.

---

## Ferramentas ambíguas

Ferramentas com responsabilidades parecidas aumentam a chance de uso incorreto.

---

## Ferramentas “canivete suíço”

Ferramentas gigantes e multifuncionais geralmente:

* possuem schemas complexos,
* aumentam erros de parâmetros,
* dificultam debugging,
* reduzem confiabilidade.

---

## Parsing inseguro

Nunca assuma que a resposta de uma ferramenta será sempre válida.

### Ruim

```python
data = json.parse(response)
```

### Melhor

```python
try:
    data = json.parse(response)
except:
    fallback()
```

---

## Falta de guardrails

Sem validação e monitoramento, agentes podem:

* executar ações indevidas,
* gerar comportamentos inseguros,
* falhar silenciosamente em produção.

---

# 7. Boas práticas

| Princípio            | Explicação                                                | Exemplo                                      |
| -------------------- | --------------------------------------------------------- | -------------------------------------------- |
| Falhe com elegância  | Sempre trate estados de erro e carregamento               | Mostrar progresso durante execução           |
| Otimize tokens       | Retorne apenas os dados necessários                       | Evitar respostas gigantescas                 |
| Forneça exemplos     | Exemplos ajudam o modelo a usar a ferramenta corretamente | `{ "location": "São Paulo, SP" }`            |
| Use modelos fortes   | Seleção complexa exige maior capacidade de raciocínio     | Rotear casos ambíguos para modelos avançados |
| Avalie continuamente | Teste constantemente o comportamento do agente            | Criar benchmarks internos                    |

# 8. Principais aprendizados

* Ferramentas são interfaces para modelos, não para humanos.
* Descrições e schemas bem definidos aumentam drasticamente a confiabilidade.
* O padrão ReAct é a base da maioria dos agentes modernos.
* Sistemas confiáveis dependem de:

  * guardrails,
  * limites de permissão,
  * HITL,
  * avaliações constantes.
* Comece simples:

  * ferramentas somente leitura,
  * responsabilidades pequenas,
  * workflows controlados.
* Protocolos como MCP ajudam a evitar fragmentação e dependência de fornecedores.

# Fontes

- STEIN, Merlin. How are AI agents used? Evidence from 177,000 MCP tools. arXiv preprint arXiv:2603.23802, 2026.
- YAO, Shunyu et al. React: Synergizing reasoning and acting in language models. arXiv preprint arXiv:2210.03629, 2022.
- LOU, Renze et al. The Tool Illusion: Rethinking Tool Use in Web Agents. arXiv preprint arXiv:2604.03465, 2026.
- https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents
- https://docs.langchain.com/oss/python/langchain/frontend/tool-calling
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools