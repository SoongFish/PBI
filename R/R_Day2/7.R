relationship = c(100,90,98,79,81,69,80,77,68,54)
personality = c(5,4,5,3,4,3,2,3,2,1)
apperance = c(5,3,4,3,4,3,2,3,2,1)
mind = c(5,3,3,2,3,3,4,3,2,1)

# 귀무가설 : 개인요인은 인맥관리에 영향을 미치지 않는다
# 대립가설 : 개인요인은 인맥관리에 영향을 미친다

# 여러 독립변수가 종속변수에 영향을 미치는지 분석하기위해 다중회귀분석을 사용

mydata = data.frame(y = relationship, s1 = personality, s2 = apperance, s3 = mind)

summary(model)

# 회귀식 : relationship = 44.84 + 13.84personality -8.22apperance + 5.22mind
# p-value가 0.001 < 0.05이므로 귀무가설을 기각, 개인요인은 인맥관리에 영향을 미친다고 볼 수 있다.
# 88%의 신뢰도를 가지며, personality와 mind가 유의미한 영향을 미친다.