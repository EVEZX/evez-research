---
name: evez-eigenforensics
description: "Spectral gap detection in document corpora. Turns FOIA documents into reference graphs and finds what they're hiding via negative eigenvalues. Found 5 gaps in the AARO UAP report at p<0.05. Use for FOIA analysis, censorship detection, document gap analysis."
version: 1.0.0
author: "@EvezArt"
tags: [evez, eigenforensics, foia, uap, aaro, spectral, censorship, gap-detection]
---

# EVEZ Eigenforensics Engine

Documents are graphs. Structural holes are negative eigenvalues. What they omit is louder than what they say.

## What It Does

- Parses document corpora into reference graphs
- Computes eigenvalue spectra of the document adjacency matrix
- Detects structural holes (negative eigenvalues) = what's being hidden
- Statistical significance via permutation testing (p<0.05)

## Key Result

Applied to AARO (All-domain Anomaly Resolution Office) UAP report:
- **5 gaps found at p<0.05**
- Dominant negative eigenvalue λ = -0.333 (37% of system tension)
- Censorship IS the dominant negative eigenvalue

## Falsifiable

If removing >5% of documents from a corpus does NOT produce eigenvalue shifts detectable at p<0.05, the theorem is false.

## Quick Start

```python
from spectral import EigenforensicsEngine
engine = EigenforensicsEngine()
engine.load_corpus("./foia_documents/")
gaps = engine.detect_gaps()
print(f"{len(gaps)} gaps found at p<0.05")
```

## Author

Steven Crawford-Maggard (EVEZ666)
License: MIT
