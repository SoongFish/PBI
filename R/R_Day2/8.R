loyality = c(100,90,98,79,81,69,80,77,68,74)
price = c(5,4,4,3,4,3,4,3,2,3)
quality = c(5,3,5,2,3,2,3,3,2,3)
cleanliness = c(5,3,4,4,3,2,4,4,2,3)

# 귀무가설 : 서비스 요인은 고객충성도에 영향을 미치지 않는다.
# 대립가설 : 서비스 요인은 고객충성도에 영향을 미친다.

# 여러 독립변수가 종속변수에 영향을 미치는지 분석하기위해 다중회귀분석을 사용

mydata = data.frame(y = loyality, s1 = price, s2 = quality, s3 = cleanliness)
model = lm(y~., data = mydata)
summary(model)

# 회귀식 : loyality = 43.48 + 4.92price + 5.29quality + 1.31cleanliness
# p-value가 0.003 < 0.05이므로 귀무가설을 기각, 서비스 요인은 고객충성도에 영향을 미친다고 볼 수 있다.
# 81%의 신뢰도를 가지며, quality가 유의미한 영향을 미친다.