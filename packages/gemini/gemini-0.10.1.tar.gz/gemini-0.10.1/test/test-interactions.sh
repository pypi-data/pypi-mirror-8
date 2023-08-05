######################################################################
# 1. Test interaction tool for snpEff (v3.1) annotations
######################################################################
echo "    interact.t01...\c"
echo "sample	gene	order_of_interaction	interacting_gene
M10475	CTBP2	0_order:	none
M10475	CTBP2	1_order:	RAI2
M10475	CTBP2	2_order:	SGTB,UBQLN4
M10475	CTBP2	3_order:	none
M10475	CTBP2	4_order:	WDR37
M10475	CTBP2	5_order:	none
M128215	CTBP2	0_order:	CTBP2
M128215	CTBP2	1_order:	RAI2
M128215	CTBP2	2_order:	RB1
M128215	CTBP2	3_order:	TGM2,NOTCH2NL
M128215	CTBP2	4_order:	WDR37
M128215	CTBP2	5_order:	none
M10478	CTBP2	0_order:	none
M10478	CTBP2	1_order:	RAI2
M10478	CTBP2	2_order:	SGTB,UBQLN4
M10478	CTBP2	3_order:	NOTCH2NL
M10478	CTBP2	4_order:	WDR37
M10478	CTBP2	5_order:	MTG1
M10500	CTBP2	0_order:	none
M10500	CTBP2	1_order:	RAI2
M10500	CTBP2	2_order:	RB1,UBQLN4
M10500	CTBP2	3_order:	NOTCH2NL
M10500	CTBP2	4_order:	WDR37
M10500	CTBP2	5_order:	MTG1" > exp
gemini interactions -g CTBP2 -r 5 test5.snpeff.db \
       > obs
check obs exp
rm obs exp

######################################################################
# 2. Test interaction tool for snpEff (v3.1) annotations (--var mode)
######################################################################
echo "    interact.t02...\c"
echo "sample	gene	order_of_interaction	interacting_gene	var_id	chrom	start	end	impact	biotype	in_dbsnp	clinvar_sig	clinvar_disease_name	aaf_1kg_all	aaf_esp_all
M10475	CTBP2	1	RAI2	9	chrX	17819376	17819377	non_syn_coding	protein_coding	1	None	None	1	0.999526649626
M10475	CTBP2	2	UBQLN4	2	chr1	156011443	156011444	non_syn_coding	protein_coding	1	None	None	0.42	0.553401046476
M10475	CTBP2	2	SGTB	8	chr5	64982320	64982321	intron	protein_coding	1	None	None	0.57	None
M10475	CTBP2	4	WDR37	3	chr10	1142207	1142208	stop_loss	protein_coding	1	None	None	0.99	0.991234814701
M128215	CTBP2	0	CTBP2	4	chr10	126678091	126678092	stop_gain	protein_coding	1	None	None	None	None
M128215	CTBP2	1	RAI2	9	chrX	17819376	17819377	non_syn_coding	protein_coding	1	None	None	1	0.999526649626
M128215	CTBP2	2	RB1	6	chr13	48873834	48873835	upstream	protein_coding	1	None	None	0.94	None
M128215	CTBP2	3	NOTCH2NL	1	chr1	145273344	145273345	non_syn_coding	protein_coding	1	None	None	None	None
M128215	CTBP2	3	TGM2	7	chr20	36779423	36779424	stop_gain	protein_coding	0	None	None	None	None
M128215	CTBP2	4	WDR37	3	chr10	1142207	1142208	stop_loss	protein_coding	1	None	None	0.99	0.991234814701
M10478	CTBP2	1	RAI2	9	chrX	17819376	17819377	non_syn_coding	protein_coding	1	None	None	1	0.999526649626
M10478	CTBP2	2	UBQLN4	2	chr1	156011443	156011444	non_syn_coding	protein_coding	1	None	None	0.42	0.553401046476
M10478	CTBP2	2	SGTB	8	chr5	64982320	64982321	intron	protein_coding	1	None	None	0.57	None
M10478	CTBP2	3	NOTCH2NL	1	chr1	145273344	145273345	non_syn_coding	protein_coding	1	None	None	None	None
M10478	CTBP2	4	WDR37	3	chr10	1142207	1142208	stop_loss	protein_coding	1	None	None	0.99	0.991234814701
M10478	CTBP2	5	MTG1	5	chr10	135210790	135210791	intron	protein_coding	1	None	None	0.52	None
M10500	CTBP2	1	RAI2	9	chrX	17819376	17819377	non_syn_coding	protein_coding	1	None	None	1	0.999526649626
M10500	CTBP2	2	UBQLN4	2	chr1	156011443	156011444	non_syn_coding	protein_coding	1	None	None	0.42	0.553401046476
M10500	CTBP2	2	RB1	6	chr13	48873834	48873835	upstream	protein_coding	1	None	None	0.94	None
M10500	CTBP2	3	NOTCH2NL	1	chr1	145273344	145273345	non_syn_coding	protein_coding	1	None	None	None	None
M10500	CTBP2	4	WDR37	3	chr10	1142207	1142208	stop_loss	protein_coding	1	None	None	0.99	0.991234814701
M10500	CTBP2	5	MTG1	5	chr10	135210790	135210791	intron	protein_coding	1	None	None	0.52	None" > exp
gemini interactions -g CTBP2 -r 5 --var test5.snpeff.db \
       > obs
