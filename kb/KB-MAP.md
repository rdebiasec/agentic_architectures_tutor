# KB Map — Agentic Architectural Patterns for Building Multi-Agent Systems

> Knowledge base index for learning agentic architectures. Source: Packt, Arsanjani & Bustos (2026).

## Book overview

This book provides design patterns and practices for building production-grade multi-agent GenAI systems,
covering LLM selection, RAG/fine-tuning, coordination patterns, compliance, fault tolerance, human-agent
interaction, and hands-on implementations with ADK, CrewAI, and LangGraph.

## Chapter index

| Ch | Title | Part | Figures | Code |
|----|-------|------|---------|------|
| [1](chapters/01-genai-in-the-enterprise.md) | GenAI in the Enterprise: Landscape, Maturity, and Agent Focus | 1 | 4 | 0 |
| [2](chapters/02-agent-ready-llms.md) | Agent-Ready LLMs: Selection, Deployment, and Adaptation | 1 | 2 | 0 |
| [3](chapters/03-llm-adaptation-rag-to-finetuning.md) | The Spectrum of LLM Adaptation for Agents: RAG to Fine-tuning | 1 | 6 | 0 |
| [4](chapters/04-agentic-ai-architecture.md) | Agentic AI Architecture: Components and Interactions | 1 | 5 | 0 |
| [5](chapters/05-multi-agent-coordination-patterns.md) | Multi-Agent Coordination Patterns | 2 | 14 | 0 |
| [6](chapters/06-explainability-compliance-patterns.md) | Explainability and Compliance Agentic Patterns | 2 | 5 | 0 |
| [7](chapters/07-robustness-fault-tolerance-patterns.md) | Robustness and Fault Tolerance Patterns | 2 | 17 | 1 |
| [8](chapters/08-human-agent-interaction-patterns.md) | Human-Agent Interaction Patterns | 2 | 6 | 0 |
| [9](chapters/09-agent-level-patterns.md) | Agent-Level Patterns | 2 | 8 | 0 |
| [10](chapters/10-system-level-production-patterns.md) | System-Level Patterns for Production Readiness | 2 | 6 | 0 |
| [11](chapters/11-advanced-adaptation.md) | Advanced Adaptation: Building Agents That Learn | 2 | 8 | 0 |
| [12](chapters/12-practical-roadmap-maturity.md) | A Practical Roadmap: Implementing Agentic Patterns by Maturity Level | 3 | 3 | 0 |
| [13](chapters/13-use-case-single-agent-loan.md) | Use Case: A Single Agent for Loan Processing | 3 | 1 | 0 |
| [14](chapters/14-use-case-multi-agent-loan.md) | Use Case: A Multi-Agent System for Loan Processing | 3 | 2 | 0 |
| [15](chapters/15-agent-frameworks-comparison.md) | Agent Frameworks – Use Case: A Multi-Agent System for Loan Processing with CrewAI and LangGraph | 3 | 0 | 0 |
| [16](chapters/16-conclusion.md) | Conclusion: Charting Your Agentic AI Journey | 3 | 0 | 0 |

## Chapter summaries

### Chapter 1: GenAI in the Enterprise: Landscape, Maturity, and Agent Focus

This chapter provided a foundational overview of the GenAI landscape within the enterprise context, charting a
course from core concepts toward the sophisticated realm of agentic AI systems.
We examined the transformative potential of GenAI, its underlying capabilities, and diverse applications. We
emphasized the critical role of context management in achieving reliable results and introduced the
fundamental anatomy of AI agents (sense, reason, plan, and act) as the building blocks for more auto

### Chapter 2: Agent-Ready LLMs: Selection, Deployment, and Adaptation

In this chapter, we focused on the critical role LLMs play as the cognitive engine of agentic AI systems and
detailed the journey to prepare these models to be truly agent-ready.
We began by establishing the LLM as the central reasoning core within an agent, responsible for understanding
complex inputs, formulating plans, making decisions, orchestrating the use of tools, and generating coherent
communication. This "brain" is essential for an agent to move from perceiving its environment to takin

### Chapter 3: The Spectrum of LLM Adaptation for Agents: RAG to Fine-tuning

