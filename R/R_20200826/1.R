name = c("사과", "딸기", "바나나", "수박", "배")
sweetness = c(8, 9, 13 , 11, 10)
weight = c(120, 25, 30, 1500, 300)
price = c(1000, 200, 600, 17000, 2500)

sells = data.frame(name, sweetness, weight, price)
sells

#문제1. 당도(sweetness)가 10 이상인 데이터를 출력하라.
subset(sells, sweetness >= 10)

#문제2. 무게(weight)가 200 이하이고 당도(sweetness)가 짝수인 데이터를 출력하라.
subset(sells, weight <= 200 & sweetness%%2 == 0)

#문제3. 가성비가 1 이상인 데이터의 이름과 가격을 출력하라. (가성비는 당도x무게를 가격으로 나눈 값으로 한다)
subset(sells, (sweetness * weight / price) >= 1, select = c(name, price))
