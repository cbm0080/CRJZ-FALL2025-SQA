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
- `miner/git.repo.miner.py` including the methods`deleteRepo`, `cloneRepo`, `dumpContentIntoFile`, `getPythonCount`, and `getMLLibraryUsage`

We log important running information like where the function is looking, what it is doing, where and how much it is writing, any errors that occur, and more.

## Continuous Integration
Added continuous integration to the project via the use of Codacy, ensuring that smells like hardcoded values and unnecessary redundancy are checked for when new code is pushed to the repository via Github Actions. Whenever changes are pushed or a merge request to main is submitted, the CI workflow takes the following actions:
- Ensures that changes to code were made, as opposed to changes in the readme or other markdown files.
  - If changes were exclusively made to markdown files, then the tasks below are skipped to save time. 
- Checks out the modified branch, giving Codacy access to it.
- Runs Codacy on the provided changes
- Outputs the logs in the Github Actions tab.
Of note is that this runs whenever code is pushed to *any* branch, as opposed to only main. The original implementation from workshop 7 only applied to the main branch, so further measures were taken ensure that all branches were subject to continuous integration.

## Conclusion
Though adding the above features for software quality assurance wasn't trivial, the above changes represent a notable improvement in the project's maintainability and security. The fuzzer serves to expedite testing, automatically finding potentially problematic input that could cause unexpected or unwanted behavior in the program. The implementation of logging statements for factors such as time, dataflow, and environment integrety aids in debugging while also leaving a paper trail with which to track usage of the program. Finally, the implementation of continuous integration vets new changes to help prevent new bugs from being introduced.
