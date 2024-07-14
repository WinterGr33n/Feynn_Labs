mcdonalds <- read.csv("mcdonalds.csv")
names(mcdonalds)

dim(mcdonalds)

head(mcdonalds, 3)

MD.x <- as.matrix(mcdonalds[, 1:11])
MD.x <- (MD.x == "Yes") + 0
round(colMeans(MD.x), 2)

MD.pca <- prcomp(MD.x)
summary(MD.pca)

print(MD.pca, digits = 1)

library("flexclust")
plot(predict(MD.pca), col = "grey")
projAxes(MD.pca)

set.seed(1234)
MD.km28 <- stepFlexclust(MD.x, 2:8, nrep = 10, verbose = FALSE)
MD.km28 <- relabel(MD.km28)

plot(MD.km28, xlab = "number of segments")

set.seed(1234)
MD.b28 <- bootFlexclust(MD.x, 2:8, nrep = 10, nboot = 100)
plot(MD.b28, xlab = "number of segments", ylab = "adjusted Rand index")


MD.k4 <- MD.km28[["4"]]
histogram(MD.km28[["4"]], data = MD.x, xlim = 0:1)

slsaplot(MD.km28)

MD.r4 <- slswFlexclust(MD.x, MD.k4)

plot(MD.r4, ylim = 0:1, xlab = "segment number", ylab = "segment stability")

library("flexmix")
set.seed(1234)
MD.m28 <- stepFlexmix(MD.x ~ 1, k = 2:8, nrep = 10, model = FLXMCmvbinary(), verbose = FALSE)
MD.m28

plot(MD.m28, ylab = "value of information criteria (AIC, BIC, ICL)")

MD.m4 <- getModel(MD.m28, which = "4")
table(kmeans = clusters(MD.k4), mixture = clusters(MD.m4))

MD.m4a <- flexmix(MD.x ~1, cluster = clusters(MD.k4), model = FLXMCmvbinary())
table(kmeans = clusters(MD.k4), mixture = clusters(MD.m4a))

logLik(MD.m4a)

logLik(MD.m4)

mcdonalds$Like[mcdonalds$Like == "I hate it!-5"] <- "-5"
mcdonalds$Like[mcdonalds$Like == "I love it!+5"] <- "5"
mcdonalds$Like.n <- 6 - as.numeric(mcdonalds$Like)

table(mcdonalds$Like.n)

f <- paste(names(mcdonalds)[1:11], collapse = "+")
f <- paste("Like.n ~ ", f, collapse = "")
f <- as.formula(f)
f

set.seed(1234)
MD.reg2 <- stepFlexmix(f, data = mcdonalds, k = 2, nrep = 10, verbose = FALSE)
MD.reg2

MD.ref2 <- refit(MD.reg2)
summary(MD.ref2)

plot(MD.ref2, significance = TRUE)

MD.vclust <- hclust(dist(t(MD.x)))
barchart(MD.k4, shade = TRUE, which = rev(MD.vclust$order))

plot(MD.k4, project = MD.pca, data = MD.x, hull = FALSE, simlines = FALSE, xlab = "principal component 1", ylab = "principal component 2")
projAxes(MD.pca)

k4 <- clusters(MD.k4)
mosaicplot(table(k4, mcdonalds$Like), shade = TRUE, main = "", xlab = "segment number")

mosaicplot(table(k4, mcdonalds$Gender), shade = TRUE)

boxplot(mcdonalds$Age ~ k4, varwidth = TRUE, notch = TRUE)

library("partykit")
# VisitFrequency should be a factor (or numeric if it's a count)
mcdonalds$VisitFrequency <- factor(mcdonalds$VisitFrequency)

# Gender should be a factor
mcdonalds$Gender <- factor(mcdonalds$Gender)
tree <- ctree(factor(k4 == 3) ~ Like.n + Age + VisitFrequency + Gender, data = mcdonalds)
plot(tree)

visit <- tapply(as.numeric(mcdonalds$VisitFrequency), k4, mean)
visit

like <- tapply(mcdonalds$Like.n, k4, mean)
like

female <- tapply((mcdonalds$Gender == "Female") + 0, k4, mean)
female

plot(visit, like, cex = 10 * female, xlim = c(2, 4.5), ylim = c(-3, 3))
text(visit, like, 1:4)

