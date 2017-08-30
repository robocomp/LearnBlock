
# About Learnblock.

Learnblock is a project to teach children how to program a robot.


This project have a similar IDE to Scratch.The program, that is created by children, is composed of a set of blocks, in a certain order. These blocks represent functions, conditions, variables and operatros. Also, the user can add new funtions and created new variables and new funtions.

Below explained the steps to follow to program the Learnbot with tis IDE:

## Run LearnBlock

For run this IDE you should execute the follow lines:

    $ chmod +x startLearnblock
    $ ./startLearnblock

## Simple program

With this code the LearnBot follow the red lines.

![Program for the LearnBot follow the red lines](img/follow_red_line.png)

## Use of variables

For use a variable in the program, the user should declare a variable. These variables can use as params of a block. Also, the user can delete a variable of his code.

In the next video show a example for use a variable in the code.

[![Tutorial about how create a variables and how use these](http://img.youtube.com/vi/yHtW8mTa4B0/0.jpg)](https://www.youtube.com/watch?v=yHtW8mTa4B0 "Tutorial - how create and use a variable - LearnBlock")

## Add functions to IDE

For add a new functions to IDE, the user should complete the next form.

The user can selected diferents blocks and add difrents variables.

![Form for create new block](img/form_new_block.png)

## Create and used a new functions

Create a functions is similar to create a variable,The first step is declare the function, after, complete the function and finaly, use the function.

## Save and Open a project

The user can save and open project, for this the user should click in the next buttons.

![Bottons for save and open project](img/save_and_open.png)

## Add Number or String

The user can create Number or String with this buttons:

![Bottons for add Number or String](img/addNumberOrString.png)

# Examples

In this repository there are 4 examples:

1. follow_black_line.blockProject
2. follow_red_line_with_method.blockProject
3. follow_black_line_and_stop_counter.blockProject
4. follow_lines_and_change_of_line_with_method_and_variable.blockProject

This examples can open with this IDE.

# Importam

In order to use Learnblock, you must first install learnbot, for this you should execute the following lines.

    $ cd learnbot/
    $ sudo python setup.py install

For run this IDE you should run the robocomp simulator rcis

The XML to run is

    learnbot/learnbot-simulator/learnBotWorldDSL_lines.xml

You must install robocomp from:

[Repository of Robocomp](https://github.com/robocomp/robocomp)
