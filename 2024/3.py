import re

pattern = r"(mul\((\d+),(\d+)\))|(do\(\))|(don't\(\))"

with open('3.txt') as f:
    text = f.read()

matches = re.findall(pattern, text)

mul_sum = 0
do = True
for match in matches:
    if match[3]:
        do = True
    elif match[4]:
        do = False
    elif do:
        mul_sum += int(match[1]) * int(match[2])

print(mul_sum)
