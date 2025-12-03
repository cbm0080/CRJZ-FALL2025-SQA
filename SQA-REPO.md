## Full Logs of Fuzzer and CI located in Actions
Actions tab at https://github.com/cbm0080/TEAMNAME-FALL2025-SQA/actions

Results from `fuzz.py` in `Automated Fuzzing` job in each instance of continuous integration. Check the `Run Fuzzing Script` step for results of fuzzing
- First instance: https://github.com/cbm0080/TEAMNAME-FALL2025-SQA/actions/runs/19835802232/job/56832658037

Continuous Integration also located in the actions tab.
- Utilizes Codacy and runs the fuzzer automatically

# Notable information and what we learned
## Fuzzer

## Forensics
Integrated forensics within git.repo.miner.py by adding a logging function and modifying the deleteRepo(), cloneRepo(), dumpContentIntoFile(), getPythonCount(), and getMLLibraryUsage() to log important running information like where the function is looking, what it is doing, where and how much it is writing, any errors that occur, and more.

## Continuous Integration

## Conclusion
