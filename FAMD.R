library(FactoMineR)
rm(list = ls())
setwd("~/Desktop/lst data")
files <- list.files()

spearman = c()
for (id in files){
  data <- read.csv(id,header = T)[,-1]
  dims <- dim(data)
  if (dims[1] > 5){
    data$stress = factor(data$stress)
    data$alcohol = factor(data$alcohol)
    data$sleepquality = factor(data$sleepquality)
    j = 1
    data <- na.omit(data)
    for (i in data$sports){
      if (i == 1){
        data$sports[j] <- 0
      }else{
        data$sports[j] <- 1
      }
      j = j + 1
    }
    data$sports = factor(data$sports)
    data$bluelight = factor(data$bluelight)
    res <- FAMD(base = data, ncp = dims[2])
    mypath <- paste("/Users/kasperipalkama/Desktop/lst figs/plot_", id,".png", sep = "")
    png(file=mypath)
    # print('saved')
    plot(res,choix = 'var',habillage = 4,title = id)
    dev.off()
    data$sleepquality = as.numeric(data$sleepquality)
    if (dims[2] >6){
      print(id)
      corr_spear <- cor.test(x = as.numeric(data$sleepquality), y = data$peak_count)
      spearman <- c(spearman,corr_spear$estimate)
    }else{
      
      spearman <- c(spearman,NA)
    }
  }
}
