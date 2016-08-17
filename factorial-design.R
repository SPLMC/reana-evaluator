#!/usr/bin/env Rscript
#rm(list=ls(all=TRUE))
library(WRS)
library("optparse")

option_list = list(
  make_option(c("-a", "--alpha"),  default=0.01, 
              help="alpha value [default= %default]"),
  make_option(c("-d", "--decimal"), type="character", default=".", 
              help="decimal separator [default= %default]", metavar="character"),
  
  make_option(c("-i", "--input"), type="character", default="data.csv", 
              help="input data file [default= %default]", metavar="character"),
  make_option(c("-o", "--output"), type="character", default=sprintf("results.txt"), 
              help="output results file [default= %default]", metavar="character"),
    make_option(c("-r", "--result"), type="character", default=getwd(), 
              help="results dir [default= %default]", metavar="character"),
  make_option(c("-v", "--verbose"),  default=FALSE, 
              help="verbose mode [default= %default]")
); 

opt_parser = OptionParser(option_list=option_list);
opt = parse_args(opt_parser)
sink(opt$output,split=opt$verbose,type = c("output", "message"))
print(Sys.time())
print(sprintf("Script dir %s",getwd()))
print(sprintf("Input file: %s",opt$input))
print(sprintf("Output results file: %s",opt$output))
print(sprintf("Decimal separator: %s",opt$decimal))
print(sprintf("Alpha: %s",opt$alpha))

threewaytrimmed <- function(z,nlevelsf1,nlevelsf2,nlevelsf3, alpha) {
  result<-t3way(nlevelsf1,nlevelsf2,nlevelsf3,z)
  
  print(result)
  
  print(sprintf("A.p.value: %s %s",result$A.p.value,result$A.p.value<=alpha ))
  print(sprintf("B.p.value: %s %s",result$B.p.value,result$B.p.value<=alpha))
  print(sprintf("C.p.value: %s %s",result$C.p.value,result$C.p.value<=alpha))
  print(sprintf("AB.p.value: %s %s",result$AB.p.value,result$AB.p.value<=alpha))
  print(sprintf("AC.p.value: %s %s",result$AC.p.value,result$AC.p.value<=alpha))
  print(sprintf("BC.p.value: %s %s",result$BC.p.value,result$BC.p.value<=alpha))
  print(sprintf("ABC.p.value: %s %s",result$ABC.p.value,result$ABC.p.value<=alpha))
  
  return(result)
}


smp <- read.csv(opt$input,quote="",dec=opt$decimal)
 
 
 
nlevelsf1<-nlevels(as.factor(smp[,1]))
nlevelsf2<-nlevels(as.factor(smp[,2]))
nlevelsf3<-nlevels(as.factor(smp[,3]))

#print("Shapiro test memory F1")
#print(shapiro.test(smp$memory))
#print(by(data=smp$memory, smp[,1], FUN = shapiro.test));
# print("Shapiro test memory F2")
# by(smp$memory, smp[,2], shapiro.test);
# #print("Shapiro test memory F3")
# #by(smp$memory, smp[,3], shapiro.test);
# 
# print("Shapiro test time F1")
# by(smp$time, smp[,1], shapiro.test);
# print("Shapiro test time F2")
# by(smp$time, smp[,2], shapiro.test);
# print("Shapiro test time F3")
# by(smp$time, smp[,3], shapiro.test);
# 
 print("Bartlett test memory F1")
 print(bartlett.test(smp$memory ~ smp[,1]));
 print("Bartlett test memory F2")
 print(bartlett.test(smp$memory ~ smp[,2]));
 print("Bartlett test memory F3")
 print(bartlett.test(smp$memory ~ smp[,3]));
 
 print("Bartlett test time F1")
 print(bartlett.test(smp$time ~ smp[,1]));
 print("Bartlett test time F2")
 print(bartlett.test(smp$time ~ smp[,2]));
 print("Bartlett test time F3")
 print(bartlett.test(smp$time ~ smp[,3]));
 


print(sprintf("Factorial design %sx%sx%s",nlevelsf1,nlevelsf2,nlevelsf3 ))
 
 # print("Three Way ANOVA memory")
 # smp.memory.aov <- aov(memory ~ F1*F2*strategy, data=smp)
 # summary(smp.memory.aov)
# print("Three Way ANOVA time")
# smp.time.aov <- aov(time ~ F1*F2*F3, data=smp)
# summary(smp.time.aov)


#print("Tukey test time")
# TukeyHSD(smp.memory.aov, conf.level=.99)
# print("Tukey test time")
# TukeyHSD(smp.time.aov, conf.level=.99)
# options("contrasts")
# summary.lm(npk.aov)
# plot(npk.aov)
# plot.design(yield~N*P*K, data=npk)
# qqnorm(npk$yield); qqline(npk$yield, col=4)


if(!is.null(smp$memory)){
  print(sprintf("Three-way with trimmed means for memory"))

  
  x=fac2list(smp$memory,smp[,c(1,2,3)])
 
  result<-threewaytrimmed(x,nlevelsf1,nlevelsf2,nlevelsf3,opt$alpha)

}
if(!is.null(smp$time)){
  print(sprintf("Three-way with trimmed means for time"))
  y=fac2list(smp$time,smp[,c(1,2,3)])
  threewaytrimmed(y,nlevelsf1,nlevelsf2,nlevelsf3,opt$alpha)
}



 # if(nlevelsf1==2&&nlevelsf2==2){
 #     strategies=levels(as.factor(smp$strategy))
 #     for (strategy in strategies) {
 #        if(strategy!='Feature-family-based'){
 #          
 #          print(sprintf("Three-way contrast for memory Feature-family x %s",strategy))    
 #          
 #      subset=smp[smp$strategy=='Feature-family-based' | smp$strategy==strategy,] 
 #      print (subset)
 #      z=fac2list(subset$memory,subset[,c(1,2,3)])
 #    
 #      threewaycontrast(z,opt$alpha)
 #       
 #      
 #      print(sprintf("Three-way contrast for time Feature-family x %s",strategy))
 #      w=fac2list(subset$time,subset[,c(1,2,3)])
 #      threewaycontrast(y,opt$alpha)
 #        }
 #     }
 # }
sink()
closeAllConnections()


