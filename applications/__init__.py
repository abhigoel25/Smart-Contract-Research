"""
applications package — namespace shim for the Experiments folder.

The actual implementation lives in applications/contract-translator/core/.
Because `contract-translator` contains a hyphen it cannot be imported via
normal Python dotted-path notation.  This __init__.py resolves that by:

  1. Adding applications/contract-translator/ to sys.path so that `core`
     (the properly-named sub-package) becomes directly importable.
  2. Pre-importing each core sub-module so their relative imports (which
     reference each other via `from .X import …`) resolve correctly.
  3. Aliasing each sub-module under the `applications.*` namespace so that
     experiment files can simply write:

         from applications.solidity_compiler import SolidityCompilationChecker
         from applications.translator import IBMAgenticContractTranslator
         from applications.task_builders import create_quality_evaluation_task_description
         from applications import agents as _agents_module
"""
import sys
from pathlib import Path

# ── 1. Expose  contract-translator/  so that  `import core`  works ──────────
_ct_path = str(Path(__file__).parent / "contract-translator")
if _ct_path not in sys.path:
    sys.path.insert(0, _ct_path)

# ── 2. Import core sub-modules in dependency order (schemas first) ──────────
import core.schemas          # noqa: F401  – Pydantic models
# core.programs uses legacy IBM Agentics LLM/Program API; guard so experiments
# that don't need it still load cleanly if that API is unavailable.
try:
    import core.programs     # noqa: F401  – Legacy Program classes
    _programs_ok = True
except ImportError:
    _programs_ok = False
import core.task_builders    # noqa: F401  – Task description builders
import core.agents           # noqa: F401  – Agent factories + _convert_to_crew_llm
import core.solidity_compiler  # noqa: F401  – SolidityCompilationChecker
import core.translator       # noqa: F401  – IBMAgenticContractTranslator

# ── 3. Register aliases so  `from applications.X import Y`  resolves ────────
sys.modules.setdefault("applications.schemas",            core.schemas)
if _programs_ok:
    sys.modules.setdefault("applications.programs",       core.programs)
sys.modules.setdefault("applications.task_builders",      core.task_builders)
sys.modules.setdefault("applications.agents",             core.agents)
sys.modules.setdefault("applications.solidity_compiler",  core.solidity_compiler)
sys.modules.setdefault("applications.translator",         core.translator)
