Feedback from Reviewer #1:
# Summary
Cleary - the candidate is well experienced developer and has wide knowledge in
Django, Python, shell scripting, JavaScript, docker, etc. To answer the
candidate's note for reviewers - I find this homework more than acceptable. Use
of Makefile for settings things up is a pleasure to see, though I was slightly
frustrated and distracted, by unfortunes of running bootstrapping script.
To me it's obvious - candidate seem to have done this work with great pleasure
and attention to detail. In my opinion - all tasks are completed (and I won't
nitpick on GraphQL/REST API choice).
Any critising comments are minor, because I understand the stress of doing the
task and things may run differently on different machines, operating systems,
etc. (hence problems with bootstrapping).
All in all, home-work is completed with flying colours and it would be a
pleasure to have such person as my teammate.
# Summary of notes in bullet points
Good:
- I really enjoy seeing makefile for automation;
- Shell scripts are impressive to say the least;
- Excellent readme;
- Enjoy seeing `poetry` and `pre-commit`;
- Listed prerequisites and dependencies, with hard version checks;
- Fixtures for initial data;
- Tests are passing;
- Nicely layered logic:
- API imports what it needs from the apps;
- Apps have "service" layer;
Neutral observations:
- Latest python, though not latest Django. Probably LTS was taken as a safe
choice?
- Similarly - not latest postgres in a new project. Why 12, when 15 is out
there? Major cloud providers and libraries I think must be supporting at
least 14;
- Yet again - not latest redis. 7 is out there. 5.0 is from 2018;
- Candidate mentioned use of (personal?) cookiecutter - so maybe that needs
updating;
- No `clean` target in `Makefile`, i.e. just like we automatically set things
up it would be nice to automate removal/cleaning the setup so we would be
able to redo the setup if anything;
- Why GraphQL, when REST API expected?
Not so good (because I wouldn't call it bad):
- Cookie cutter template seems a bit too big and smart for the small homework
task I was expecting;
- A bit too much "noise" from the cookie cutter template:
- Unused (I think): celery, `lib/registry.py`, `lib/reversion.py`
- Makefile and scripts are neat and I mostly like it, but it wasn't without
trouble for me;
Feedback from Reviewer #2:
Overall it looks good, I get that it’s a bootstrapped project, but I would have removed the celery,
reversion and other not needed dependencies. I don’t really get why the choice of graphql (the
task was asking for rest api), I am not that familiar with it, but the candidate seems to have
pretty deep knowledge of it. I would love to discuss the performance of this implementation.
How would it deal with concurrency and how it would scale.
The project is well documented, it has tests, but not integration tests, the code is very clean and
well organised. I bet the candidate has quite some experience and is well prepared to take on
big projects. I really liked the abstraction of `services`. Nice to see that there are linters and
attention to code style. There was some code duplication but it’s home task so I get that the
quality can’t be at its highest.
The candidate has good knowledge of django, I would like to discuss his/her decisions and
his/her coding style
