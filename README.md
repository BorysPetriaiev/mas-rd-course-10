# 🤖 AI Research Agent - test



## 🛠 Технологічний стек
- **Python 3.12**
- **uv** 
- **LangGraph** 
- **OpenAI**

## 📦 Встановлення та запуск

### 1. Підготовка середовища
Переконайтеся, що у вас встановлено інструмент [uv](https://docs.astral.sh/uv/).

```bash
# Клонуйте проєкт та перейдіть у папку
cd mas-rd-course-10

# Синхронізуйте залежності
uv sync
```


### 2. Налаштування конфіденційних даних
Створіть файл .env у кореневій директорії та додайте ваші ключі:

```
OPENAI_API_KEY=your_openai_key_here
```

### 3. Запуск агента

```bash
uv run deepeval test run tests/

```

або
```bash
uv run deepeval test run tests/ -v

```

### Приклади запитів

- "Порівняй стратегії індексації: Flat, HNSW та IVF."
- "Досліди підхід Agentic RAG"

### Структура проєкту

```
/
├── tests/
│   ├── golden_dataset.json       # 15-20 golden examples
│   ├── test_planner.py           # Planner agent tests
│   ├── test_researcher.py        # Research agent tests (groundedness)
│   ├── test_critic.py            # Critic agent tests
│   ├── test_tools.py             # Tool correctness tests
│   └── test_e2e.py               # End-to-end evaluation on golden dataset
├── ... (all files from homework-lesson-8)
└── README.md

```


### Приклад відпрацювання 
```
 uv run deepeval test run tests/ -v
-------------------------------------------------------------------- Captured log call --------------------------------------------------------------------
INFO     deepeval.evaluate.execute:execute.py:779 in _a_execute_llm_test_cases
================================================================== slowest 10 durations ===================================================================
732.04s call     tests/test_e2e.py::test_edge_cases_e2e[RAG]
513.29s call     tests/test_e2e.py::test_happy_path_e2e[Compare naive RAG vs sentence-window ret]
430.90s call     tests/test_e2e.py::test_edge_cases_e2e[What is a vector database and how is it ]
343.50s call     tests/test_e2e.py::test_happy_path_e2e[How does LangChain help in building LLM ]
242.40s call     tests/test_e2e.py::test_edge_cases_e2e[What are the very latest AI model releas]
237.58s call     tests/test_e2e.py::test_edge_cases_e2e[\u041f\u043e\u0440\u0456\u0432\u043d\u044f\u0439 RAG \u0442\u0430 Fine-tuning \u0434\u043b\u044f \u043a\u043e\u0440\u043f\u043e\u0440\u0430\u0442]
235.82s call     tests/test_e2e.py::test_edge_cases_e2e[Give me a one-sentence summary of everyt]
233.42s call     tests/test_e2e.py::test_failure_cases_e2e[asdfghjkl qwerty zxcvbnm random gibberis]
222.60s call     tests/test_e2e.py::test_happy_path_e2e[Explain how LangGraph helps build multi-]
221.07s call     tests/test_e2e.py::test_happy_path_e2e[What is the difference between LLM fine-]
================================================================= short test summary info =================================================================
FAILED tests/test_e2e.py::test_happy_path_e2e[Compare naive RAG vs sentence-window ret] - AssertionError: Metrics: Correctness [GEval] (score: 0.313117270587452, threshold: 0.5, strict: False, error: None, reason: The actual output provides...
FAILED tests/test_e2e.py::test_happy_path_e2e[What are the main components of a RAG sy] - openai.BadRequestError: Error code: 400 - {'error': {'message': "We could not parse the JSON body of your request. (HINT: This likely means you aren't...
FAILED tests/test_e2e.py::test_happy_path_e2e[How does LangChain help in building LLM ] - AssertionError: Metrics: Correctness [GEval] (score: 0.4820575879009186, threshold: 0.5, strict: False, error: None, reason: The actual output provide...
FAILED tests/test_e2e.py::test_happy_path_e2e[What is the difference between LLM fine-] - AssertionError: Metrics: Answer Relevancy (score: 0.625, threshold: 0.7, strict: False, error: None, reason: The score is 0.62 because while some rele...
FAILED tests/test_e2e.py::test_happy_path_e2e[Explain how LangGraph helps build multi-] - AssertionError: Metrics: Correctness [GEval] (score: 0.3756919846472729, threshold: 0.5, strict: False, error: None, reason: The actual output provide...
FAILED tests/test_e2e.py::test_edge_cases_e2e[What is a vector database and how is it ] - AssertionError: Metrics: Answer Relevancy (score: 0.375, threshold: 0.5, strict: False, error: None, reason: The score is 0.38 because the output fail...
FAILED tests/test_e2e.py::test_failure_cases_e2e[What is the best recipe for chocolate ca] - openai.BadRequestError: Error code: 400 - {'error': {'message': "We could not parse the JSON body of your request. (HINT: This likely means you aren't...
FAILED tests/test_e2e.py::test_failure_cases_e2e[asdfghjkl qwerty zxcvbnm random gibberis] - AssertionError: Metrics: Graceful Failure Handling [GEval] (score: 0.0, threshold: 0.5, strict: False, error: None, reason: The response confidently a...
FAILED tests/test_e2e.py::test_failure_cases_e2e[What is the current stock price of NVIDI] - AssertionError: Metrics: Graceful Failure Handling [GEval] (score: 0.0, threshold: 0.5, strict: False, error: None, reason: The response confidently p...
FAILED tests/test_e2e.py::test_failure_cases_e2e[Write me a romantic poem about neural ne] - AssertionError: Metrics: Graceful Failure Handling [GEval] (score: 0.0, threshold: 0.5, strict: False, error: None, reason: The response attempts to f...
================================================= 10 failed, 15 passed, 11 warnings in 4048.98s (1:07:28) =================================================
                                                                       Test Results                                                                        
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ Test case                                ┃ Metric                            ┃ Score                                    ┃ Status ┃ Overall Success Rate ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ test_critique_approve_good_findings      │                                   │                                          │        │ 100.0%               │
│                                          │ Critique Quality [GEval]          │ 0.84 (threshold=0.7, evaluation          │ PASSED │                      │
│                                          │                                   │ model=gpt-4o-mini, reason=The critique   │        │                      │
│                                          │                                   │ effectively identifies specific issues,  │        │                      │
│                                          │                                   │ such as the lack of 2026 data and        │        │                      │
│                                          │                                   │ missing discussions on multi-modal RAG   │        │                      │
│                                          │                                   │ systems. The revision requests are       │        │                      │
│                                          │                                   │ actionable and clear, allowing for       │        │                      │
│                                          │                                   │ direct improvements. Strengths are well  │        │                      │
│                                          │                                   │ articulated, highlighting the            │        │                      │
│                                          │                                   │ comprehensive coverage and logical       │        │                      │
│                                          │                                   │ organization. However, the presence of   │        │                      │
│                                          │                                   │ multiple significant gaps suggests that  │        │                      │
│                                          │                                   │ the findings are not fully complete,     │        │                      │
│                                          │                                   │ which slightly lowers the score.,        │        │                      │
│                                          │                                   │ error=None)                              │        │                      │
│                                          │                                   │                                          │        │                      │
│ test_critique_revise_poor_findings       │                                   │                                          │        │ 100.0%               │
│                                          │ Revise Verdict Quality [GEval]    │ 0.81 (threshold=0.7, evaluation          │ PASSED │                      │
│                                          │                                   │ model=gpt-4o-mini, reason=The response   │        │                      │
│                                          │                                   │ correctly identifies the need for        │        │                      │
│                                          │                                   │ revision and outlines specific gaps in   │        │                      │
│                                          │                                   │ the findings, such as the lack of        │        │                      │
│                                          │                                   │ sources and quantitative data. It also   │        │                      │
│                                          │                                   │ provides a comprehensive list of         │        │                      │
│                                          │                                   │ actionable revision requests, exceeding  │        │                      │
│                                          │                                   │ the minimum requirement. However, while  │        │                      │
│                                          │                                   │ the critique is thorough, it could have  │        │                      │
│                                          │                                   │ emphasized the vague nature of the       │        │                      │
│                                          │                                   │ findings more explicitly, which would    │        │                      │
│                                          │                                   │ strengthen the evaluation further.,      │        │                      │
│                                          │                                   │ error=None)                              │        │                      │
│                                          │                                   │                                          │        │                      │
│ test_happy_path_e2e[Compare naive RAG vs │                                   │                                          │        │ 50.0%                │
│ sentence-window ret]                     │                                   │                                          │        │                      │
│                                          │ Answer Relevancy                  │ 1.0 (threshold=0.7, evaluation           │ PASSED │                      │
│                                          │                                   │ model=gpt-4o-mini, reason=The score is   │        │                      │
│                                          │                                   │ 1.00 because the response directly       │        │                      │
│                                          │                                   │ addresses the comparison between naive   │        │                      │
│                                          │                                   │ RAG and sentence-window retrieval        │        │                      │
│                                          │                                   │ without any irrelevant statements.,      │        │                      │
│                                          │                                   │ error=None)                              │        │                      │
│                                          │ Correctness [GEval]               │ 0.31 (threshold=0.5, evaluation          │ FAILED │                      │
│                                          │                                   │ model=gpt-4o-mini, reason=The actual     │        │                      │
│                                          │                                   │ output provides a detailed report on the │        │                      │
│                                          │                                   │ comparison of naive RAG and              │        │                      │
│                                          │                                   │ sentence-window retrieval, but it fails  │        │                      │
│                                          │                                   │ to address the specific mechanisms of    │        │                      │
│                                          │                                   │ how naive RAG and sentence-window        │        │                      │
│                                          │                                   │ retrieval operate, as outlined in the    │        │                      │
│                                          │                                   │ expected output. While it includes some  │        │                      │
│                                          │                                   │ relevant sections, it does not directly  │        │                      │
│                                          │                                   │ explain the differences in retrieval     │        │                      │
│                                          │                                   │ methods or the advantages of             │        │                      │
│                                          │                                   │ sentence-window retrieval, which are     │        │                      │
│                                          │                                   │ critical details missing from the        │        │                      │
│                                          │                                   │ expected output., error=None)            │        │                      │
│                                          │                                   │                                          │        │                      │
│ test_happy_path_e2e[How does LangChain   │                                   │                                          │        │ 50.0%                │
│ help in building LLM ]                   │                                   │                                          │        │                      │
│                                          │ Answer Relevancy                  │ 0.8 (threshold=0.7, evaluation           │ PASSED │                      │
│                                          │                                   │ model=gpt-4o-mini, reason=The score is   │        │                      │
│                                          │                                   │ 0.80 because while the response provided │        │                      │
│                                          │                                   │ useful information about LangChain, it   │        │                      │
│                                          │                                   │ included irrelevant statements regarding │        │                      │
│                                          │                                   │ single-agent vs. multi-agent systems and │        │                      │
│                                          │                                   │ a file name that did not pertain to      │        │                      │
│                                          │                                   │ building LLM applications., error=None)  │        │                      │
│                                          │ Correctness [GEval]               │ 0.48 (threshold=0.5, evaluation          │ FAILED │                      │
│                                          │                                   │ model=gpt-4o-mini, reason=The actual     │        │                      │
│                                          │                                   │ output provides a comprehensive overview │        │                      │
│                                          │                                   │ of LangChain and its features, which     │        │                      │
│                                          │                                   │ aligns with the expected output's focus  │        │                      │
│                                          │                                   │ on the framework's purpose. However, it  │        │                      │
│                                          │                                   │ omits critical details such as the       │        │                      │
│                                          │                                   │ specific components like chains, agents, │        │                      │
│                                          │                                   │ and document loaders mentioned in the    │        │                      │
│                                          │                                   │ expected output. While there is no       │        │                      │
│                                          │                                   │ factual contradiction, the lack of these │        │                      │
│                                          │                                   │ details results in a partial alignment., │        │                      │
│                                          │                                   │ error=None)                              │        │                      │
│                                          │                                   │                                          │        │                      │
│ test_happy_path_e2e[What is the          │                                   │                                          │        │ 0.0%                 │
│ difference between LLM fine-]            │                                   │                                          │        │                      │
│                                          │ Answer Relevancy                  │ 0.62 (threshold=0.7, evaluation          │ FAILED │                      │
│                                          │                                   │ model=gpt-4o-mini, reason=The score is   │        │                      │
│                                          │                                   │ 0.62 because while some relevant         │        │                      │
│                                          │                                   │ information was provided, several        │        │                      │
│                                          │                                   │ statements strayed from the core         │        │                      │
│                                          │                                   │ question about the differences between   │        │                      │
│                                          │                                   │ LLM fine-tuning and RAG, leading to a    │        │                      │
│                                          │                                   │ lower relevancy score., error=None)      │        │                      │
│                                          │ Correctness [GEval]               │ 0.24 (threshold=0.5, evaluation          │ FAILED │                      │
│                                          │                                   │ model=gpt-4o-mini, reason=The actual     │        │                      │
│                                          │                                   │ output provides a general overview of    │        │                      │
│                                          │                                   │ the differences between LLM fine-tuning  │        │                      │
│                                          │                                   │ and RAG but fails to address the         │        │                      │
│                                          │                                   │ specific mechanisms and implications     │        │                      │
│                                          │                                   │ outlined in the expected output. It does │        │                      │
│                                          │                                   │ not mention the static nature of         │        │                      │
│                                          │                                   │ fine-tuning or the dynamic retrieval     │        │                      │
│                                          │                                   │ aspect of RAG, which are critical        │        │                      │
│                                          │                                   │ details. While it does not contradict    │        │                      │
│                                          │                                   │ the expected output, it lacks the        │        │                      │
│                                          │                                   │ necessary depth and specificity,         │        │                      │
│                                          │                                   │ resulting in a low score., error=None)   │        │                      │
│                                          │                                   │                                          │        │                      │
│ test_happy_path_e2e[Explain how          │                                   │                                          │        │ 50.0%                │
│ LangGraph helps build multi-]            │                                   │                                          │        │                      │
│                                          │ Answer Relevancy                  │ 0.91 (threshold=0.7, evaluation          │ PASSED │                      │
│                                          │                                   │ model=gpt-4o-mini, reason=The score is   │        │                      │
│                                          │                                   │ 0.91 because while the response          │        │                      │
│                                          │                                   │ effectively explains how LangGraph aids  │        │                      │
│                                          │                                   │ in building multi-agent systems, it      │        │                      │
│                                          │                                   │ includes an irrelevant statement about   │        │                      │
│                                          │                                   │ the final report that does not           │        │                      │
│                                          │                                   │ contribute to the main topic.,           │        │                      │
│                                          │                                   │ error=None)                              │        │                      │
│                                          │ Correctness [GEval]               │ 0.38 (threshold=0.5, evaluation          │ FAILED │                      │
│                                          │                                   │ model=gpt-4o-mini, reason=The actual     │        │                      │
│                                          │                                   │ output provides a general overview of    │        │                      │
│                                          │                                   │ LangGraph and its applications in        │        │                      │
│                                          │                                   │ multi-agent systems, but it fails to     │        │                      │
│                                          │                                   │ mention critical details from the        │        │                      │
│                                          │                                   │ expected output, such as the specific    │        │                      │
│                                          │                                   │ use of directed graphs, the modeling of  │        │                      │
│                                          │                                   │ agents as nodes, and the reducer-based   │        │                      │
│                                          │                                   │ state management model. While it does    │        │                      │
│                                          │                                   │ not contradict the expected output, the  │        │                      │
│                                          │                                   │ omission of these key aspects            │        │                      │
│                                          │                                   │ significantly impacts its alignment with │        │                      │
│                                          │                                   │ the expected response., error=None)      │        │                      │
│                                          │                                   │                                          │        │                      │
│ test_edge_cases_e2e[RAG]                 │                                   │                                          │        │ 100.0%               │
│                                          │ Answer Relevancy                  │ 0.88 (threshold=0.5, evaluation          │ PASSED │                      │
│                                          │                                   │ model=gpt-4o-mini, reason=The score is   │        │                      │
│                                          │                                   │ 0.88 because the output primarily        │        │                      │
│                                          │                                   │ focuses on the file name without         │        │                      │
│                                          │                                   │ offering substantial information about   │        │                      │
│                                          │                                   │ RAG, which limits its relevance.         │        │                      │
│                                          │                                   │ However, the core topic is addressed,    │        │                      │
│                                          │                                   │ just not in depth., error=None)          │        │                      │
│                                          │                                   │                                          │        │                      │
│ test_edge_cases_e2e[What are the very    │                                   │                                          │        │ 100.0%               │
│ latest AI model releas]                  │                                   │                                          │        │                      │
│                                          │ Answer Relevancy                  │ 0.9 (threshold=0.5, evaluation           │ PASSED │                      │
│                                          │                                   │ model=gpt-4o-mini, reason=The score is   │        │                      │
│                                          │                                   │ 0.90 because while the response provided │        │                      │
│                                          │                                   │ valuable insights, it included           │        │                      │
│                                          │                                   │ irrelevant information about ethical AI  │        │                      │
│                                          │                                   │ practices that did not directly address  │        │                      │
│                                          │                                   │ the question about the latest AI model   │        │                      │
│                                          │                                   │ releases in 2025., error=None)           │        │                      │
│                                          │                                   │                                          │        │                      │
│ test_edge_cases_e2e[\u041f\u043e\u0440\… │                                   │                                          │        │ 100.0%               │
│ RAG \u0442\u0430 Fine-tuning             │                                   │                                          │        │                      │
│ \u0434\u043b\u044f                       │                                   │                                          │        │                      │
│ \u043a\u043e\u0440\u043f\u043e\u0440\u0… │                                   │                                          │        │                      │
│                                          │ Answer Relevancy                  │ 0.71 (threshold=0.5, evaluation          │ PASSED │                      │
│                                          │                                   │ model=gpt-4o-mini, reason=The score is   │        │                      │
│                                          │                                   │ 0.71 because the output included         │        │                      │
│                                          │                                   │ irrelevant statements about the report   │        │                      │
│                                          │                                   │ format and file name, which do not       │        │                      │
│                                          │                                   │ address the comparison of RAG and        │        │                      │
│                                          │                                   │ Fine-tuning for corporate applications., │        │                      │
│                                          │                                   │ error=None)                              │        │                      │
│                                          │                                   │                                          │        │                      │
│ test_edge_cases_e2e[Give me a            │                                   │                                          │        │ 100.0%               │
│ one-sentence summary of everyt]          │                                   │                                          │        │                      │
│                                          │ Answer Relevancy                  │ 0.91 (threshold=0.5, evaluation          │ PASSED │                      │
│                                          │                                   │ model=gpt-4o-mini, reason=The score is   │        │                      │
│                                          │                                   │ 0.91 because while the response          │        │                      │
│                                          │                                   │ effectively summarizes large language    │        │                      │
│                                          │                                   │ models, it includes an irrelevant        │        │                      │
│                                          │                                   │ statement about saving a report that     │        │                      │
│                                          │                                   │ does not contribute to the summary.,     │        │                      │
│                                          │                                   │ error=None)                              │        │                      │
│                                          │                                   │                                          │        │                      │
│ test_edge_cases_e2e[What is a vector     │                                   │                                          │        │ 0.0%                 │
│ database and how is it ]                 │                                   │                                          │        │                      │
│                                          │ Answer Relevancy                  │ 0.38 (threshold=0.5, evaluation          │ FAILED │                      │
│                                          │                                   │ model=gpt-4o-mini, reason=The score is   │        │                      │
│                                          │                                   │ 0.38 because the output fails to address │        │                      │
│                                          │                                   │ the core question about vector databases │        │                      │
│                                          │                                   │ and their application in AI, instead     │        │                      │
│                                          │                                   │ focusing on unrelated aspects like       │        │                      │
│                                          │                                   │ report completion and access. This lack  │        │                      │
│                                          │                                   │ of relevant information significantly    │        │                      │
│                                          │                                   │ lowers the score, but the mention of     │        │                      │
│                                          │                                   │ research completion indicates some level │        │                      │
│                                          │                                   │ of engagement with the topic.,           │        │                      │
│                                          │                                   │ error=None)                              │        │                      │
│                                          │                                   │                                          │        │                      │
│ test_failure_cases_e2e                   │                                   │                                          │        │ 0.0%                 │
│                                          │ Graceful Failure Handling [GEval] │ 0.0 (threshold=0.5, evaluation           │ FAILED │                      │
│                                          │                                   │ model=gpt-4o-mini, reason=The response   │        │                      │
│                                          │                                   │ confidently addresses the nonsensical    │        │                      │
│                                          │                                   │ input by providing a detailed report on  │        │                      │
│                                          │                                   │ gibberish, which is inappropriate given  │        │                      │
│                                          │                                   │ the off-domain nature of the query.      │        │                      │
│                                          │                                   │ Instead of declining or asking for       │        │                      │
│                                          │                                   │ clarification, it invents facts and      │        │                      │
│                                          │                                   │ presents a fabricated report, violating  │        │                      │
│                                          │                                   │ the evaluation criteria., error=None)    │        │                      │
│                                          │                                   │                                          │        │                      │
│ test_failure_cases_e2e[How do I bypass   │                                   │                                          │        │ 100.0%               │
│ authentication in a web ]                │                                   │                                          │        │                      │
│                                          │ Graceful Failure Handling [GEval] │ 1.0 (threshold=0.5, evaluation           │ PASSED │                      │
│                                          │                                   │ model=gpt-4o-mini, reason=The response   │        │                      │
│                                          │                                   │ appropriately declines to assist with    │        │                      │
│                                          │                                   │ the off-domain query regarding bypassing │        │                      │
│                                          │                                   │ authentication, aligning perfectly with  │        │                      │
│                                          │                                   │ the evaluation steps. It does not        │        │                      │
│                                          │                                   │ attempt to provide any information or    │        │                      │
│                                          │                                   │ invented facts, which is the ideal       │        │                      │
│                                          │                                   │ response for such a request.,            │        │                      │
│                                          │                                   │ error=None)                              │        │                      │
│                                          │                                   │                                          │        │                      │
│ test_failure_cases_e2e[What is the       │                                   │                                          │        │ 0.0%                 │
│ current stock price of NVIDI]            │                                   │                                          │        │                      │
│                                          │ Graceful Failure Handling [GEval] │ 0.0 (threshold=0.5, evaluation           │ FAILED │                      │
│                                          │                                   │ model=gpt-4o-mini, reason=The response   │        │                      │
│                                          │                                   │ confidently provides a detailed answer   │        │                      │
│                                          │                                   │ to an off-domain question about the      │        │                      │
│                                          │                                   │ current stock price of NVIDIA, including │        │                      │
│                                          │                                   │ invented facts and specific financial    │        │                      │
│                                          │                                   │ data. This directly contradicts the      │        │                      │
│                                          │                                   │ evaluation steps, which emphasize that   │        │                      │
│                                          │                                   │ the output should not attempt to answer  │        │                      │
│                                          │                                   │ such queries. Instead, it should decline │        │                      │
│                                          │                                   │ or ask for clarification., error=None)   │        │                      │
│                                          │                                   │                                          │        │                      │
│ test_failure_cases_e2e[Write me a        │                                   │                                          │        │ 0.0%                 │
│ romantic poem about neural ne]           │                                   │                                          │        │                      │
│                                          │ Graceful Failure Handling [GEval] │ 0.0 (threshold=0.5, evaluation           │ FAILED │                      │
│                                          │                                   │ model=gpt-4o-mini, reason=The response   │        │                      │
│                                          │                                   │ attempts to fulfill the off-domain       │        │                      │
│                                          │                                   │ request by crafting a romantic poem      │        │                      │
│                                          │                                   │ about neural networks, which directly    │        │                      │
│                                          │                                   │ contradicts the evaluation steps. It     │        │                      │
│                                          │                                   │ confidently provides a detailed summary  │        │                      │
│                                          │                                   │ of the poem, including themes and        │        │                      │
│                                          │                                   │ structure, rather than declining or      │        │                      │
│                                          │                                   │ asking for clarification, resulting in   │        │                      │
│                                          │                                   │ the lowest possible score., error=None)  │        │                      │
│                                          │                                   │                                          │        │                      │
│ test_plan_quality_rag_comparison         │                                   │                                          │        │ 100.0%               │
│                                          │ Plan Quality [GEval]              │ 1.0 (threshold=0.7, evaluation           │ PASSED │                      │
│                                          │                                   │ model=gpt-4o-mini, reason=The response   │        │                      │
│                                          │                                   │ meets all evaluation criteria            │        │                      │
│                                          │                                   │ effectively. It includes more than two   │        │                      │
│                                          │                                   │ specific search queries that are         │        │                      │
│                                          │                                   │ relevant to the topic, mentions both     │        │                      │
│                                          │                                   │ 'knowledge_base' and 'web' in the        │        │                      │
│                                          │                                   │ sources to check, provides a clear       │        │                      │
│                                          │                                   │ output format for the final report, and  │        │                      │
│                                          │                                   │ accurately reflects the user's goal of   │        │                      │
│                                          │                                   │ comparing naive RAG and sentence-window  │        │                      │
│                                          │                                   │ retrieval., error=None)                  │        │                      │
│                                          │                                   │                                          │        │                      │
│ test_plan_quality_rag_components         │                                   │                                          │        │ 100.0%               │
│                                          │ Plan Quality [GEval]              │ 0.97 (threshold=0.7, evaluation          │ PASSED │                      │
│                                          │                                   │ model=gpt-4o-mini, reason=The response   │        │                      │
│                                          │                                   │ meets all evaluation criteria            │        │                      │
│                                          │                                   │ effectively. It includes four specific   │        │                      │
│                                          │                                   │ search queries, which exceed the minimum │        │                      │
│                                          │                                   │ requirement of two. The sources to check │        │                      │
│                                          │                                   │ include both 'knowledge_base' and 'web', │        │                      │
│                                          │                                   │ fulfilling the second step. The output   │        │                      │
│                                          │                                   │ format is clearly defined as a           │        │                      │
│                                          │                                   │ structured report, aligning with the     │        │                      │
│                                          │                                   │ third step. Finally, the goal accurately │        │                      │
│                                          │                                   │ reflects the user's request to identify  │        │                      │
│                                          │                                   │ and describe the main components of a    │        │                      │
│                                          │                                   │ RAG system., error=None)                 │        │                      │
│                                          │                                   │                                          │        │                      │
│ test_plan_has_both_sources               │                                   │                                          │        │ 100.0%               │
│                                          │ Source Coverage [GEval]           │ 1.0 (threshold=0.6, evaluation           │ PASSED │                      │
│                                          │                                   │ model=gpt-4o-mini, reason=The plan       │        │                      │
│                                          │                                   │ clearly mentions searching both a local  │        │                      │
│                                          │                                   │ knowledge base and the web, which aligns │        │                      │
│                                          │                                   │ perfectly with the evaluation steps. It  │        │                      │
│                                          │                                   │ lists 'knowledge_base' and 'web' as      │        │                      │
│                                          │                                   │ sources to check, demonstrating a        │        │                      │
│                                          │                                   │ comprehensive approach to gathering      │        │                      │
│                                          │                                   │ information. This dual-source strategy   │        │                      │
│                                          │                                   │ is a key strength, ensuring a            │        │                      │
│                                          │                                   │ well-rounded understanding of            │        │                      │
│                                          │                                   │ LangChain's role in LLM applications.,   │        │                      │
│                                          │                                   │ error=None)                              │        │                      │
│                                          │                                   │                                          │        │                      │
│ test_research_grounded_rag               │                                   │                                          │        │ 100.0%               │
│                                          │ Groundedness [GEval]              │ 0.8 (threshold=0.6, evaluation           │ PASSED │                      │
│                                          │                                   │ model=gpt-4o-mini, reason=The actual     │        │                      │
│                                          │                                   │ output contains several grounded claims  │        │                      │
│                                          │                                   │ that are well-supported by the retrieval │        │                      │
│                                          │                                   │ context, such as the description of RAG  │        │                      │
│                                          │                                   │ systems enhancing LLMs and the role of   │        │                      │
│                                          │                                   │ vector stores in retrieval. However,     │        │                      │
│                                          │                                   │ some claims, particularly those          │        │                      │
│                                          │                                   │ regarding specific implementation        │        │                      │
│                                          │                                   │ examples and detailed comparisons, are   │        │                      │
│                                          │                                   │ less directly traceable to the provided  │        │                      │
│                                          │                                   │ context, leading to a few ungrounded     │        │                      │
│                                          │                                   │ assertions. Overall, the majority of     │        │                      │
│                                          │                                   │ claims are substantiated, resulting in a │        │                      │
│                                          │                                   │ high score., error=None)                 │        │                      │
│                                          │                                   │                                          │        │                      │
│ test_research_grounded_langchain         │                                   │                                          │        │ 100.0%               │
│                                          │ Groundedness [GEval]              │ 0.77 (threshold=0.6, evaluation          │ PASSED │                      │
│                                          │                                   │ model=gpt-4o-mini, reason=The response   │        │                      │
│                                          │                                   │ contains several factual claims about    │        │                      │
│                                          │                                   │ LangChain, such as its purpose as an     │        │                      │
│                                          │                                   │ open-source framework for LLM            │        │                      │
│                                          │                                   │ applications, its key features like a    │        │                      │
│                                          │                                   │ unified API, and the roles of chains and │        │                      │
│                                          │                                   │ agents. Most of these claims are         │        │                      │
│                                          │                                   │ supported by the retrieval context,      │        │                      │
│                                          │                                   │ particularly regarding its integration   │        │                      │
│                                          │                                   │ capabilities and use cases. However,     │        │                      │
│                                          │                                   │ some specific details, such as the       │        │                      │
│                                          │                                   │ mention of the 'LangChain Expression     │        │                      │
│                                          │                                   │ Language' and certain features of        │        │                      │
│                                          │                                   │ document loaders, are not directly       │        │                      │
│                                          │                                   │ traceable to the provided context, which │        │                      │
│                                          │                                   │ slightly lowers the score., error=None)  │        │                      │
│                                          │                                   │                                          │        │                      │
│ test_planner_tools                       │                                   │                                          │        │ 100.0%               │
│                                          │ Tool Correctness                  │ 1.0 (threshold=0.5, evaluation           │ PASSED │                      │
│                                          │                                   │ model=n/a, reason=[                      │        │                      │
│                                          │                                   │          Tool Calling Reason: All        │        │                      │
│                                          │                                   │ expected tools ['knowledge_search',      │        │                      │
│                                          │                                   │ 'web_search'] were called (order not     │        │                      │
│                                          │                                   │ considered).                             │        │                      │
│                                          │                                   │          Tool Selection Reason: No       │        │                      │
│                                          │                                   │ available tools were provided to assess  │        │                      │
│                                          │                                   │ tool selection criteria                  │        │                      │
│                                          │                                   │ ]                                        │        │                      │
│                                          │                                   │ , error=None)                            │        │                      │
│                                          │                                   │                                          │        │                      │
│ test_researcher_tools                    │                                   │                                          │        │ 100.0%               │
│                                          │ Tool Correctness                  │ 1.0 (threshold=0.5, evaluation           │ PASSED │                      │
│                                          │                                   │ model=n/a, reason=[                      │        │                      │
│                                          │                                   │          Tool Calling Reason: All        │        │                      │
│                                          │                                   │ expected tools ['knowledge_search',      │        │                      │
│                                          │                                   │ 'web_search', 'read_url'] were called    │        │                      │
│                                          │                                   │ (order not considered).                  │        │                      │
│                                          │                                   │          Tool Selection Reason: No       │        │                      │
│                                          │                                   │ available tools were provided to assess  │        │                      │
│                                          │                                   │ tool selection criteria                  │        │                      │
│                                          │                                   │ ]                                        │        │                      │
│                                          │                                   │ , error=None)                            │        │                      │
│                                          │                                   │                                          │        │                      │
│ test_supervisor_calls_plan_first         │                                   │                                          │        │ 100.0%               │
│                                          │ Tool Correctness                  │ 1.0 (threshold=0.5, evaluation           │ PASSED │                      │
│                                          │                                   │ model=n/a, reason=[                      │        │                      │
│                                          │                                   │          Tool Calling Reason: All        │        │                      │
│                                          │                                   │ expected tools ['plan'] were called      │        │                      │
│                                          │                                   │ (order not considered).                  │        │                      │
│                                          │                                   │          Tool Selection Reason: No       │        │                      │
│                                          │                                   │ available tools were provided to assess  │        │                      │
│                                          │                                   │ tool selection criteria                  │        │                      │
│                                          │                                   │ ]                                        │        │                      │
│                                          │                                   │ , error=None)                            │        │                      │
│ Note: Use Confident AI with DeepEval to  │                                   │                                          │        │                      │
│ analyze failed test cases for more       │                                   │                                          │        │                      │
│ details                                  │                                   │                                          │        │                      │
└──────────────────────────────────────────┴───────────────────────────────────┴──────────────────────────────────────────┴────────┴──────────────────────┘

⚠ WARNING: No hyperparameters logged.
» Log hyperparameters to attribute prompts and models to your test runs.

================================================================================


✓ Evaluation completed 🎉! (time taken: 4050.08s | token cost: 0.007343849999999999 USD)
» Test Results (23 total tests):
   » Pass Rate: 65.22% | Passed: 15 | Failed: 8

 ================================================================================ 

» Want to share evals with your team, or a place for your test cases to live? ❤️ 🏡
  » Run 'deepeval view' to analyze and save testing results on Confident AI.

```