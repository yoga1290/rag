# Hexagonal Architecture for Provider-Agnostic RAG Pipelines

Demo stack: [**LangChain**](https://reference.langchain.com/python/langchain-community/llms/llamacpp/LlamaCpp), [**LlamaCpp**](https://github.com/ggml-org/llama.cpp), [**Mistral.ai**](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3), [**Qwen Embeddings**](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B-GGUF), **PostgreSQL**, **Telegraf**, **Prometheus** on Docker.

---

I recently came across [**Machine Learning Mastery's guide**](https://machinelearningmastery.com/building-a-rag-pipeline-with-llama-cpp-in-python/) on **Building a RAG Pipeline with llama.cpp** and decided to try it myself.

One thing quickly became apparent: some of the APIs and methods used in the example had already changed or become deprecated.
That led me to a bigger question:
**How do you design a RAG system that can evolve as the underlying technologies change?**
Instead of tightly coupling the application to a specific LLM, vector database, or document-processing framework, I experimented with a more modular architecture.
This way I get a more resilient architecture, for instance if I need a transition between local on-premise to fully on cloud or just hybrid; ability to switch to different database like PostgreSQL instead of ChromaDB, due to the data integration and ACID compliance!

A few principles became particularly important:
- **🧩 Decouples the technology dependency** Provider implementations can be replaced without changing core logic, as the architecture relies on **interfaces, abstractions & models**, while Lazy Imports **isolate technology-specific dependencies**.
```python
def importOnCall(..):
    from.. import .. # Lazy import
    return ResultModel(..) # tied to Abstracts & Models
```

- **🔌️ On-premise, hybrid & Multi-platform support** Decoupling from certain SDK or API or local implementations keep my options open to plug & play the document sources, different LLM models or vector stores/databases, regardless of being local, hybrid or on cloud services. 🖥️🔄☁️
```python
vectorstore: VectorStore = PGVectorStore(...)
vectorstore: VectorStore = OtherVectorDBService(..)
```

- **🛠️ Separation of responsibilities**
Each layer has a focused responsibility:
    - **🧠 Domain** — business concepts, models, and contracts
    - **🔌 Ports** — define what the application needs
    - **⚙️ Infrastructure** — provides concrete implementations
    - **🔄 Pipelines/Application** — orchestrates the workflow
    - **🧩 Composition** — selects and wires implementations together

- 📦️ **Observability, Containerization & Resource/Network monitoring**, Confiurations are pass in form of **Environment Variables**, see [`sample.env`](https://github.com/yoga1290/rag/raw/master/sample.env). **Telegraf** is used to monitor the **resource consumsion** and **network traffic**, and project metrics to **Prometheus**. See the [👁️ Observability](#%EF%B8%8F-container-observability) section.

---

![docs/domain-models-methods-horizontal.png](https://github.com/yoga1290/rag/raw/master/docs/domain-models-methods-horizontal.png)
![docs/domain-overview.png](https://github.com/yoga1290/rag/raw/master/docs/domain-overview.png)

---

# Overview
Startup this Jupiter notebook, PostgressSQL database & Promethus+Grafana servers via: `docker compose up notebook`.
+ [📚️ Ingestion Pipeline](#%EF%B8%8F-ingestion-pipeline)
+ [🔍️ Retrieval Pipeline](#%EF%B8%8F-retrieval-pipeline)
+ [🏗️ Extraction Pipeline](#%EF%B8%8F-extraction-pipeline)
+ [👁️ Observability](#%EF%B8%8F-container-observability)
+ [🔧️ Turning Implementations](#%EF%B8%8F-tuning-implementations)

----

# 📚️ Ingestion Pipeline


```python
########################### INTERFACES & MODELS ###########################
from yoga1290.rag.domain.models import (
                            Document,
                            ParsedDocument,
                            SearchDocument)
from yoga1290.rag.domain.ports import (
                            DocumentSource,
                            DocumentParser,
                            VectorStore,
                            SearchPreparer,
                            Embedder)
########################### IMPLEMENTATIONS ###########################
from yoga1290.rag.infrastructure.embeddings import LlamaCppEmbeddings
from yoga1290.rag.infrastructure.vectorstores import PGVectorStore
from yoga1290.rag.infrastructure.local.sources.csv_document_source import CsvDocumentSource
from yoga1290.rag.infrastructure.local.parsing.local_document_parser import LocalDocumentParser
from yoga1290.rag.infrastructure.local.search.local_search_preparer import LocalSearchPreparer

from yoga1290.rag.application.pipelines import IngestionPipeline

document_source: DocumentSource = (
                    CsvDocumentSource(
                        # configuration injected from Environment Variables
                        # csv_path
                        # document_column
                    ))

document_parser: DocumentParser = (
                    LocalDocumentParser())

document_search_preparer: SearchPreparer = (
                    LocalSearchPreparer())

embedder: Embedder = (
                    LlamaCppEmbeddings())

vectorstore: VectorStore = (
                    PGVectorStore(
                        # configration from Environment Variables; connection_string=f"postgresql+psycopg://{os.getenv("POSTGRES_USER")}.."
                        embedder=embedder))

IngestionPipeline(
    parser= document_parser,
    extractor= None,
    classifier= None,
    search_preparer= document_search_preparer,
    vectorstore= vectorstore
).process( documents= document_source )
```

# 🔍️ Retrieval Pipeline


```python
########################### INTERFACES & MODELS ###########################
from yoga1290.rag.domain.models import (
                            Document,
                            ParsedDocument,
                            SearchDocument,
                            )
from yoga1290.rag.domain.ports import (
                            DocumentSource,
                            DocumentParser,
                            VectorStore,
                            SearchPreparer,
                            Embedder,
                            Retriever)
########################### IMPLEMENTATIONS ###########################
from yoga1290.rag.infrastructure.embeddings import LlamaCppEmbeddings
from yoga1290.rag.infrastructure.vectorstores import PGVectorStore, PGVectorRetriever
from yoga1290.rag.infrastructure.local.sources.csv_document_source import CsvDocumentSource
from yoga1290.rag.infrastructure.local.parsing.local_document_parser import LocalDocumentParser
from yoga1290.rag.infrastructure.local.search.local_search_preparer import LocalSearchPreparer

from yoga1290.rag.factories.llm_factory import LLMFactory
from yoga1290.rag.application.pipelines import RetrievalPipeline

embedder: Embedder = (
                    LlamaCppEmbeddings())

vectorstore: VectorStore = (
                    PGVectorStore(
                        #connection_string=f"postgresql+psycopg://{os.getenv("POSTGRES_USER")}.."
                        embedder=embedder))

pgvector_retriever: Retriever = (
                    PGVectorRetriever(vectorstore=vectorstore, ));

llm_llama= LLMFactory.createLocalLlamaCppLLM()

response =  RetrievalPipeline(
                llm= llm_llama,
                retriever= pgvector_retriever,
                top_k=2,
            ).run( question= "Make a good introduction about my backend skillset" )

print(f"Answer {response.answer}")
```

    init: embeddings required but some input tokens were not marked as outputs -> overriding


    Answer 
    "Welcome to my backend skillset! I specialize in the practical, hands-on experience of using AI-assisted development tools such as GitHub Copilot and Claude Code. This allows me to write, review, refactor, debug, and optimize code efficiently.
    
    In addition to my AI-assisted development skills, I have extensive experience with Docker for building and managing container images.
    
    My expertise also extends to API gateway configuration, proxy development, and policy management, using tools such as Apigee or similar API gateways.
    
    While these are my primary skillsets, I also possess a nice-to-have set of skills that include experience with AWS, GCP, or Azure; Kafka or RabbitMQ; Helm charts and/or Kubernetes operators; Jira, Confluence, Atlassian Rovo, and similar tools.
    
    In summary, my backend skillset is well-rounded, with a focus on AI-assisted development, Docker, API gateway configuration, proxy development, and policy management. I also possess a nice-to-have set of skills that include experience with various cloud providers, Kafka or RabbitMQ, Helm charts and/or Kubernetes operators, Jira, Confluence, Atlassian Rovo, and similar tools."


# 🏗️ Extraction Pipeline

Here's an example of asking the LLM (Mistral on llamaCpp) to extract fields from my receipt emails pulled using [yoga1290/python-imap-smtp](https://github.com/yoga1290/python-imap-smtp/blob/main/notebook.ipynb) [see [`docker-compose.yml`](https://github.com/yoga1290/rag/blob/master/docker-compose.yml#L136)] that outputs to CSV table.
It simply generates inner prompt per each requested field and collects the responses into a dict map.

```python
########################### INTERFACES & MODELS ###########################
from yoga1290.rag.domain.models import (
                            ParsedDocument,
                            ExtractedData,)
from yoga1290.rag.domain.ports import (
                            DocumentSource,
                            DocumentParser,
                            DocumentExtractor,)
############################################################################
from yoga1290.rag.infrastructure.local.extraction import LlamaCppDocumentExtractor
from yoga1290.rag.infrastructure.local.sources.csv_document_source import CsvDocumentSource
from yoga1290.rag.infrastructure.local.parsing.local_document_parser import LocalDocumentParser

document_source: DocumentSource = (
                    CsvDocumentSource(
                        # configuration injected from Environment Variables
                        csv_path = "documents/output.csv",
                        document_column = "attachments"
                    ))

document_parser: DocumentParser = (
                    LocalDocumentParser())
document_extractor: DocumentExtractor = (
                    LlamaCppDocumentExtractor())

for document in document_source:
    parsed_document: ParsedDocument = (
                        document_parser.parse(document))
    response: ExtractedData = document_extractor.extract(
                        parsed_document=parsed_document,
                        fields= ['Is there a payment receipt?',
                                 'Total Payment Amount',
                                 'Vendor' ,
                                 'Item name',
                                 'Date of purchase'])
    print(f'response: {response}')
```

# 👁️ Container Observability
Monitoring the **resource consumption**, **network** traffic & **isolation** can ideicate how well different LLM models can perform under larger sets. 
In my `docker-compose.yml` configuration, there're the following 3 containers:
+ `monitored-job`: a container with Python & Telegraf pre-installed, see my [[Dockerfile]](https://github.com/yoga1290/rag/blob/master/ci/docker-telegraf-python/Dockerfile), [[docker-compose.yml]](https://github.com/yoga1290/rag/blob/master/docker-compose.yml#L24).  
+ `Promethus`: collecting metric data from the Telegraf server in the `monitored-job`
+ `Grafana`: for visualizing `Promethus` metrics into an intuitive dashboard; I used the [**Grafana's dashboard: System Metrics for the Linux Hosts**](https://grafana.com/grafana/dashboards/15365-system-metrics-for-the-linux-hosts/), which is compatible with Telegraf projected metrics but it needs a tweak:
    + Make sure, Prometheus can see the Job container, try query the [`monitored-job`](http://localhost:9090/query?g0.expr=up%7Binstance%3D%22monitored-job%3A9273%22%7D&g0.show_tree=1&g0.tab=table&g0.range_input=1h&g0.res_type=auto&g0.res_density=medium&g0.display_mode=lines&g0.show_exemplars=0)
    + Make sure, the `DS_PROMETHEUS` dashboard variable matches the name of the Datasource variable in the Grafana's [`datasource.yml`](https://github.com/yoga1290/rag/blob/master/observability/grafana/provisioning/datasources/datasource.yml), which is `DS_SERVERMONITOR` in my case.

![](https://github.com/yoga1290/rag/raw/master/docs/grafana-dashboards-15365-system-metrics-for-the-linux-hosts.png)

# 🔧️ Tuning Implementations

To add support for a new LLM, you will need to implement on the existing abstracts, interfaces & return the domain's data models, for example LlamaCppLLM:

```python
# %load ./src/yoga1290/rag/domain/ports/llm.py
from abc import ABC, abstractmethod
class LLM(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a response from a prompt.
        """
        raise NotImplementedError
```


```python
# %load ./src/yoga1290/rag/infrastructure/local/llm/llama_cpp_llm.py
from yoga1290.rag.domain.ports import LLM

class LlamaCppLLM(LLM):

    def __init__(
        self,
        model_path: str,
        temperature: float = 0.15,
        max_tokens: int = 450,
        context_size: int = 4096,
        batch_size: int = 384,
    ) -> None:
        from langchain_community.llms import LlamaCpp
        self._llm = LlamaCpp(
            model_path=model_path,
            temperature=temperature,
            max_tokens=max_tokens,
            n_ctx=context_size,
            n_batch=batch_size,
            verbose=False,
        )

    def generate(self, prompt: str) -> str:
        return self._llm.invoke(prompt)
```
