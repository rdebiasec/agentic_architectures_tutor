---
chapter: 15
title: "Agent Frameworks – Use Case: A Multi-Agent System for Loan Processing with CrewAI and LangGraph"
part: 3
part_name: "Part 3: Execution: Strategy, Use Cases, and The Future"
pdf_pages: [508, 545]
figures: 0
code_files: []
patterns: []
---

# Chapter 15: Agent Frameworks – Use Case: A Multi-Agent System for Loan Processing with CrewAI and LangGraph

Agent Frameworks - Use Case: A
Multi-Agent System for Loan
Processing with CrewAI and
LangGraph
Throughout this book, we've explored the concepts, architectures, and patterns that underpin agentic AI
systems. We've examined their building blocks, how they interact, and how they can be coordinated to tackle
complex tasks. However, translating these theoretical constructs into functional, production-ready applications
requires practical tools and libraries that handle the underlying complexities of agent creation, execution, and
communication. This is where agent frameworks come into play.
Building an agentic system from scratch involves managing numerous moving parts: defining agent roles and
capabilities, handling state and memory, orchestrating workflows, integrating LLMs, managing tool use (such
as function calling), and facilitating communication between agents.
Agent frameworks provide abstractions and pre-built components that simplify these tasks, allowing
developers to focus on the application logic and agent capabilities rather than reinventing the foundational
plumbing. They offer structured approaches to common challenges in agent development that promote faster
development cycles and more maintainable code, and often incorporate best practices for interaction and
control.
In the rapidly evolving landscape of agentic AI, several frameworks have emerged, each with its own philosophy,
strengths, and target use cases. While we will focus on three prominent examples to demonstrate
implementation, it is important to note that these are illustrative rather than exhaustive; the underlying design
patterns discussed in this book are universal and generalize to other frameworks.
In this chapter, we will provide a practical introduction to three prominent examples:
Google's Agent Development Kit (ADK)
CrewAI
LangGraph
We will start by briefly introducing each framework, highlighting its core concepts. Then, we will explore their
similarities and differences to help you understand their respective design philosophies. To make the
comparison concrete, we will reimplement the loan processing agent use case from Chapter 13 using both
CrewAI and LangGraph. Since we extensively utilized Google's ADK in the previous chapters to establish the
baseline architecture, we will not repeat that implementation here. Instead, we will focus on showing how the
same problem can be approached using different framework paradigms based on the code in our accompanying
notebook. Finally, we'll discuss key considerations when choosing an agent framework for your project,
emphasizing the importance of aligning the framework's capabilities with your specific use case, and the
ongoing need for robust observability and adherence to responsible AI principles, regardless of the tools you
choose.
Now that we understand the importance of frameworks in building agentic systems, let's take a closer look at
our first example: Google's ADK.
Technical requirements
To get the most out of the practical examples in this chapter, you will need the following:
A Python environment (version 3.10+)
A Jupyter Notebook interface (e.g., JupyterLab, Google Colab, or VS Code)
A Google Cloud project with the Vertex AI API enabled or a Google AI Studio API key
The following Python libraries installed: crewai, langgraph, langchain-google-genai, and googlecloud-aiplatform
The complete code for this chapter is available in the following folder within the book's GitHub repository:
https://github.com/PacktPublishing/Agentic-Architectural-Patterns-for-Building-MultiAgent-Systems/tree/main/Chapter_15.
Now that we understand the importance of frameworks in building agentic systems, let's take a closer look at
our first example: Google's ADK.
Google's Agent Development Kit (ADK)
As we saw in the previous examples, Google's ADK provides a structured environment for building and
ploying AI agents. It is designed with production readiness in mind, offering components for defining agents,
managing their life cycles, integrating tools, and facilitating communication, particularly in multi-agent
scenarios.
Chapter 15 472
ADK aims to provide the foundational scaffolding for building agents that can reason, plan, and interact reliably
## with external systems and other agents. Key features often include the following:

Agent abstraction: A base class or structure for defining an agent's core logic, including its
instructions, tools, and how it handles incoming tasks or messages.
Tool integration: Mechanisms for defining and registering tools (often functions or APIs) that agents
can utilize to interact with the outside world or perform specific actions, aligning with the concept of
agents using tools to act on their environment.
## Planning and reasoning: Integration with LLMs (such as Gemini) to power the agent's reasoning loop:

processing information, planning steps, and deciding when to use tools. ADK often includes built-in
planners or allows for custom planning logic.
State management: Mechanisms for agents to maintain state and memory across interactions, which
is crucial for complex, multi-step tasks.
Communication protocol: Native support for the Agent-to-Agent (A2A) interoperability protocol.
ADK enables agents to use A2A's standardized message formats and task life cycles to communicate and
collaborate across different frameworks and enterprise boundaries.
Runtime environment: An execution environment (agent runtime or agent engine) that manages
agent deployment, task distribution, parallel execution, and retries, and potentially integrates with
observability tools.
The loan processing example in Chapters 13 and 14 demonstrated how ADK allows defining distinct agent
functionalities (document validation, credit check, risk assessment, and compliance check) as tools and
orchestrating their execution via an LLM-powered agent following specific instructions. ADK provides the
structure to build such goal-oriented, tool-using agents within a managed runtime.
CrewAI
CrewAI offers different perspective on building agentic systems, focusing explicitly on collaborative
intelligence through role-playing agents. It provides a framework for orchestrating autonomous AI agents that
work together as a cohesive "crew."
The core philosophy behind CrewAI is that complex tasks can often be broken down and assigned to agents with
specific roles, responsibilities, and even "backstories" that guide their behavior and expertise. These agents then
collaborate, sharing information and intermediate results, to achieve a common objective.
## Key concepts in CrewAI include the following:

Agents: Defined with a specific role, goal, and backstory, the LLM they use, and potentially specific tools
they have access to. The role-playing aspect helps the LLM embody a particular persona or expertise.
Tasks: Specific assignments given to agents. Each task has a description and expected output and is
assigned to a particular agent. Tasks can be chained, allowing the output of one task to become the
input for another.
Tools: Similar to other frameworks, these are functions or capabilities agents can use to interact with
external systems or perform actions (e.g., search the web, access an API). In CrewAI, tools often inherit
from a BaseTool class.
473 Agent Frameworks - Use Case: A Multi-Agent System for Loan Processing with CrewAI and LangGraph
Crew: The collection of agents and the tasks they need to perform. The crew defines how the agents
collaborate.
Process: The workflow or methodology the crew follows to execute the tasks. Common processes
include sequential (tasks executed one after another) or hierarchical (a manager agent delegates tasks).
CrewAI emphasizes the social aspect of agent interaction, making it intuitive to design systems where different
AI personas contribute specialized skills, mirroring how human teams operate. It aims to simplify the creation
of multi-agent systems by providing high-level abstractions for defining roles and managing collaborative
workflows.
However, a key consideration for enterprise architects is that this "persona-driven" style can introduce
variability in the model's output. When applying CrewAI to regulated or high-stakes workflows, such as our
loan adjudication use case, it is critical to counterbalance this flexibility with strict tool contracts and rigorous
testing to ensure deterministic and compliant outcomes.
LangGraph
LangGraph extends the popular LangChain library, providing a robust way to build stateful, multi-actor
applications, including complex agentic systems, using graphs. While LangChain focuses on chaining calls
(linear sequences), LangGraph allows for cycles, making it suitable for modeling agent behaviors more flexibly,
as agents often need to loop, retry, or dynamically decide the next step based on the current state.
LangGraph represents gentic workflows as state machines. Each step in the workflow is a node in the graph,
and the transitions between steps are edges. This graph structure explicitly manages the application's state as it
evolves.
## Key concepts in LangGraph include the following:

