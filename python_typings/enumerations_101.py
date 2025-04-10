from enum import Enum


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"


male = Gender.MALE.name
female = Gender.FEMALE.name


gender = "Trans"

result = Gender.__contains__(gender.lower())
print(result)


for gender_ in Gender:
    if gender.lower() == gender_.value:
        print(f"Found gender: {gender_.name}")
        break
    else:
        print("Gender not found")


print()
for _ in range(20):
    print("Richard Osei")
print()





















