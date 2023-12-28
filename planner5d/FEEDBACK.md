Thank you for taking the time to complete the test task. While we found several ideas interesting, we observed room for improvement in the overall code quality. Here is a brief feedback from our team:

Issues with architecture: * Everything written with functions * Tight coupling of unrelated functions for example _make_csv_writer and run_workers in same file * Strange and complex solution with 3 parallel - abuse of cancel in run_workers
SOLID Violations: * S - worker.py one big violation * O - scraper.py full of violations
STUPID Violations: * T - everything is quite tightly coupled, for example change of outputting csv to xml will require changing file that contains network and parsing code * U - big part of code is un-testable, as example _make_csv_writer, run_workers, ... * D - works kind of duplication logic duplication f"{API_PROJECT_URL}{hash_}"
* 5 level nesting
 
We are sorry to inform you that we won't be moving forward with your application at this time. 
