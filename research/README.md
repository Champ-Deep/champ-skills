# Research & Science (`research/`)

Literature review, paper narrative, scientific figure/prompt work, bioinformatics (AlphaFold, Boltz, Evo2, scGPT, etc.).

Install: copy a skill folder into your agent's skills dir (e.g. `cp -R {cat}/<skill> ~/.claude/skills/`). Each skill is self-contained with `SKILL.md`.

| Skill | What it does |
|---|---|
| `alphafold2` | Predict protein structure for monomers and multimers with AlphaFold2 via the ColabFold runner (Mirdita et al. 2022, github.com/sokrypton/ColabFold; AlphaFold2 Jumper et a |
| `boltz` | Structure prediction for protein, nucleic-acid, and small-molecule complexes with Boltz-2 (Passaro & Wohlwend et al. 2025, github.com/jwohlwend/boltz). Reach for this ski |
| `borzoi` | Predict genome-wide functional tracks (RNA-seq, CAGE, DNase, ChIP) from DNA sequence with Borzoi. Use this skill when: (1) Scoring the regulatory effect of a variant on e |
| `chai1` | Structure prediction for protein, nucleic-acid, and small-molecule complexes with the Chai-1 foundation model (Chai Discovery 2024, github.com/chaidiscovery/chai-lab). Re |
| `champ-brainstorm` | Interactive brainstorming skill using the CHAMP framework, a structured ideation method that adapts its lens depending on context. Use this skill whenever a user wants to |
| `diffdock` | Predict small-molecule binding poses with DiffDock-L (Corso et al. 2023/2024, github.com/gcorso/DiffDock), blind diffusion docking that places a ligand into a protein poc |
| `esmfold2` | Biohub ESMFold2 / ESMFold2-Fast all-atom co-folding (Candido et al. 2026, github.com/Biohub/esm). Single-sequence and MSA modes; protein, DNA, RNA, ligand (CCD/SMILES), m |
| `evo2` | Score, embed, and generate DNA sequences with Evo 2, a long-context genomic foundation model. Use this skill when: (1) Computing per-nucleotide or per-sequence likelihood |
| `fair-esm2` | Embed proteins with Meta AI's ESM-2 (`fair-esm` package). Use this skill when: (1) Extracting per-residue or per-sequence embeddings for downstream ML, (2) Masked-LM like |
| `indication-dossier` | Generate a therapeutic indication dossier. Covers the patient population, epidemiology, disease biology, standard of care, regulatory precedent, and landmark clinical tri |
| `ligandmpnn` | Inverse-fold a backbone with ligand, nucleic-acid, and metal context using LigandMPNN (Dauparas et al. 2023, github.com/dauparas/LigandMPNN). Reach for this skill to rede |
| `literature-review` | Find, verify, and synthesize scientific literature, from "what's the seminal paper for X" through full multi-source reviews. Covers grounding claims in real retrieved sou |
| `openfold3` | Structure prediction using OpenFold3, an open-weights PyTorch reproduction of AlphaFold3 from the AlQuraishi Lab. Use this skill when predicting protein/nucleic-acid/liga |
| `paper-narrative` | Judge and reshape the STORY a paper's figures tell. Input is the work itself, manuscript (or abstract) + figure deck, no hand-written brief. `derive_paper_brief(abstract, |
| `pdf-explore` | Use this skill when the user has attached a PDF, paper, report, or other document and the answer needs content from more than one place in it: summarize the methods or an |
| `proteinmpnn` | Inverse-fold a protein backbone (PDB structure) into amino-acid sequence with ProteinMPNN (Dauparas et al. 2022, github.com/dauparas/ProteinMPNN). Reach for this skill to |
| `scgpt` | Embed and annotate single-cell expression data with scGPT, a foundation model for single-cell biology. Use this skill when: (1) Producing cell embeddings from an AnnData  |
| `scvi-tools` | Probabilistic single-cell RNA-seq with scvi-tools, scVI for a batch-corrected latent space, scANVI for semi-supervised label transfer, and Bayesian differential expressio |
| `solublempnn` | Inverse-fold a backbone with SolubleMPNN, ProteinMPNN retrained on a soluble-PDB subset (Dauparas et al. 2022), for sequences biased toward cytosolic expression and reduc |

See the master [INDEX.md](../INDEX.md) for every skill.