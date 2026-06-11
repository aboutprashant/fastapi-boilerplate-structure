For the entire repo, LangChain/LangGraph would only serve one purpose:
orchestrating multi-step AI workflows across services.
In the scaffold, that means:

```
assistant-gateway
  uses LangGraph to decide the flow:
    classify intent
    maybe call knowledge-base
    maybe call data-analytics
    maybe call report-generator later
    synthesize final answer
```

So LangChain is not the database layer, not the API framework, not the RAG store, and not required for FastAPI. It is just an optional orchestration/agent framework.
In this repo, its intended role was:

```
User asks one broad question
        |
        v
LangGraph decides the path
        |
        +--> knowledge-base
        +--> data-analytics
        +--> report-generator
        |
        v
Final answer
```



Example where it helps:

> “Compare my donor commitments against progress reports and tell me which indicators are behind.”



That could require:

1. Identify this as multi-document reasoning.
2. Search donor agreements in `knowledge-base`.
3. Search progress reports in `knowledge-base`.
4. Maybe call `data-analytics` for indicator numbers.
5. Combine the answer with citations.

That orchestration is what LangGraph is for.



But if our app already has explicit workflows, then LangChain/LangGraph does not add much:

```
User clicks Search Documents -> call knowledge-base
User clicks Generate Report -> call report-generator
User asks Analytics question -> call data-analytics
```



In that setup, LangChain is unnecessary for our product. Each service can expose normal FastAPI endpoints and implement its own AI logic internally.