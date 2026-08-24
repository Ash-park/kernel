## `kernel/core/models.py`

Defines the core domain data shapes shared by every other module: `Role`, `Message`,
`ToolCall`, `ToolResult`, `EventType`, and `Event`. Pure data — no logic, no I/O, no
dependency on any other `kernel` module.

```mermaid
classDiagram
    class Message {
        +role: Role
        +content: str
        +tool_call: ToolCall
        +tool_result: ToolResult
    }
    class Event {
        +type: EventType
        +correlation_id: str
        +payload: dict
        +timestamp: datetime
    }
    Message --> ToolCall
    Message --> ToolResult
    Event --> EventType

    class ConversationState
    class ContextManager
    class ToolExecutor
    class AgentRuntime
    class LLMClient
    class EventBus
    class Tool

    ConversationState ..> Message : uses
    ContextManager ..> Message : uses
    ToolExecutor ..> Event : publishes
    ToolExecutor ..> ToolCall : consumes
    ToolExecutor ..> ToolResult : produces
    AgentRuntime ..> Message : uses
    AgentRuntime ..> Event : publishes
    LLMClient ..> Message : returns
    EventBus ..> Event : carries
    Tool ..> ToolResult : returns
```

Everything else in `core/`, `interfaces/`, and `adapters/` imports these types — this file
has no outgoing dependencies within the project.
