# First I want to say


I am from China.

Please email me if this article is not well written or the package has some bug.

My Mail Number : 2119244804@qq.com


# Package


This is a package. You can use

[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)


# RecognitionType


It can take your ***STR*** to other thing, for example, you can take a str to a list.


# Class RecognitionType


First your should `from RecognitionType import RT`

Use `a_object = RT.RecognitionType()` to take a new object.


# The `everyr(content)`


Use `everyr(content)` to take ***STR*** to other thing.

For example:

```
import RT
a_object = RT.rt()
a_v = a_object.everyr('["thing","thing"]')
print(type(a_v), a_v)
```

`>>> <class 'list'> ['thing', 'thing']`

![img_1.png](img_1.png)

And:
 
```
import RT
a_object = RT.RecognitionType()
a_v = a_object.everyr('"thing"')
print(type(a_v), a_v)
```
 
`>>> <class 'str'> thing`


# Other method


`strr(content)`
`intr(content)`
`floatr(content)`
`boolr(content)`
`listr(content)`

For example:
 
```
import RT
a_object = RT.rt()
a_v = a_object.dictr('{"thing_1":1, "thing_2":"thing"}')
print(type(a_v), a_v)
```
 
`>>> <class 'dict'> {'thing_1': 1, 'thing_2': 'thing'}`


# Can't get thing


If the `everyr(codent)` or others can't get thing.

They will return `None`

For example:
 
```
import RT
a_object = RT.rt()
a_v = a_object.dictr('["thing"]')
print(type(a_v), a_v)
```
 
`>>> <class 'NoneType'> None`

Or:
 
```
import RT
a_object = RT.rt()
a_v = a_object.everyr(ddddd)
print(t]ype(a_v), a_v)
```

```
>>> RTError: Can't Return [Return None]
>>> <class 'NoneType'> None
```
 
![img.png](img.png)


# RecognitionTypeVersion


The version is v1.0

Use `rversion()` can get version.


# Update log(Future plans)


v1.0 Can take your STR to other thing
 
v1.1 `dictr` and `tupler`

v1.2 `byter`

v2.0 Use new way to rt