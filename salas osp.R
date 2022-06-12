library(EnvStats)


tpo_desde_opr <- read_excel("Desktop/ONCEAVO SEMESTRE Y AL CSM LARGA/CAPSTONE/DATA DEF DEF/desde_opr_hacia_hosp.xlsx")


data <- tpo_desde_opr$permanencia #sin el outlayer
summary(data)
boxplot(data)
hist(data, freq = T)

intervalo_1 = data[data<=72] # menos de 3 dias
summary(intervalo_1)
sd = sd(intervalo_1)
l_i_1 = length(intervalo_1)/length(data)
hist(intervalo_1, freq = F)
min(intervalo_1)

#ptruncnorm(q, a=-Inf, b=Inf, mean = 0, sd = 1)

fit <- fitdist(intervalo_1, "gamma", method = "mme")
fit
plot(fit)
ksnormtrunc <- ks.test(intervalo_1, "pgamma", fit$estimate[1], fit$estimate[2])
ksnormtrunc

x <- rgamma(100,  fit$estimate[1], fit$estimate[2])
x <- x[x<72 & x>0]
hist(x, freq = F)



intervalo_2 = data[data > 72 & data < 285]#entre 3 dias y 7 dias
l_i_2 = length(intervalo_2)/length(data)
summary(intervalo_2)
sd = sd(intervalo_2)
hist(intervalo_2, freq = F)
min(intervalo_2)


fit <- fitdist(intervalo_2, "norm", method = "mme")
fit
plot(fit)
ksnormtrunc2 <- ks.test(intervalo_2, "pnorm", fit$estimate[1], fit$estimate[2])
ksnormtrunc2

x <- rnorm(1000,  fit$estimate[1], fit$estimate[2])
x2 <- x[x>72 & x < 281]
hist(x2, breaks = seq(70, 350, 25))

summary(x2)
mean(x2)
sd(x2)
###############
## desde opr_033

tpo_desde_opr_033 <- read_excel("Desktop/ONCEAVO SEMESTRE Y AL CSM LARGA/CAPSTONE/DATA DEF DEF/desde_opr_hacia_hosp.xlsx",
                            sheet = "Hoja2")

data2 <- tpo_desde_opr_033$permanencia
da <- data2[data2 < 450]
hist(da)

int_1 <- da[da<=72]
hist(int_1)
l_i1 = length(int_1)/length(data2)
fit1 <- fitdist(int_1, "norm", method = "mme")
plot(fit1)
ksnormtrunc22 <- ks.test(int_1, "pnorm", fit1$estimate[1], fit1$estimate[2])
ksnormtrunc22



int_2 <- da[da>72]
summary(int_2)
hist(int_2, freq = F)
l_i2 =  length(int_2)/length(data2)
min(int_2)
fit2 <- fitdist(int_2, "norm", method = "mme")
plot(fit2)
ksnormtrunc3 <- ks.test(int_2, "pnorm", fit2$estimate[1], fit2$estimate[2] )
ksnormtrunc3

m <- rnorm(1000,  fit2$estimate[1], fit2$estimate[2])
xxx <- m[m>72 & m < 290]
mean(xxx)
summary(xxx)
hist(xxx, freq = F)


########

data_opr_003 <- read_excel("Desktop/ONCEAVO SEMESTRE Y AL CSM LARGA/CAPSTONE/DATA DEF DEF/desde_opr_hacia_hosp.xlsx",
                           sheet = "Hoja3")


data_opr_003 <- data_opr_003$permanencia
data_opr_003


i.1 <- data_opr_003[data_opr_003<24]
length(i.1)/length(data_opr_003)
fitin <- fitdist(i.1, "gamma", method = "mge")
plot(fitin)

min(i.1)
max(i.1)


ksnormtrunc3 <- ks.test(i.1, "pgamma", fitin$estimate[1], fitin$estimate[2] )
ksnormtrunc3


length(i.1)
hist(i.1)

i.2 <- data_opr_003[data_opr_003>24]


fitxd <- fitdist()

##############
div203 <- read_excel("Desktop/ONCEAVO SEMESTRE Y AL CSM LARGA/CAPSTONE/DATA DEF DEF/desde_opr_hacia_hosp.xlsx",
                           sheet = "desde DIV103_204")

data_div203 <- div203$permanencia
data_div203


i.11 <- data_div203
length(i.11)/length(data_div203)
hist(i.11)


fitin <- fitdist(i.11, "lnorm", method = "mme")
plot(fitin)
fitin$estimate

logno_moments <- function(meanlog, sdlog) {
  m <- exp(meanlog + (1/2)*sdlog^2)
  s <- exp(meanlog + (1/2)*sdlog^2)*sqrt(exp(sdlog^2) - 1)
  return(list(mean = m, sd = s))
}

min(i.11)
max(i.11)


ksnormtrunc3 <- ks.test(i.11, "plnorm", fitin$estimate[1], fitin$estimate[2] )
ksnormtrunc3
x <- rlnorm(1000, fitin$estimate[1], fitin$estimate[2])
x <- x[x>3 & x < 500]
length(x)
hist(x)


#####
div107 <- read_excel("Desktop/ONCEAVO SEMESTRE Y AL CSM LARGA/CAPSTONE/DATA DEF DEF/desde_opr_hacia_hosp.xlsx",
                     sheet = "desde div101_107")

div107 <- div107$permanencia

length(div107)
hist(div107)


interv.1 <- div107[div107<=9]
length(interv.1)/length(div107)
hist(interv.1)

min(interv.1)
max(interv.1)

fit.1 <- fitdist(interv.1, "lnorm", method = "mme")
plot(fit.1)
fitin$estimate


ksnormtrunc3 <- ks.test(interv.1, "plnorm", fit.1$estimate[1], fit.1$estimate[2] )
ksnormtrunc3

h <- rlnorm(1000, fit.1$estimate[1], fit.1$estimate[2])
h <- h[h>0.4 & h<9]



interv.2 <- div107[div107>9 & div107 < 35]
length(interv.2)/length(div107)
hist(interv.2)

min(interv.2)
max(interv.2)

fit.2 <- fitdist(interv.2, "gamma", method = "mle")
plot(fit.2)
fit.2$estimate


ksnormtrunc3 <- ks.test(interv.2, "pgamma", fit.2$estimate[1], fit.2$estimate[2] )
ksnormtrunc3




interv.3 <- div107[div107>=35 & div107<700]
length(interv.3)/length(div107)
hist(interv.3)

min(interv.3)
max(interv.3)

fit.3 <- fitdist(interv.3, "lnorm", method = "mse")
plot(fit.3)
fit.3$estimate


ksnormtrunc3 <- ks.test(interv.3, "plnorm", fit.3$estimate[1], fit.3$estimate[2] )
ksnormtrunc3



#####
otro <- read_excel("Desktop/ONCEAVO SEMESTRE Y AL CSM LARGA/CAPSTONE/DATA DEF DEF/desde_opr_hacia_hosp.xlsx",
                     sheet = "promedio desde no opr hacia div")

otros <- otro$permanencia

length(otros)
hist(otros)


interv.11 <- otros[otros<=24]
length(interv.11)/length(otros)
hist(interv.11)

min(interv.1)
max(interv.1)

fit.1 <- fitdist(interv.1, "lnorm", method = "mme")
plot(fit.1)
fitin$estimate


ksnormtrunc3 <- ks.test(interv.1, "plnorm", fit.1$estimate[1], fit.1$estimate[2] )
ksnormtrunc3

h <- rlnorm(1000, fit.1$estimate[1], fit.1$estimate[2])
h <- h[h>0.4 & h<9]


