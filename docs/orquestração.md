# Guia de Engenharia: Orquestração de Agentes

## 1. O que é Orquestração de Agentes?
Orquestração é a lógica que governa o fluxo de trabalho entre agentes de IA. Ela determina qual agente executa, em qual ordem e como eles compartilham informações para resolver uma tarefa complexa que uma única chamada para um LLM não conseguiria resolver de forma confiável.

### A Evolução da Agência
* **Sistemas de Agente Único:** Um único LLM com um conjunto de ferramentas. Ótimo para tarefas específicas, mas falha diante de lógicas complexas ou estados de longo prazo.
* **Sistemas Multiagentes:** Múltiplos agentes trabalhando em paralelo ou em sequência. Frequentemente se tornam caóticos sem um “gerente”.
* **Sistemas Orquestrados:** Coordenação estruturada. Os agentes possuem papéis específicos e uma lógica definida (via código ou conduzida por LLM) move o objetivo adiante.

**Por que escalar exige orquestração:** À medida que as tarefas crescem, colocar tudo em um único prompt (“O Agente Deus”) aumenta latência, custo e o problema de raciocínio conhecido como “lost in the middle”.

---

## 2. Princípios Fundamentais

| Princípio | Descrição | Exemplo |
|---|---|---|
| **Separação de Responsabilidades** | Cada agente deve possuir apenas uma função específica. | Um agente faz pesquisa enquanto outro verifica fatos. |
| **Gerenciamento de Contexto** | Passe para cada agente apenas as informações necessárias para executar a tarefa. | O agente de resumo recebe apenas o texto final, não todo o histórico da conversa. |
| **Determinístico vs. Autônomo** | Use código para fluxos previsíveis e LLMs para tarefas abertas de raciocínio. | Um `if/else` escolhe o fluxo; o LLM escreve a resposta ao usuário. |
| **Gerenciamento de Estado** | Mantenha uma fonte central de verdade compartilhada entre os agentes. | Todos os agentes atualizam o status de tarefas em um banco de dados. |
| **Confiabilidade e Tolerância a Falhas** | O sistema deve conseguir lidar com falhas de agentes automaticamente. | Se uma API falhar, o orquestrador executa novamente ou usa outro agente. |
| **Human-in-the-Loop (HITL)** | Inclua validação humana em ações críticas ou sensíveis. | Um humano aprova o envio de um e-mail financeiro antes da execução. |
| **Observabilidade** | O sistema deve permitir rastrear decisões e raciocínios dos agentes. | Logs mostram qual agente tomou cada decisão durante a execução. |

---

## 3. Padrões Comuns de Orquestração

### Padrão Router
* **O que é:** Um agente de entrada direciona a solicitação para um agente especializado.
* **Caso de Uso:** Triagem de suporte ao cliente (Financeiro vs. Suporte Técnico).
* **Prós/Contras:** Rápido e eficiente; exige um roteador extremamente preciso.

### Planner + Executor
* **O que é:** Um agente cria um plano passo a passo; outro executa cada etapa.
* **Caso de Uso:** Escrita de um relatório técnico complexo.
* **Prós/Contras:** Alta qualidade; pode ser lento caso o planejador precise replanejar constantemente.

### Agentes Supervisores (Managers)
* **O que é:** Um agente central delega tarefas para “workers” e revisa suas saídas.
* **Caso de Uso:** Desenvolvimento de software (o Manager distribui tarefas para Programador, Revisor e Testador).
* **Prós/Contras:** Espelha equipes humanas; possui alto custo de tokens.

### Workflows em Pipeline
* **O que é:** Uma sequência linear e determinística (A → B → C).
* **Caso de Uso:** Extração e sumarização de dados.
* **Prós/Contras:** Altamente previsível; inflexível para casos extremos.

### Orquestração Orientada a Eventos
* **O que é:** Agentes são acionados por eventos externos (ex.: um novo e-mail ou alteração no banco de dados).
* **Caso de Uso:** Sistemas de monitoramento e resposta em tempo real.

### Agentes Hierárquicos
* **O que é:** Orquestração “aninhada”, onde um gerente supervisiona outros gerentes.
* **Caso de Uso:** Operações em escala empresarial.

