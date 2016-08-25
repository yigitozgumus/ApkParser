# ApkParser

### Using Config
In your config, you will be seeing something like this:

```
[B1]  
resConfigs = en, tr

[B5]  
minSdkVersion = 16

...
```

* To add more than one items like in **[B1]**, use **' , '** to seperate items.  
* For others, you can just change the value. For example in **[B5]** you can change your **minSdkVersion** into 19 by changing B5 into:  
```
[B5] 
minSdkVersion = 19
```

**Warning**: you should not delete any of the sections in the default configuration file, otherwise the program will crash.

### Command Line Parameters

 There are 3 parameters that the script uses. You can use -h option to see the parameter tags and their description like below:
``` bash 
python initializer.py -h
usage: initializer.py [-h] [-d [DIR]] [-c [CONFIG]] [-a [APK]] [-t TASKS]

optional arguments:
  -h, --help            show this help message and exit
  -d [DIR], --dir [DIR]
                        Directory location
  -c [CONFIG], --config [CONFIG]
                        Config File Location
  -a [APK], --apk [APK]
                        Apk Location
  -t TASKS, --tasks TASKS
                        Optional task file to import check functions
```

### Test functions

Tests of the Checklist are divided into 2 files. *yigit.py* and *berker.py* .  
Each contains a Checklist class and relevant test functions.
You can call __execute_test_batch()__ function after initializing the Checklist object to run all the tests or 
you can call the tests from the initialized object individually.

* Executing all tests
```python
 test_results = self.checklist_yigit.execute_test_batch(config_location)
```
* Executing individual tests
```python
  man1_result = self.checklist_yigit.man1()
  # Some tests require extra parameters so you need to parse the configuration file
  config = ConfigParser.ConfigParser()
  config.read(config_location)
  proguardList = config.get('PRG3', 'proguardList')
  prg3_result = self.checklist_yigit.prg3(proguardList)
```
