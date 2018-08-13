#Multiple factor EdgeR analysis
#James T. Taylor, Jr 2018
setwd("C:/Users/jimta/Desktop/")
library(edgeR)
library(readxl)
path_to_phenotypes = "C:/Users/jimta/Desktop/jim_ballgown/pheno_data.csv"

counts <- read.csv(file="transcript_count_matrix.csv", header=TRUE, sep=",") #Then create the count matrix using read.csv()
cmat <- counts[ , -c(1,ncol(counts)) ] #format the data
rownames(cmat) <- counts[ , 1 ] # add gene names to new object
libsize <- colSums(cmat) # calculate library size in each sample
libmr <- libsize/1e06 #library size in millions of reads
cmat <- cmat[rowSums(cmat > 10) >= 3,] #keep only those rows where there are at least 10 counts in at least 3 samples
sample.description <- data.frame(sample=colnames(cmat))
genotype=regmatches(colnames(cmat),regexpr("fungus|fungus_and_maize",colnames(cmat))) #define genotypes for each column
treatment=regmatches(colnames(cmat),regexpr("6|12|15|24|36",colnames(cmat))) #define treatment variable for each column

#time to build the object for edgeR
batches <- genotype
conditions <- treatment

#The pipeline could look like this:
dge <- DGEList(cmat, group = batches ) # Create object
dge <- calcNormFactors(dge, method='TMM') # Normalize library sizes using TMM
dge <- dge[rowSums(1e+06 * dge$counts/expandAsMatrix(dge$samples$lib.size, dim(dge)) > 1) >= 6, ] #keep only those genes that have at least 1 read per million in at least 6 samples.

targets <- read.csv(file = path_to_phenotypes,sep = ',')

Group <- factor(paste(targets$treatment,targets$time,sep = '.'))
targets <- cbind(targets,Group=Group)

design <- model.matrix(~0+Group)
colnames(design) <- levels(Group)
dge <- estimateGLMCommonDisp(dge, design) # Estimate common dispersion
dge <- estimateGLMTrendedDisp(dge,design) #Estimate Trended dispersion
dge <- estimateGLMTagwiseDisp(dge, design)

my.contrasts <- makeContrasts(
  fungus6hvs.maize6h = negative.6-positive.6,
  fungus12hvs.maize12h = negative.12-positive.12,
  fungus15hvs.maize15h = negative.15-positive.15,
  fungus24hvs.maize24h = negative.24-positive.24,
  fungus36hvs.maize36h = negative.36-positive.36,
  maize12hvs.maize6h = positive.12-positive.6,
  maize15hvs.maize12h = positive.15-positive.12,
  maize24hvs.maize15h = positive.24-positive.15,
  maize36hvs.maize24h = positive.36-positive.24,
  fungus12hvs.fungus6h = negative.12-negative.6,
  fungus15hvs.fungus12h = negative.15-negative.12,
  fungus24hvs.fungus15h = negative.24-negative.15,
  fungus36hvs.fungus24h = negative.36-negative.24,
  levels=design
  
)


fit <- glmQLFit(dge, design)
lrt <- glmLRT(fit,contrast=my.contrasts)
out <- topTags(lrt,n=Inf)
mart_export <-read_excel("C:/Users/jimta/Downloads/mart_export.xls")
out$table$JGI <- mart_export$GeneID[match(row.names(out$table),mart_export$transcriptNames)]
#import signalp data from jgi
signalp <- read.delim("C:/Users/jimta/Downloads/Tvirens_v2.signalp_FrozenGeneCatalog_20100318.tab")

#fix gene numbers so they match current format
signalp$proteinid <- paste("TRIVIDRAFT_",signalp$proteinid, sep="")
#add signalp data to results file
out$table$signalp <- signalp$hmm_signalpep_probability[match(out$table$JGI,signalp$proteinid)]

kogg <- read.delim("C:/Users/jimta/Downloads/Tvirens_v2.koginfo_FrozenGeneCatalog_20100318.tab")
goinfo <- read.delim("C:/Users/jimta/Downloads/Tvirens_v2.goinfo_FrozenGeneCatalog_20100318.tab") 
kogg$proteinId <- paste("TRIVIDRAFT_",kogg$proteinId,sep = "")
out$table$kogg <- kogg$kogdefline[match(out$table$JGI,kogg$proteinId)]
out$table$koggcat <- kogg$kogClass[match(out$table$JGI,kogg$proteinId)]
goinfo$proteinId <- paste("TRIVIDRAFT_",goinfo$proteinId,sep = "")
out$table$goinfo <- goinfo$goName[match(out$table$JGI,goinfo$proteinId)]


write.csv(out,file="edgeR_with_kog_unfiltered.csv")
