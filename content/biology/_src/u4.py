from common import build
lesson = r"""
## Reading a protein sequence

A protein is a chain of amino acids written N-terminus → C-terminus in **one-letter codes**. To read sequences, alignments and mutation notation (R175H, G12D), learn the 20 letters by chemical class:

| Class | Residues | Notes |
|---|---|---|
| Hydrophobic aliphatic | **A** Ala, **V** Val, **L** Leu, **I** Ile, **M** Met | Buried in the core, in TM helices |
| Aromatic | **F** Phe, **W** Trp, **Y** Tyr | W largest; Y can be phosphorylated |
| Polar uncharged | **S** Ser, **T** Thr, **N** Asn, **Q** Gln | S/T phosphorylated; N glycosylated |
| Positive (basic) | **K** Lys, **R** Arg, **H** His | H is ~neutral at pH 7, binds metals, common in active sites |
| Negative (acidic) | **D** Asp, **E** Glu | |
| Special | **G** Gly, **P** Pro, **C** Cys | G is flexible; P is rigid and breaks helices; C forms disulfides |

The letters that don't match the name are the ones to drill: **F** Phe, **Y** Tyr, **W** Trp, **K** Lys, **R** Arg, **D** Asp, **E** Glu, **N** Asn, **Q** Gln. In sequence files, **X** = unknown, **B** = D/N, **Z** = E/Q, **U** = selenocysteine, **O** = pyrrolysine, `*` = stop, `-` = alignment gap. Proteins usually start with M.

Biochemical intuition helps with variant effects. A substitution between similar residues (I→V) is usually mild. Charge reversals (E→K), proline in a helix, glycine replacements in tight turns, and loss of a buried hydrophobic residue are usually damaging. Substitution matrices like **BLOSUM62** encode these tendencies from observed alignments.

## Levels of structure

- **Primary**: the sequence.
- **Secondary**: local backbone hydrogen-bond patterns. In the **α-helix** (3.6 residues per turn), residue i bonds to i+4. **β-strands** pair into parallel or antiparallel **β-sheets**. Everything else is loops/coils. DSSP assigns these from coordinates.
- **Tertiary**: the 3D fold of one chain, driven largely by burying hydrophobic residues.
- **Quaternary**: assembly of multiple chains (hemoglobin is α2β2).

Many proteins have **intrinsically disordered regions (IDRs)** with no stable structure: transactivation domains, linkers, low-complexity sequence. p53's N-terminal transactivation domain is disordered while its DNA-binding core is folded.

## Domains

A **domain** is a compact, independently folding unit that often carries a function and recurs across proteins. Proteins are frequently mosaics: a receptor tyrosine kinase has an extracellular ligand-binding domain, one transmembrane helix, and an intracellular kinase domain. **Pfam** models domain families with profile HMMs (PF00069 = protein kinase domain). **InterPro** integrates Pfam with other signature databases (SMART, PROSITE, CATH-Gene3D, etc.) into entries like IPR000719. Structural classifications **CATH** and **SCOP** group domains by fold and are used to make fold-level train/test splits. Common named domains: SH2 (binds phosphotyrosine), SH3 (binds proline-rich motifs), PDZ, zinc finger, homeobox, immunoglobulin (Ig) fold.

## AlphaFold confidence: pLDDT and PAE

- **pLDDT** (predicted local distance difference test, 0–100) is per-residue confidence, stored in the B-factor column of AlphaFold PDB files. **>90** very high (side chains are often accurate). **70–90** confident (backbone is good). **50–70** low. **<50** very low, which often indicates disorder. Low-pLDDT regions look like floating spaghetti, and you should not interpret them as structure. Low pLDDT is itself a decent disorder predictor.
- **PAE** (predicted aligned error) is a matrix: the expected position error, in Å, of residue *x* when the prediction is aligned on residue *y*. Low-PAE blocks on the diagonal mark confidently placed domains. High PAE between two domains means their **relative orientation** is uncertain, even if each domain has high pLDDT.
- For complexes: **pTM** and **ipTM** (interface pTM). ipTM above ~0.8 suggests a confident interface; below ~0.6 suggests a likely failed one.
- Structure comparison metrics: **RMSD** (Å, sensitive to outliers), **TM-score** (0–1; >0.5 is generally the same fold), **GDT_TS** (CASP's classic metric), **lDDT** (superposition-free, local).

## MSAs and coevolution

A **multiple sequence alignment (MSA)** lines up homologous sequences, found by tools like JackHMMER, HHblits or MMseqs2 (ColabFold uses MMseqs2), so that each column is an equivalent position. Two signals matter:

1. **Conservation**: columns that never vary are functionally constrained, so mutations there are likely damaging. This is the basis of SIFT, EVE and others.
2. **Coevolution**: if residues i and j touch, a mutation at one is often compensated at the other, so the columns covary. Potts models / **direct coupling analysis (DCA)** extract these couplings to predict contacts. AlphaFold2's Evoformer learns this from the MSA. Protein language models such as **ESM-2** learn similar information implicitly from single sequences, which is why ESMFold works without an explicit MSA.

MSA depth (often quantified as **Neff**, the effective number of sequences) predicts accuracy. "Orphan" proteins with few homologs, and designed proteins, are hard for MSA-based methods.

## Families worth knowing

- **Protein kinases** (~500 in humans, the "kinome"): transfer phosphate from ATP to Ser/Thr or Tyr. They share a bilobed fold with the ATP pocket between the lobes, plus a conserved activation loop, DFG motif and gatekeeper residue. Most kinase drugs (imatinib, osimertinib) are ATP-competitive.
- **GPCRs** (~800 human genes): seven transmembrane helices. They signal through heterotrimeric G proteins (Gs, Gi, Gq) and arrestins. They are the target of roughly a third of approved drugs. Pfam 7tm_1 covers the rhodopsin-like class A, the largest group.
- **Ion channels**: pore-forming membrane proteins, such as voltage-gated Na⁺/K⁺/Ca²⁺ channels and ligand-gated channels.
- **Transcription factors** (~1,600 human): bind DNA motifs through DNA-binding domains (C2H2 zinc finger, the largest class; homeodomain; bHLH; bZIP; nuclear receptors; forkhead).
- **Antibodies (IgG)**: two heavy and two light chains joined by disulfides, Y-shaped. **Fab** arms bind antigen and the **Fc** stem engages immune effectors. Each variable domain (VH, VL) has three **complementarity-determining regions (CDRs)** on a framework. **CDR-H3** is the most diverse and usually dominates binding. Diversity comes from **V(D)J recombination** plus somatic hypermutation. Camelid **nanobodies (VHH)** are single-domain heavy-chain antibodies. Antibody language models (AbLang, AntiBERTy) train on OAS repertoire data.
- Others: proteases, E3 ubiquitin ligases, nuclear receptors, enzymes classified by **EC numbers** (EC 2.7.11.1 = a Ser/Thr kinase class).

## How you'll see this in a paper

- "Regions with pLDDT < 70 were masked": discarding low-confidence or disordered parts.
- "The predicted complex had ipTM 0.85": a confident interface prediction.
- "MSAs generated with ColabFold's MMseqs2 pipeline against UniRef30 and environmental databases."
- "ESM-2 650M embeddings, mean-pooled over residues": a per-protein representation from a PLM.
- "Mutations cluster in the kinase activation loop / DNA-binding domain": domain-level interpretation of variants.
"""
cards = [
("identify","One-letter code F","Phenylalanine (aromatic, hydrophobic)",["amino-acids"]),
("identify","One-letter code Y","Tyrosine (aromatic; phosphorylatable)",["amino-acids"]),
("identify","One-letter code W","Tryptophan (largest, aromatic)",["amino-acids"]),
("identify","One-letter code K","Lysine (positive; ubiquitination/acetylation site)",["amino-acids"]),
("identify","One-letter code R","Arginine (positive)",["amino-acids"]),
("identify","One-letter code D vs E","D = aspartate, E = glutamate (both negative)",["amino-acids"]),
("identify","One-letter code N vs Q","N = asparagine, Q = glutamine (polar uncharged)",["amino-acids"]),
("identify","One-letter code H","Histidine: near-neutral at pH 7, metal binding, catalytic sites",["amino-acids"]),
("recall","Which residues are positively charged at physiological pH?","K, R (H partially)",["amino-acids"]),
("recall","Which residues are negatively charged?","D, E",["amino-acids"]),
("recall","Hydrophobic aliphatic residues?","A, V, L, I, M",["amino-acids"]),
("recall","Why are G and P special?","G: no side chain, very flexible; P: cyclic, rigid, breaks helices",["amino-acids"]),
("identify","Sequence symbols X, U, *, -","Unknown residue; selenocysteine; stop; alignment gap",["amino-acids","formats"]),
("apply","Rank by likely severity: I→V, E→K in a buried salt bridge, L→P in a helix.","I→V mild; E→K and L→P likely damaging (charge reversal; helix breaker)",["variants","amino-acids"]),
("recall","What is BLOSUM62?","Amino acid substitution matrix derived from conserved blocks of aligned sequences",["alignment"]),
("cloze","An α-helix has ___ residues per turn; residue i H-bonds to residue i+___.","3.6; 4",["structure"]),
("recall","Parallel vs antiparallel β-sheet?","Strands run in the same vs opposite N→C direction",["structure"]),
("recall","Tertiary vs quaternary structure?","Tertiary: fold of one chain; quaternary: assembly of multiple chains",["structure"]),
("recall","What is an IDR?","Intrinsically disordered region: no stable 3D structure (e.g., p53 transactivation domain)",["structure"]),
("recall","What is a protein domain?","Compact, independently folding, often functional unit that recurs across proteins",["domains"]),
("recall","Pfam models domains using…?","Profile hidden Markov models (HMMs) built from seed alignments",["domains"]),
("identify","PF00069","Pfam family: protein kinase domain (Pkinase)",["domains","identifiers"]),
("identify","IPR000719","InterPro entry: protein kinase domain",["domains","identifiers"]),
("recall","CATH/SCOP are used in ML for…?","Structural classifications (by fold) used for fold-level train/test splits",["domains","ml"]),
("recall","SH2 domains bind…?","Phosphotyrosine-containing motifs",["domains","signaling"]),
("recall","What is pLDDT?","AlphaFold per-residue confidence (0–100), stored in the B-factor column",["AlphaFold"]),
("recall","pLDDT bands?",">90 very high; 70–90 confident; 50–70 low; <50 very low (often disordered)",["AlphaFold"]),
("recall","What is PAE?","Predicted aligned error: expected error (Å) at residue x when aligned on residue y; a matrix",["AlphaFold"]),
("apply","Two domains each have pLDDT >90 but the PAE between them is ~25 Å. Interpretation?","Each domain is confident, but their relative orientation is not",["AlphaFold"]),
("recall","What is ipTM?","Interface predicted TM-score for complexes; >~0.8 confident, <~0.6 likely wrong",["AlphaFold"]),
("recall","TM-score threshold for 'same fold'?","> 0.5",["metrics"]),
("recall","Why is lDDT preferred over RMSD for some comparisons?","Superposition-free and local, so not dominated by domain-motion outliers",["metrics"]),
("recall","Two signals extracted from an MSA?","Conservation (constrained positions) and coevolution (covarying positions ≈ contacts)",["MSA"]),
("recall","Why do coevolving columns suggest a contact?","Mutation at one residue is compensated at a touching partner, so columns covary",["MSA"]),
("recall","What is DCA?","Direct coupling analysis: Potts model that separates direct couplings from transitive correlations to predict contacts",["MSA"]),
("recall","What is Neff?","Effective number of (reweighted, non-redundant) sequences in an MSA; low Neff → harder prediction",["MSA"]),
("recall","Which search tool does ColabFold use to build MSAs?","MMseqs2",["MSA","tools"]),
("recall","Why can ESMFold skip MSAs?","ESM-2 learned evolutionary/coevolutionary information implicitly during pretraining",["ml"]),
("recall","What do protein kinases do?","Transfer γ-phosphate from ATP to Ser/Thr or Tyr on substrates",["families"]),
("recall","Approximate size of the human kinome?","~500 protein kinases (~518 in Manning et al. 2002)",["families"]),
("recall","Most kinase inhibitor drugs bind where?","ATP-binding pocket (ATP-competitive)",["families","drugs"]),
("recall","GPCR defining feature?","Seven transmembrane helices; signal via heterotrimeric G proteins and arrestins",["families"]),
("recall","Roughly what fraction of approved drugs target GPCRs?","About one third",["families","drugs"]),
("recall","Largest human TF DNA-binding domain class?","C2H2 zinc finger",["families"]),
("recall","IgG structure?","2 heavy + 2 light chains; Fab (antigen binding) and Fc (effector) regions",["antibodies"]),
("recall","What are CDRs, and which is most diverse?","Complementarity-determining regions (3 per variable domain); CDR-H3 most diverse",["antibodies"]),
("recall","Sources of antibody diversity?","V(D)J recombination, junctional diversity, somatic hypermutation",["antibodies"]),
("recall","What is a nanobody?","Single-domain camelid heavy-chain antibody fragment (VHH)",["antibodies"]),
("recall","Which database holds antibody repertoire sequences used to train antibody LMs?","OAS (Observed Antibody Space)",["antibodies","ml"]),
]
quiz = [
("In a sequence, which letter denotes lysine?",["L","K","Y","I"],1,"K = Lys; L = Leu, Y = Tyr, I = Ile."),
("A residue with pLDDT 42 in an AlphaFold model most likely:",["Is highly accurate","Lies in a disordered or unconfident region","Is a catalytic residue","Is in a β-sheet"],1,"pLDDT < 50 is very low confidence, often indicating disorder."),
("PAE between two domains is high while each domain's pLDDT is high. Conclusion?",["Both domains are wrong","Relative placement of the domains is uncertain","The protein is disordered","The MSA was empty"],1,"PAE reports inter-residue positional confidence, so it captures domain orientation."),
("Which residue is most likely to disrupt an α-helix if introduced?",["Alanine","Leucine","Proline","Glutamate"],2,"Proline's ring constrains the backbone and lacks an amide H, breaking helices."),
("Coevolution in an MSA is mainly used to infer:",["Expression level","Residue-residue contacts","Post-translational modifications","Subcellular location"],1,"Covarying positions tend to be in spatial contact."),
("Which amino acids can be phosphorylated by protein kinases?",["S, T, Y","K, R, H","D, E","G, P, C"],0,"Ser/Thr kinases and Tyr kinases."),
("Which family has seven transmembrane helices?",["Receptor tyrosine kinases","GPCRs","Nuclear receptors","Immunoglobulins"],1,"GPCRs = 7TM receptors."),
("The antibody region most responsible for antigen-binding diversity is:",["Fc","CDR-H3","Hinge","Constant light domain"],1,"CDR-H3 is the most variable loop and usually central to binding."),
("A TM-score of 0.3 between a prediction and the true structure suggests:",["Same fold","Different fold / largely incorrect","Atomic accuracy","Identical sequence"],1,"TM-score > 0.5 generally indicates the same fold; ~0.3 is close to random."),
("Pfam represents protein families primarily as:",["3D structures","Profile HMMs","Pathway diagrams","k-mer counts"],1,"Pfam builds profile HMMs from curated seed alignments."),
("Which is a sign that a protein will be hard for MSA-based structure prediction?",["Many homologs","Low Neff / few homologs","High pLDDT","Presence of a kinase domain"],1,"Shallow MSAs provide little coevolutionary signal."),
("Which pair is both negatively charged?",["K and R","D and E","N and Q","S and T"],1,"Aspartate (D) and glutamate (E) are acidic."),
("Where are pLDDT values stored in AlphaFold PDB files?",["Occupancy column","B-factor column","Header remarks only","Chain ID"],1,"AlphaFold writes pLDDT into the B-factor field."),
("Most clinically used kinase inhibitors are:",["Allosteric activators","ATP-competitive","Covalent DNA binders","GPCR agonists"],1,"Most target the ATP pocket; some are covalent (e.g., osimertinib binds Cys797) but still in the ATP site."),
]
build(4,"proteins","Proteins: sequence, structure, families","Amino acid one-letter codes by chemistry, levels of protein structure, domains and the databases that catalog them, AlphaFold confidence metrics (pLDDT, PAE, ipTM), MSAs and coevolution, and the protein families you'll meet most often in papers.",lesson,cards,quiz)
