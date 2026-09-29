# Science & Research (champ-science plugin) (`science/`)

Bio models, literature, figures, Claude Science platform skills.

| Skill | What it does |
|---|---|
| `alphafold2` | Predict protein structure for monomers and multimers with AlphaFold2 via the ColabFold runner (Mirdita et al. 2022, github.com/sokrypton/ColabFold; AlphaFold2 Jumper et a |
| `boltz` | Structure prediction for protein, nucleic-acid, and small-molecule complexes with Boltz-2 (Passaro & Wohlwend et al. 2025, github.com/jwohlwend/boltz). Reach for this ski |
| `borzoi` | Predict genome-wide functional tracks (RNA-seq, CAGE, DNase, ChIP) from DNA sequence with Borzoi. Use this skill when: (1) Scoring the regulatory effect of a variant on e |
| `chai1` | Structure prediction for protein, nucleic-acid, and small-molecule complexes with the Chai-1 foundation model (Chai Discovery 2024, github.com/chaidiscovery/chai-lab). Re |
| `compute-env-setup` | Set up a compute environment on a remote provider so Claude Science jobs can run there. Covers direct SSH/conda hosts, Slurm clusters, container-via-bridge runners, and m |
| `customize` | Create, configure, and maintain custom agent profiles and author new skills via the `repl` tool. Use when the user wants to create an agent profile, build a custom agent, |
| `diffdock` | Predict small-molecule binding poses with DiffDock-L (Corso et al. 2023/2024, github.com/gcorso/DiffDock), blind diffusion docking that places a ligand into a protein poc |
| `esmfold2` | Biohub ESMFold2 / ESMFold2-Fast all-atom co-folding (Candido et al. 2026, github.com/Biohub/esm). Single-sequence and MSA modes; protein, DNA, RNA, ligand (CCD/SMILES), m |
| `evo2` | Score, embed, and generate DNA sequences with Evo 2, a long-context genomic foundation model. Use this skill when: (1) Computing per-nucleotide or per-sequence likelihood |
| `fair-esm2` | Embed proteins with Meta AI's ESM-2 (`fair-esm` package). Use this skill when: (1) Extracting per-residue or per-sequence embeddings for downstream ML, (2) Masked-LM like |
| `figure-composer` | Compose one publication-grade multi-panel figure. Entry from a one-line claim + data refs, OR from an existing figure via `derive_outline(png)`. Runs a per-figure loop: o |
| `figure-style` | Publication-grade figure correctness and legibility rules for final-deliverable figures, not every plot. Quick look or iterating on the analysis (EDA scatters, sanity-che |
| `indication-dossier` | Generate a therapeutic indication dossier. Covers the patient population, epidemiology, disease biology, standard of care, regulatory precedent, and landmark clinical tri |
| `ligandmpnn` | Inverse-fold a backbone with ligand, nucleic-acid, and metal context using LigandMPNN (Dauparas et al. 2023, github.com/dauparas/LigandMPNN). Reach for this skill to rede |
| `literature-review` | Find, verify, and synthesize scientific literature, from "what's the seminal paper for X" through full multi-source reviews. Covers grounding claims in real retrieved sou |
| `managed-model-endpoints` | Register a model service in the managed family, a local model server container the daemon starts/stops on demand, or a remote upstream model API (https). Read the runbook |
| `openfold3` | Structure prediction using OpenFold3, an open-weights PyTorch reproduction of AlphaFold3 from the AlQuraishi Lab. Use this skill when predicting protein/nucleic-acid/liga |
| `paper-narrative` | Judge and reshape the STORY a paper's figures tell. Input is the work itself, manuscript (or abstract) + figure deck, no hand-written brief. `derive_paper_brief(abstract, |
| `pdf-explore` | Use this skill when the user has attached a PDF, paper, report, or other document and the answer needs content from more than one place in it: summarize the methods or an |
| `product-self-knowledge` | Stop and consult this skill whenever your response would include specific facts about Anthropic's products. Covers: Claude Code (how to install, Node.js requirements, pla |
| `proteinmpnn` | Inverse-fold a protein backbone (PDB structure) into amino-acid sequence with ProteinMPNN (Dauparas et al. 2022, github.com/dauparas/ProteinMPNN). Reach for this skill to |
| `remote-compute-modal` | Run GPU jobs on the user's own Modal account via host.compute.create('modal', provider_params={...}), the create→submit→wait_for_notification flow, the compute_provider k |
| `remote-compute-ssh` | Submit→wait_for_notification→collect-outputs workflow for the user's SSH/SLURM hosts. Load once you've decided to dispatch remote. |
| `scgpt` | Embed and annotate single-cell expression data with scGPT, a foundation model for single-cell biology. Use this skill when: (1) Producing cell embeddings from an AnnData  |
| `scvi-tools` | Probabilistic single-cell RNA-seq with scvi-tools, scVI for a batch-corrected latent space, scANVI for semi-supervised label transfer, and Bayesian differential expressio |
| `self-awareness` | Claude Science's own session database schema and SDK surface for introspection via host.query(). Load this when you need to query your own conversation history, token usa |
| `solublempnn` | Inverse-fold a backbone with SolubleMPNN, ProteinMPNN retrained on a soluble-PDB subset (Dauparas et al. 2022), for sequences biased toward cytosolic expression and reduc |
| `using-model-endpoint` | Call a registered model endpoint over its native HTTP API from the endpoint's scoped inference kernel (BASE_URL preloaded). Load once a task needs predictions from a regi |
