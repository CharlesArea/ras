---
name: setup
description: Set up the local Python rendering runtime after RAS is installed, or diagnose a missing ras-report command or rendering dependency. Use only for RAS installation and environment setup.
---

# Set up RAS

RAS needs Python 3.11 or newer and its rendering dependencies. Check the
Python version and whether `ras-report --help` succeeds.

If the runtime is missing, explain that the following command installs the RAS
CLI and DOCX/PDF rendering dependencies from the pinned release, then obtain
the user's approval before running it:

```text
python -m pip install "ras-report-anything[render] @ git+https://github.com/CharlesArea/ras.git@v0.1.0"
```

After installation, run `ras-report --help` and `ras-report template list` to
verify the environment. PPTX is an optional companion and also requires the
host's supported Node.js and presentation runtime.
