# Comparison-ddmin-probdd

### Input program
```angular2html
import string
import random
a = '2'
b = 2
a = random.choice(string.ascii_letters)
c = a + b
```
This piece of code carefully designed to show off 
the claimed advatange of ProbDD. 

ProbDD removes elements in a "smart" order,
whereas ddmin carries out in a fixed order.

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
ProbDD keeps a dictionary (`map[ element ] = prob`), and this `prob` guides the variant generation.
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
Note that the initial probability does affect the result to some extents,
though its effect may be negligible when input program is large.
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

### Random (every iter) Output
I further implemented this version of random ddmin.
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