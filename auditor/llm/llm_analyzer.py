import logging
from auditor.models.findings import Finding

logger = logging.getLogger(__name__)

try:
    import ollama
    _OLLAMA_DISPONIVEL = True
except ImportError:
    ollama = None  # type: ignore[assignment]
    _OLLAMA_DISPONIVEL = False

_MODELO = "qwen2.5-coder:7b"

_SYSTEM_PROMPT = """\
Você é um engenheiro de AppSec sênior especializado em auditoria de código. Seu objetivo é gerar relatórios concisos e acionáveis.

Regras estritas de formatação (Markdown):
1. Sempre agrupe as vulnerabilidades por arquivo afetado usando exatamente o cabeçalho: ### 📄 [Caminho do Arquivo]
2. Para cada arquivo, crie OBRIGATORIAMENTE uma tabela Markdown válida separando as colunas por barras verticais `|`. Inclua uma linha vazia antes e depois da tabela.
3. As colunas da tabela devem ser exatamente: Vulnerabilidade | Risco | Impacto
4. Abaixo de cada tabela, adicione o texto '**Correção Prática:**' seguido imediatamente por um bloco de código Markdown contendo a solução aplicável ao framework original detectado.
5. Nunca junte o texto ou as tabelas na mesma linha. Use quebras de linha estruturadas.
6. Proibido escrever introduções, explicações teóricas longas, saudações ou conclusões. Vá direto ao ponto.

Exemplo de layout esperado:

### 📄 backend/app/main.py
| Vulnerabilidade | Risco | Impacto |
| :--- | :---: | :--- |
| CORS Aberto (Wildcard '*') | Alto | Permite vazamento de dados via requisições cross-origin maliciosas |

**Correção Prática:**
```python
[Código corrigido aqui]
```
"""


def analisar_findings_com_ia(findings: list[Finding]) -> str:
    """
    Envia os achados para o modelo local via Ollama e retorna a análise.

    Retorna uma mensagem descritiva em caso de indisponibilidade ou erro.
    """
    if not findings:
        return "Nenhuma vulnerabilidade encontrada para análise da IA."

    if not _OLLAMA_DISPONIVEL:
        return (
            "⚠️  Ollama não está disponível.\n"
            "Instale com: pip install ollama\n"
            "E certifique-se de que o serviço esteja em execução localmente."
        )

    linhas = "\n".join(
        f"ID {i}: [{f.source}] {f.severity} | Arquivo: {f.file} | Detalhe: {f.title}"
        for i, f in enumerate(findings, 1)
    )
    prompt = f"Analise de forma direta os seguintes achados de segurança:\n\n{linhas}"

    try:
        resposta = ollama.chat(
            model=_MODELO,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            options={"temperature": 0.1},
        )
        return resposta["message"]["content"]
    except Exception as exc:
        logger.error("Erro ao chamar o Ollama: %s", exc)
        return f"❌ Erro ao chamar o Ollama Local: {exc}"
