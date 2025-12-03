## Full Logs located in Actions
Actions tab at https://github.com/cbm0080/TEAMNAME-FALL2025-SQA/actions

Results from `fuzz.py` in `Automated Fuzzing` job in each instance of continuous integration. Check the `Run Fuzzing Script` step for results of fuzzing
- Example instance: https://github.com/cbm0080/CRJZ-FALL2025-SQA/actions/runs/19883716649/job/56986676554

The logs from the forensic logging are also implemented, and run with continuous integration. Check the `Upload Forensics Logs` step
- Example instance: https://github.com/cbm0080/CRJZ-FALL2025-SQA/actions/runs/19883716649/job/56986676560

Continuous Integration also located in the actions tab.
- Utilizes Codacy and runs the fuzzer automatically.
- Example Instance: https://github.com/cbm0080/CRJZ-FALL2025-SQA/actions/runs/19883716649/job/56986676541

Partial Screenshots were also taken of these locations

# Notable information and what we learned
## Fuzzer
For the fuzzer, we fuzzed the 5 methods:
- `days_between` in `mining/mining.py`
- `getPythonFileCount` in `mining/mining.py`
- `checkIfParsablePython` in `FAME-ML/py_parser.py`
- `getDataLoadCount` in `FAME-ML/lint_engine.py`
- `Average` in `emperical/report.py`

In the fuzzer, we test different input methods into each of these functions. We found several different things that were taken as inputs and resulted in crashes. For example, date cannot be in a string format and datetime format in `days_between`. `chechIfParsablePython` breaks with bad file inputs (mostly to be expected). `Average` can fail due to divide by 0 errors.

## Forensics
Integrated forensics within git.repo.miner.py by adding a logging function and modifying the files 
- `miner/git.repo.miner.py` including the 5 methods `deleteRepo`, `cloneRepo`, `dumpContentIntoFile`, `getPythonCount`, and `getMLLibraryUsage`

We log important running information like where the function is looking, what it is doing, where and how much it is writing, any errors that occur, and more.

## Continuous Integration
Added continuous integration to the project via the use of Codacy, ensuring that smells like hardcoded values and unnecessary redundancy are checked for when new code is pushed to the repository via Github Actions. Whenever changes are pushed or a merge request to main is submitted, the CI workflow takes the following actions:
- Ensures that changes to code were made, as opposed to changes in the readme or other markdown files.
  - If changes were exclusively made to markdown files, then the tasks below are skipped to save time. 
- Checks out the modified branch, giving Codacy access to it.
- Runs Codacy on the provided changes
- Outputs the logs in the Github Actions tab.

Of note is that this runs whenever code is pushed to *any* branch, as opposed to only main. The original implementation from workshop 7 only applied to the main branch, so further measures were taken ensure that all branches were subject to continuous integration. Additionally, there is consideration for changes that only modify the markdown files in the project. Codacy takes a decent amount of time to run, so preventing it from running when it's not needed saves time. These weren't things that were initially accounted for; these descisions were made as we continued working with the project in order to streamline and optimize the workflow to fit this project's needs.

## Conclusion
Though adding the above features for software quality assurance wasn't trivial, the above changes represent a notable improvement in the project's maintainability and security. The fuzzer serves to expedite testing, automatically finding potentially problematic input that could cause unexpected or unwanted behavior in the program. The implementation of logging statements for factors such as time, dataflow, and environment integrety aids in debugging while also leaving a paper trail with which to track usage of the program. Finally, the implementation of continuous integration vets new changes to help prevent new bugs from being introduced.
