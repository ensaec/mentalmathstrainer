#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Mental Math Trainer – Quant Edition
===================================

Single-file, professional mental math training suite for:
- Quant trading interviews (All Options, Optiver, IMC, Jane Street...)
- Arithmetic speed improvement
- Probability intuition
- Approximation skills (ln, exp, sqrt…)
- 80-in-8 speed test

No dependencies. Fully terminal-based. Designed to showcase coding skills
and mental math understanding on GitHub.
"""

import random
import math
import time

# ============================================================================
# Global helpers
# ============================================================================

def get_choice(prompt, valid):
    """Force user input to be one of the allowed values."""
    valid_lower = [v.lower() for v in valid]
    while True:
        ans = input(prompt).strip().lower()
        if ans in valid_lower:
            return ans
        print(f"Please choose from {valid}.")


def round_to_difficulty(value, difficulty):
    """Round decimals according to difficulty."""
    if difficulty == "easy":
        return round(value, 1)
    elif difficulty == "medium":
        return round(value, 2)
    else:
        return round(value, 3)


def is_integer(x):
    """Detect if value is close to an integer."""
    return abs(x - round(x)) < 1e-9


def generate_integer_distractors(correct, n=4):
    """MCQ distractors for integer answers."""
    opts = {correct}
    magnitude = max(5, abs(correct) // 5)

    while len(opts) < n:
        delta = random.randint(-magnitude, magnitude)
        if delta == 0:
            continue
        cand = correct + delta
        opts.add(cand)

    opts = list(opts)
    random.shuffle(opts)
    return opts


def generate_decimal_distractors(correct, difficulty, n=4):
    """MCQ distractors for decimal answers with forced decimal depth."""
    decimals = {"easy": 1, "medium": 2, "hard": 3}[difficulty]
    opts = {round(correct, decimals)}
    spread = abs(correct) * 0.15 + 0.1

    while len(opts) < n:
        noise = (random.random() - 0.5) * spread
        cand = round(correct + noise, decimals)
        opts.add(cand)

    opts = list(opts)
    random.shuffle(opts)
    return opts


def mcq_options(correct, difficulty):
    """Generate MCQ options respecting integer/decimal type."""
    if is_integer(correct):
        return generate_integer_distractors(int(correct))
    else:
        return generate_decimal_distractors(correct, difficulty)


# ============================================================================
# Arithmetic generators
# ============================================================================

def gen_add(d):
    if d == "easy":
        a, b = random.randint(20, 200), random.randint(20, 200)
    elif d == "medium":
        a, b = random.randint(100, 900), random.randint(100, 900)
    else:
        a, b = random.randint(1000, 9999), random.randint(1000, 9999)
    return f"{a} + {b}", a + b


def gen_sub(d):
    if d == "easy":
        a, b = random.randint(50, 300), random.randint(10, 200)
    elif d == "medium":
        a, b = random.randint(500, 2000), random.randint(200, 1500)
    else:
        a, b = random.randint(2000, 9999), random.randint(500, 9000)
    return f"{a} - {b}", a - b


def gen_mul(d):
    if d == "easy":
        a, b = random.randint(10, 80), random.randint(2, 9)
    elif d == "medium":
        a, b = random.randint(20, 99), random.randint(10, 99)
    else:
        a, b = random.randint(100, 999), random.randint(10, 99)
    return f"{a} × {b}", a * b


def gen_div(d):
    if d == "easy":
        b = random.choice([2,4,5,8])
        a = b * random.randint(2, 50)
        return f"{a} ÷ {b}", a / b

    elif d == "medium":
        b = random.randint(2, 40)
        a = random.randint(50, 800)
        return f"{a} ÷ {b}", round_to_difficulty(a / b, d)

    else: # hard
        b = random.randint(3, 90)
        a = random.randint(100, 4000)
        return f"{a} ÷ {b}", round_to_difficulty(a / b, d)


def gen_decimal(d):
    """Decimal multiplication like 0.25 × 600, 0.002 × 20000."""
    if d == "easy":
        dec = random.choice([0.1, 0.2, 0.25, 0.5, 0.75])
        n = random.randint(20, 500)

    elif d == "medium":
        dec = random.choice([0.1,0.2,0.25,0.33,0.5,0.66,0.75])
        n = random.randint(50, 2000)

    else:
        dec = round(random.uniform(0.001, 0.9), 3)
        n = random.randint(200, 20000)

    result = round_to_difficulty(dec * n, d)
    return f"{dec} × {n}", result


def gen_square(d):
    if d == "easy":
        n = random.randint(5, 20)
    elif d == "medium":
        n = random.randint(20, 50)
    else:
        n = random.randint(40, 120)
    return f"{n}²", n*n


def gen_cube(d):
    if d == "easy":
        n = random.randint(2, 6)
    elif d == "medium":
        n = random.randint(5, 12)
    else:
        n = random.randint(8, 20)
    return f"{n}³", n**3


# ============================================================================
# Approximation generators
# ============================================================================

def gen_sqrt(d):
    if d == "easy":
        x, tol = random.randint(5, 200), 0.05
    elif d == "medium":
        x, tol = random.randint(100, 500), 0.03
    else:
        x, tol = random.randint(300, 2000), 0.02
    return f"Approximate √{x} (±{tol})", (math.sqrt(x), tol)


def gen_ln(d):
    x = round(random.uniform(0.01, 0.5), 3)
    if d == "easy":
        approx = x
    elif d == "medium":
        approx = x - x**2/2
    else:
        approx = x - x**2/2 + x**3/3
    return f"Approximate ln(1 + {x})", round_to_difficulty(approx, d)


def gen_exp(d):
    x = round(random.uniform(-0.4, 0.4), 3)
    if d == "easy":
        approx = 1 + x
    elif d == "medium":
        approx = 1 + x + x**2/2
    else:
        approx = 1 + x + x**2/2 + x**3/6
    return f"Approximate e^{x}", round_to_difficulty(approx, d)


def gen_inv(d):
    x = round(random.uniform(0.05, 1.0), 3)
    if d == "easy":
        approx = 1 - x
    elif d == "medium":
        approx = 1 - x + x**2
    else:
        approx = 1/(1+x)
    return f"Approximate 1/(1 + {x})", round_to_difficulty(approx, d)


def gen_logret(d):
    r = round(random.uniform(-0.2, 0.2), 3)
    true = math.log(1+r)

    if d == "easy":
        approx = r
    elif d == "medium":
        approx = r - r**2/2
    else:
        approx = true

    return f"Approximate ln(1 + {r})", round_to_difficulty(approx, d)


# ============================================================================
# Probability
# ============================================================================

def gen_prob(d):
    mode = random.choice(["coin","urn","interval","cond"])

    if mode == "coin":
        n = random.randint(3, 10)
        k = random.randint(0, n)
        return f"Prob(exactly {k} heads in {n} fair flips)?", round((0.5)**n, 5)

    if mode == "urn":
        r, b = random.randint(3,15), random.randint(3,15)
        return f"Urn with {r} red + {b} blue. Prob(red)?", round(r/(r+b), 4)

    if mode == "interval":
        a, b = random.random(), random.random()
        lo, hi = min(a,b), max(a,b)
        return f"X~U(0,1). Prob({lo:.2f} < X < {hi:.2f})?", round(hi-lo, 4)

    # conditional
    a, b = random.randint(1,9), random.randint(1,9)
    return f"Approximate P(A|A or B), with A,B indep and weights {a},{b}", round(a/(a+b),4)


# ============================================================================
# Mappings
# ============================================================================

ARITH = {
    "addition": gen_add,
    "subtraction": gen_sub,
    "multiplication": gen_mul,
    "division": gen_div,
    "decimals": gen_decimal,
    "square": gen_square,
    "cube": gen_cube,
}

APPROX = {
    "sqrt": gen_sqrt,
    "ln": gen_ln,
    "exp": gen_exp,
    "inverse": gen_inv,
    "logret": gen_logret,
}

# ============================================================================
# Modes
# ============================================================================

def run_classic():
    print("\n=== CLASSIC++ MODE ===")
    difficulty = get_choice("Difficulty (easy/medium/hard): ", ["easy","medium","hard"])
    n = int(input("How many questions? "))

    topics = list(ARITH.keys())
    score = 0
    t0 = time.time()

    for i in range(1,n+1):
        topic = random.choice(topics)
        Q, ans = ARITH[topic](difficulty)

        print(f"\nQ{i}: {Q}")
        user = input("Your answer: ").strip()
        if user in ("q","quit"):
            break

        try:
            u = float(user)
        except:
            print("Invalid.")
            continue

        if abs(u - ans) < 1e-6:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong. Correct = {ans}")

    print("\n=== SUMMARY ===")
    print(f"Score: {score}/{n}")
    print(f"Time: {round(time.time()-t0,2)} seconds")


def run_eighty():
    print("\n=== 80-IN-8 (Quant Drill) ===")
    difficulty = get_choice("Difficulty (easy/medium/hard): ", ["easy","medium","hard"])

    topics = list(ARITH.keys())
    score = 0
    t0 = time.time()
    limit = 480

    for i in range(1,81):
        if time.time()-t0 > limit:
            print("\nTIME IS UP!")
            break

        remaining = limit - (time.time()-t0)
        topic = random.choice(topics)
        Q, ans = ARITH[topic](difficulty)

        opts = mcq_options(ans, difficulty)

        print(f"\nQ{i}  (Time left: {int(remaining//60)}:{int(remaining%60):02})")
        print(Q)
        for idx,o in enumerate(opts,1):
            print(f" {idx}) {o}")

        choice = get_choice("Your choice (1-4 or q): ", ["1","2","3","4","q"])
        if choice == "q":
            break
        if opts[int(choice)-1] == opts[opts.index(ans)]:
            pass

        if abs(opts[int(choice)-1] - ans) < 1e-9:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong. Correct = {ans}")

    print("\n=== SUMMARY ===")
    print(f"Score: {score}/{i}")
    print(f"Accuracy: {round(score/i*100,2)}%")


def run_approximations():
    print("\n=== APPROXIMATION MODE ===")
    difficulty = get_choice("Difficulty (easy/medium/hard): ", ["easy","medium","hard"])
    n = int(input("How many questions? "))

    topics = list(APPROX.keys())
    score = 0

    for i in range(1,n+1):
        t = random.choice(topics)
        Q, val = APPROX[t](difficulty)

        print(f"\nQ{i}: {Q}")

        if t == "sqrt":
            true, tol = val
            u = float(input("Your approximation: "))
            if abs(u - true) <= tol:
                print("Good! Within tolerance.")
                score += 1
            else:
                print(f"Too far. True ≈ {round(true,4)}")

        else:
            correct = val
            opts = mcq_options(correct, difficulty)
            print("Choose:")
            for idx,o in enumerate(opts,1):
                print(f"{idx}) {o}")

            c = get_choice("Your answer: ", ["1","2","3","4"])
            if abs(opts[int(c)-1] - correct) < 1e-9:
                print("Correct!")
                score += 1
            else:
                print(f"Wrong. True = {correct}")

    print("\n=== SUMMARY ===")
    print(f"Score: {score}/{n}")


def run_probability():
    print("\n=== PROBABILITY MODE ===")
    difficulty = get_choice("Difficulty (easy/medium/hard): ", ["easy","medium","hard"])
    n = int(input("How many questions? "))

    score = 0
    for i in range(1,n+1):
        Q, ans = gen_prob(difficulty)
        print(f"\nQ{i}: {Q}")

        opts = mcq_options(ans, difficulty)
        for k,o in enumerate(opts,1):
            print(f"{k}) {o}")

        c = get_choice("Your answer: ", ["1","2","3","4"])
        if abs(opts[int(c)-1] - ans) < 1e-9:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong. Correct = {ans}")

    print("\n=== SUMMARY ===")
    print(f"Score: {score}/{n}")


# ============================================================================
# MAIN MENU
# ============================================================================

def main():
    print("\nWelcome to the Mental Math Trainer – Quant Edition")

    while True:
        print("\nMAIN MENU")
        print("1) Classic++ arithmetic")
        print("2) 80-in-8 quant drill")
        print("3) Approximation mode")
        print("4) Probability mode")
        print("5) Exit")

        c = get_choice("Select (1-5): ", ["1","2","3","4","5"])
        if c == "1": run_classic()
        elif c == "2": run_eighty()
        elif c == "3": run_approximations()
        elif c == "4": run_probability()
        else:
            print("Good luck on your next interview!")
            break


if __name__ == "__main__":
    main()