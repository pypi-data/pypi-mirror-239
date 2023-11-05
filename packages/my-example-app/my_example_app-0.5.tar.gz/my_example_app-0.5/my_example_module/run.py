# run.py

from my_example_module import my_module

if __name__ == "__main__":
    a = 10
    b = 5
    
    # 패키지의 함수를 사용
    result_add = my_module.add(a, b)
    result_subtract = my_module.subtract(a, b)
    result_multiply = my_module.multiply(a, b)
    result_divide = my_module.divide(a, b)
    
    print(f"Addition: {a} + {b} = {result_add}")
    print(f"Subtraction: {a} - {b} = {result_subtract}")
    print(f"Multiplication: {a} * {b} = {result_multiply}")
    print(f"Division: {a} / {b} = {result_divide}")
