new = c(15,10,13,7,9,8,21,9,14,8)
fake = c(15,14,12,8,14,7,16,10,15,12)

shapiro.test(new)
shapiro.test(fake)

# 두 경우 모두 p-value가 0.05 이상이므로 정규분포를 따른다.

# 귀무가설 : 신약이 효과가 없다
# 대립가설 : 신약이 효과가 있다

# 두 집단의 평균 비교이므로 t분석을 사용

t.test(new, fake)

# p-value 0.60 > 0.05이므로 귀무가설을 채택, 신약이 효과가 없다고 볼 수 있다.