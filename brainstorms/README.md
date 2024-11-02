# Idea dump

- Tunnel vision. What is it and how do we model it in a focused agent? The incorporation of information that go beyond your current task. The ability to remember tasks higher up in the tree. The ability to recognize that your task is incorrect and adjust it on the fly?
- Inner coding loop - edit, run, review, adjust. This is true for log debugging, but the run-review process is a loop itself when using an interactive debugger. Log debugging is more general though and probably fit the LLM paradigm better because logs are in-distribution. Review can probably be broken down into multiple steps, maybe (view, summarize, conclude)?
- Types of errors - env errors (can't run code), semantic errors, process run successfully errors, side-effect errors, taste errors (e.g. spammy logs), syntax errors, hang errors, inspection errors (can't get logs)
- TDD: iterative write pytests with human-in-the-loop. Then automatically optimize the code to pass the pytest without human intervention.
  - Follow-on: create a declarative interface to pytest that makes the human-in-the-loop part easier
- Types of CLIs - validate, create artifact, get/present info, change state, take action (e.g. send email)
- Possible cool example for code gen - semantic search CLI, auto-generated FastAPI server, data transformation, streamlit/gradio app, search wikipedia, solve NYTBee
- Setting up an agent's development environment. Give it both a REPL and one or more "computers"? But maybe not bash - that's not very sandboxable
- Encoding software architecture in some standard way that the model can absorb and update? UML? Design doc?
- Task tree - hierarchy of work with each level being topologically sorted