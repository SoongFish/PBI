data_factor = read.table("C:\\data_factor.txt")

colnames(data_factor) = c("tohit", "strength", "dexterity", "maxlife", "maxmana", "allresist", "coldresist", "fireresist", "poisonresist", "lightresist", "regenlife", "poisonduration", "price")

model = lm(data_factor$price ~ ., data = data_factor)
summary(model)

#plot(data_factor$price, data_factor$strength, pch = 20, col = "red")