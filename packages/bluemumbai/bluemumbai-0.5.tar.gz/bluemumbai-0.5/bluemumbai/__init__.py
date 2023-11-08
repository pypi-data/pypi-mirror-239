import pyperclip
from datetime import datetime

def greet_and_copy():
    choice = input('''Choose an option:
1. Program to calculate age turning 100 years old.
2. Check if a number is even or odd.
3. Generate Fibonacci series.
4. Reverse a number.
5. Check for Armstrong number and Palindrome.
6. Recursive factorial function.
7. Check if a character is a vowel.
8. Compute the length of a given list or string.
9. Print a histogram for a list of integers.
10. Check if a sentence is a pangram.
11. Print elements of a list less than 5.
12. Check if two lists have at least one common element.
13. Remove specific elements from a list.
14. Clone or copy a list.
15. Sum all items in a dictionary.
16. Sort a dictionary by value.
17. Concatenate dictionaries to create a new one.
18. Read an entire text file.
19. Append text to a file and display it.
20. Read the last n lines of a file.
21. Create a class to store student information and display it.
22. Implement inheritance using Python.
23. Implement multiple inheritance in Python.
24. Implement multilevel inheritance in Python.
25. Implement exception handling in Python.
26. Configure various widget options in a GUI.
27. Change widget types and configuration options in a GUI.
28. Implement exception handling with widget options in a GUI.
Enter your choice (1-28): ''')

    if choice == '1':
        code = '''from datetime import datetime

name = input('Enter your name: ')
age = int(input('Enter your age: '))
result = (100 - age) + datetime.now().year
print(f'Hello {name}, you will turn 100 years in {result}')'''
    elif choice == '2':
        code = '''number = int(input('Enter a number: '))
if number % 2 == 0:
    print(f'{number} is even')
else:
    print(f'{number} is odd')'''
    elif choice == '3':
        code = '''n = int(input('Enter the length for Fibonacci Series: '))
a, b = 0, 1
print(a)
print(b)
for _ in range(n-2):
    c = a + b
    print(c)
    a, b = b, c'''
    elif choice == '4':
        code = '''num = int(input('Enter a number: '))

def reverse(n):
    rev = 0
    while n != 0:
        rem = n % 10
        rev = rev * 10 + rem
        n = n // 10
    return rev

print(f'Reverse of the given number is {reverse(num)}')'''
    elif choice == '5':
        code = '''num = int(input('Enter a number: '))

def is_armstrong(n):
    arm = 0
    temp = n
    while temp != 0:
        rem = temp % 10
        arm += rem ** 3
        temp //= 10
    return arm == n

def is_palindrome(n):
    return str(n) == str(n)[::-1]

if is_armstrong(num):
    print('The number is Armstrong!')
else:
    print('The number is not Armstrong.')

if is_palindrome(num):
    print('The number is a palindrome!')
else:
    print('The number is not a palindrome.')'''
    elif choice == '6':
        code = '''def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

num = int(input('Enter a number: '))
print(f'The factorial of {num} is {factorial(num)}')'''
    elif choice == '7':
        code = '''char = input('Enter a character: ')

def is_vowel(char):
    vowels = 'aeiouAEIOU'
    return char in vowels

if is_vowel(char):
    print(f'{char} is a vowel.')
else:
    print(f'{char} is not a vowel.')'''
    elif choice == '8':
        code = '''input_string = input('Enter a string or list: ')

def compute_length(input_string):
    if isinstance(input_string, str):
        return len(input_string)
    elif isinstance(input_string, list):
        return len(input_string)
    else:
        return 0

length = compute_length(input_string)
print(f'Length of the input: {length}')'''
    elif choice == '9':
        code = '''def print_histogram(input_list):
    for num in input_list:
        print('*' * num)

input_list = list(map(int, input('Enter a list of integers separated by space: ').split()))
print_histogram(input_list)'''
    elif choice == '10':
        code = '''import string

def is_pangram(sentence):
    alphabet = set(string.ascii_lowercase)
    return set(sentence.lower()) >= alphabet

sentence = input('Enter a sentence: ')
if is_pangram(sentence):
    print('The sentence is a pangram.')
else:
    print('The sentence is not a pangram.')'''
    elif choice == '11':
        code = '''input_list = list(map(int, input('Enter a list of integers separated by space: ').split()))
result_list = [num for num in input_list if num < 5]
print('Elements less than 5:', result_list)'''
    elif choice == '12':
        code = '''list1 = list(map(int, input('Enter the first list of integers separated by space: ').split()))
list2 = list(map(int, input('Enter the second list of integers separated by space: ').split()))

common_elements = list(set(list1) & set(list2))
if common_elements:
    print('The lists have common elements:', common_elements)
else:
    print('The lists do not have common elements.')'''
    elif choice == '13':
        code = '''input_list = list(map(int, input('Enter a list of integers separated by space: ').split()))
elements_to_remove = list(map(int, input('Enter elements to remove separated by space: ').split()))

result_list = [num for num in input_list if num not in elements_to_remove]
print('List after removal:', result_list)'''
    elif choice == '14':
        code = '''original_list = list(map(int, input('Enter a list of integers separated by space: ').split()))
copied_list = original_list.copy()
print('Copied list:', copied_list)'''
    elif choice == '15':
        code = '''input_dict = {101: 12, 103: 3, 104: 4, 105: 16}
sum_values = sum(input_dict.values())
print('Sum of all items in the dictionary:', sum_values)'''
    elif choice == '16':
        code = '''input_dict = {101: 12, 102: 7, 103: 4, 104: 16}
sorted_dict = {k: v for k, v in sorted(input_dict.items(), key=lambda item: item[1])}
print('Dictionary sorted by value:', sorted_dict)'''
    elif choice == '17':
        code = '''dict1 = {101: 'abc', 102: 'pqr'}
dict2 = {'name': 'Snehal', 'surname': 'Kajaniya'}
dict3 = {'department': 'IT', 'Year': 'SY'}

merged_dict = {**dict1, **dict2, **dict3}
print('Concatenated dictionary:', merged_dict)'''
    elif choice == '18':
        code = '''file_path = input('Enter the file path: ')
with open(file_path, 'r') as file:
    content = file.read()
print('File content:')
print(content)'''
    elif choice == '19':
        code = '''file_path = input('Enter the file path: ')
text_to_append = input('Enter text to append: ')
with open(file_path, 'a') as file:
    file.write('\\n' + text_to_append)
with open(file_path, 'r') as file:
    content = file.read()
print('File content after appending text:')
print(content)'''
    elif choice == '20':
        code = '''file_path = input('Enter the file path: ')
n = int(input('Enter the number of lines to read from the end: '))
with open(file_path, 'r') as file:
    lines = file.readlines()[-n:]
print('Last', n, 'lines of the file:')
print(''.join(lines))'''
    elif choice == '21':
        code = '''class Student:
    def __init__(self, name, pid, course):
        self.name = name
        self.pid = pid
        self.course = course

    def display(self):
        print('Student Details:')
        print('Name:', self.name)
        print('PID Number:', self.pid)
        print('Course:', self.course)

name = input('Enter student name: ')
pid = int(input('Enter PID Number: '))
course = input('Enter course: ')

student_obj = Student(name, pid, course)
student_obj.display()'''
    elif choice == '22':
        code = '''class Parent:
    def method(self):
        print('Parent method called')

class Child(Parent):
    def method(self):
        print('Child method called')

child_obj = Child()
child_obj.method()'''
    elif choice == '23':
        code = '''class Parent1:
    def method1(self):
        print('Parent1 method called')

class Parent2:
    def method2(self):
        print('Parent2 method called')

class Child(Parent1, Parent2):
    pass

child_obj = Child()
child_obj.method1()
child_obj.method2()'''
    elif choice == '24':
        code = '''class Grandparent:
    def grandparent_method(self):
        print('Grandparent method called')

class Parent(Grandparent):
    def parent_method(self):
        print('Parent method called')

class Child(Parent):
    def child_method(self):
        print('Child method called')

child_obj = Child()
child_obj.grandparent_method()
child_obj.parent_method()
child_obj.child_method()'''
    elif choice == '25':
        code = '''try:
    num = int(input('Enter a number: '))
    result = 100 / num
except (ValueError, ZeroDivisionError):
    print('Error: Invalid input or division by zero')
else:
    print('Result:', result)'''
    elif choice == '26':
        code = '''import tkinter as tk

root = tk.Tk()
root.title('Widget Options Demo')

label = tk.Label(root, text='Widget Options Demo', font=('Arial', 16))
label.pack(pady=20)

widget_options = {
    'bg': 'red',
    'fg': 'white',
    'font': ('Arial', 14),
    'width': 20,
    'height': 2
}

button = tk.Button(root, text='Click Me', **widget_options)
button.pack()

root.mainloop()'''
    elif choice == '27':
        code = '''import tkinter as tk

root = tk.Tk()
root.title('Widget Types Demo')

label = tk.Label(root, text='Widget Types Demo', font=('Arial', 16))
label.pack(pady=20)

widget_types = ['Button', 'Message', 'Entry', 'Checkbutton', 'Radiobutton', 'Scale']
selected_widget = tk.StringVar()

widget_menu = tk.OptionMenu(root, selected_widget, *widget_types)
widget_menu.pack()

def display_widget():
    widget_type = selected_widget.get()
    if widget_type == 'Button':
        widget = tk.Button(root, text='Button')
    elif widget_type == 'Message':
        widget = tk.Message(root, text='Message')
    elif widget_type == 'Entry':
        widget = tk.Entry(root)
    elif widget_type == 'Checkbutton':
        widget = tk.Checkbutton(root, text='Checkbutton')
    elif widget_type == 'Radiobutton':
        widget = tk.Radiobutton(root, text='Radiobutton')
    elif widget_type == 'Scale':
        widget = tk.Scale(root, from_=0, to=10, orient='horizontal')
    else:
        widget = tk.Label(root, text='Invalid selection')
    widget.pack()

display_button = tk.Button(root, text='Display Widget', command=display_widget)
display_button.pack()

root.mainloop()'''
    elif choice == '28':
        code = '''import tkinter as tk

root = tk.Tk()
root.title('Exception Handling Widget Demo')

try:
    label = tk.Label(root, text='Exception Handling Widget Demo', font=('Arial', 16))
    label.pack(pady=20)

    widget = tk.Button(root, text='Click Me', command=lambda: 1/0)
    widget.pack()
except Exception as e:
    error_label = tk.Label(root, text=f'Error: {e}', fg='red')
    error_label.pack()

root.mainloop()'''
    else:
        code = "Invalid choice"

    print(code)
    pyperclip.copy(code)

greet_and_copy()

