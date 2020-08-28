attach(cars)

plot(dist~speed, data = cars)

m3 = lm(dist ~ speed, cars)
abline(m3, col = "red")

yhat = predict(m3)

cbind(dist, yhat)

join = function(i)
  lines(c(speed[i], speed[i]), c(dist[i], yhat[i]), col = "green")
  sapply(1:50, join)