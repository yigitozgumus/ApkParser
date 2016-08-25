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
