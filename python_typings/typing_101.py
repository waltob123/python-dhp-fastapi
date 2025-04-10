from typing import List, Dict, Tuple, Set, Any, Union, Optional


# integer typing
age: int = 25

# string typing
name: str = "John Doe"

# boolean typing
is_student: bool = True

fee: float = 99.99

# list typing
grades: List[List[str]] = [["A", "B"], ["C", "D"]]


# dictionary typing
student_info: Dict[str, str] = {
    "name": "John Doe",
    "age": "25",
    "is_student": "True"
}

student_info_2: Dict[str, Dict] = {
    "course": {
        "name": "Python Programming",
        "id": "CSPP101",
        "instructor": "Dr. Richard Osei"
    }
}

# tuple typing
coordinates: Tuple[int, int, int] = (10, 9, 90)

# any typing
age2: Any = None
print(age2)
age2 = "john"
print(age2)
age2 = 2


# union typing
users_ages: List[Union[str, int]] = ["John"]


# optional typing
gender: Optional[str] = "male"
print(gender)

gender = None
print(gender)

gender = 25
print(gender)