### Workers Paralelos
* **O que é:** Múltiplos agentes executam a mesma tarefa em diferentes dados simultaneamente.
* **Caso de Uso:** Analisar 50 documentos PDF ao mesmo tempo.

### Orquestração Tool-First
* **O que é:** O sistema é construído em torno da disponibilidade de ferramentas; os agentes atuam apenas como “condutores” dessas ferramentas.
* **Caso de Uso:** Consultas em banco de dados ou automação via APIs.

---

## 4. Memória e Contexto

* **Curto Prazo:** Histórico imediato da conversa (efêmero).
* **Longo Prazo:** Dados persistentes armazenados em banco de dados ou vector store (recuperados via RAG).
* **Compartilhado vs. Isolado:** Contexto compartilhado funciona como um “quadro branco” visível para todos os agentes; contexto isolado mantém os agentes focados.
* **O Custo do Contexto:** Contexto excessivo aumenta custos e degrada a capacidade do LLM de seguir instruções.

---

## 5. Tratamento de Falhas

* **Retries:** Reexecuções automáticas para erros transitórios de API ou eventos de “alucinação detectada”.
* **Timeouts:** Interrompa um agente se ele passar tempo demais em um loop.
* **Camadas de Validação:** Use um LLM menor ou código para validar o formato da saída (ex.: schema JSON).
* **Agentes de Fallback:** Se um agente especializado falhar, redirecione para um modelo “Generalista” robusto.
* **Escalonamento:** Se o sistema travar, notifique um humano via Slack/E-mail.
* **Guardrails:** Restrições rígidas sobre o que um agente pode dizer ou fazer (ex.: sem negociação de preços).

---

## 6. Boas Práticas em Produção

1. **Mantenha os Agentes Especializados:** Se o prompt de sistema de um agente tiver mais de duas páginas, ele provavelmente está fazendo coisas demais.
2. **Prefira Lógica Determinística:** Se você sabe que B sempre vem após A, use código, não um roteador baseado em LLM.
3. **Limite Contexto Agressivamente:** Passe apenas os últimos 3–5 turnos ou um estado resumido.
4. **Meça Latência:** Monitore quanto tempo cada “salto” entre agentes leva.
5. **Versione Tudo:** Prompts são código. Versione-os junto da lógica dos agentes.
6. **Registre o Raciocínio Intermediário:** Sempre registre o campo “Thought” dos agentes para depuração.

---

## 7. Anti-Padrões

* **O “Agente Deus”:** Um único agente com 50 ferramentas e um prompt gigantesco. Ele vai falhar.
* **Loops Infinitos:** O Agente A pergunta ao Agente B, que pergunta ao Agente A. Implemente um limite `max_turns`.
* **Autonomia Excessiva:** Permitir que um agente decida todo o orçamento ou estratégia sem validação de um “Planner”.
* **Prompts Ocultos:** Instruções hardcoded no código da aplicação em vez de um gerenciador central de prompts.
* **Sem Observabilidade:** Implantar um sistema onde você só consegue ver a saída final.

---

## 8. Exemplo Real: Fluxo de Suporte ao Cliente

1. **Router:** Analisa a solicitação → “Preciso de um reembolso.”
2. **Agente de Recuperação:** Busca o histórico de compras do cliente no banco de dados.
3. **Validador de Política:** Verifica se o pedido atende à janela de reembolso de 30 dias.
4. **Gerador de Resposta:** Redige uma resposta educada com base na validação.
5. **Escalonamento Humano:** Se a validação da política for “Limítrofe”, o ticket é enviado para um atendente humano.

---

## 9. Principais Lições

* **Orquestração é sobre restrições.** Os melhores sistemas limitam o que um agente pode fazer em determinado momento.
* **Código para Fluxo, LLM para Raciocínio.** Não faça o LLM executar tarefas que um simples `if/else` resolveria.
* **Modularidade é Rei.** Construa agentes como microserviços — intercambiáveis e focados em tarefas específicas.

## Fontes

- https://platform.claude.com/docs/en/managed-agents/multi-agent
- https://resources.anthropic.com/ty-building-effective-ai-agents
- https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
- ADIMULAM, Apoorva; GUPTA, Rajesh; KUMAR, Sumit. The Orchestration of Multi-Agent Systems: Architectures, Protocols, and Enterprise Adoption. arXiv preprint arXiv:2601.13671, 2026.

