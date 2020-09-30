# .sim File Generator
A python program that generates a .sim file from a input boolean expression. 

**Gates identified by the program**
 - NOT Gate: ~
 - AND Gate: &
 - OR Gate: |
 - XOR Gate: ^
 - NAND Gate: ~&
 - NOR Gate: ~|
 - XNOR Gate: ~^

## Prerequisites
 - The latest version of Python
   ```bash
   $ sudo apt-get update
   $ sudo apt-get install python3.8
   ```
 - Pip3
   ```bash
   $ curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
   $ python3 get-pip.py
   ```
 - Sympy
   ```bash
   $ pip3 install sympy
   ```
 - Irsim
   ```bash
   $ sudo apt-get update
   $ sudo apt-get upgrade
   $ sudo apt-get install irsim
   ```
   
## Usage
 - Generating the .sim file
   ```bash
   $ python3 main.py
   ```
 - Running the .sim file
   ```bash
   $ irsim "file_name".sim
   ```

## Using Irsim
 - Watching the variables
   ```bash
   w "list_of_variables"
   ```
 - Display the variables
   ```bash
   d
   ```
 - Setting a variable as high
   ```bash
   h "variable_name"
   ```
 - Setting a variable as low
   ```bash
   l "variable_name"
   ```
 - Show the updated variables
   ```bash
   s
   ```