This chapter explored the critical spectrum of techniques for adapting LLMs to make them truly agent-ready,
moving beyond their generic pretrained capabilities to become specialized engines for AI agents. We established
that such adaptation is vital for enhancing agent performance in specific enterprise domains, improving
accuracy, reliability, efficiency, and goal alignment.

### Chapter 4: Agentic AI Architecture: Components and Interactions

This chapter built upon the foundational concepts of Part 1, providing a detailed architectural blueprint for the
agentic systems that LLMs power. We moved from theory to structure by defining what makes a system
"agentic," dissecting the core components that enable intelligent behavior, and mapping technical challenges
directly to this new architectural framework.

### Chapter 5: Multi-Agent Coordination Patterns

This chapter explored the essential patterns that enable multiple autonomous agents to work together as a
cohesive and intelligent system. We established that moving from a single agent to a multi-agent system
introduces a new layer of complexity that requires structured solutions for collaboration, competition, and
communication. These patterns provide the architectural blueprints for building robust, scalable, and coherent
multi-agent systems. We not only detailed these individual patterns but

### Chapter 6: Explainability and Compliance Agentic Patterns

This chapter tackled the critical enterprise requirements of explainability and compliance in agentic AI systems.
We established that as autonomy increases, so does the need for transparency and accountability to build trust
and ensure reliability. We also showed how the application of these patterns deepens as a system matures from
a single-agent to a multi-agent architecture.
The primary challenge we addressed was instruction drift, where the original intent of a task becomes diluted or
lost i

### Chapter 7: Robustness and Fault Tolerance Patterns

This chapter explored the architectural patterns essential for building robust and fault-tolerant agentic AI
systems. We have seen that creating a production-grade system requires moving beyond simply achieving a
task, such as function calling of a tool by an agent, correctly, and architecting for the real world; for example, the
inevitability of eventual failure, error, and unexpected conditions. By focusing on resilience through a layered
approach, we build the foundation for systems that are 

### Chapter 8: Human-Agent Interaction Patterns

This chapter explored the critical patterns that govern the interface between humans and AI agents. We have
established that for agentic systems to be truly useful and trusted, their interactions with people must be
designed with intention, clarity, and safety in mind. These patterns provide the architectural solutions for
managing the spectrum of human-agent collaborations, from direct commands to complex, long-running
delegations.

### Chapter 9: Agent-Level Patterns

Act and tools Executes direct
commands and uses
simple tools
Single Agent Baseline The agent functions as a
basic automator. It uses
the Act block to execute
workflows and the Tools
block to interface with
external APIs.
Memory Handles multi-turn
conversations and
remembers key facts
Agent-Specific MemoryThe agent becomes
stateful. The Memory
component persists
session history and user
preferences to maintain
context.
Memory Accesses and reasons
over external, domainspecific data
Context-Aware R

### Chapter 10: System-Level Patterns for Production Readiness

This chapter shifted our focus from the internal capabilities of individual agents to the critical, holistic, and
external architecture that enables them to operate as a cohesive, enterprise-grade multi-agent system or
application. We moved beyond the agent's mind and into the "city" it inhabits, that is, the infrastructure that
ensures it can communicate, act securely, and scale effectively. These system-level patterns present the
blueprints for transforming a promising agentic proof of concept

### Chapter 11: Advanced Adaptation: Building Agents That Learn

This chapter journeyed to the cutting edge of agentic AI, moving beyond the creation of static agents to the
cultivation of dynamic, self-improving ecosystems. We introduced the Self-Improvement Flywheel as a
conceptual model for this process, detailed the specific patterns required to enable it, and provided a strategic
guide for implementation.

### Chapter 12: A Practical Roadmap: Implementing Agentic Patterns by Maturity Level

This chapter provided a crucial bridge between the theoretical knowledge of individual design patterns and the
practical reality of building a complete agentic system. We addressed the fundamental question of "Where do I
start?" by introducing a strategic, three-level maturity model that serves as a practical roadmap for
implementation. This approach allows organizations to adopt agentic AI progressively, aligning architectural
complexity with their specific business goals and operational readin

### Chapter 13: Use Case: A Single Agent for Loan Processing

In this chapter, we undertook the practical journey of building a complete, autonomous agent from the ground
up. We began with a real-world business challenge (loan processing) and progressed through architectural
design, implementation using ADK, and finally, execution and analysis.
The result is a functional Level 3 agent that successfully uses a sophisticated cognitive framework and a toolbelt
to complete a complex, multi-step task.