StateGraph: The core object representing the workflow graph. It holds the application's state.
State: A defined ta structure (often a Python class or dictionary, such as TypedDict) that holds all the
information relevant to the workflow's progress (e.g., user input, intermediate results, agent messages).
Nodes: Functions or runnable objects that represent steps or actors (agents) in the graph. Each node
receives the current state, performs an action (such as calling an LLM, using a tool, or processing data),
and returns updates to the state.
Edges: Define the transitions between nodes. Edges determine the next node to execute based on the
current state or the output of the previous node.
Conditional edges: Allow for branching logic. Based on the current state or the output of a node, the
graph can route execution to different subsequent nodes, enabling complex decision-making and loops.
## LangGraph is particularly well suited for applications where the following apply:

Explicit state management is crucial
Cyclical processes are needed (e.g., an agent reflecting on its output and retrying, or Human-in-theLoop (HITL) interactions)
Complex control flow involving branching and dynamic routing is required
Modeling interactions between multiple agents or actors (including humans) is necessary
Chapter 15 474
By representing gent interactions as a graph, LangGraph provides fine-grained control over the flow of
execution and state persistence, making it a powerful tool for building sophisticated and reliable agentic
applications.
Now that we have seen what each of these frameworks is capable of, let's highlight the similarities and
differences between them.
Similarities and differences between the three
frameworks
While all three frameworks aim to help you build sophisticated agentic applications, their underlying
philosophies and architectures guide them toward different strengths.
Similarities
## All three rameworks share a common conceptual foundation:

LLM as the reasoning engine: At their heart, all three frameworks use an LLM (such as Gemini, GPT-4,
or an open source model) as the "brain" of the agent. The LLM is responsible for reasoning, planning,
and deciding what to do next based on a prompt, the current state, and available tools.
Tool integration: They are ll built around the Function Calling or Tool Use pattern, which we've
identified as fundamental to agentic AI. An gent's ability to act upon the world, for example, to search
a database, read a file, or call an API, is enabled by providing it with a set of tools. All three frameworks
provide a structured way to define these tools and make them available to the LLM.
Goal-oriented: These are not tools for simple, single-shot Q&A. They are designed to build applications
that can execute complex, multi-step tasks to achieve a specific, developer-defined goal.
Key differences
The primary differences lie in their core abstraction, that is, the mental model they use to represent an gentic
workflow. This fundamental difference influences everything from control flow to state management. To help
you evaluate which mental model best fits your specific use case, let's examine how each framework
## conceptualizes its primary building blocks and operational logic:

## Core philosophy and abstraction:

CrewAI-role-based collaboration: CrewAI's abstraction is a team of specialists. You define
agents by their role (e.g., "senior loan officer"), goal (e.g., "Analyze a loan application"), and
backstory (e.g., "You are a meticulous analyst..."). This makes it incredibly intuitive for
workflows that mimic human teams. The collaboration is the central feature.
LangGraph -stateful graphs: LangGraph's abstraction is a flowchart or state machine. You
define nodes (agents or functions) and edges (the paths between them). This shifts the focus
from the agents to the process. Its power lies in making the application's state explicit and the
control flow deterministic.
Google ADK -production-ready agents: ADK's abstraction is the agent itself, treated as a
modular, testable, and deployable software component. It provides a more structured, code-
◦
◦
◦
475 Agent Frameworks - Use Case: A Multi-Agent System for Loan Processing with CrewAI and LangGraph
first approach that feels familiar to software engineers. It focuses on the agent's life cycle and
## relies on two key mechanisms for enterprise robustness:

Callbacks (middleware for active filtering, PII detection, and HITL control)
Workflow agents (scaffolding for defining sequential, looping, or parallel tasks
alongside autonomous reasoning)
## Control flow and cyclical behavior:

CrewAI manages control flow at a high level. You typically define a process as either sequential
(task 1 -> Task 2 -> Task 3) or hierarchical (a manager agent delegates tasks). This is simple and
effective for linear or simple delegated tasks, as seen in our notebook's example.
LangGraph provides complete, fine-grained control. Because the workflow is a graph, you can
easily create cycles, branches, and loops. You can define conditional edges that say, "If the
validation failed, go to the 'Rejection' node; otherwise, go to the 'Credit Check' node." This
ability to manage errors and loop is a key requirement for many advanced agent patterns.
ADK balances these. It can run deterministic workflows (such as SequentialAgent) but also
allows for dynamic, LLM-driven planning where the agent itself decides the next steps, which
are then managed by the agent runtime.
State management:
LangGraph's superpower is its explicit state management. You define a State object (e.g., a
dictionary or TypedDict) that contains all the information for your application. This entire state
is passed to every node. Each node performs its work and returns updates to the state. This
makes debugging much easier; you can inspect the state at every single step.
CrewAI's state management is more implicit. The output of one task is automatically formatted
and passed as context to the next task that depends on it. This is fast for simple chains but offers
less direct control and inspection than LangGraph's explicit state.
ADK uses managed state. The agent runtime and session service are responsible for persisting
the agent's state and memory across interactions, abstracting this complexity away from the
developer and ensuring that even long-running agents can pick up where they left off.
Now that we have a deeper understanding of these frameworks, let's step back and compare them.
Comparative analysis: ADK, CrewAI, and LangGraph
Now that we have explored the individual characteristics of each framework, let's look at how they compare
side by side. This analysis will help you select the right tool based on your project's specific maturity,
complexity, and operational requirements.
The following table provides a high-level overview of the ecosystem and philosophy behind each framework:
▪
▪
◦
◦
◦
◦
◦
◦
Chapter 15 476
Framework Primary supporter Announced/launched Core philosophy and
focus
GoogleADK Google 2024 (prototype)/2025
(public)
A comprehensive, open
source toolkit for
building, evaluating, and
deploying productiongrade, robust agents.
Optimized for the
Google ecosystem
(Gemini and Vertex AI)
but designed to be
model-agnostic.
CrewAI CrewAI (founded by João
Moura)
2023 (open source
launch)
A framework or
orchestrating roleplaying, autonomous AI
agents. Emphasizes
collaborative
intelligence, where
agents work together as
a "crew" to accomplish
goals.
LangGraph LangChain 2024 An extension of
LangChain for building
stateful, multi-actor
applications. It excels at
creating applications
with cyclical processes
and complex control
flows by modeling them
as graphs (state
machines).
Table 15.1 - Agentic frameworks comparison
477 Agent Frameworks - Use Case: A Multi-Agent System for Loan Processing with CrewAI and LangGraph
For a deeper technical comparison, the following table breaks down the frameworks by their architectural
## approach, control flow mechanisms, and suitability for different development stages:

## Feature Google ADK CrewAI LangGraph

