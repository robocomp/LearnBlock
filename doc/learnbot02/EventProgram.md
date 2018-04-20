## Tutorial for create a program with events

This type of program have different blocks, these blocks are __when__ blocks, it blocks work like a event, when a condition is __true__ this is execute.

Below is shown how you can create this type of programs.

### Open a example

In folder __learnbot_dsl/learnbotCode/examples/__ there are some examples. We can open the example __follow_red_line_with_events.blockProject__ with the program Learnblock.

![Example follow red line with events](/doc/img/follow_red_line_with_events_en.png)

In order to execute this example you should check the checkbox __Used Events__.

This example have 5 when blocks.

###### No line

This block is executed when the robot don't see the red line.

###### Red line right

This block is executed when the robot see the red line to its right.

###### Red line left

This block is executed when the robot see the red line to its left.

###### Red line center

This block is executed when the robot see the red line to its center.

###### Line crossing

This block is executed when the robot see the red line cross with black line.

### Create your own when block

In Learnblock, with the checkbox __Used Events__ checked, you can push button __Add When__ in control panel.

Then you should choose the type of block and the name of block.

There are two type of blocks:

#### block8

This type need a condition and when condition is __true__ the block is active.

![Imagen block8](/doc/img/block8.png)


#### block10

This type have two functions __Active nameWhen__ and __Deactivate nameWhen__ for active and deactivate the block.


![Imagen block10](/doc/img/block10.png)

Both have a variable with its own the time of execution. It is restart when the block is deactivate and its value is 0.
