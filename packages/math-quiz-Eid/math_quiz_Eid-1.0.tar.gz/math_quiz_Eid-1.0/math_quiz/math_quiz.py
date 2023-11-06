import random


def generate_random_int(min: int, max: int):
    
    """
    min: int
    max: int
    
    Returns a random integer between min and max.
    """
    
    # return a random integer between min and max
    return random.randint(min, max)


def choose_random_op():
    
    """
    Returns a random operator from the list ['+', '-', '*']
    """

    # return a random operator from the list ['+', '-', '*']
    return random.choice(['+', '-', '*'])


def operator(number1: int, number2: int, operator: str):
    
    """_summary_
    number1 (int): number 1
    number2 (int): number 2
    operator:
        _type_: returns the result of the operation between n1 and n2
    """
    
    # return the result of the operation between n1 and n2
    result = f"{number1} {operator} {number2}"
    sol = 0
    if operator == '+': sol = number1 + number2
    elif operator == '-': sol = number1 - number2
    else: 
        sol = number1 * number2
    return result, sol

def math_quiz():
    
    """_summary_
    """
    
    # initialize score and pi
    score = 0
    num_problems = 3

    print("Welcome to the Math Quiz Game!")
    print("You will be presented with math problems, and you need to provide the correct answers.")

    for _ in range(num_problems):
        n1 = generate_random_int(1, 10); n2 = generate_random_int(1, 5); o = choose_random_op()

        PROBLEM, ANSWER = operator(n1, n2, o)
        print(f"\nQuestion: {PROBLEM}")
        
        try:
            useranswer = input("Your answer: ")
            useranswer = int(useranswer)
        except ValueError:
            print("Wrong input. Please enter an integer.")
            continue

        if useranswer == ANSWER:
            print("Correct! You earned a point.")
            score += 1
        else:
            print(f"Wrong answer. The correct answer is {ANSWER}.")

    print(f"\nGame over! Your score is: {score}/{num_problems}")

if __name__ == "__main__":
    math_quiz()