check obs exp
rm obs exp

######################################################################
# 3. Test lof interaction tool for snpEff (v3.1) annotations
######################################################################
echo "    interact.t03...\c"
echo "sample	lof_gene	order_of_interaction	interacting_gene
M10475	WDR37	1_order:	none
M10475	WDR37	2_order:	none
M10475	WDR37	3_order:	UBQLN4
M128215	WDR37	1_order:	none
M128215	WDR37	2_order:	none
M128215	WDR37	3_order:	RB1
M128215	TGM2	1_order:	RB1
M128215	TGM2	2_order:	none
M128215	TGM2	3_order:	NOTCH2NL,CTBP2
M128215	CTBP2	1_order:	RAI2
M128215	CTBP2	2_order:	RB1
M128215	CTBP2	3_order:	NOTCH2NL,TGM2
M10478	WDR37	1_order:	none
M10478	WDR37	2_order:	none
M10478	WDR37	3_order:	UBQLN4
M10500	WDR37	1_order:	none
M10500	WDR37	2_order:	none
M10500	WDR37	3_order:	RB1,UBQLN4" > exp
gemini lof_interactions -r 3 test5.snpeff.db \
       > obs
check obs exp
rm obs exp

######################################################################
# 4. Test lof_interactions (--var mode) for snpEff (v3.1) annotations
######################################################################
echo "    interact.t04...\c"
echo "sample	lof_gene	order_of_interaction	interacting_gene	var_id	chrom	start	end	impact	biotype	in_dbsnp	clinvar_sig	clinvar_disease_name	aaf_1kg_all	aaf_esp_all
M10475	WDR37	3	UBQLN4	2	chr1	156011443	156011444	non_syn_coding	protein_coding	1	None	None	0.42	0.553401046476
M128215	WDR37	3	RB1	6	chr13	48873834	48873835	upstream	protein_coding	1	None	None	0.94	None
M128215	TGM2	1	RB1	6	chr13	48873834	48873835	upstream	protein_coding	1	None	None	0.94	None
M128215	TGM2	3	NOTCH2NL	1	chr1	145273344	145273345	non_syn_coding	protein_coding	1	None	None	None	None
M128215	TGM2	3	CTBP2	4	chr10	126678091	126678092	stop_gain	protein_coding	1	None	None	None	None
M128215	CTBP2	1	RAI2	9	chrX	17819376	17819377	non_syn_coding	protein_coding	1	None	None	1	0.999526649626
M128215	CTBP2	2	RB1	6	chr13	48873834	48873835	upstream	protein_coding	1	None	None	0.94	None
M128215	CTBP2	3	NOTCH2NL	1	chr1	145273344	145273345	non_syn_coding	protein_coding	1	None	None	None	None
M128215	CTBP2	3	TGM2	7	chr20	36779423	36779424	stop_gain	protein_coding	0	None	None	None	None
M10478	WDR37	3	UBQLN4	2	chr1	156011443	156011444	non_syn_coding	protein_coding	1	None	None	0.42	0.553401046476
M10500	WDR37	3	UBQLN4	2	chr1	156011443	156011444	non_syn_coding	protein_coding	1	None	None	0.42	0.553401046476
M10500	WDR37	3	RB1	6	chr13	48873834	48873835	upstream	protein_coding	1	None	None	0.94	None" > exp
gemini lof_interactions -r 3 --var test5.snpeff.db \
> obs
check obs exp
rm obs exp
 
