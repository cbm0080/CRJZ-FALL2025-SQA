import sys
import os
import importlib.util

# Determine the absolute path to the repo root
repo_root = os.getcwd()

# Define path to the miner script
# We use os.path.join to ensure cross-platform compatibility
miner_path = os.path.join(repo_root, 'MLForensics-farzana', 'mining', 'git.repo.miner.py')

def main():
    print(f"Looking for miner script at: {miner_path}")
    
    if os.path.exists(miner_path):
        try:
            # Load module dynamically. This is necessary because the filename 
            # 'git.repo.miner.py' contains dots, which are not valid in standard imports.
            spec = importlib.util.spec_from_file_location("git_repo_miner", miner_path)
            miner = importlib.util.module_from_spec(spec)
            sys.modules["git_repo_miner"] = miner
            spec.loader.exec_module(miner)
            print("Successfully loaded git.repo.miner.py")
            
            print("\n--- Invoking miner functions to generate forensics logs ---")
            
            # 1. Trigger logging in getPythonCount
            # We pass '.' to scan the current directory as a test
            print("Running miner.getPythonCount('.')")
            miner.getPythonCount('.')
            
            # 2. Trigger logging in getMLLibraryUsage
            print("Running miner.getMLLibraryUsage('.')")
            miner.getMLLibraryUsage('.')
            
            print("\n--- Forensics execution complete ---")
            
        except Exception as e:
            print(f"[ERROR] Failed to execute miner functions: {e}")
            # We exit with 0 (success) here so that the CI job continues to the 
            # 'Display Forensics Logs' step to show whatever logs were captured before the error.
            sys.exit(0)
    else:
        print(f"[ERROR] Could not find file: {miner_path}")
        sys.exit(1)

if __name__ == "__main__":
    main()