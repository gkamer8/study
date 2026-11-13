"""Regenerate every lesson figure into content/biology/figures/.
Run with a Python that has Pillow and numpy:  python3 build_all.py
(render.py additionally needs cairosvg and is only for visual checks)."""
import u1_figs, u2_figs, u3_figs, u4_figs, u5_figs, u6_figs, u7_figs
u1_figs.dna_strands(); u1_figs.codon_table(); u1_figs.reading_frames(); u1_figs.gene_structure(); u1_figs.splicing(); u1_figs.central_dogma(); u1_figs.karyotype()
u2_figs.hgvs(); u2_figs.c_numbering(); u2_figs.identifiers(); u2_figs.hla()
u3_figs.database_map(); u3_figs.geo_sra(); u3_figs.go_dag()
u4_figs.amino_acids(); u4_figs.structure_levels(); u4_figs.domains(); u4_figs.alphafold_p53(); u4_figs.msa()
u5_figs.mapk(); u5_figs.pi3k(); u5_figs.p53(); u5_figs.cell_cycle(); u5_figs.wnt()
u6_figs.fastq(); u6_figs.coordinates(); u6_figs.sam(); u6_figs.vcf(); u6_figs.workflows(); u6_figs.anndata()
u7_figs.splits(); u7_figs.tokenization(); u7_figs.masked_marginal()
print("ok")
