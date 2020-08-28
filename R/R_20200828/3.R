#1. 데이터 셋 읽어오기
std90 = read.table(("c:\\student90.csv"),
                   sep = ",",
                   stringsAsFactors = FALSE,
                   header = TRUE,
                   na.strings = "")
nrow(std90)

head(std90)
#2. 회귀 모델 생성
(m = lm(weight_kg ~ height_cm, data = std90))

#3. 회귀 계수 구하기
coef(m)
# weight = 32.6604 + 0.2247height

#4. 회귀 계수 값 검증하기
#예측된 값 구하기
fitted(m)[1:4]#예측값
#((32.6604144) + (0.2246605) * (std90$height_cm[1:4]))

# 이상값 진단 (cooks.distance)
plot(m, which = 4)

x_cooks.d = cooks.distance(m)
x_cooks.d[1:4]

NROW(x_cooks.d) #소문자로 하면 NULL값

x_cooks.d[which(x_cooks.d>qf(0.5, df1 = 2, df2 = 88))]
#df1 : 분모 자유도, df2 : 분자 자유도, 분위수 50%

library(car)
outlierTest(m) # Bonferroni p-value가 0.73으로 0.05보다 크다. 따라서 이상값이 검출되지 않았다.

#5. 잔차 구하기
residuals(m)[1:4] # 대학생 90명 데이터의 1~4번째 잔차 구하기
std90$weight_kg[1:4] # 대학생 90명 데이터의 1~4번째 실제 몸무게
fitted(m)[1:4] + residuals(m)[1:4] # 실제 몸무게 = 예측된 값 + 잔차

qqnorm(residuals(m)) # Q-Q plot을 이용하여 전차의 정규성 확인
qqline(residuals(m))

#shapiro-Wilk Test
shapiro.test(residuals(m)) # p-value가 0.2189로 0.05보다 크다. 따라서 정규 분포를 따른다는 귀무가설을 기각할 수 없음.

#6. 잔차 제곱합 구하기
deviance(m)

#7. 회귀계수 신뢰구간 구하기 (confint(model))
confint(m, level = 0.95)

m_conf = predict(m, level = 0.95, interval = "confidence")
head(m_conf)
plot(weight_kg ~ height_cm, data = std90)
lwr = m_conf[,2]
upr = m_conf[,3]
sx = sort(std90$height_cm, index.return = T)
abline(coef(m), lwd = 2)
lines(sx$x, lwr[sx$ix], col = "blue", lty = 2)
lines(sx$x, upr[sx$ix], col = "blue", lty = 2)

m_pred = predict(m, level = 0.95, interval = "predict")
p_lwr = m_pred[,2]
p_upr = m_pred[,3]
lines(std90$height_cm, p_lwr, col = "red", lty = 2)
lines(std90$height_cm, p_upr, col = "red", lty = 2)

#8. 새로운 학생 키로 몸무게 예측하기

predict(m, newdata = data.frame(height_cm = 175), interval = "confidence") # 새로운 학생의 키가 175일때 몸무게 예측

#9. 모델 평가
summary(m) # F-statistic = 7.274, p-value = 0.008, 절편과 계수는 통계적으로 유의함.
anova(m)

(m_a = lm(weight_kg ~ height_cm, data = std90))
(m_b = lm(weight_kg ~ 1, data = std90)) # 축소모델
anova(m_a, m_b) #

compare = c(rmse(m_a, std90), rmse(m_b, std90), mae(m_a, std90), mae(m_b, std90))
result = matrix(compare, nrow = 2, byrow = F, dimnames = list("Model" = c("m_a", "m_b"),
                                                              "Tools" = c("RMSE", "MAE")))
# RMSE값과 MAE값이 더 낮은 m_a 모델이 더 우수하다고 할 수 있다.
