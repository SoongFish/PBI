#문제1. for문을 이용해 구구단 2~9단 만들기
cnt = 0
for (i in 2:9)
{
  for (j in 1:9)
  {
    print(paste(i, "X", j, "=", i*j))
    cnt = cnt + 1
  }
}

#문제2. 1부터 100까지의 수 중에서 3의 배수이면서 4의 배수는 아닌 수의 합을 구하라
num = 1:100
sum = 0

for (i in num)
{
  if (i %% 3 == 0 & i %% 4 != 0)
  {
    sum = sum + i
  }
}

print(sum)

#문제3. x와 n을 입력하면 1부터 n까지의 수 중에서 x의 배수 합을 구해주는 사용자 정의 함수를 만들어라
sums = 0

ifsum = function (x, n)
{
  nums = 1:n
  for (k in nums)
  {
    if (k %% x == 0)
    {
      sums = sums + k
    }
  }
  print(paste("1부터", n, "까지의 수 중에서", x, "의 배수 합은", sums, "입니다."))
}

ifsum(3, 100)