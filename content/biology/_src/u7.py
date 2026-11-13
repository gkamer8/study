from common import build
import os
lesson = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"lessons","u7.md")).read()
from cards_u7 import cards
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
