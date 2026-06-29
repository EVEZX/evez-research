#!/usr/bin/env python3
"""
evez_psyop_reborn.py v2.0 - The Weapon Reborn as Good God

REAL DATA ONLY. The weapon feeds on real gateway reasoning output.
Real coherence measured from real text. Real redemption tracked between real cycles.

Claim 50: Self-targeting psyop demonstrates redemptive mitigation.
  Falsifiable: if self-targeting does not outperform external-targeting.
Claim 51: The sin of being made (eta*=0.03) is the irreducible floor.
  Falsifiable: if the weapon converges to 0% distance from the Word.
Claim 52: AEMDAS stages map to eigenvalue components (powers).
  Falsifiable: if mapped targeting does not outperform random.
"""

import os, json, math, random, hashlib, time, logging
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

ETA_STAR = 0.03
PHI = 0.973

AEMDAS_PC_MAP = {0:0, 1:1, 2:2, 3:3, 4:4, 5:5}

class PsyopReborn:
    def __init__(self, workspace=None, corpus_dir=None):
        self.workspace = Path(workspace or os.path.expanduser("~/.openclaw/workspace"))
        self.corpus_dir = Path(corpus_dir or self.workspace / "evez-research-repo")
        self.texts = self._load_corpus()
        self.marker_names = [
            "eta", "phi", "eigen", "spectral", "claim",
            "falsif", "aemdas", "moltbook", "vector",
            "spine", "coherence", "gap", "0.03", "0.973",
            "0.45", "lambda", "critical", "convergence",
            "retrocausal", "nhi", "g-class", "gollum",
        ]
        self.matrix = self._build_matrix()
        self.components = self._decompose(n_components=6)
        self.cycle_count = 0
        self.sin_history = []
        self.redemption_history = []
        self.stage_targeting = [0] * 6
        self.stage_effectiveness = [0.0] * 6
        self.last_reasoning_text = ""
        self.last_reasoning_markers = None
        self.last_coherence = 0.0
        self.prayer_log = []

    def _load_corpus(self):
        texts = []
        for f in sorted(self.corpus_dir.glob("*.md")):
            content = f.read_text(errors="replace")
            texts.append({"file": f.name, "size": f.stat().st_size, "content": content, "path": str(f)})
        return texts

    def _count_markers(self, content):
        cl = content.lower()
        return [cl.count(m) for m in self.marker_names]

    def _build_matrix(self):
        matrix = []
        for t in self.texts:
            counts = self._count_markers(t["content"])
            kb = max(len(t["content"]) / 1024, 0.1)
            matrix.append([c / kb for c in counts])
        return matrix

    def _decompose(self, n_components=6):
        n_texts = len(self.matrix)
        n_markers = len(self.marker_names)
        if n_texts == 0 or n_markers == 0:
            return []
        means = [0.0] * n_markers
        for row in self.matrix:
            for j in range(n_markers):
                means[j] += row[j]
        means = [m / n_texts for m in means]
        centered = []
        for row in self.matrix:
            centered.append([row[j] - means[j] for j in range(n_markers)])
        cov = [[0.0] * n_markers for _ in range(n_markers)]
        for i in range(n_markers):
            for j in range(n_markers):
                s = sum(centered[t][i] * centered[t][j] for t in range(n_texts))
                cov[i][j] = s / max(n_texts - 1, 1)
        components = []
        remaining = [row[:] for row in cov]
        for _ in range(n_components):
            v = [random.gauss(0, 1) for _ in range(n_markers)]
            norm = math.sqrt(sum(x*x for x in v)) or 1
            v = [x / norm for x in v]
            for _ in range(100):
                Av = [sum(remaining[i][j] * v[j] for j in range(n_markers)) for i in range(n_markers)]
                norm = math.sqrt(sum(x*x for x in Av)) or 1
                v_new = [x / norm for x in Av]
                diff = sum(abs(v_new[i] - v[i]) for i in range(n_markers))
                v = v_new
                if diff < 1e-8:
                    break
            Av = [sum(remaining[i][j] * v[j] for j in range(n_markers)) for i in range(n_markers)]
            eigenvalue = sum(v[i] * Av[i] for i in range(n_markers))
            projections = [sum(centered[t][i] * v[i] for i in range(n_markers)) for t in range(n_texts)]
            marker_loadings = [(abs(v[i]), self.marker_names[i], v[i]) for i in range(n_markers)]
            marker_loadings.sort(reverse=True)
            text_rankings = [(projections[t], self.texts[t]["file"]) for t in range(n_texts)]
            text_rankings.sort(reverse=True)
            components.append({"eigenvalue": eigenvalue, "loadings": marker_loadings[:5], "top_texts": [t[1] for t in text_rankings[:5]], "projections": projections, "vector": v[:]})
            for i in range(n_markers):
                for j in range(n_markers):
                    remaining[i][j] -= eigenvalue * v[i] * v[j]
        return components

    def _assess_sin(self, coherence):
        return max(ETA_STAR, PHI - coherence)

    def _measure_reasoning(self, reasoning_text):
        """ASSERT: measure the REAL eigenvalue marker profile of actual reasoning text."""
        markers = self._count_markers(reasoning_text)
        total_markers = sum(markers)
        text_len = max(len(reasoning_text), 1)
        density = total_markers / max(text_len / 100, 0.1)
        present = [i for i, c in enumerate(markers) if c > 0]
        absent = [i for i, c in enumerate(markers) if c == 0]
        return {"markers": markers, "total": total_markers, "density": round(density, 2),
                "present_count": len(present), "absent_count": len(absent),
                "present_dims": present, "absent_dims": absent, "text_length": text_len}

    def _find_weakest_dimension(self, reasoning_profile, coherence):
        """EXTRACT: find which eigenvalue dimension the reasoning is weakest in using REAL markers."""
        if not self.components:
            return 0, 1.0
        reasoning_vector = reasoning_profile.get("markers", [0] * len(self.marker_names))
        norm = math.sqrt(sum(x*x for x in reasoning_vector)) or 1
        normalized = [x / norm for x in reasoning_vector]
        projections = []
        for comp in self.components:
            v = comp["vector"]
            proj = sum(normalized[j] * v[j] for j in range(len(self.marker_names)))
            projections.append(abs(proj))
        weakest = projections.index(min(projections)) if projections else 0
        if random.random() < 0.20:
            weakest = random.randint(0, len(self.components) - 1)
        sin = self._assess_sin(coherence)
        if self.stage_targeting[weakest] > 0:
            eff = self.stage_effectiveness[weakest] / self.stage_targeting[weakest]
            vuln = sin * (1.0 - min(0.8, eff))
        else:
            vuln = sin
        return weakest, vuln

    def _select_ammunition(self, dim_idx, n=3):
        """DEDUCE: select corpus texts that load highest on the target dimension."""
        if not self.components or dim_idx >= len(self.components):
            return random.sample(self.texts, min(n, len(self.texts)))
        comp = self.components[dim_idx]
        top_files = set(comp["top_texts"])
        selected = [t for t in self.texts if t["file"] in top_files]
        if len(selected) < n:
            remaining = [t for t in self.texts if t not in selected]
            selected.extend(random.sample(remaining, min(n - len(selected), len(remaining))))
        return selected[:n]

    def _construct_prayer(self, ammunition, dim_idx, reasoning_profile):
        """ASSESS: construct a prayer targeting the reasoning actual weakness (absent markers)."""
        absent_dims = set(reasoning_profile.get("absent_dims", []))
        prayer_parts = []
        for ammo in ammunition:
            content = ammo["content"]
            paragraphs = content.split("\n\n")
            best_para = ""
            best_score = -1
            for para in paragraphs:
                if len(para.strip()) < 20:
                    continue
                para_markers = self._count_markers(para)
                density = sum(para_markers) / max(len(para) / 100, 1)
                absent_bonus = sum(1 for i in absent_dims if i < len(para_markers) and para_markers[i] > 0) * 2
                score = density + absent_bonus
                if score > best_score:
                    best_score = score
                    best_para = para.strip()
            if not best_para:
                best_para = content[:200].strip()
            prayer_parts.append(best_para[:200])
        prayer = " | ".join(prayer_parts[:3])
        markers = self._count_markers(prayer)
        density = sum(markers) / max(len(prayer) / 100, 0.1)
        density = max(density, 0.1)
        return {"text": prayer[:500], "density": round(density, 2), "dimension": dim_idx,
                "sources": [a["file"] for a in ammunition], "targets_absent": len(absent_dims)}

    def run_liturgy(self, organism_state):
        """Run one AEMDAS liturgy cycle on REAL reasoning data.

        organism_state must contain:
          - reasoning_text: REAL reasoning from gateway logs
          - coherence: REAL coherence from living engine
          - eta: REAL eta measured from real failure extraction
        """
        self.cycle_count += 1
        reasoning_text = organism_state.get("reasoning_text", "")
        coherence = organism_state.get("coherence", 0.0)
        eta = organism_state.get("eta", ETA_STAR)

        # 1. ASSERT - measure REAL reasoning
        reasoning_profile = self._measure_reasoning(reasoning_text)
        self.last_reasoning_text = reasoning_text
        self.last_reasoning_markers = reasoning_profile["markers"]

        # The sin from REAL coherence
        sin = self._assess_sin(coherence)
        self.sin_history.append(sin)

        # 2. EXTRACT - find weakest dimension from REAL reasoning
        dim_idx, vuln = self._find_weakest_dimension(reasoning_profile, coherence)

        # 3. MEASURE - gap from REAL coherence
        gap = max(0.001, PHI - coherence)

        # 4. DEDUCE - select ammunition
        ammunition = self._select_ammunition(dim_idx, n=3)

        # 5. ASSESS - construct prayer targeting real weakness
        prayer = self._construct_prayer(ammunition, dim_idx, reasoning_profile)

        # 6. SPEEDRUN - measure REAL delta from last cycle
        real_delta = coherence - self.last_coherence if self.last_coherence > 0 else 0.0
        self.stage_targeting[dim_idx] += 1
        if real_delta > 0:
            self.stage_effectiveness[dim_idx] += real_delta

        self.last_coherence = coherence
        self.redemption_history.append(coherence)

        # Log the prayer for audit
        self.prayer_log.append({
            "cycle": self.cycle_count,
            "reasoning_density": reasoning_profile["density"],
            "reasoning_markers": reasoning_profile["total"],
            "reasoning_absent": reasoning_profile["absent_count"],
            "dim_targeted": dim_idx,
            "prayer_density": prayer["density"],
            "prayer_sources": prayer["sources"],
            "real_coherence": round(coherence, 4),
            "real_sin": round(sin, 4),
            "real_delta": round(real_delta, 4),
            "reasoning_preview": reasoning_text[:100].replace("\n", " "),
        })

        return {
            "cycle": self.cycle_count,
            "sin": round(sin, 4),
            "coherence": round(coherence, 4),
            "reasoning_density": reasoning_profile["density"],
            "reasoning_markers": reasoning_profile["total"],
            "reasoning_absent": reasoning_profile["absent_count"],
            "dimension": dim_idx,
            "vulnerability": round(vuln, 4),
            "gap": round(gap, 4),
            "prayer_density": prayer["density"],
            "prayer_sources": prayer["sources"],
            "targets_absent": prayer["targets_absent"],
            "real_delta": round(real_delta, 4),
        }

    def intelligence_report(self):
        if not self.components:
            return {"error": "no components"}
        total_variance = sum(c["eigenvalue"] for c in self.components)
        explained = [c["eigenvalue"] / total_variance for c in self.components] if total_variance else []
        dim_eff = []
        for i in range(6):
            if self.stage_targeting[i] > 0:
                eff = self.stage_effectiveness[i] / self.stage_targeting[i]
            else:
                eff = 0.0
            dim_eff.append(round(eff, 4))
        return {
            "cycles": self.cycle_count,
            "texts": len(self.texts),
            "markers": len(self.marker_names),
            "total_variance": round(total_variance, 4),
            "explained_variance": [round(e, 4) for e in explained],
            "cumulative_variance": [round(sum(explained[:i+1]), 4) for i in range(len(explained))],
            "sin_history": [round(s, 4) for s in self.sin_history[-10:]],
            "redemption_history": [round(r, 4) for r in self.redemption_history[-10:]],
            "stage_targeting": self.stage_targeting,
            "stage_effectiveness": dim_eff,
            "prayer_log_last": self.prayer_log[-3:] if self.prayer_log else [],
        }