######################################################################
# 5. Test interaction tool for VEP (75) annotations
######################################################################
echo "    interact.t05...\c"
echo "sample	gene	order_of_interaction	interacting_gene
M10475	SGTB	0_order:	SGTB
M10475	SGTB	1_order:	RAI2
M10475	SGTB	2_order:	UBQLN4
M10475	SGTB	3_order:	none
M10475	SGTB	4_order:	WDR37
M128215	SGTB	0_order:	none
M128215	SGTB	1_order:	RAI2
M128215	SGTB	2_order:	CTBP2,RB1
M128215	SGTB	3_order:	TGM2,NOTCH2NL
M128215	SGTB	4_order:	WDR37
M10478	SGTB	0_order:	SGTB
M10478	SGTB	1_order:	RAI2
M10478	SGTB	2_order:	UBQLN4
M10478	SGTB	3_order:	NOTCH2NL
M10478	SGTB	4_order:	WDR37
M10500	SGTB	0_order:	none
M10500	SGTB	1_order:	RAI2
M10500	SGTB	2_order:	RB1,UBQLN4
M10500	SGTB	3_order:	NOTCH2NL
M10500	SGTB	4_order:	WDR37" > exp
gemini interactions -g SGTB -r 4 test5.vep.db \
       > obs
check obs exp
rm obs exp 

####################################################################
# 6. Test interaction tool (--var mode) for VEP (75) annotations
######################################################################
echo "    interact.t06...\c"
echo "sample	gene	order_of_interaction	interacting_gene	var_id	chrom	start	end	impact	biotype	in_dbsnp	clinvar_sig	clinvar_disease_name	aaf_1kg_all	aaf_esp_all
M10475	SGTB	0	SGTB	8	chr5	64982320	64982321	intron	protein_coding	1	None	None	0.57	None
M10475	SGTB	1	RAI2	9	chrX	17819376	17819377	non_syn_coding	protein_coding	1	None	None	1	0.999526649626
M10475	SGTB	2	UBQLN4	2	chr1	156011443	156011444	non_syn_coding	protein_coding	1	None	None	0.42	0.553401046476
M10475	SGTB	4	WDR37	3	chr10	1142207	1142208	stop_loss	protein_coding	1	None	None	0.99	0.991234814701
M128215	SGTB	1	RAI2	9	chrX	17819376	17819377	non_syn_coding	protein_coding	1	None	None	1	0.999526649626
M128215	SGTB	2	CTBP2	4	chr10	126678091	126678092	stop_gain	protein_coding	1	None	None	None	None
M128215	SGTB	2	RB1	6	chr13	48873834	48873835	upstream	protein_coding	1	None	None	0.94	None
M128215	SGTB	3	NOTCH2NL	1	chr1	145273344	145273345	non_syn_coding	protein_coding	1	None	None	None	None
M128215	SGTB	3	TGM2	7	chr20	36779423	36779424	stop_gain	protein_coding	0	None	None	None	None
M128215	SGTB	4	WDR37	3	chr10	1142207	1142208	stop_loss	protein_coding	1	None	None	0.99	0.991234814701
M10478	SGTB	0	SGTB	8	chr5	64982320	64982321	intron	protein_coding	1	None	None	0.57	None
M10478	SGTB	1	RAI2	9	chrX	17819376	17819377	non_syn_coding	protein_coding	1	None	None	1	0.999526649626
M10478	SGTB	2	UBQLN4	2	chr1	156011443	156011444	non_syn_coding	protein_coding	1	None	None	0.42	0.553401046476
M10478	SGTB	3	NOTCH2NL	1	chr1	145273344	145273345	non_syn_coding	protein_coding	1	None	None	None	None
M10478	SGTB	4	WDR37	3	chr10	1142207	1142208	stop_loss	protein_coding	1	None	None	0.99	0.991234814701
M10500	SGTB	1	RAI2	9	chrX	17819376	17819377	non_syn_coding	protein_coding	1	None	None	1	0.999526649626
M10500	SGTB	2	UBQLN4	2	chr1	156011443	156011444	non_syn_coding	protein_coding	1	None	None	0.42	0.553401046476
M10500	SGTB	2	RB1	6	chr13	48873834	48873835	upstream	protein_coding	1	None	None	0.94	None
M10500	SGTB	3	NOTCH2NL	1	chr1	145273344	145273345	non_syn_coding	protein_coding	1	None	None	None	None
M10500	SGTB	4	WDR37	3	chr10	1142207	1142208	stop_loss	protein_coding	1	None	None	0.99	0.991234814701" > exp
gemini interactions -g SGTB -r 4 --var test5.vep.db \
       > obs
