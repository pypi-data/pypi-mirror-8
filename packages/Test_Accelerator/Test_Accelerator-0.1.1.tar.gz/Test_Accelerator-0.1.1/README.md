# Test Accelerator


##Intro
Test Acclerator is a tool for use with [ElectricAccelerator](http://electric-cloud.com/products/electricaccelerator/) to accelerate unittests tests. 
How this works is test acclerator parses the unittest source files to deduce the full names
of tests an

##Installation
**Requires >=Python 2.7** 

**Windows**: Make sure Python27/Scripts in your PATH variable.

With the proper permissions run:
```bash
pip install test_accelerator
```

Alternativly you can download and extract the source and then
```bash
python setup.py install
```

 
##Usage
To create the MakeFile run the command  ```ecconvert``` with the following
required arguments:
```
  --framework FRAMEWORK				
  		Name of Framework to Parse
  --testrunner TEST_RUNNER			 
  				Path to the testrunner
  --files FILES, -f FILES			  
  				A comma separated list of files and/or directories to parse unittests
  --test_target TEST_TARGET, -t TEST_TARGET  	
  				The compiled test file. ex. tests.dll
```
These optional arguments can also be used
```
 --pattern PATTERN, -p PATTERN
 			glob pattern for files to search
             default = '*'
  --recursive, -r       
  			Whether to recursively search directory
  			default = False
  --makefile-m MAKEFILE_PATH
  			Path to write makefile to.
              default = MakeFile
  --agent AGENTS, -a AGENTS
  			How many agents are you using.
              default = 1

```
An example call:
```bash   
    ecconvert --framework NUnit --testrunner nunit-console.exe -t foo_tests.dll 
    -f Foo/tests,bartests.cs -r -p *.cs --agents 8
```
Then run emake on the Makefile
```
emake -f Makefile
```

By default NUnit is the only testing framework defined. However other frameworks can easily be added.

##Defining Frameworks
The settings of a testing framework are defined with a dictonary in settings.py  containg four components:


###Nodes
A list of dictonaries defining how to find the full names of a a test suite or test. (How granular we want to go is up to how many nodes we put in the list)

Consider this example of NUnit code.
```cs
namespace Foo{
	[TestFixture]
	public class CalcTests{
    
    	[Test]
        public void addTest() {
        	Assert.areEqual(4,2+2};
            }
}

```
To run the test fixture CalcTests we would need to call:
```
nunit-console /run=Foo.CalcTests tests.dll 
``` 

High level, we want to define the nodes to create a unary tree structred as
```
namespace
	|
    |
TestFixture
```
So we can traverse the (albeit small) tree where the leaf is the full name.

Here's an example for the nodes to parse for NUnit testfixtures.

```python
"nodes":[{'depth': 0, 'initial': lambda text: replace(text, re.sub(r'namespace(. ?)', '', text))}
{'depth': 1, 'initial': lambda text: re.search('\[TestFixture.*\]', text),
 'after': lambda text: c_class(text)}]
```
where replace and c_class are helper functions.
```python
def c_class(text):
	""" Isolates clang class names"""
    if re.search(r'class', text):
        return  re.sub(r'[-(<: ].*', '', re.sub(r'.*class(. ?)', '', text))
    return None


replace = lambda text, substitute: substitute if substitute != text else None

```

Let's keep this example in mind when we talk about the components of a Node.


####depth
this is the position in the tree with the root starting at 0 and increasing.
So the depth for the TestFixture node is 1.

####initial
A lambda function that determines if the line in a file is a match. 
If the inital match is the only match we're looking for the lambda must 
return the a new string if there's a match.
In the case of the namespace node.
```python
nodes[0]["initial"]("namespace Foo")
> Foo
```
If you're only intersted in getting the line after the inital match
the lambda can merely return ``True`` if a match exists.

####after
As alluded to in the tail end of the last section, this is for checking the line after the inital match in the exact same fashion.
This is useful for cases like the test fixtures where the signifier is before the part we're interested in like so.
```
[TestFixture]
public class CalcTests
```
The inital match resolves to true so it will check the next line for a match.
```python
nodes[1]["after"]("public class CalcTests")
>CalcTests
```

There can be any number >=1 as desired, the search we yield all the results of a full tree traversal; the combined strings of each node to the leaf.
Which in our example would be ```Foo.CalcTests```
###Strip
A boolean whether we want to strip the lines of a file when searching for matches.
###Command
A string of the command used in the console to run a subset of tests with 
the format variables ```suite``` and ```test_file```
The NUnit example:
```python
"command": /run={suite} /nologo {test_file}
```
###Makefile
The makefile template to be used for the test framework. These are defined and imported from ``makefile_templates.py``. The NUnit example:
```python
from makefile_templates import gnu_makefile

"makefile":gnu_makefile
```
###Installing Frameworks
To install the a new framework assign the dictonary to a variable then add a name, value pair to INSTALLED_FRAMEWORKS in settings.py
```python
NUnit = {
    'nodes': [
        {'depth': 0, 'initial': lambda text: replace(text, 
        re.sub(r'namespace(. ?)', '', text))},
        {'depth': 1, 'initial': lambda text: re.search('\[TestFixture.*\]', text),
         'after': lambda text: c_class(text)}
    ],
    'command': '/run={suite} /nologo {test_file}',
    'strip': True,
    'makefile': gnumake_template,
}

INSTALLED_FRAMEWORKS = {"NUnit":NUnit}

```

