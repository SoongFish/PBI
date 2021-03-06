post = c(58,49,39,99,32,88,62,30,55,65,44,55,57,53,88,42,39)

shapiro.test(post)

# p-value가 0.05 이상이므로 정규분포를 따른다.

# 귀무가설 : 교육 후 성적이 오르지 않았다.
# 대립가설 : 교육 후 성적이 올랐다.

# 두 집단의 평균 비교이므로 t분석을 사용

result = t.test(post, alternative = c("greater"), mu = 55)

# p-value가 0.40 > 0.05이므로 귀무가설을 채택, 교육 후 성적이 오르지 않았다고 볼 수 있다.