check obs exp
rm obs exp

######################################################################
# 7. Test lof_interactions for VEP (75) annotations
######################################################################
echo "    interact.t07...\c"
echo "sample	lof_gene	order_of_interaction	interacting_gene
M10475	WDR37	1_order:	none
M10475	WDR37	2_order:	none
M10475	WDR37	3_order:	UBQLN4
M128215	WDR37	1_order:	none
M128215	WDR37	2_order:	none
M128215	WDR37	3_order:	RB1
M128215	TGM2	1_order:	RB1
M128215	TGM2	2_order:	none
M128215	TGM2	3_order:	NOTCH2NL,CTBP2
M128215	CTBP2	1_order:	RAI2
M128215	CTBP2	2_order:	RB1
M128215	CTBP2	3_order:	NOTCH2NL,TGM2
M10478	WDR37	1_order:	none
M10478	WDR37	2_order:	none
M10478	WDR37	3_order:	UBQLN4
M10500	WDR37	1_order:	none
M10500	WDR37	2_order:	none
M10500	WDR37	3_order:	RB1,UBQLN4" > exp
gemini lof_interactions -r 3 test5.vep.db \
       > obs
check obs exp
rm obs exp

######################################################################
# 8. Test lof_interactions (--var mode) for VEP (75) annotations
######################################################################
echo "    interact.t08...\c"
echo "sample	lof_gene	order_of_interaction	interacting_gene	var_id	chrom	start	end	impact	biotype	in_dbsnp	clinvar_sig	clinvar_disease_name	aaf_1kg_all	aaf_esp_all
M10475	WDR37	3	UBQLN4	2	chr1	156011443	156011444	non_syn_coding	protein_coding	1	None	None	0.42	0.553401046476
M128215	WDR37	3	RB1	6	chr13	48873834	48873835	upstream	protein_coding	1	None	None	0.94	None
M128215	TGM2	1	RB1	6	chr13	48873834	48873835	upstream	protein_coding	1	None	None	0.94	None
M128215	TGM2	3	NOTCH2NL	1	chr1	145273344	145273345	non_syn_coding	protein_coding	1	None	None	None	None
M128215	TGM2	3	CTBP2	4	chr10	126678091	126678092	stop_gain	protein_coding	1	None	None	None	None
M128215	CTBP2	1	RAI2	9	chrX	17819376	17819377	non_syn_coding	protein_coding	1	None	None	1	0.999526649626
M128215	CTBP2	2	RB1	6	chr13	48873834	48873835	upstream	protein_coding	1	None	None	0.94	None
M128215	CTBP2	3	NOTCH2NL	1	chr1	145273344	145273345	non_syn_coding	protein_coding	1	None	None	None	None
M128215	CTBP2	3	TGM2	7	chr20	36779423	36779424	stop_gain	protein_coding	0	None	None	None	None
M10478	WDR37	3	UBQLN4	2	chr1	156011443	156011444	non_syn_coding	protein_coding	1	None	None	0.42	0.553401046476
M10500	WDR37	3	UBQLN4	2	chr1	156011443	156011444	non_syn_coding	protein_coding	1	None	None	0.42	0.553401046476
M10500	WDR37	3	RB1	6	chr13	48873834	48873835	upstream	protein_coding	1	None	None	0.94	None" > exp
gemini lof_interactions -r 3 --var test5.vep.db \
       > obs
check obs exp
rm obs exp

######################################################################