Core abstraction Production-grade agents
and runtimes.
Role-playing teams (a
"crew").
Stateful graph (a "state
machine").
Controlflow Planner-driven;
managed by an agent
runtime. Can be
sequential or parallel.
High-level process
(sequential or
hierarchical).
Fine-grained; defined by
graph edges. Excellent
for cycles and branching.
Statemanagement Managed: Handled by
the agent's session and
runtime.
Implicit: Passed between
tasks automatically via
context.
Explicit: A central State
object is passed to and
updated by each node.
Callbacks andhooks Middleware/Interceptor
pattern. Callbacks act as
"guardrails" designed to
intercept input/output
before or after LLM calls.
Key pability:
Modifying data in flight
(e.g., PII redaction) or
bypassing the LLM
entirely (caching).
Event-driven hooks.
Callbacks are triggered
on specific life cycle
events (e.g.,
on_task_start,
on_task_end).
Key capability:
Observability and side
effects (logging,
updating a UI, or
triggering a webhook)
without altering the core
agent logic.
State listeners and
interrupts. Uses
callbacks for tracing
(LangSmith) but relies
on "interrupts" for
control.
Key capability: Pausing
the graph at a specific
node (checkpointing) to
wait for HITL input
before resuming.
Bestfor... Production systems,
enterprise integration
(especially Google
Cloud), robust and
testable agents.
Rapid prototyping of
collaborative tasks, roledefined workflows (e.g.,
"researcher," "writer").
Complex, dynamic
workflows; explicit error
handling; loops; and
HITL.
Table 15.2 - Comparison between the ADK, CrewAI, and LangGraph frameworks
To understand these differences better, let's now reimplement our loan processing use case from Chapter 13,
using the specific code from our development notebook.
Chapter 15 478
Re-implementing the loan agent: A practical comparison
To illustrate the differences between these frameworks concretely, we will now implement the multi-agent loan
processing system based on the code in the accompanying notebook. The goal remains to take applicant_id
and document_id, fetch the document content, and produce a final, auditable loan decision.
The workflow involves several distinct tasks. Next, we map each task to the specific component that handles it
## in our two implementations:

## Document fetch: Retrieve the content of the loan application document (LangGraph:

node_fetch_document | CrewAI: Passed as initial input/preprocessing).
Document validation: Check whether the fetched document content is valid and complete
(LangGraph: node_validate_document | CrewAI: Document validation specialist).
## Credit check: Retrieve the borrower's credit score based on their customer_id value (LangGraph:

node_check_credit | CrewAI: Credit check agent).
Risk assessment: Analyze the document status, credit score, and income to determine a risk level
(LangGraph: node_assess_risk | CrewAI: Risk assessment analyst).
## Compliance check: Ensure the final decision adheres to lending regulations (LangGraph:

node_check_compliance | CrewAI: Compliance officer).
We will build this workflow in both CrewAI and LangGraph to highlight their different approaches using
Google's Gemini LLM.
Regardless of the framework, the agent's ability to interact with external systems is defined by its tools. For both
implementations, we define our core business logic. In the provided notebook, these are defined as Python
## classes inheriting from CrewAI's BaseTool:

```python
# --- Define Tool Classes inheriting from BaseTool ---
import json
from crewai.tools import BaseTool
classValidateDocumentFieldsTool(BaseTool):
name: str = "Validate Document Fields"
description: str = (
"Validates that the loan application JSON string contains the required fields: "
"'customer_id', 'loan_amount', 'income', and 'credit_history'."
)
```

def_run(self, application_data: str) -> str:
"""Validates the application data."""
print(f"--- TOOL: Validating document fields ---")
try:
data = json.loads(application_data)
required_fields = ["customer_id", "loan_amount", "income", "credit_history"]
1.
2.
3.
4.
5.
479 Agent Frameworks - Use Case: A Multi-Agent System for Loan Processing with CrewAI and LangGraph
missing_fields = [field for field in required_fields if field notin data]
if missing_fields:
return json.dumps({"error":
f"Validation failed: Missing required fields: {', '.join(missing_fields)}"})
```python
# Return the original data if valid
return json.dumps({"status": "validated", "data": data})
except json.JSONDecodeError:
return json.dumps({"error": "Invalid JSON format in application data."})
classQueryCreditBureauAPITool(BaseTool):
name: str = "Query Credit Bureau API"
description: str = (
"Simulates a call to a credit bureau API to retrieve a credit score given a
customer_id."
)
```

def_run(self, customer_id: str) -> str:
"""Queries the mock credit bureau."""
print(f"--- TOOL: Calling Credit Bureau API for customer: {customer_id} ---")
mock_credit_scores = {
"CUST-12345": 810, # Happy Path
"CUST-55555": 620, # High Risk Path
"borrower_good_780": 810,
"borrower_bad_620": 620
}
score = mock_credit_scores.get(customer_id)
## if score isnotNone:

return json.dumps({"customer_id": customer_id, "credit_score": score})
return json.dumps({"error": "Customer ID not found."})
classCalculateRiskScoreTool(BaseTool):
name: str = "Calculate Risk Score"
description: str = (
"Calculates a risk score based on loan_amount, income, and credit_score."
)
## def_run(self, loan_amount: int, income: str, credit_score: int) -> str:

"""Calculates the risk score."""
print(f"--- TOOL: Calculating risk score ---")
try:
```python
# Attempt to parse income string (e.g., "USD 120000 a year", "$60k/month")
income_value = int(''.join(filter(str.isdigit, income)))
annual_income = income_value * 12if"month"in income.lower() else
income_value
Chapter 15 480
```

except (ValueError, TypeError):
annual_income = 0# Default to 0 if income cannot be parsed
## if annual_income == 0:

risk_score = 10# Assign highest risk if income is zero or invalid
else:
loan_to_income_ratio = loan_amount / annual_income
risk_score = 1# Start with base risk
if credit_score < 650: risk_score += 4
elif credit_score < 720: risk_score += 2
if loan_to_income_ratio > 0.8: risk_score += 5
elif loan_to_income_ratio > 0.5: risk_score += 2
```python
# Cap risk score at 10
return json.dumps({"risk_score": min(risk_score, 10)})
classCheckLendingComplianceTool(BaseTool):
name: str = "Check Lending Compliance"
description: str = (
"Checks the application against internal policies using credit_history and
risk_score."
)
```

def_run(self, credit_history: str, risk_score: int) -> str:
"""Checks compliance rules."""
print(f"--- TOOL: Checking compliance rules (including risk score) ---")
## if credit_history == "No History":

