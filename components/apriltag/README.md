```
```
#
``` aprilTag
```
Intro to component here


## Configuration parameters
As any other component,
``` *aprilTag* ```
needs a configuration file to start. In

    etc/config

you can find an example of a configuration file. We can find there the following lines:

    EXAMPLE HERE

    
## Starting the component
To avoid changing the *config* file in the repository, we can copy it to the component's home directory, so changes will remain untouched by future git pulls:

    cd

``` <aprilTag 's path> ```

    cp etc/config config
    
After editing the new config file we can run the component:

    bin/

```aprilTag ```

    --Ice.Config=config

## How to install apriltag library

Install apriltag:

    git clone https://github.com/swatbotics/apriltag.git
    cd /path/to/apriltag
    mkdir build
    cd build
    cmake .. -DCMAKE_BUILD_TYPE=Release
    make -j4
    sudo make install

First append the follow line to /etc/ld.so.conf

    /usr/local/lib

Execute the command:

    sudo ldconfig -v
    
Append the follow line to ~/.bashrc file

    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib

Execute the command

    source ~/.bashrc

Install apriltag with pip

    pip install apriltag