### Chapter 14: Use Case: A Multi-Agent System for Loan Processing

In this chapter, we put our design patterns and architectural theories into practice, culminating in a
sophisticated, multi-agent system for loan processing. By moving beyond abstract concepts and into a
functional implementation, we can now outline the key lessons learned from this transition:.
From monolith to a team of agents: Our journey began with a capable but brittle Level 3 monolithic
agent. We deliberately exposed its architectural weaknesses (poor fault isolation and difficult
maintain

### Chapter 15: Agent Frameworks – Use Case: A Multi-Agent System for Loan Processing with CrewAI and LangGraph

In this chapter, we explored three prominent agent frameworks-Google's ADK, CrewAI, and LangGraph-and
saw how each provides a different but powerful abstraction for building complex agentic systems using Google
Gemini as our LLM.
Our practical implementations of the loan processing agent, updated based on the revised notebook, showed
CrewAI's strength in modeling collaborative teams via a hierarchical process, while LangGraph demonstrated
fine-grained control, explicit state management, and robu

### Chapter 16: Conclusion: Charting Your Agentic AI Journey




## Parts

### Part 1: Foundations and Core Agent Concepts

- [Chapter 1](chapters/01-genai-in-the-enterprise.md): GenAI in the Enterprise: Landscape, Maturity, and Agent Focus
- [Chapter 2](chapters/02-agent-ready-llms.md): Agent-Ready LLMs: Selection, Deployment, and Adaptation
- [Chapter 3](chapters/03-llm-adaptation-rag-to-finetuning.md): The Spectrum of LLM Adaptation for Agents: RAG to Fine-tuning
- [Chapter 4](chapters/04-agentic-ai-architecture.md): Agentic AI Architecture: Components and Interactions

### Part 2: Agentic Design Patterns

- [Chapter 5](chapters/05-multi-agent-coordination-patterns.md): Multi-Agent Coordination Patterns
- [Chapter 6](chapters/06-explainability-compliance-patterns.md): Explainability and Compliance Agentic Patterns
- [Chapter 7](chapters/07-robustness-fault-tolerance-patterns.md): Robustness and Fault Tolerance Patterns
- [Chapter 8](chapters/08-human-agent-interaction-patterns.md): Human-Agent Interaction Patterns
- [Chapter 9](chapters/09-agent-level-patterns.md): Agent-Level Patterns
- [Chapter 10](chapters/10-system-level-production-patterns.md): System-Level Patterns for Production Readiness
- [Chapter 11](chapters/11-advanced-adaptation.md): Advanced Adaptation: Building Agents That Learn

### Part 3: Execution: Strategy, Use Cases, and The Future

- [Chapter 12](chapters/12-practical-roadmap-maturity.md): A Practical Roadmap: Implementing Agentic Patterns by Maturity Level
- [Chapter 13](chapters/13-use-case-single-agent-loan.md): Use Case: A Single Agent for Loan Processing
- [Chapter 14](chapters/14-use-case-multi-agent-loan.md): Use Case: A Multi-Agent System for Loan Processing
- [Chapter 15](chapters/15-agent-frameworks-comparison.md): Agent Frameworks – Use Case: A Multi-Agent System for Loan Processing with CrewAI and LangGraph
- [Chapter 16](chapters/16-conclusion.md): Conclusion: Charting Your Agentic AI Journey

## Learning paths

### For software architects
1. [Ch 1](chapters/01-genai-in-the-enterprise.md) → [Ch 4](chapters/04-agentic-ai-architecture.md) → [Ch 5–10](chapters/05-multi-agent-coordination-patterns.md) → [Ch 12](chapters/12-practical-roadmap-maturity.md)

### For AI / ML engineers
1. [Ch 2](chapters/02-agent-ready-llms.md) → [Ch 3](chapters/03-llm-adaptation-rag-to-finetuning.md) → [Ch 13–15](chapters/13-use-case-single-agent-loan.md) (code)

### For technical leaders
1. [Ch 1 Maturity Model](chapters/01-genai-in-the-enterprise.md) → [Ch 12 Roadmap](chapters/12-practical-roadmap-maturity.md) → [Ch 16 Conclusion](chapters/16-conclusion.md)

## Pattern chapters (deep dive)

- [Chapter 5](chapters/05-multi-agent-coordination-patterns.md): Multi-Agent Coordination Patterns
- [Chapter 6](chapters/06-explainability-compliance-patterns.md): Explainability and Compliance Agentic Patterns
- [Chapter 7](chapters/07-robustness-fault-tolerance-patterns.md): Robustness and Fault Tolerance Patterns
- [Chapter 8](chapters/08-human-agent-interaction-patterns.md): Human-Agent Interaction Patterns
- [Chapter 9](chapters/09-agent-level-patterns.md): Agent-Level Patterns
- [Chapter 10](chapters/10-system-level-production-patterns.md): System-Level Patterns for Production Readiness
- [Chapter 11](chapters/11-advanced-adaptation.md): Advanced Adaptation: Building Agents That Learn

## Pattern catalog (by chapter)

### Chapter 5: Multi-Agent Coordination Patterns

- [Multi-Agent Coordination Patterns](chapters/05-multi-agent-coordination-patterns.md#multi-agent-coordination-patterns)
- [Task Delegation Frameworks](chapters/05-multi-agent-coordination-patterns.md#task-delegation-frameworks)
- [Agent Composition Topologies](chapters/05-multi-agent-coordination-patterns.md#agent-composition-topologies)
- [Swarm or hybrid architectures:](chapters/05-multi-agent-coordination-patterns.md#swarm-or-hybrid-architectures)
- [A user submits a loan application to a LoanOrchestratorAgent. Here is the workflow:](chapters/05-multi-agent-coordination-patterns.md#a-user-submits-a-loan-application-to-a-loanorchestratoragent-here-is-the-workflow)
- [Feature Supervisor Architecture](chapters/05-multi-agent-coordination-patterns.md#feature-supervisor-architecture)
- [Blackboard Knowledge Hub](chapters/05-multi-agent-coordination-patterns.md#blackboard-knowledge-hub)
- [The negotiation, mediated by the ResourceManagerAgent, unfolds:](chapters/05-multi-agent-coordination-patterns.md#the-negotiation-mediated-by-the-resourcemanageragent-unfolds)

### Chapter 6: Explainability and Compliance Agentic Patterns

- [This brings us to the critical domains of explainability and compliance:](chapters/06-explainability-compliance-patterns.md#this-brings-us-to-the-critical-domains-of-explainability-and-compliance)
- [patterns evolves as a system matures from a single-agent to a multi-agent architecture:](chapters/06-explainability-compliance-patterns.md#patterns-evolves-as-a-system-matures-from-a-single-agent-to-a-multi-agent-architecture)
- [Instruction Fidelity Auditing](chapters/06-explainability-compliance-patterns.md#instruction-fidelity-auditing)
- [This pattern operates on several core principles:](chapters/06-explainability-compliance-patterns.md#this-pattern-operates-on-several-core-principles)
- [Persistent Instruction Anchoring](chapters/06-explainability-compliance-patterns.md#persistent-instruction-anchoring)
- [Shared Epistemic Memory](chapters/06-explainability-compliance-patterns.md#shared-epistemic-memory)
- [A resilient hierarchical system can be designed by combining the following patterns:](chapters/06-explainability-compliance-patterns.md#a-resilient-hierarchical-system-can-be-designed-by-combining-the-following-patterns)

### Chapter 7: Robustness and Fault Tolerance Patterns

- [Parallel Execution Consensus](chapters/07-robustness-fault-tolerance-patterns.md#parallel-execution-consensus)
- [Delayed Escalation Strategy](chapters/07-robustness-fault-tolerance-patterns.md#delayed-escalation-strategy)
- [Watchdog Timeout Supervisor](chapters/07-robustness-fault-tolerance-patterns.md#watchdog-timeout-supervisor)
- [Auto-Healing Agent Resuscitation](chapters/07-robustness-fault-tolerance-patterns.md#auto-healing-agent-resuscitation)
- [Majority Voting Across Agents](chapters/07-robustness-fault-tolerance-patterns.md#majority-voting-across-agents)
- [Causal Dependency Graph](chapters/07-robustness-fault-tolerance-patterns.md#causal-dependency-graph)
- [Fallback Model Invocation](chapters/07-robustness-fault-tolerance-patterns.md#fallback-model-invocation)
- [Canary Agent Testing](chapters/07-robustness-fault-tolerance-patterns.md#canary-agent-testing)
- [Pattern Metric Instrumentation](chapters/07-robustness-fault-tolerance-patterns.md#pattern-metric-instrumentation)
- [A pipeline gent is tasked with a three-step process:](chapters/07-robustness-fault-tolerance-patterns.md#a-pipeline-gent-is-tasked-with-a-three-step-process)
- [Vote tally: The orchestrator counts the votes for each possible outcome:](chapters/07-robustness-fault-tolerance-patterns.md#vote-tally-the-orchestrator-counts-the-votes-for-each-possible-outcome)
- [The sandboxing pattern neutralizes the threat:](chapters/07-robustness-fault-tolerance-patterns.md#the-sandboxing-pattern-neutralizes-the-threat)
- [print(f"ORCHESTRATOR: Delegating task to {agent_name} (Score:](chapters/07-robustness-fault-tolerance-patterns.md#print-f-orchestrator-delegating-task-to-agent-name-score)

### Chapter 8: Human-Agent Interaction Patterns

- [Human-Agent Interaction Patterns](chapters/08-human-agent-interaction-patterns.md#human-agent-interaction-patterns)
- [Human Calls Agent](chapters/08-human-agent-interaction-patterns.md#human-calls-agent)
- [Agent Calls Proxy Agent](chapters/08-human-agent-interaction-patterns.md#agent-calls-proxy-agent)
- [Agent Calls Human](chapters/08-human-agent-interaction-patterns.md#agent-calls-human)
- [Pattern Metric Instrumentation](chapters/08-human-agent-interaction-patterns.md#pattern-metric-instrumentation)
- [A marketing manager delegates a research task to a MarketAnalysisAgent:](chapters/08-human-agent-interaction-patterns.md#a-marketing-manager-delegates-a-research-task-to-a-marketanalysisagent)
- [The interaction is handled securely and efficiently:](chapters/08-human-agent-interaction-patterns.md#the-interaction-is-handled-securely-and-efficiently)

### Chapter 9: Agent-Level Patterns

- [Single Agent Baseline](chapters/09-agent-level-patterns.md#single-agent-baseline)
- [Multimodal Sensory Input](chapters/09-agent-level-patterns.md#multimodal-sensory-input)
- [Component Capabilities Interactionamong](chapters/09-agent-level-patterns.md#component-capabilities-interactionamong)
- [The stateful interaction unfolds:](chapters/09-agent-level-patterns.md#the-stateful-interaction-unfolds)
- [Pattern Metric Instrumentation](chapters/09-agent-level-patterns.md#pattern-metric-instrumentation)

### Chapter 10: System-Level Patterns for Production Readiness

- [Real-Time Compliance Monitoring](chapters/10-system-level-production-patterns.md#real-time-compliance-monitoring)
- [agents, called SalesAgent and MarketingAgent:](chapters/10-system-level-production-patterns.md#agents-called-salesagent-and-marketingagent)
- [relies on the interaction between three core components:](chapters/10-system-level-production-patterns.md#relies-on-the-interaction-between-three-core-components)

### Chapter 11: Advanced Adaptation: Building Agents That Learn

- [Advanced Adaptation: Building](chapters/11-advanced-adaptation.md#advanced-adaptation-building)
- [Custom Evaluation Metrics](chapters/11-advanced-adaptation.md#custom-evaluation-metrics)
- [Preference-Controlled Synthetic Data Generation](chapters/11-advanced-adaptation.md#preference-controlled-synthetic-data-generation)
- [Advanced Model Tuning Patterns](chapters/11-advanced-adaptation.md#advanced-model-tuning-patterns)
- [Coevolved Agent Training](chapters/11-advanced-adaptation.md#coevolved-agent-training)
- [Architecture, Coevolved Agent](chapters/11-advanced-adaptation.md#architecture-coevolved-agent)
- [Execution: Strategy, Use](chapters/11-advanced-adaptation.md#execution-strategy-use)


## Code examples

### Chapter 7
- [`code/ch07-snippet-01.py`](code/ch07-snippet-01.py)


## Figures by chapter

### Chapter 1
- Figure 1.1: [Agentic anatomy by Dr. Ali Arsanjani](../assets/ch01/fig-1-1-agentic-anatomy-by-dr-ali-arsanjani.png)
- Figure 1.2: [The agentic loop](../assets/ch01/fig-1-2-the-agentic-loop.png)
- Figure 1.3: [Maturity Model levels](../assets/ch01/fig-1-3-maturity-model-levels.png)
- Figure 1.4: [Distributed multi-agent systems using MCP and A2A](../assets/ch01/fig-1-4-distributed-multi-agent-systems-using-mcp-and-a2a.png)

### Chapter 2
- Figure 2.1: [The LLM as the central reasoning core of an AI agent](../assets/ch02/fig-2-1-the-llm-as-the-central-reasoning-core-of-an-ai-age.png)
- Figure 2.2: [AgentOps sequence](../assets/ch02/fig-2-2-agentops-sequence.png)

### Chapter 3
- Figure 3.1: [An LLM as the brain of agents (image generated with Google Imagen)](../assets/ch03/fig-3-1-an-llm-as-the-brain-of-agents-image-generated-with.png)
- Figure 3.2: [Agent specialization: adapting agents for task-specific execution](../assets/ch03/fig-3-2-agent-specialization-adapting-agents-for-task-spec.png)
- Figure 3.3: [Orchestrator agent architecture](../assets/ch03/fig-3-3-orchestrator-agent-architecture.png)
- Figure 3.4: [Example flow for RAG with a real-time specialist](../assets/ch03/fig-3-4-example-flow-for-rag-with-a-real-time-specialist.png)
- Figure 3.5: [The risky generalist workflow](../assets/ch03/fig-3-5-the-risky-generalist-workflow.png)
- Figure 3.6: [Example workflow leveraging a RAG-enabled agent](../assets/ch03/fig-3-6-example-workflow-leveraging-a-rag-enabled-agent.png)

### Chapter 4
- Figure 4.1: [The hierarchy of autonomy](../assets/ch04/fig-4-1-the-hierarchy-of-autonomy.png)
- Figure 4.2: [Use case example: Agentic loan processing](../assets/ch04/fig-4-2-use-case-example-agentic-loan-processing.png)
- Figure 4.3: [Contextual inputs versus grounding failures](../assets/ch04/fig-4-3-contextual-inputs-versus-grounding-failures.png)
- Figure 4.4: [Agent interaction models](../assets/ch04/fig-4-4-agent-interaction-models.png)
- Figure 4.5: [Emerging agentic stack](../assets/ch04/fig-4-5-emerging-agentic-stack.png)

### Chapter 5
- Figure 5.1: [The Agent Router pattern](../assets/ch05/fig-5-1-the-agent-router-pattern.png)
- Figure 5.2: [Supervisor Architecture workflow](../assets/ch05/fig-5-2-supervisor-architecture-workflow.png)
- Figure 5.3: [Swarm Architecture workflow](../assets/ch05/fig-5-3-swarm-architecture-workflow.png)
- Figure 5.4: [Blackboard topology](../assets/ch05/fig-5-4-blackboard-topology.png)
- Figure 5.5: [Contract-Net Protocol](../assets/ch05/fig-5-5-contract-net-protocol.png)
- Figure 5.6: [Supervision Tree with Guarded Capabilities](../assets/ch05/fig-5-6-supervision-tree-with-guarded-capabilities.png)
- Figure 5.7: [Multi-Agent Planning workflow](../assets/ch05/fig-5-7-multi-agent-planning-workflow.png)
- Figure 5.8: [Agent information sharing](../assets/ch05/fig-5-8-agent-information-sharing.png)
- Figure 5.9: [Centralized tool routing example implementation](../assets/ch05/fig-5-9-centralized-tool-routing-example-implementation.png)
- Figure 5.10: [Agent consensus workflow](../assets/ch05/fig-5-10-agent-consensus-workflow.png)
- Figure 5.11: [Agent Negotiation workflow](../assets/ch05/fig-5-11-agent-negotiation-workflow.png)
- Figure 5.12: [Resource Allocation](../assets/ch05/fig-5-12-resource-allocation.png)
- Figure 5.13: [Conflict Resolution workflow](../assets/ch05/fig-5-13-conflict-resolution-workflow.png)
- Figure 5.14: [A single agent's control loop for Formation Control](../assets/ch05/fig-5-14-a-single-agent-s-control-loop-for-formation-contro.png)

### Chapter 6
- Figure 6.1: [Instruction Fidelity Auditing workflow](../assets/ch06/fig-6-1-instruction-fidelity-auditing-workflow.png)
- Figure 6.2: [FCoT internal reasoning loop](../assets/ch06/fig-6-2-fcot-internal-reasoning-loop.png)
- Figure 6.3: [FCoT use case example](../assets/ch06/fig-6-3-fcot-use-case-example.png)
- Figure 6.4: [Persistent Instruction Anchoring workflow](../assets/ch06/fig-6-4-persistent-instruction-anchoring-workflow.png)
- Figure 6.5: [Shared Epistemic Memory Workflow](../assets/ch06/fig-6-5-shared-epistemic-memory-workflow.png)

### Chapter 7
- Figure 7.1: [Robustness and fault tolerance pattern chaining](../assets/ch07/fig-7-1-robustness-and-fault-tolerance-pattern-chaining.png)
- Figure 7.2: [Parallel execution consensus workflow](../assets/ch07/fig-7-2-parallel-execution-consensus-workflow.png)
- Figure 7.3: [Delayed Escalation Strategy](../assets/ch07/fig-7-3-delayed-escalation-strategy.png)
- Figure 7.4: [Watchdog Timeout Supervisor](../assets/ch07/fig-7-4-watchdog-timeout-supervisor.png)
- Figure 7.5: [Adaptive Retry with Prompt Mutation](../assets/ch07/fig-7-5-adaptive-retry-with-prompt-mutation.png)
- Figure 7.6: [Auto-Healing Agent Resuscitation](../assets/ch07/fig-7-6-auto-healing-agent-resuscitation.png)
- Figure 7.7: [Incremental Checkpointing](../assets/ch07/fig-7-7-incremental-checkpointing.png)
- Figure 7.8: [Majority Voting Across Agents](../assets/ch07/fig-7-8-majority-voting-across-agents.png)
- Figure 7.9: [Causal Dependency Graph](../assets/ch07/fig-7-9-causal-dependency-graph.png)
- Figure 7.10: [Agent Self-Defense](../assets/ch07/fig-7-10-agent-self-defense.png)
- Figure 7.11: [Agent Mesh Defense](../assets/ch07/fig-7-11-agent-mesh-defense.png)
- Figure 7.12: [Execution Envelope Isolation](../assets/ch07/fig-7-12-execution-envelope-isolation.png)
- Figure 7.13: [Optimizing for Translation Overhead](../assets/ch07/fig-7-13-optimizing-for-translation-overhead.png)
- Figure 7.14: [Rate-Limited Invocation](../assets/ch07/fig-7-14-rate-limited-invocation.png)
- Figure 7.15: [Fallback Model Invocation](../assets/ch07/fig-7-15-fallback-model-invocation.png)
- Figure 7.16: [Trust Decay and Scoring](../assets/ch07/fig-7-16-trust-decay-and-scoring.png)
- Figure 7.17: [Canary Agent Testing](../assets/ch07/fig-7-17-canary-agent-testing.png)

### Chapter 8
- Figure 8.1: [Agent Calls Human escalation flow](../assets/ch08/fig-8-1-agent-calls-human-escalation-flow.png)
- Figure 8.2: [Agent Calls Human escalation flow (cont.)](../assets/ch08/fig-8-2-agent-calls-human-escalation-flow-cont.png)
- Figure 8.3: [Human Delegates to Agent workflow](../assets/ch08/fig-8-3-human-delegates-to-agent-workflow.png)
- Figure 8.4: [Human Calls Agent sequence](../assets/ch08/fig-8-4-human-calls-agent-sequence.png)
- Figure 8.5: [Agent Delegates to Agent architecture](../assets/ch08/fig-8-5-agent-delegates-to-agent-architecture.png)
- Figure 8.6: [Agent Calls Proxy Agent pattern for secure interaction](../assets/ch08/fig-8-6-agent-calls-proxy-agent-pattern-for-secure-interac.png)

### Chapter 9
- Figure 9.1: [The agent anatomy](../assets/ch09/fig-9-1-the-agent-anatomy.png)
- Figure 9.2: [The Single Agent Baseline pattern](../assets/ch09/fig-9-2-the-single-agent-baseline-pattern.png)
- Figure 9.3: [Single Agent loan agent workflow](../assets/ch09/fig-9-3-single-agent-loan-agent-workflow.png)
- Figure 9.4: [Agent-specific memory](../assets/ch09/fig-9-4-agent-specific-memory.png)
- Figure 9.5: [Context-aware retrieval (RAG) agent](../assets/ch09/fig-9-5-context-aware-retrieval-rag-agent.png)
- Figure 9.6: [A self-correction loop, where an agent generates a preliminary output and then critiques it against its goals,](../assets/ch09/fig-9-6-a-self-correction-loop-where-an-agent-generates-a.png)
- Figure 9.7: [Multimodal processing via multimodal pipeline](../assets/ch09/fig-9-7-multimodal-processing-via-multimodal-pipeline.png)
- Figure 9.8: [Native multimodal LLM multimodal processing](../assets/ch09/fig-9-8-native-multimodal-llm-multimodal-processing.png)

### Chapter 10
- Figure 10.1: [A system integration architecture showing how system-level patterns provide the foundational infrastructure](../assets/ch10/fig-10-1-a-system-integration-architecture-showing-how-syst.png)
- Figure 10.2: [A sequence diagram showing how system-level patterns chain together in an automated supply chain](../assets/ch10/fig-10-2-a-sequence-diagram-showing-how-system-level-patter.png)
- Figure 10.3: [The Tool and Agent Registry pattern decouples the agent from the tool implementation](../assets/ch10/fig-10-3-the-tool-and-agent-registry-pattern-decouples-the.png)
- Figure 10.4: [The Real-Time Compliance Monitoring pattern intercepts actions for policy adjudication](../assets/ch10/fig-10-4-the-real-time-compliance-monitoring-pattern-interc.png)
- Figure 10.5: [The Agent Authentication and Authorization pattern secures interactions using standard IAM protocols](../assets/ch10/fig-10-5-the-agent-authentication-and-authorization-pattern.png)
- Figure 10.6: [The Event-Driven Reactivity pattern enables scalable and responsive systems through a central message](../assets/ch10/fig-10-6-the-event-driven-reactivity-pattern-enables-scalab.png)

### Chapter 11
- Figure 11.1: [The Self-Improvement Flywheel for agentic systems](../assets/ch11/fig-11-1-the-self-improvement-flywheel-for-agentic-systems.png)
- Figure 11.2: [The planner-scorer architecture](../assets/ch11/fig-11-2-the-planner-scorer-architecture.png)
- Figure 11.3: [Components of a custom evaluation metric](../assets/ch11/fig-11-3-components-of-a-custom-evaluation-metric.png)
- Figure 11.4: [Synthetic data generation workflow](../assets/ch11/fig-11-4-synthetic-data-generation-workflow.png)
- Figure 11.5: [The co-evolutionary training loop](../assets/ch11/fig-11-5-the-co-evolutionary-training-loop.png)
- Figure 11.6: [The adversarial testing loop](../assets/ch11/fig-11-6-the-adversarial-testing-loop.png)
- Figure 11.7: [The cost management feedback loop](../assets/ch11/fig-11-7-the-cost-management-feedback-loop.png)
- Figure 11.8: [The ROI measurement pipeline](../assets/ch11/fig-11-8-the-roi-measurement-pipeline.png)

### Chapter 12
- Figure 12.1: [Level 1 patterns](../assets/ch12/fig-12-1-level-1-patterns.png)
- Figure 12.2: [Level 2 maturity](../assets/ch12/fig-12-2-level-2-maturity.png)
- Figure 12.3: [Level 3 patterns](../assets/ch12/fig-12-3-level-3-patterns.png)

### Chapter 13
- Figure 13.1: [Architectural diagram of the monolithic loan processing agent](../assets/ch13/fig-13-1-architectural-diagram-of-the-monolithic-loan-proce.png)

### Chapter 14
- Figure 14.1: [A simplified model of a hierarchical agent architecture](../assets/ch14/fig-14-1-a-simplified-model-of-a-hierarchical-agent-archite.png)
- Figure 14.2: [Contrasting monolithic with multi-agent architectures](../assets/ch14/fig-14-2-contrasting-monolithic-with-multi-agent-architectu.png)
