raw_data = c(7,13,9,12,13,21,10,19,11,18,12,13)
mtx = matrix(raw_data, byrow = T, nrow = 3)
dimnames(mtx) = list("Class" = c("Class 1", "Class 2", "Class 3"),
                     "Score" = c("Score A", "Score B", "Score C", "Score F"))

barplot(t(mtx), beside = T, legend = T,
        ylim = c(0, 30),
        ylab = "Observed frequencies in sample",
        main = "Frequency of math score by class")

chisq.test(mtx)

# p-vaue 0.9667 -> independent