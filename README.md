# Comparison-ddmin-probdd
Here, we explore the similarity and difference between 
[delta debugging](https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/delta-debugging.pdf)
(specifically `ddmin`) algorithm and 
[probalistic delta debugging](https://xiongyingfei.github.io/papers/FSE21a.pdf)
(`probdd`).

Delta debugging is a state-of-the-art tool automating the scientific debugging process.
It iteratively removes elements within the input sequence (e.g., lines of codes) with increasing granularity.
Each step, the subsequence and its compliment are tested against the user-specified property.
The result is a smaller program taht still exhibits the specified property (e.g., trigging a bug).
Delta debugging is integrated to many program reduction tools and used as the base logic.

Probalistic delta debugging is the lastest advancement of delta debugging recently.
Unlike `ddmin` removing elements in a fixed order, `probdd` maintains a probalistic model that guides the generation of subsequences,
leading to faster runtime performance and potentially smaller results.
`probdd` algorithm can be effortlessly integrated with program reduction tools that currently employs `ddmin`.


### Input program
```angular2html
import string
import random
a = '2'
b = 2
a = random.choice(string.ascii_letters)
c = a + b
```
This piece of code carefully designed to show case
the claimed advatange of ProbDD. 

ProbDD removes elements in a intelligent order,
whereas ddmin carries out the process in a fixed order.

### DDmin Output
Due to fixed order, ddmin quickly gets to the single-element level and thus removed `a = 2` before finish.
```angular2html
Test(['import string\n', 'import random\n', "a = '2'\n", 'b = 2\n', 'a = random.choice(string.ascii_letters)\n', 'c = a + b\n']):       FAIL
Test(['import string\n', 'import random\n', "a = '2'\n", 'b = 2\n', 'a = random.choice(string.ascii_letters)\n', 'c = a + b\n']):       FAIL
Test(['b = 2\n', 'a = random.choice(string.ascii_letters)\n', 'c = a + b\n']):  UNRESOLVED
Test(['import string\n', 'import random\n', "a = '2'\n"]):      PASS
Test(['import random\n', "a = '2'\n", 'b = 2\n', 'a = random.choice(string.ascii_letters)\n', 'c = a + b\n']):  UNRESOLVED
Test(['import string\n', "a = '2'\n", 'b = 2\n', 'a = random.choice(string.ascii_letters)\n', 'c = a + b\n']):  UNRESOLVED
Test(['import string\n', 'import random\n', 'b = 2\n', 'a = random.choice(string.ascii_letters)\n', 'c = a + b\n']):    FAIL
Test(['import random\n', 'b = 2\n', 'a = random.choice(string.ascii_letters)\n', 'c = a + b\n']):       UNRESOLVED
Test(['import string\n', 'b = 2\n', 'a = random.choice(string.ascii_letters)\n', 'c = a + b\n']):       UNRESOLVED
Test(['import string\n', 'import random\n', 'a = random.choice(string.ascii_letters)\n', 'c = a + b\n']):       UNRESOLVED
Test(['import string\n', 'import random\n', 'b = 2\n', 'c = a + b\n']): UNRESOLVED
Test(['import string\n', 'import random\n', 'b = 2\n', 'a = random.choice(string.ascii_letters)\n']):   PASS
time:
 0.19990110397338867
input size:
 6
output size
 5
querry:
 15
Final Reduced Output -->
 ['import string\n', 'import random\n', 'b = 2\n', 'a = random.choice(string.ascii_letters)\n', 'c = a + b\n']
```
### ProbDD Output (fixed version)
##### initial_prob = 0.1
ProbDD keeps a dictionary (`map[ element ] = prob`), and this `prob` guides the subsequence generation.
```angular2html
Test(['import string\n', 'import random\n', "a = '2'\n", 'b = 2\n', 'a = random.choice(string.ascii_letters)\n', 'c = a + b\n']):       FAIL
Test([]):       PASS
Test(['a = random.choice(string.ascii_letters)\n', 'c = a + b\n']):     UNRESOLVED
Test(['import string\n', 'import random\n', "a = '2'\n", 'b = 2\n']):   PASS
Test(["a = '2'\n", 'b = 2\n', 'a = random.choice(string.ascii_letters)\n', 'c = a + b\n']):     UNRESOLVED
Test(['import string\n', 'import random\n', 'a = random.choice(string.ascii_letters)\n', 'c = a + b\n']):       UNRESOLVED
Test(['import string\n', 'import random\n', "a = '2'\n", 'b = 2\n', 'c = a + b\n']):    FAIL
Test(['import string\n', 'import random\n', "a = '2'\n", 'b = 2\n']):   PASS
Test(['import random\n', "a = '2'\n", 'b = 2\n', 'c = a + b\n']):       FAIL
Test(["a = '2'\n", 'b = 2\n', 'c = a + b\n']):  FAIL
Test(['b = 2\n', 'c = a + b\n']):       UNRESOLVED
Test(["a = '2'\n", 'c = a + b\n']):     UNRESOLVED
Iteration needs to stop :: because all elements are decided.
time:
 0.1900489330291748
input size:
 6
output size
 3
querry:
 11
Final Reduced Output -->
 ["a = '2'\n", 'b = 2\n', 'c = a + b\n']
```
##### initial_prob = 0.01
Note that the initial probability does affect the result to some extents (by affecting the element selection order),
though its effect appears to be negligible when input program is large as its paper.
```angular2html
Test(['import string\n', 'import random\n', "a = '2'\n", 'b = 2\n', 'a = random.choice(string.ascii_letters)\n', 'c = a + b\n']):       FAIL
Test([]):       PASS
Test(['c = a + b\n']):  UNRESOLVED
Test(["a = '2'\n", 'b = 2\n', 'a = random.choice(string.ascii_letters)\n']):    UNRESOLVED
Test(['import string\n', 'import random\n', 'c = a + b\n']):    UNRESOLVED
Test(['import string\n', 'import random\n', 'b = 2\n', 'a = random.choice(string.ascii_letters)\n']):   PASS
Test(['import string\n', 'import random\n', "a = '2'\n", 'c = a + b\n']):       UNRESOLVED
Test(['import random\n', "a = '2'\n", 'b = 2\n', 'a = random.choice(string.ascii_letters)\n']): UNRESOLVED
Test(['import string\n', "a = '2'\n", 'b = 2\n', 'a = random.choice(string.ascii_letters)\n', 'c = a + b\n']):  UNRESOLVED
Test(['import string\n', 'import random\n', "a = '2'\n", 'a = random.choice(string.ascii_letters)\n', 'c = a + b\n']):  UNRESOLVED
Test(['import string\n', 'import random\n', "a = '2'\n", 'b = 2\n', 'c = a + b\n']):    FAIL
Test(['import string\n', 'import random\n', "a = '2'\n", 'b = 2\n']):   PASS
Test(['import random\n', "a = '2'\n", 'b = 2\n', 'c = a + b\n']):       FAIL
Test(['import random\n', 'b = 2\n', 'c = a + b\n']):    UNRESOLVED
Iteration needs to stop :: because all elements are decided.
time:
 0.2331538200378418
input size:
 6
output size
 4
querry:
 13
Final Reduced Output -->
 ['import random\n', "a = '2'\n", 'b = 2\n', 'c = a + b\n']
```

### Summary
As results shown, `probdd` achieves better reduced size in this artificial program.


Something more...
--
Clearly, the order of elements selection affects reduction performance.
Then, how does different levels of randomness affects it?
Two levels of randomness are investigated:
1. One shuffle before the entire process begins
2. Shuffle at each granularity level.

### Random (once) Output
##### Best case (same as ProbDD):
```angular2html
Test(['import string\n', 'import random\n', "a = '2'\n", 'b = 2\n', 'a = random.choice(string.ascii_letters)\n', 'c = a + b\n']):       FAIL
random ddmin now starts
Test(['a = random.choice(string.ascii_letters)\n', 'b = 2\n', "a = '2'\n", 'c = a + b\n', 'import random\n', 'import string\n']):       UNRESOLVED
Test(['c = a + b\n', 'import random\n', 'import string\n']):    UNRESOLVED
Test(['a = random.choice(string.ascii_letters)\n', 'b = 2\n', "a = '2'\n"]):    UNRESOLVED
Test(['b = 2\n', "a = '2'\n", 'c = a + b\n', 'import random\n', 'import string\n']):    FAIL
Test(["a = '2'\n", 'c = a + b\n', 'import random\n', 'import string\n']):       UNRESOLVED
Test(['b = 2\n', 'c = a + b\n', 'import random\n', 'import string\n']): UNRESOLVED
Test(['b = 2\n', "a = '2'\n", 'import random\n', 'import string\n']):   PASS
Test(['b = 2\n', "a = '2'\n", 'c = a + b\n', 'import string\n']):       FAIL
Test(['c = a + b\n', 'import string\n']):       UNRESOLVED
Test(['b = 2\n', "a = '2'\n"]): PASS
Test(["a = '2'\n", 'c = a + b\n', 'import string\n']):  UNRESOLVED
Test(['b = 2\n', 'c = a + b\n', 'import string\n']):    UNRESOLVED
Test(['b = 2\n', "a = '2'\n", 'import string\n']):      PASS
Test(['b = 2\n', "a = '2'\n", 'c = a + b\n']):  FAIL
Test(["a = '2'\n", 'c = a + b\n']):     UNRESOLVED
Test(['b = 2\n', 'c = a + b\n']):       UNRESOLVED
time:
 0.2628598213195801
input size:
 6
output size
 3
querry:
 16
Final Reduced Output -->
 ['b = 2\n', "a = '2'\n", 'c = a + b\n']
```

##### Common Case
```angular2html
Test(['import string\n', 'import random\n', "a = '2'\n", 'b = 2\n', 'a = random.choice(string.ascii_letters)\n', 'c = a + b\n']):       FAIL
random ddmin now starts
Test(['import string\n', 'a = random.choice(string.ascii_letters)\n', 'import random\n', 'b = 2\n', 'c = a + b\n', "a = '2'\n"]):       UNRESOLVED
Test(['b = 2\n', 'c = a + b\n', "a = '2'\n"]):  UNRESOLVED
Test(['import string\n', 'a = random.choice(string.ascii_letters)\n', 'import random\n']):      UNRESOLVED
Test(['a = random.choice(string.ascii_letters)\n', 'import random\n', 'b = 2\n', 'c = a + b\n', "a = '2'\n"]):  UNRESOLVED
Test(['import string\n', 'import random\n', 'b = 2\n', 'c = a + b\n', "a = '2'\n"]):    UNRESOLVED
Test(['import string\n', 'a = random.choice(string.ascii_letters)\n', 'b = 2\n', 'c = a + b\n', "a = '2'\n"]):  UNRESOLVED
Test(['import string\n', 'a = random.choice(string.ascii_letters)\n', 'import random\n', 'c = a + b\n', "a = '2'\n"]):  UNRESOLVED
Test(['import string\n', 'a = random.choice(string.ascii_letters)\n', 'import random\n', 'b = 2\n', "a = '2'\n"]):      UNRESOLVED
Test(['import string\n', 'a = random.choice(string.ascii_letters)\n', 'import random\n', 'b = 2\n', 'c = a + b\n']):    UNRESOLVED
time:
 0.1544780731201172
input size:
 6
output size
 6
querry:
 14
Final Reduced Output -->
 ['import string\n', 'a = random.choice(string.ascii_letters)\n', 'import random\n', 'b = 2\n', 'c = a + b\n', "a = '2'\n"]
```

### Random (every gran-lvl) Output
In each iteration (granularity-level) (not compliment-level), the input sequence is shuffled.
```angular2html
Test(['import string\n', 'import random\n', "a = '2'\n", 'b = 2\n', 'a = random.choice(string.ascii_letters)\n', 'c = a + b\n']):       FAIL
random ddmin now starts
Test(['import string\n', 'import random\n', "a = '2'\n", 'b = 2\n', 'a = random.choice(string.ascii_letters)\n', 'c = a + b\n']):       FAIL
Test(['import string\n', 'b = 2\n', "a = '2'\n"]):      PASS
Test(['import random\n', 'a = random.choice(string.ascii_letters)\n', 'c = a + b\n']):  UNRESOLVED
Test(['a = random.choice(string.ascii_letters)\n', 'c = a + b\n', 'import string\n', 'b = 2\n', 'import random\n']):    UNRESOLVED
Test(["a = '2'\n", 'c = a + b\n', 'import string\n', 'b = 2\n', 'import random\n']):    UNRESOLVED
Test(["a = '2'\n", 'a = random.choice(string.ascii_letters)\n', 'import string\n', 'b = 2\n', 'import random\n']):      UNRESOLVED
Test(["a = '2'\n", 'a = random.choice(string.ascii_letters)\n', 'c = a + b\n', 'b = 2\n', 'import random\n']):  UNRESOLVED
Test(["a = '2'\n", 'a = random.choice(string.ascii_letters)\n', 'c = a + b\n', 'import string\n', 'import random\n']):  UNRESOLVED
Test(["a = '2'\n", 'a = random.choice(string.ascii_letters)\n', 'c = a + b\n', 'import string\n', 'b = 2\n']):  UNRESOLVED
Test(['a = random.choice(string.ascii_letters)\n', 'c = a + b\n', "a = '2'\n", 'import random\n', 'b = 2\n']):  UNRESOLVED
Test(['import string\n', 'c = a + b\n', "a = '2'\n", 'import random\n', 'b = 2\n']):    UNRESOLVED
Test(['import string\n', 'a = random.choice(string.ascii_letters)\n', "a = '2'\n", 'import random\n', 'b = 2\n']):      UNRESOLVED
Test(['import string\n', 'a = random.choice(string.ascii_letters)\n', 'c = a + b\n', 'import random\n', 'b = 2\n']):    UNRESOLVED
Test(['import string\n', 'a = random.choice(string.ascii_letters)\n', 'c = a + b\n', "a = '2'\n", 'b = 2\n']):  UNRESOLVED
Test(['import string\n', 'a = random.choice(string.ascii_letters)\n', 'c = a + b\n', "a = '2'\n", 'import random\n']):  UNRESOLVED
time:
 0.25446510314941406
input size:
 6
output size
 6
querry:
 14
Final Reduced Output -->
 ['import string\n', 'a = random.choice(string.ascii_letters)\n', 'c = a + b\n', "a = '2'\n", 'import random\n', 'b = 2\n']
```

### Observations
The random delta debugging could potentialy improves the quality of reduced program, but the performance is bounded.
Further evaluations should be performed.

### Disclaimer
* Both algorithm implementations are reprodcued as per their publications. (minor tweaks may involve.)

* This project is solely meant to quickly prototype the latest techniques, by no mean of comparing their real-world performance.