return json.dumps({"is_compliant": False, "reason": "Policy violation: No
credit history is an automatic denial."})
if risk_score >= 8: # Risk score of 8 or higher is non-compliant
return json.dumps({"is_compliant": False, "reason": f"Policy violation: Risk
score of {risk_score} is too high for approval."})
return json.dumps({"is_compliant": True, "reason": "Application meets all
internal policy guidelines."})
```python
# --- Instantiate the Tools ---
validate_document_fields_tool = ValidateDocumentFieldsTool()
query_credit_bureau_api_tool = QueryCreditBureauAPITool()
calculate_risk_score_tool = CalculateRiskScoreTool()
check_lending_compliance_tool = CheckLendingComplianceTool()
481 Agent Frameworks - Use Case: A Multi-Agent System for Loan Processing with CrewAI and LangGraph
```

We also need a helper function to simulate fetching the document content based on an ID:
```python
# --- Helper Function for Mock Data ---
import json
```

defget_document_content(document_id: str) -> str:
"""
Simulates fetching document content based on its ID.
Returns a JSON STRING.
"""
print(f"--- HELPER: Simulating fetch for doc_id: {document_id} ---")
## if document_id == "document_valid_123":

data = {
"customer_id": "CUST-12345",
"loan_amount": 50000,
"income": "USD 120000 a year",
"credit_history": "7 years"
}
return json.dumps(data)
## elif document_id == "document_invalid_456":

data = {
"customer_id": "CUST-55555",
"loan_amount": 200000,
```python
# "income" is missing
"credit_history": "1 year"
}
return json.dumps(data)
else:
return json.dumps({"error": "Document ID not found."})
Note on tool output patterns
You will notice that these tools return JSON-encoded strings rather than Python dictionaries. This is a
deliberate design choice for agentic systems. Since the primary consumer of a tool's output is often the
LLM itself (which processes text tokens), returning an explicit JSON string ensures the model receives a
```

structured, readable format that it can easily parse or reason about.
Furthermore, we are establishing a data contract here: the tool guarantees it will return either a
{"status": "validated", "data":...} structure for success or an {"error":...} structure for
failure. This consistency allows downstream agents (or the CheckLendingCompliance tool) to handle
errors deterministically.
Note
Chapter 15 482
Now, let's see how CrewAI and LangGraph orchestrate these same tools.
Implementation 1: CrewAI (the collaborative team)
The notebook implements CrewAI using a hierarchical process, where a manager agent delegates tasks to
specialized agents:
Define the LLM and agents.
First, we configure the Gemini LLM using CrewAI's LLM abstraction. Then, we define the specialist
## agents, each ssigned with specific tools, and the manager gent, which has no tools but can delegate:

```python
import os
import json
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import BaseTool
# Assume tools (ValidateDocumentFieldsTool, etc.) and get_document_content are
defined above
# --- Initialize the LLM ---
# Assumes GOOGLE_API_KEY environment variable is set
llm = LLM(
model='gemini/gemini-2.5-flash', # Or another Gemini model
api_key=os.getenv("GOOGLE_API_KEY"),
temperature=0.0
)
Production tip: Data normalization patterns
```

In this xample, the CalculateRiskScoreTool performs basic string parsing to extract income figures.
In a production environment, this approach is too fragile. You should implement a dedicated
normalization node or preprocessing tool upstream that handles currency conversion, locale formatting
(e.g., "$100k" versus "100,000 EUR"), and standardization before the data ever reaches the logic-heavy
risk assessment agents.
Tip
Production pattern -the proxy tool (Agent Calls Proxy Agent)
The preceding if/else logic is a simplified heuristic for demonstration. In a real-world enterprise
architecture, this tool would function s a proxy (see the Agent Calls Proxy Agent pattern in Chapter 8).
The _run method would act as a wrapper that constructs a secure API request to an external risk decision
engine or a deployed ML model endpoint, executes the call, and parses the response. This pattern keeps
the agent lightweight and ensures that critical business logic remains centralized and governable.
Note
1.
483 Agent Frameworks - Use Case: A Multi-Agent System for Loan Processing with CrewAI and LangGraph
```python
# --- Define Agents ---
# 1. Document Validation Agent
doc_specialist = Agent(
role="Document Validation Specialist",
goal="Validate the completeness and format of a new loan application provided as
a JSON string.",
backstory=(
"You are a meticulous agent responsible for the first step of loan
processing. "
"Your sole task is to receive a JSON string, call the `Validate Document
Fields` tool, "
"and return its exact JSON output. You do not talk to the user or other
agents."
),
tools=[validate_document_fields_tool],
llm=llm,
allow_delegation=False,
verbose=True
)
# 2. Credit Check Agent
credit_analyst = Agent(
role="Credit Check Agent",
goal="Query the credit bureau API to retrieve an applicant's credit score.",
backstory=(
"You are a specialized agent that interacts with the Credit Bureau. "
"Your sole task is to receive a `customer_id`, call the `Query Credit
Bureau API` tool, "
"and return its exact JSON output."
),
tools=[query_credit_bureau_api_tool],
llm=llm,
allow_delegation=False,
verbose=True
)
# 3. Risk Assessment Agent
risk_assessor = Agent(
role="Risk Assessment Analyst",
goal="Calculate the financial risk score for a loan application.",
backstory=(
"You are a quantitative analyst agent. Your sole task is to receive
`loan_amount`, `income`, and `credit_score`, "
Chapter 15 484
"call the `Calculate Risk Score` tool, and return its exact JSON output."
),
tools=[calculate_risk_score_tool],
llm=llm,
allow_delegation=False,
verbose=True
)
# 4. Compliance Agent
compliance_officer = Agent(
role="Compliance Officer",
goal="Check the application against all internal lending policies and
compliance rules.",
backstory=(
"You are the final checkpoint for policy and compliance. Your sole task
is to receive `credit_history` and `risk_score`, "
"call the `CheckLendingCompliance` tool, and return its exact JSON
output."
),
tools=[check_lending_compliance_tool],
llm=llm,
allow_delegation=False,
verbose=True
)
# 5. Manager Agent (for the final report)
manager = Agent(
role="Loan Processing Manager",
goal="Manage the loan application workflow and compile the final report.",
backstory=(
"You are the manager responsible for orchestrating the "
"loan processing pipeline, ensuring data flows correctly, and formulating the "
"final decision and report based on your team's findings."
),
llm=llm,
allow_delegation=True, # The manager delegates tasks
verbose=True
)
485 Agent Frameworks - Use Case: A Multi-Agent System for Loan Processing with CrewAI and LangGraph
Define the tasks.
Next, we define the tasks. Note how the description for task_validate includes a placeholder,
{document_content}, which will receive the fetched JSON string as input. The context parameter
```

implicitly passes outputs between dependent tasks:
```python
# Define input document IDs for testing
loan_application_doc_ids = {
"valid": "document_valid_123",
"invalid": "document_invalid_456"
}
# Task 1: Validate Document Content
task_validate = Task(
description=(
```

"Validate the loan application, which is provided as a JSON string:
'{document_content}'. "
"You MUST pass this entire JSON string directly to the 'Validate Document Fields'
tool."
),
expected_output="A JSON string with the validation status and all extracted
data ('status': '...', 'data': {...}) or an error message.",
```python
# Agent is not assigned here; manager will delegate
)
# Task 2: Check Credit
task_credit = Task(
description=(
"1. Parse the JSON output from the validation task. \\n"
"2. Extract the `customer_id` from its 'data' field. \\n"
"3. Call the `Query Credit Bureau API` tool with this `customer_id`."
),
expected_output="A JSON string containing the customer_id and their
Minimizing variance with temperature
We deliberately set temperature=0.0 for this agent. In agentic workflows that rely on precise tool usage
and structured outputs (such as JSON), minimizing randomness is crucial. Note that while
temperature=0.0 significantly reduces variance, it does not guarantee 100% deterministic behavior due
to the inherent non-determinism of floating-point operations on GPUs. However, it provides the
```

maximum stability possible for logic and orchestration tasks.
Tip
1.
Chapter 15 486
credit_score.",
context=[task_validate] # Depends on task_validate
)
```python
# Task 3: Assess Risk
task_risk = Task(
description=(
"1. Parse the JSON output from the validation task to get `loan_amount`
and `income`. \\n"
"2. Parse the JSON output from the credit check task to get
`credit_score`. \\n"
"3. Call the `Calculate Risk Score` tool with these three values."
),
expected_output="A JSON string containing the calculated risk_score.",
context=[task_validate, task_credit] # Depends on two tasks
)
# Task 4: Check Compliance
task_compliance = Task(
description=(
"1. Parse the JSON output from the validation task to get
`credit_history`. \\n"
"2. Parse the JSON output from the risk assessment task to get
`risk_score`. \\n"
"3. Call the `Check Lending Compliance` tool with these two values."
),
```

expected_output="A JSON string with the compliance status (is_compliant:
true/false) and a reason.",
context=[task_validate, task_risk] # Depends on two tasks
)
```python
# Task 5: Compile Final Report
task_report = Task(
description=(
"Compile a final loan decision report synthesizing all findings from the
previous tasks. "
"The report must include: \\n"
"- The final decision (Approve/Deny). \\n"
"- A clear justification for the decision, referencing the validation
status, "
"credit score, risk score, and compliance check."
),
expected_output="A comprehensive final report in Markdown format.",
context=[task_validate, task_credit, task_risk, task_compliance]
487 Agent Frameworks - Use Case: A Multi-Agent System for Loan Processing with CrewAI and LangGraph
# Depends on all tasks
)
Assemble nd run the crew.
```

Finally, we assemble the Crew, specifying the hierarchical process and assigning the manager_agent.
## We fetch the document content before kicking off the crew and pass it as input:

```python
# Assemble the crew
loan_crew = Crew(
agents=[doc_specialist, credit_analyst, risk_assessor, compliance_officer],
# Manager assigned below
tasks=[task_validate, task_credit, task_risk, task_compliance, task_report],
process=Process.hierarchical,
manager_agent=manager,
verbose=True
)
# --- Run with VALID inputs ---
print("--- KICKING OFF CREWAI PROCESS (VALID INPUTS) ---")
valid_json_content = get_document_content(loan_application_doc_ids['valid'])
inputs_valid = {'document_content': valid_json_content}
result_valid = loan_crew.kickoff(inputs=inputs_valid)
print("\n\n--- CREWAI FINAL REPORT (VALID) ---")
print(result_valid)
# --- Run with INVALID inputs ---
print("\n\n--- KICKING OFF CREWAI PROCESS (INVALID INPUTS) ---")
invalid_json_content = get_document_content(loan_application_doc_ids['invalid'])
inputs_invalid = {'document_content': invalid_json_content}
result_invalid = loan_crew.kickoff(inputs=inputs_invalid)
print("\n\n--- CREWAI FINAL REPORT (INVALID) ---")
print(result_invalid)
CrewAI's hierarchical pproach allows the manager agent to orchestrate the workflow. The manager delegates
each task to the appropriate specialist agent based on the task description and available tools. Error handling is
somewhat implicit; if task_validate returns an error (such as the missing 'income' field in the invalid case),
```

subsequent tasks that depend on its output might still run but will likely fail or produce incorrect results, as the
manager attempts to proceed. The final report in the invalid case reflects the validation failure, but the
intermediate steps (credit check, risk assessment) are still executed, potentially performing unnecessary
actions.
2.
Chapter 15 488
Implementation 2: LangGraph (the state machine)
LangGraph's implementation uses an explicit state machine. We define nodes for each step, including fetching
## the document, and use conditional edges for robust error handling:

Define the state.
We define LoanGraphState using TypedDict, including all fields needed by the tools and nodes
## throughout the process:

#@title 2.1: Define LangGraph State
```python
import typing
import json
classLoanGraphState(typing.TypedDict):
"""
```

Represents the state of our loan processing graph.
It contains all the data that needs to be passed between nodes.
"""
applicant_id: str# Initial input, may not be directly used if
customer_id is in doc
document_id: str # Initial input
document_content: str # Fetched content (JSON string)
```python
# Data extracted or generated by tools/nodes
validation_status: str
customer_id: str
loan_amount: int
income: str
credit_history: str
credit_score: int
risk_score: int
risk_level: str# Added for LLM-based risk assessment output
compliance_status: str
# Final output
final_decision: str# Simplified final report/decision string
error: str# To track errors explicitly
Define the graph nodes.
```

We define Python functions as nodes.node_fetch_document simulates fetching content.
node_validate_document calls the validation tool and updates the state with extracted data or an error.
1.
2.
489 Agent Frameworks - Use Case: A Multi-Agent System for Loan Processing with CrewAI and LangGraph
Subsequent nodes check for errors before proceeding.node_assess_risk uses the LLM directly to
## generate a risk assessment:

#@title 2.2: Define LangGraph Nodes
```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# Re-initialize LLM specifically for LangGraph (using LangChain's integration)
lg_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash") # Or your preferred
Gemini model
# Node 0: Fetch Document Content
defnode_fetch_document(state: LoanGraphState):
print("--- NODE: Fetching Document ---")
doc_id = state["document_id"]
try:
content = get_document_content(doc_id)
# Check if the helper returned an error (e.g., document not found)
content_json = json.loads(content)
if"error"in content_json:
print(f" Error fetching document: {content_json['error']}")
return {
```

"error": f"Failed to fetch document {doc_id}:
{content_json['error']}",
"document_content": ""
}
return {"document_content": content}
## except Exception as e:

print(f" Error during document fetch node: {e}")
return {"error": f"Critical error fetching document {doc_id}",
"document_content": ""}
```python
# Node 1: Validate Document
defnode_validate_document(state: LoanGraphState):
print("--- NODE: Validating Document ---")
# Check if fetch already failed
if state.get("error"):
return {"validation_status": "SKIPPED due to fetch error"}
doc_content = state["document_content"]
try:
result_str =
validate_document_fields_tool._run(application_data=doc_content)
Chapter 15 490
result_json = json.loads(result_str)
if"error"in result_json:
validation_status = f"Validation FAILED: {result_json['error']}"
print(f" ->{validation_status}")
# Explicitly set error state
```

return {"validation_status": validation_status, "error":
validation_status}
else:
validation_status = result_json.get('status', 'Validation PASSED')
app_data = result_json.get("data", {})
print(f" ->{validation_status}")
```python
# Update state with extracted data
return {
"validation_status": validation_status,
"customer_id": app_data.get("customer_id"),
"loan_amount": app_data.get("loan_amount"),
"income": app_data.get("income"),
"credit_history": app_data.get("credit_history"),
"error": None# Clear any previous error if validation succeeds
}
```

except Exception as e:
validation_status = f"Critical error during validation node: {e}"
print(f" ->{validation_status}")
## return {"validation_status": validation_status, "error":

validation_status}
```python
# Node 2: Check Credit
defnode_check_credit(state: LoanGraphState):
print("--- NODE: Checking Credit ---")
if state.get("error"): # Skip if validation failed
return {"credit_score": -1}
cust_id = state["customer_id"]
try:
result_str = query_credit_bureau_api_tool._run(customer_id=cust_id)
result_json = json.loads(result_str)
if"error"in result_json:
print(f" ->Error: {result_json['error']}")
# Set error state if credit check fails
```

return {"credit_score": -1, "error": f"Credit check failed:
{result_json['error']}"}
score = result_json.get("credit_score", -1)
print(f" -> Credit Score: {score}")
491 Agent Frameworks - Use Case: A Multi-Agent System for Loan Processing with CrewAI and LangGraph
return {"credit_score": score, "error": None} # Clear error on success
## except Exception as e:

print(f" Critical error during credit check node: {e}")
## return {"error": "Critical error in credit check tool.", "credit_score":

-1}
```python
# Node 3: Assess Risk (LLM-Powered)
defnode_assess_risk(state: LoanGraphState):
print("--- NODE: Assessing Risk (LLM-Powered) ---")
if state.get("error"):
return {"risk_score": -1, "risk_level": "UNKNOWN"}
prompt = ChatPromptTemplate.from_template(
```

"""You are a senior loan underwriter. Assess the financial risk based on:
- Validation Status: {validation}
- Credit Score: {credit}
- Loan Amount: {amount}
- Applicant Income: {income}
- Credit History: {history}
## Provide a one-sentence justification, then conclude with the risk level:

LOW, MEDIUM, or HIGH.
Example:
Justification: Applicant has excellent credit and low debt-to-income.
Risk: LOW
"""
)
parser = StrOutputParser()
risk_chain = prompt | lg_llm | parser
try:
result_str = risk_chain.invoke({
"validation": state.get("validation_status", "N/A"),
"credit": state.get("credit_score", "N/A"),
"amount": state.get("loan_amount", "N/A"),
"income": state.get("income", "N/A"),
"history": state.get("credit_history", "N/A")
})
print(f" -> LLM Assessment Output:\n{result_str}")
```python
# Basic parsing
risk_level = "UNKNOWN"
if"LOW"in result_str.upper(): risk_level = "LOW"
elif"MEDIUM"in result_str.upper(): risk_level = "MEDIUM"
Chapter 15 492
elif"HIGH"in result_str.upper(): risk_level = "HIGH"
score_map = {"LOW": 3, "MEDIUM": 6, "HIGH": 9, "UNKNOWN": 10}
risk_score = score_map.get(risk_level, 10)
print(f" -> Parsed Risk Level: {risk_level},Score: {risk_score}")
```

return {"risk_score": risk_score, "risk_level": risk_level, "error":
None}
## except Exception as e:

print(f" Critical error during LLM risk assessment node: {e}")
## return {"error": "Critical error in LLM Risk assessment.", "risk_score":

-1, "risk_level": "UNKNOWN"}
```python
# Node 4: Check Compliance
defnode_check_compliance(state: LoanGraphState):
print("--- NODE: Checking Compliance ---")
if state.get("error"):
return {"compliance_status": "SKIPPED due to prior error."}
try:
result_str = check_lending_compliance_tool._run(
credit_history=state["credit_history"],
risk_score=state["risk_score"]
)
result_json = json.loads(result_str)
status = result_json.get("reason", "Check FAILED")
print(f" -> Compliance Status: {status}")
# Set error if non-compliant, otherwise clear it
error_msg = status if result_json.get("is_compliant") isFalseelseNone
return {"compliance_status": status, "error": error_msg}
```

except Exception as e:
print(f" Critical error during compliance check node: {e}")
return {"error": "Critical error in compliance check tool.",
"compliance_status": "Check FAILED due to tool error."}
```python
# Node 5: Compile Final Report (Handles success path)
defnode_compile_report(state: LoanGraphState):
print("--- NODE: Compiling Success Report ---")
# This node is only reached if all previous steps succeeded without setting
the error state
decision = "Approve"
reason = (f"Approved based on:\n"
f" - Validation: {state.get('validation_status', 'N/A')}\n"
f" - Credit Score: {state.get('credit_score', 'N/A')}\n"
493 Agent Frameworks - Use Case: A Multi-Agent System for Loan Processing with CrewAI and LangGraph
```

f" - Risk Assessment: {state.get('risk_level', 'N/A')} (Score:
{state.get('risk_score', 'N/A')})\n"
f" - Compliance: {state.get('compliance_status', 'N/A')}")
report = f"FINAL DECISION: {decision}\nREASON: {reason}"
return {"final_decision": report.strip()}
```python
# Node 6: Compile Rejection Report (Handles any failure path)
defnode_compile_rejection(state: LoanGraphState):
print("--- NODE: Compiling Rejection Report ---")
decision = "Deny"
reason = f"Denied due to error: {state.get('error', 'Unknown error during
processing.')}"
# Add more specific reasons based on which stage failed if needed
```

if"Validation FAILED"in state.get("validation_status", ""):
## reason = f"Denied due to validation failure:

{state.get('validation_status', '')}"
## elif"Credit check failed"in state.get("error", ""):

reason = f"Denied due to credit check failure: {state.get('error', '')}"
elif"compliance"in state.get("error", "").lower(): # Check if compliance
node set the error
## reason = f"Denied due to compliance failure:

{state.get('compliance_status', '')}"
report = f"FINAL DECISION: {decision}\nREASON: {reason}"
return {"final_decision": report.strip()}
Production tip: Enforcing structured output
In this example, we use simple string matching to parse the LLM's response. In a production
system, this is risky as the model might be verbose (e.g., "The risk is relatively LOW"). For
enterprise applications, you should use structured output features (supported by both
LangChain and Gemini). By passing a Pydantic schema to the model, you can force it to return a
valid JSON object (e.g., {"risk_level": "LOW"}), guaranteeing that the output matches your
downstream requirements without the need for fragile string parsing logic.
Note
Chapter 15 494
Define the graph and its edges.
We wire the nodes, starting with fetch_doc. Crucially, we add conditional edges after fetch_doc and
validate_doc that heck the error field in the state, routing to compile_rejection immediately if an
error occurs:
#@title 2.3: Define and Compile the Graph
from langgraph.graph import StateGraph, END
workflow = StateGraph(LoanGraphState)
```python
# Add nodes
workflow.add_node("fetch_doc", node_fetch_document)
workflow.add_node("validate_doc", node_validate_document)
workflow.add_node("check_credit", node_check_credit)
workflow.add_node("assess_risk", node_assess_risk)
workflow.add_node("check_compliance", node_check_compliance)
workflow.add_node("compile_report", node_compile_report) # Success end node
workflow.add_node("compile_rejection", node_compile_rejection) # Failure end node
# Set entry point
workflow.set_entry_point("fetch_doc")
# Define conditional edge logic
defdecide_after_fetch(state: LoanGraphState):
return"reject"if state.get("error") else"continue"
defdecide_after_validation(state: LoanGraphState):
return"reject"if state.get("error") else"continue"
defdecide_after_credit_check(state: LoanGraphState):
return"reject"if state.get("error") else"continue"
defdecide_after_risk(state: LoanGraphState):
# Even if risk is HIGH, we proceed to compliance check,
```

# but compliance node might set error state.
return"reject"if state.get("error") else"continue"
defdecide_after_compliance(state: LoanGraphState):
```python
# If compliance node set an error (e.g., non-compliant), reject.
return"reject"if state.get("error") else"continue"
# Add edges
```

workflow.add_conditional_edges("fetch_doc", decide_after_fetch, {"continue":
1.
495 Agent Frameworks - Use Case: A Multi-Agent System for Loan Processing with CrewAI and LangGraph
"validate_doc", "reject": "compile_rejection"})
workflow.add_conditional_edges("validate_doc", decide_after_validation,
{"continue": "check_credit", "reject": "compile_rejection"})
workflow.add_conditional_edges("check_credit", decide_after_credit_check,
{"continue": "assess_risk", "reject": "compile_rejection"})
## workflow.add_conditional_edges("assess_risk", decide_after_risk, {"continue":

"check_compliance", "reject": "compile_rejection"})
workflow.add_conditional_edges("check_compliance", decide_after_compliance,
{"continue": "compile_report", "reject": "compile_rejection"})
```python
# Define end points
workflow.add_edge("compile_report", END)
workflow.add_edge("compile_rejection", END)
# Compile
try:
app = workflow.compile()
print("LangGraph Compiled Successfully!")
# Optional: Visualize
# from IPython.display import Image, display
# display(Image(app.get_graph().draw_mermaid_png()))
```

except Exception as e:
print(f"Error compiling LangGraph: {e}")
app = None
Run the graph.
We run the compiled graph (app) using.stream() to observe the state transitions for both valid and
## invalid document IDs:

#@title 2.4: Run the LangGraph Workflow
## if app isNone:

print("LangGraph app not compiled. Skipping execution.")
else:
```python
# --- Test 1: Valid Data ---
print("\n--- LANGGRAPH RUN 1: VALID DOCUMENT ---")
inputs_valid = {
"applicant_id": "borrower_good_780", # Included but might not be used if
customer_id is preferred
"document_id": "document_valid_123",
}
print("Streaming intermediate steps (Valid):")
```

for s_chunk in app.stream(inputs_valid, {"recursion_limit": 10}):
step_name = list(s_chunk.keys())[0]
print(f" Step: {step_name}") # Simpler logging
2.
Chapter 15 496
```python
# print(f" Output: {s_chunk[step_name]}") # Uncomment for full state
change detail
print("-" * 10)
print("\nInvoking for final state (Valid)...")
final_state_valid = app.invoke(inputs_valid, {"recursion_limit": 10})
print("\n--- LANGGRAPH FINAL REPORT (VALID) ---")
print(final_state_valid.get('final_decision', 'Final decision not found.'))
# print("\nFull Final State (Valid):", final_state_valid) # Uncomment to see
full state
# --- Test 2: Invalid Data ---
print("\n\n--- LANGGRAPH RUN 2: INVALID DOCUMENT ---")
inputs_invalid = {
"applicant_id": "borrower_bad_620",
"document_id": "document_invalid_456",
}
print("Streaming intermediate steps (Invalid):")
```

for s_chunk in app.stream(inputs_invalid, {"recursion_limit": 10}):
step_name = list(s_chunk.keys())[0]
print(f" Step: {step_name}")
```python
# print(f" Output: {s_chunk[step_name]}")
print("-" * 10)
print("\nInvoking for final state (Invalid)...")
final_state_invalid = app.invoke(inputs_invalid, {"recursion_limit": 10})
print("\n--- LANGGRAPH FINAL REPORT (INVALID) ---")
print(final_state_invalid.get('final_decision', 'Final decision not found.'))
# print("\nFull Final State (Invalid):", final_state_invalid)
This LangGraph implementation demonstrates explicit control flow and state management. The addition of
node_fetch_document makes the process start cleanly. The conditional edges based on the error key in the state
ensure that if fetching or validation fails, the graph immediately routes to the compile_rejection node,
```

preventing unnecessary tool calls (such as credit check or risk assessment) on invalid data.
This explicit routing provides a tangible efficiency gain: it liminates unnecessary API costs and latency by
halting execution immediately upon failure, a direct contrast to our CrewAI example, where intermediate agents
continued to operate despite the initial validation error.
The use of an LLM directly within node_assess_risk showcases how LangGraph can integrate generative steps
alongside deterministic tool calls. This graph-based approach provides superior robustness and traceability
compared to the simpler CrewAI process for this specific workflow, especially concerning error handling.
Let's now go through the observability and responsible AI considerations.
497 Agent Frameworks - Use Case: A Multi-Agent System for Loan Processing with CrewAI and LangGraph
Observability and responsible AI considerations
Choosing a framework isn't just about the development experience; it's about your ability to manage, monitor,
and govern the resulting application. In the context of agentic AI, where non-determinism is a factor,
observability is a cornerstone of responsible AI. If you cannot trace why an agent made a decision, you cannot
ensure it is fair, safe, or compliant.
Observability in practice
Each framework leverages specific tools and protocols to provide the visibility required for debugging complex
## agent interactions and maintaining a verifiable audit trail:

LangGraph and CrewAI (with LangSmith): The LangChain ecosystem, including LangGraph and
CrewAI, is built to integrate natively with LangSmith. LangSmith is an observability platform
specifically designed for tracing complex LLM applications. Because LangGraph's state is explicit, its
traces in LangSmith are incredibly detailed, allowing you to "time-travel" debug by seeing the full state
and LLM calls at every single node. CrewAI traces also benefit from LangSmith, which shows the
actions and tool calls of an agent. This provides a complete audit trail of the agent's thoughts and
actions, which is invaluable for debugging and explainability.
Google ADK: As a production-focused toolkit, ADK is instrumented with OpenTelemetry, the industry
standard for tracing and metrics. This allows it to integrate directly with enterprise-grade monitoring
solutions such as Google Cloud'soperations suite (Cloud Trace and Cloud Logging). This treats the
agent less like a script and more like a manageable microservice, which is essential for enterprise
governance.
Enabling responsible AI
The principles of responsible AI are fairness, transparency, accountability, and safety. These are not abstract
goals; they are enabled by concrete architectural choices and implemented in organizations through sustained
## governance and oversight of enforcing the incorporation of the following principles and guardrails:

Transparency and explainability: LangGraph's explicit state graph is a form of explainability. The
graph itself documents the decision-making logic, and the final state object contains all the
intermediate data used to reach a conclusion. The final report from our loan agent, which includes the
## rationale, is a direct output of this traceable process:

Demographic parity testing scenario: Incorporating a fairness evaluation step in the CI/CD
pipeline using ADK's testing framework. This runs the agent against a curated "golden dataset"
of user queries from diverse demographics to mathematically measure whether response
quality (e.g., helpfulness, tone) remains consistent across different user groups before a version
promotion.
Reasoning transparency scenario: Utilizing the Trace view in the Google Cloud console
(linked to the ADK deployment). This exposes the agent's internal "thought, action,
◦
◦
Chapter 15 498
observation" loop, allowing developers to see exactly why the agent chose to call the
getUserBalance tool instead of the getLoanStatus tool, rather than just seeing the final answer.
Explicit state graph visualization scenario: Before deploying the loan agent, running the
model against a "golden dataset" of diverse applicant profiles to ensure the approval logic does
not exhibit disparate impact based on protected attributes (e.g., ZIP code or gender), even if
those attributes aren't explicitly used as features.
Safety and robustness: The use of conditional edges in our LangGraph implementation acts as a
programmatic safety pattern by enforcing "fail-fast" logic. Rather than allowing the LLM to continue
reasoning over incomplete or corrupted data, the graph monitors a dedicated error key in the state
object. If an error is detected, such as a missing income field during validation, the conditional edge
immediately reroutes the execution flow to a terminal rejection node. This prevents downstream agents
from attempting to process invalid inputs, which significantly reduces the risk of the model
hallucinating a decision or performing unauthorized API calls based on faulty information.
Safety guardrails and PII protection scenario: Explicitly configuring safety_settings in the
ADK model parameters to block "hate speech" or "harassment" at the BLOCK_LOW_AND_ABOVE
threshold. Additionally, implementing specific input guardrails (such as PII detection) that
intercept and redact sensitive data before it reaches the LLM context window.
Conditional edge guardrails scenario: Hardcoding a stop condition in the graph (a
conditional edge) that immediately halts the process if the income verification API returns a
null or negative value, preventing the LLM from hallucinating a credit decision based on bad
data.
Accountability and governance: A traceable, observable workflow is a prerequisite for accountability.
When an auditor asks why a loan was denied, you can provide the complete trace from LangSmith or
Google Cloud Trace, showing the exact data, tool outputs, and LLM reasoning at each step (especially
with the explicit state in LangGraph). This transforms the agent from a "black box" to a transparent,
## auditable component of your business process:

Immutable audit trail scenario: Enabling data access logs and exporting all agent interaction
logs to BigQuery. This creates an immutable record where every API call made by the agent is
timestamped and associated with a specific service account identity, allowing compliance
teams to query exactly when and who authorized a specific transaction.
Full execution traces (LangSmith/Cloud Trace)scenario: When an auditor challenges a
specific loan denial, retrieving the exact trace ID from LangSmith that logs the specific prompt,
the retrieved credit score, and the LLM's intermediate reasoning step that led to the Denied
output.
Now that we've seen these frameworks in action with the updated code, let's discuss how to choose the right
one for your project.
◦
◦
◦
◦
◦
499 Agent Frameworks - Use Case: A Multi-Agent System for Loan Processing with CrewAI and LangGraph
Recommendations for choosing a framework
There is no single "best" agent framework. The right choice depends on your project's complexity, your team's
familiarity with the concepts, and your production requirements. However, a critical long-term strategy is to
avoid framework lock-in. The agentic landscape is volatile; today's leader may be deprecated tomorrow. We
recommend designing your system around stable interfaces, such as standardized tool definitions (contracts),
explicit state schemas, and pattern-based orchestration logic, rather than tightly coupling every component to a
specific framework's proprietary classes. This abstraction allows you to migrate or swap frameworks with
minimal friction as your needs evolve.
## So, let's see which framework should be considered:

Consider CrewAI when...
You are prototyping rapidly and want to get a multi-agent system running quickly
Your workflow naturally maps to a collaborative team of specialists (e.g., "researcher," "writer,"
"editor")
Your process benefits from a hierarchical (manager/worker) structure where delegation is key
Implicit state passing via context is sufficient for your needs
Consider LangGraph when...
You need complex, non-linear control flow (loops, branches, dynamic routing based on state)
Explicit state management and inspection at each step is critical for logic or debugging
Robust error handling with specific routing based on failures is required
You require high-fidelity debugging and traceability (seeing the full state at every step)
You are building long-running agents that need precise state control
You need to implement HITL patterns easily by adding nodes that wait for input
Consider Google ADK when...
You are building for a production enterprise environment, especially within the Google Cloud
ecosystem
You need a more structured, software engineering-centric approach that treats agents as
modular, testable, and deployable components
Integration with standard enterprise observability (such as OpenTelemetry) and governance
systems is a primary requirement
You need to manage the full life cycle of the agent, from development and evaluation to
deployment and monitoring
You need to inspect the payload going into tools, agents, and models; inspect or take action on
outputs from tools, agents, and models
You need to orchestrate complex multi-agent patterns, such as sequential pipelines, parallel
fan-outs, or iterative loops, by utilizing specialized workflow agents that impose a deterministic
structure over the non-deterministic reasoning of your LLMs
◦
◦
◦
◦
◦
◦
◦
◦
◦
◦
◦
◦
◦
◦
◦
◦
Chapter 15 500
Ultimately, the framework is a tool to implement the patterns we've discussed. By understanding their core
## abstractions, you can select the one that best fits the problem you are trying to solve:

CrewAI's team
LangGraph's state machine
ADK's production service
Let's now map these frameworks to the different levels of agentic maturity we have been discussing throughout
the book.
Frameworks as enablers of agentic maturity
Now that we have explored the practical tools for building agents, we can explicitly map these frameworks to
the GenAI Maturity Model we introduced in Chapter 1. These tools are the enablers that help an organization
progress from basic, data-enhanced generation (Level 2) to truly autonomous and collaborative agentic systems
(Levels 4 and 5).
The following table outlines how to approach each level, with an emphasis on how the frameworks discussed in
## this chapter accelerate development at the higher, agentic levels:

Maturity level Description Framework approach/enabling
tools
Level 1 - Prompting Simple, single-turn promptingTools: Direct LLM API calls (e.g.,
Gemini, OpenAI). Frameworks are
generally not required.
Level 2 - RAG Context-enhanced generation
(RAG)
Tools: LangChain (for RAG
pipelines), or custom code that
calls a vector database and inserts
context into a prompt.
Level 3 - Tuning N/A to the agentic framework
501 Agent Frameworks - Use Case: A Multi-Agent System for Loan Processing with CrewAI and LangGraph
Level 4 - Grounding and
evaluation
CrewAI and LangGraph represent
two different philosophies: CrewAI
focuses on high-level, role-based
orchestration, while LangGraph
provides a low-level, state-driven
framework. Their approaches to
evaluation and grounding reflect
this divide.
CrewAI: Integrated and
enterprise-focused
CrewAI has specialized features to
make grounding and evaluation
more "turnkey" for developers
who want to prevent
hallucinations without building
custom logic.
Grounding and
guardrails:
Hallucination guardrail
(Enterprise): Native
feature that assigns a
faithfulness score (0-10)
and triggers selfcorrection if below
threshold.
Built-in RAG and
knowledge: Native
knowledge component for
PDFs/CSVs allows agents
to be grounded in local
data by default.
Native utility tools: Tools
like TimeAwarenessTool
ground agents in realworld facts (e.g., current
date) to prevent temporal
hallucinations.
Evaluation:
CrewAI Test CLI: Runs a
crew for $N$ iterations to
generate performance
score tables.
Patronus AI and training
loop: First-class support
for automated evaluation
and a crew.train()
method for humanfeedback-based finetuning.
LangGraph:
Architectural and
developer-driven
LangGraph treats grounding and
evaluation as customizable
structural components, offering
fine-grained control over the
"reasoning path."
Grounding and
guardrails:
Self-correction loops:
Uses conditional edges to
detect poor outputs and
route the state back to a
"Refinement" node,
creating a programmatic
grounding loop.
State checkpoints: Native
persistence allows the
system to be grounded in
a "version-controlled"
history of the
conversation, enabling
rollbacks to known good
states.
HITL (Human-in-theLoop): Explicit
"interrupts" that pause
execution for human
verification before highstakes tool calls.
Evaluation:
LangSmith
integration:
Deep trace-level
◦
Agent Frameworks - Use Case: A Multi-Agent System for Loan Processing with CrewAI and LangGraph
Maturity level Description Framework approach/enabling
tools
evaluation
where every
node transition
is measured for
latency, cost,
and accuracy
using "LLM-asa-judge"
patterns.
Unit-testable
nodes: Since
nodes are
isolated Python
functions,
developers can
perform
deterministic
unit testing on
specific logic
gates before full
system
integration.
Level 5 - Single-agent systemsAn autonomous agent with a
planner, tools, and memory
executes a multi-step task
LangGraph: A graph with
one or more agent nodes
that can call multiple
tools based on an explicit
state, potentially looping
(reflecting).
ADK: The primary use
case. Define a single
Agent class with its tools
and run it within the
agent runtime.
CrewAI: Can be used with
a "crew" of one, but this is
less common.
◦
Chapter 15 504
Maturity level Description Framework approach/enabling
tools
Level 6 - Multi-agent systemsMultiple agents collaborate,
negotiate, and delegate tasks to
solve a complex problem
LangGraph: Ideal for
complex interactions.
Each agent/function is a
node. Edges define
communication, handoffs,
and control flow. Explicit
state facilitates shared
understanding.
CrewAI: Primary design
philosophy. Define a crew
with distinct roles and a
process (sequential/
hierarchical) for
collaboration.
ADK: A system of
multiple, independently
deployed ADK agent
services communicating
via messaging or A2A
protocols.
Table 15.3 - Approaching frameworks according to the organization's maturity level
As this table illustrates, frameworks are the bridge from "agent-ready" models (Level 3) to functional agentic
systems (Levels 4 and 5). They provide the essential how for constructing the sophisticated pplications we've
designed.
Let's wrap up this chapter in the next section.
505 Agent Frameworks - Use Case: A Multi-Agent System for Loan Processing with CrewAI and LangGraph
## Summary

In this chapter, we explored three prominent agent frameworks-Google's ADK, CrewAI, and LangGraph-and
saw how each provides a different but powerful abstraction for building complex agentic systems using Google
Gemini as our LLM.
Our practical implementations of the loan processing agent, updated based on the revised notebook, showed
CrewAI's strength in modeling collaborative teams via a hierarchical process, while LangGraph demonstrated
fine-grained control, explicit state management, and robust error handling through its state machine approach.
We also positioned Google's ADK as an enterprise-grade toolkit focused on the full life cycle of building, testing,
and deploying robust, manageable agent services.
We connected the use of these frameworks to the GenAI Maturity Model, identifying them as key enablers for
reaching Level 5 (single-agent systems) and Level 6 (multi-agent systems). Finally, we emphasized that these
advanced systems demand a mature approach to observability and governance, using tools such as LangSmith
and OpenTelemetry to ensure traceability, a core component of responsible AI.
## The key takeaways from this chapter are as follows:

Frameworks are accelerators: You do not need to build agentic planners, state managers, and tool
dispatchers from scratch. Frameworks such as CrewAI, LangGraph, and ADK provide the essential
abstractions to build Level 4 and Level 5 systems effectively.
Choose the right abstraction: The framework you choose should match your problem. Use CrewAI's
team metaphor for role-based, collaborative tasks, especially with delegation. Use LangGraph's state
machine for complex, cyclical processes requiring explicit state and fine-grained control over flow and
errors. Use ADK's production agent model for enterprise-grade, testable, and manageable services.
Control flow and error handling are key differentiators: Moving beyond simple sequences is critical
for robustness. LangGraph's explicit graph structure provides a powerful way to manage complex
branching, loops, and error handling (as shown in our validation example), which is essential for
reliable applications. CrewAI's hierarchical process offers a simpler delegation model.
Observability is non-negotiable: Agentic systems are complex. The ability to trace why an agent made
a decision, facilitated by tools such as LangSmith (especially with LangGraph's explicit state), is not just
a debugging feature but a foundational requirement for governance, safety, and responsible AI.
We have now journeyed from the foundational concepts of GenAI to the architectural patterns and practical
frameworks used to build sophisticated, autonomous agentic systems. In the final chapter, we will bring
together these concepts and provide a clear action plan for you to apply these patterns, navigate the maturity
model, and lead your organization's transformation.
Chapter 15 506
then follow the steps on the page.
Note: Keep your invoice handy. Purchases made directly from Packt don't require one.
507 Agent Frameworks - Use Case: A Multi-Agent System for Loan Processing with CrewAI and LangGraph