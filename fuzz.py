import sys
import os
import traceback

# Add source directories to python path so we can import the modules
repo_root = os.getcwd()
sys.path.append(os.path.join(repo_root, 'MLForensics-farzana', 'FAME-ML'))
sys.path.append(os.path.join(repo_root, 'MLForensics-farzana', 'mining'))
sys.path.append(os.path.join(repo_root, 'MLForensics-farzana', 'empirical'))

try:
    import mining
    import py_parser
    import lint_engine
    import report  # Imported from the 'empirical' folder
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Ensure directories 'FAME-ML', 'mining', and 'empirical' exist in 'MLForensics-farzana'.")
    sys.exit(1)

def fuzz_method(method_name, method_obj, inputs):
    print(f"--- Fuzzing {method_name} ---")
    for val in inputs:
        try:
            # Handle specific argument requirements
            if method_name == "mining.days_between":
                method_obj(val, val)
            else:
                method_obj(val)
        except Exception as e:
            print(f"[BUG FOUND] Method '{method_name}' crashed with input '{val}' ({type(val)})")
            print(f"Exception message: {e}")
    print(f"--- End Fuzzing {method_name} ---\n")

def main():
    # List of "garbage" inputs to test robustness
    fuzz_inputs = [
        None, 
        12345, 
        "random_garbage_string_xyz", 
        [], 
        {}, 
        0.0
    ]

    # --- Folder 1: mining ---
    # 1. Fuzzing mining.days_between
    # Vulnerability: Type errors on subtraction, Attribute errors on .days
    fuzz_method("mining.days_between", mining.days_between, fuzz_inputs)

    # 2. Fuzzing mining.getPythonFileCount
    # Vulnerability: os.walk raises TypeError on non-string inputs
    fuzz_method("mining.getPythonFileCount", mining.getPythonFileCount, fuzz_inputs)

    # --- Folder 2: FAME-ML ---
    # 3. Fuzzing py_parser.checkIfParsablePython
    # Vulnerability: FileNotFoundError, TypeError on open()
    fuzz_method("py_parser.checkIfParsablePython", py_parser.checkIfParsablePython, fuzz_inputs)

    # 4. Fuzzing lint_engine.getDataLoadCount
    # Vulnerability: Propagates unhandled exceptions from parsing helper methods
    fuzz_method("lint_engine.getDataLoadCount", lint_engine.getDataLoadCount, fuzz_inputs)

    # --- Folder 3: empirical ---
    # 5. Fuzzing report.Average
    # Vulnerability: ZeroDivisionError on empty list [], TypeError on None/int/strings
    fuzz_method("report.Average", report.Average, fuzz_inputs)

if __name__ == "__main__":
    main()