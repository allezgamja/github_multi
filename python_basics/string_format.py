import random

name = "한세희"
eng_name = "Sehee Han"

# pyformat
print("안녕하세요, {}입니다. My name is {}".format(name,eng_name))

# f-string
print(f"안녕하세요, {name}입니다. My name is {eng_name}")


numbers = list(range(1,46))
lotto = random.sample(numbers, 6)
print(f"오늘의 행운의 번호는 {sorted(lotto)}입니다.")