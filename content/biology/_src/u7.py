from common import build
lesson = r"""
## What problem is this paper solving?

ML-for-biology papers usually fall into a few task families. Identify which one, then ask: what is the input, what is the label, where did the data come from, and how was it split?

- **Structure prediction**: sequence → 3D coordinates (AlphaFold2/3, ESMFold, RoseTTAFold). The benchmark is **CASP**, a biennial blind competition running since 1994 that scores unreleased structures with GDT_TS and lDDT. **CAMEO** runs continuously. AlphaFold2 dominated CASP14 (2020).
- **Variant effect prediction (VEP)**: given a variant, predict its functional or clinical impact. Models include EVE, ESM-1v, AlphaMissense, GEMME, and SpliceAI (for splicing). Labels come from **DMS** experiments or **ClinVar**.
- **Fitness prediction and protein design**: score or generate sequences with a desired property (stability, binding, activity). Supervised versions train on assay data; generative design uses ProteinMPNN (inverse folding), RFdiffusion, etc.
- **Regulatory genomics**: DNA sequence → functional tracks (expression, accessibility, ChIP). Models include Basenji, Enformer, Borzoi, and DNA language models (DNABERT, Nucleotide Transformer, HyenaDNA, Caduceus, Evo).
- **Single-cell foundation models**: pretrain on tens of millions of cells (Geneformer, scGPT, scFoundation, UCE), then fine-tune or probe for cell-type annotation, batch integration, perturbation response, or gene-network inference.
- **Function annotation**: predict GO terms, EC numbers, localization (CAFA benchmark), or protein-protein interactions.

## Deep mutational scanning and ProteinGym

**Deep mutational scanning (DMS)** builds a library containing nearly every single amino acid substitution of a protein (saturation mutagenesis), applies selection for a function (growth, binding, fluorescence, stability), and counts variants by sequencing before and after. The result is a fitness score for thousands of variants per protein.

**ProteinGym** (Notin et al., 2023) is the standard benchmark built on such data: **217 DMS substitution assays (~2.5M mutants)**, 66 indel assays, and clinical variant sets from ClinVar. Models are mostly evaluated **zero-shot**, without fitness labels, by checking whether model scores rank variants like the assay does. The headline metric is **Spearman's ρ** per assay, averaged across assays and grouped by function type (activity, binding, expression, organismal fitness, stability). Secondary metrics include AUC, MCC, NDCG and top-k recall. Average Spearman around 0.4–0.5 is typical of strong models, so the task is far from solved. Why Spearman? DMS scores come from different assays on different scales, often nonlinearly related to the underlying effect, so only rank order is comparable.

**Zero-shot scoring with a PLM**: the **masked marginal** score is log p(mutant aa | context) − log p(wild-type aa | context) at the masked position. Negative values mean the model finds the mutant less plausible. Autoregressive models use the log-likelihood ratio of whole sequences. The implicit assumption is that **evolutionary plausibility ≈ fitness**.

## What gets tokenized

- **Proteins**: usually **one token per amino acid** (vocabulary of ~20 plus special tokens; ESM-2, ProGen, ESM3). ESM3 adds structure tokens and function tokens. Sequence lengths reach a few hundred to ~1,000 residues, and long proteins are cropped.
- **DNA**: choices vary and matter.
  - **Single nucleotide**: HyenaDNA, Caduceus, Evo, and the one-hot inputs of Enformer/Borzoi.
  - **Overlapping k-mers**: DNABERT (3–6-mers). This leaks neighboring tokens under masking.
  - **Non-overlapping 6-mers**: Nucleotide Transformer.
  - **BPE**: DNABERT-2.
  Key issues are context length (enhancers can be ~100 kb away), reverse-complement equivariance (both strands are equivalent; Caduceus builds this in), and how much of the genome is repetitive or non-functional.
- **Genes as tokens (single-cell)**: a cell becomes a set or sequence of gene tokens. **Geneformer** uses **rank-value encoding**: genes are ordered by expression normalized against their corpus-wide level, and the expression values themselves are dropped. **scGPT** uses gene tokens plus **binned expression values**. The "sequence" has no natural order, the data are sparse, and batch effects are severe. Several papers have found that simple baselines (HVGs + PCA, linear models, or the mean expression of training perturbations) match or beat foundation models on some tasks. Read single-cell foundation model claims critically.

## Data splits and leakage

Biology data are full of near-duplicates: proteins have homologs, genomes have repeats and paralogs, and cells come from shared donors and batches. **Random splits overestimate generalization.**

- **Sequence identity clustering**: cluster all sequences with **MMseqs2** (`easy-cluster --min-seq-id 0.3`) or **CD-HIT** (CD-HIT's protein threshold bottoms out at 40%), then assign whole clusters to train or test. Common thresholds are 30%, 40%, 50% and 90% identity. Stricter is harder and more honest.
- **Fold/superfamily splits** (CATH/SCOP) for structure tasks; homologs can share a fold at <30% identity.
- **Temporal splits**: train on PDB structures released before a cutoff date and test on later ones (CASP-style). Pretraining on UniRef/PDB can still include test proteins' homologs.
- **Pretraining contamination**: a PLM pretrained on UniRef has seen the wild-type sequences of DMS proteins. That is usually accepted for zero-shot benchmarks, but it matters for claims of novelty.
- **Genomics**: hold out **entire chromosomes** (e.g., chr8/chr9 test sets in Basenji/Enformer). Even then, paralogous regions can leak.
- **Variant effect circularity**: ClinVar labels are partly informed by computational predictors, and well-studied genes are over-represented. Training on some variants of a gene and testing on others lets models learn per-gene priors (type 1/type 2 circularity, Grimm et al. 2015). Evaluate per gene, or hold out whole genes.
- **DMS**: random splits within one protein reveal positional effects. Use **position-based** or contiguous splits (ProteinGym's supervised track uses random, modulo and contiguous folds).
- **Single-cell**: split by donor, study or batch, not by cell. For perturbation prediction, hold out perturbations or cell types entirely.
- **PPI and drug-target**: hold out proteins, not pairs. A model can memorize that one partner is "sticky".

## Metrics glossary

- **Spearman ρ**: rank correlation. Standard for DMS and fitness.
- **AUROC / AUPRC**: classification (pathogenic vs benign). Use AUPRC when positives are rare.
- **Pearson r on log-counts**: genomics track prediction (Enformer reports correlation across tracks and genes).
- **lDDT / GDT_TS / TM-score / RMSD**: structure accuracy. DockQ for interfaces.
- **Precision@L** for contact prediction: precision of the top L predicted contacts, where L is sequence length. Long-range contacts (|i−j| ≥ 24) are the hard ones.
- **Perplexity**: language-model fit. Lower is better, but it is only loosely correlated with downstream usefulness.

## How to read one of these papers fast

1. Task and labels: DMS, ClinVar, structure, tracks, or cell types?
2. Pretraining corpus and its size (UniRef50 vs UniRef90, CELLxGENE, genomes of how many species).
3. Tokenization and context length.
4. Split strategy. Does it control for homology, chromosome, donor or gene?
5. Baselines. Is there a strong simple baseline (BLOSUM, conservation, mean prediction, PCA)?
6. Metric choice and aggregation (per-assay average vs pooled).

## How you'll see this in a paper

- "Average Spearman across 217 ProteinGym DMS assays": zero-shot fitness benchmark.
- "Clustered at 30% sequence identity with MMseqs2 to prevent leakage."
- "We evaluate on held-out chromosomes 8 and 9."
- "Rank-value encoding of the top 2,048 genes": Geneformer-style tokenization.
- "ipTM > 0.8 used as a filter for designed binders": structure confidence as a design oracle.
"""
cards = [
("recall","What is CASP?","Critical Assessment of protein Structure Prediction: biennial blind benchmark since 1994",["benchmarks","structure"]),
("recall","Main CASP accuracy metrics?","GDT_TS (and lDDT; TM-score; interface metrics for complexes)",["benchmarks","metrics"]),
("recall","What is deep mutational scanning?","Saturation mutagenesis library + functional selection + sequencing → fitness score per variant",["DMS"]),
("recall","What is ProteinGym?","Benchmark of DMS assays (217 substitution, 66 indel) plus clinical variants for fitness/variant-effect prediction",["benchmarks","DMS"]),
("recall","ProteinGym headline metric?","Spearman correlation per assay, averaged (grouped by function type)",["benchmarks","metrics"]),
("recall","Why Spearman rather than Pearson for DMS?","Assays use different, often nonlinear scales; only rank order is comparable",["metrics"]),
("recall","Zero-shot variant effect prediction means…?","Scoring variants without training on any fitness labels (e.g., PLM likelihoods)",["VEP"]),
("recall","Masked marginal score?","log p(mut aa) − log p(wt aa) at the masked position",["VEP","PLM"]),
("recall","Core assumption of zero-shot PLM fitness scoring?","Evolutionary plausibility (likelihood) correlates with fitness",["VEP"]),
("recall","Name three variant effect predictors.","EVE, ESM-1v, AlphaMissense (also GEMME, SIFT, PolyPhen-2, CADD)",["VEP"]),
("recall","Two main label sources for variant effect benchmarks?","DMS fitness scores and ClinVar clinical labels",["VEP"]),
("recall","Typical protein LM tokenization?","One token per amino acid (~20 + special tokens)",["tokenization"]),
("recall","DNABERT tokenization?","Overlapping k-mers (k = 3–6)",["tokenization","DNA"]),
("recall","Nucleotide Transformer tokenization?","Non-overlapping 6-mers",["tokenization","DNA"]),
("recall","DNABERT-2 tokenization?","Byte-pair encoding (BPE)",["tokenization","DNA"]),
("recall","Name DNA models using single-nucleotide resolution.","HyenaDNA, Caduceus, Evo (and one-hot Enformer/Borzoi)",["tokenization","DNA"]),
("recall","Problem with masking overlapping k-mers?","Neighboring tokens share bases, so the masked token leaks from context",["tokenization","DNA"]),
("recall","What is reverse-complement equivariance and why care?","Both DNA strands carry the same information; models should give consistent predictions for a sequence and its reverse complement",["DNA"]),
("recall","Geneformer input encoding?","Rank-value encoding: genes ordered by expression normalized to corpus-wide levels; values discarded",["tokenization","single-cell"]),
("recall","scGPT input encoding?","Gene tokens plus binned expression value tokens",["tokenization","single-cell"]),
("recall","Common critique of single-cell foundation models?","Simple baselines (HVG+PCA, linear/mean models) often match them on several tasks",["single-cell"]),
("recall","Why do random splits overestimate performance on proteins?","Homologous near-duplicates land in both train and test",["splits"]),
("recall","Tools for sequence identity clustering?","MMseqs2 (easy-cluster/linclust), CD-HIT",["splits","tools"]),
("recall","Lowest protein identity threshold supported by CD-HIT?","~40% (use MMseqs2 or PSI-CD-HIT for lower)",["splits","tools"]),
("recall","Common identity thresholds for train/test separation?","30%, 40%, 50%, 90%; lower = stricter",["splits"]),
("recall","Fold-level split?","Hold out whole CATH/SCOP folds or superfamilies, since homologs can share folds below 30% identity",["splits"]),
("recall","Temporal split in structure prediction?","Train on PDB entries before a date cutoff, test on later ones",["splits"]),
("recall","Standard genomics split?","Hold out entire chromosomes (e.g., chr8/9 test)",["splits","DNA"]),
("recall","What is circularity in variant effect evaluation?","Labels or gene-level priors shared between training and test (e.g., ClinVar labels influenced by predictors; same genes in train/test)",["splits","VEP"]),
("recall","How should single-cell data be split?","By donor, study or batch (not by cell); hold out perturbations for perturbation tasks",["splits","single-cell"]),
("recall","How should PPI data be split?","Hold out proteins (not just pairs) to avoid memorizing promiscuous partners",["splits"]),
("recall","Within-protein DMS split that avoids position leakage?","Position-based (modulo) or contiguous-region splits",["splits","DMS"]),
("recall","When prefer AUPRC over AUROC?","When positives are rare (class imbalance)",["metrics"]),
("recall","Precision@L for contact prediction?","Precision of top-L predicted contacts (L = sequence length), usually long-range (|i−j|≥24)",["metrics"]),
("recall","Perplexity in PLM papers?","exp(mean negative log-likelihood); lower = better fit, only loosely tied to downstream utility",["metrics"]),
("recall","What is inverse folding?","Predicting a sequence that folds into a given backbone (e.g., ProteinMPNN)",["design"]),
("recall","What is CAFA?","Critical Assessment of Functional Annotation: protein function (GO) prediction benchmark",["benchmarks"]),
("recall","What does Enformer predict?","Thousands of functional genomic tracks (CAGE, DNase, ChIP) from ~200 kb of DNA sequence",["genomics-models"]),
("apply","A paper splits a PLM fine-tuning set randomly and reports 0.95 accuracy. First concern?","Homology leakage: re-split by sequence identity clusters",["splits"]),
("apply","A VEP trained on ClinVar variants from BRCA1 is tested on other BRCA1 ClinVar variants. Issue?","Gene-level circularity: the model can learn a per-gene pathogenicity prior",["splits","VEP"]),
("apply","Model A has higher perplexity than B but better ProteinGym Spearman. Contradiction?","No: perplexity and fitness correlation are only loosely related",["metrics"]),
("apply","A single-cell perturbation model beats a 'no change' baseline. Is that enough?","No: also compare against the mean-of-training-perturbations and linear baselines",["single-cell"]),
]
quiz = [
("The primary ProteinGym DMS metric is:",["AUROC","Spearman's rank correlation","RMSD","Perplexity"],1,"Rank correlation between model scores and assay fitness, averaged across assays."),
("Why are protein datasets clustered by sequence identity before splitting?",["To speed up training","To prevent homologous sequences from appearing in both train and test","To balance amino acid composition","To remove disordered regions"],1,"Homology leakage inflates test performance."),
("Which DNA model uses non-overlapping 6-mer tokens?",["DNABERT","Nucleotide Transformer","HyenaDNA","Enformer"],1,"Nucleotide Transformer uses 6-mers; DNABERT uses overlapping k-mers; HyenaDNA uses single nucleotides."),
("Geneformer represents a cell as:",["A one-hot DNA sequence","Genes ranked by normalized expression","A protein sequence","A k-mer count vector"],1,"Rank-value encoding orders genes by expression relative to corpus-wide levels."),
("A masked-marginal PLM score of −4 for a mutation means:",["The mutant is more likely than wild type","The mutant is much less likely than wild type","The position is disordered","The mutation is synonymous"],1,"log p(mut) − log p(wt) < 0 means the model disfavors the mutant."),
("Standard split strategy in sequence-to-expression genomics models:",["Random 1-kb windows","Held-out chromosomes","Held-out nucleotides","Held-out reads"],1,"Entire chromosomes are held out to reduce leakage between nearby regions."),
("CASP is best described as:",["A continuous benchmark of DMS assays","A biennial blind structure prediction assessment","A clinical variant database","A single-cell atlas"],1,"Since 1994, held every two years with unreleased structures."),
("Which tool is commonly used to cluster sequences at 30% identity?",["CD-HIT (default settings)","MMseqs2","BLAST2GO","STAR"],1,"MMseqs2 handles low thresholds; CD-HIT's protein mode bottoms out around 40%."),
("For a pathogenic vs benign classifier where only 2% of variants are pathogenic, the more informative metric is:",["Accuracy","AUPRC","Perplexity","RMSD"],1,"AUPRC is sensitive to performance on the rare positive class."),
("Which split best tests generalization of a single-cell model to new people?",["Random cells","Held-out donors","Held-out genes","Held-out UMIs"],1,"Cells from the same donor share genotype and batch effects."),
("Overlapping k-mer tokenization causes a problem in masked language modeling because:",["Vocabulary is too small","Masked tokens can be inferred from overlapping neighbors","It ignores the reverse strand","It requires MSAs"],1,"Neighbors share k−1 bases with the masked token."),
("A deep mutational scan measures:",["Protein structure at atomic resolution","Functional effects of many variants of one protein in parallel","Gene expression across tissues","Chromatin accessibility"],1,"A variant library is selected for function and counted by sequencing."),
("Which is an inverse folding model?",["ProteinMPNN","Enformer","Geneformer","SpliceAI"],0,"ProteinMPNN designs sequences for a given backbone."),
("A 'temporal split' for a structure model means:",["Splitting by protein length","Testing on structures released after the training cutoff date","Splitting by organism","Splitting by resolution"],1,"Mimics CASP's prospective evaluation."),
]
build(7,"ml-for-biology","Reading ML-for-biology papers","How to decode the tasks, benchmarks (CASP, ProteinGym/DMS, ClinVar), tokenization choices for proteins, DNA and single cells, leakage-aware data splits, and evaluation metrics in ML-for-biology papers, plus a checklist for reading one quickly.",lesson,cards,quiz)
