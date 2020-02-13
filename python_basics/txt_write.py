## This is line 1....이 반복되는 내용을 담은 파일을 만들어라
# f = open('mulcam.txt', 'w')   # ('파일명', '쓰기 or 읽기모델?')
# for i in range(10):
#     f.write(f"This is line {i}. \n")
# f.close()

# with open('mulcam2.txt', 'w') as f:     # with는 open/close를 같이 수행
#     for i in range(10):
#         f.write(f"This is line {i}. \n")

with open('mulcam.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        print(line.strip())


## mulcam.txt [0 1 2 3]을 숫자 순서 바꾸어 다시 작성하라
# # 1. line 불러오기
# with open('mulcam.txt', 'r') as f:
#     lines = f.readlines()

# # 2. 뒤집기
# lines.reverse()

# # 3. line 작성하기
# with open('mulcam.txt', 'w') as f:
#     for line in lines:
#         f.write(line)