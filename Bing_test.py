# Import Tkinter and random modules
import tkinter as tk
import random

# Define a function to generate a random prime number between 1 and 1000


def generate_prime():
    # Create an empty list to store prime numbers
    primes = []
    # Loop through the numbers from 1 to 1000
    for num in range(1, 1001):
        # Assume the number is prime until proven otherwise
        is_prime = True
        # Loop through the possible divisors from 2 to the square root of the number
        for divisor in range(2, int(num**0.5) + 1):
            # If the number is divisible by any divisor, it is not prime
            if num % divisor == 0:
                is_prime = False
                break
        # If the number is prime, add it to the list of primes
        if is_prime:
            primes.append(num)
    # Choose a random prime from the list and display it on the label
    random_prime = random.choice(primes)
    label.config(text=f"The random prime number is {random_prime}")


# Create a Tkinter window
window = tk.Tk()
window.title("Random Prime Generator")

# Create a label to display the result
label = tk.Label(window, text="Click on Generate button to get a random prime number")
label.pack()

# Create a button to generate a random prime number
generate_button = tk.Button(window, text="Generate", command=generate_prime)
generate_button.pack()

# Create a button to close the program
close_button = tk.Button(window, text="Close", command=window.destroy)
close_button.pack()

# Start the main loop of the window
window.mainloop()
