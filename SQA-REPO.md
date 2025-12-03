## Full Logs located in Actions
Actions tab at https://github.com/cbm0080/TEAMNAME-FALL2025-SQA/actions

Results from `fuzz.py` in `Automated Fuzzing` job in each instance of continuous integration. Check the `Run Fuzzing Script` step for results of fuzzing
- First instance: https://github.com/cbm0080/TEAMNAME-FALL2025-SQA/actions/runs/19835802232/job/56832658037

Continuous Integration also located in the actions tab.
- Utilizes Codacy and runs the fuzzer automatically.
- Example Logs: https://github.com/cbm0080/TEAMNAME-FALL2025-SQA/actions/runs/19878334736/job/56970756895#logs

# Notable information and what we learned
## Fuzzer
For the fuzzer, we fuzzed the methods:
- `days_between` in `mining/mining.py`
- `getPythonFileCount` in `mining/mining.py`
- `checkIfParsablePython` in `FAME-ML/py_parser.py`
- `getDataLoadCount` in `FAME-ML/lint_engine.py`
- `Average` in `emperical/report.py`

In the fuzzer, we test different input methods into each of these functions.

## Forensics
Integrated forensics within git.repo.miner.py by adding a logging function and modifying the files 
- `miner/git.repo.miner.py` including the methods `deleteRepo`, `cloneRepo`, `dumpContentIntoFile`, `getPythonCount`, and `getMLLibraryUsage`
- ``
- ``
- ``
- ``
We log important running information like where the function is looking, what it is doing, where and how much it is writing, any errors that occur, and more.

## Continuous Integration
Added continuous integration to the project via the use of Codacy, ensuring that smells like hardcoded values and unnecessary redundancy are checked for when new code is pushed to the repository via Github Actions. Of note is that this runs whenever code is pushed to any branch, as opposed to only main. The original implementation from workshop 7 only applied to the main branch, so further measures were taken ensure that all branches were subject to continuous integration.


## Conclusion
