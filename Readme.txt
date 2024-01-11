Program Information
Author: Nicholas Baker
Email: nbaker05@uoguelph.ca
Student ID: 1100494
Status: Complete

Assignment: 1

Required files:
- s5.py
- functions.py
- S5-S3.conf

Run the Program: To run the Program you will need to have the versions specified in the Requirments.txt file

To actually start running the shell you can do:
- "python3 ./s5.py"
- "python ./s5.py"

Normal Behaviors: My shell will run the same as a normal bash os shell and will be able to perform all the functions
within the assignment description
- Another extra bit is that in the line "S5>" the current local directory will be before the "S5>" so like a "pwd S5>"

Limitations: From my time working on this shell I have found no limitations that cant be done based off the assignment description
- Make sure to have a S5-S3.conf!!!

Commands within the shell: All os builtin Commands
- locs3cp
    "S5> locs3cp catpictures/mycat01.jpg /cis4010b01/images/cats/mycat.jpg"

- s3loccp
    "S5> chlocn /CIS4010b01/images"
    "S5> s3loccp cats/mycat.jpg catpic001.jpg"

- create_bucket
    "S5> create_bucket /cis4010b01"

- create_folder
    "S5> create_folder /cis4010b01/images"
    "S5> create_folder /cis4010b01/images/cats"
    "S5> chlocn /cis4010b01"
    "S5> create_folder images"
    "S5> chlocn images"
    "S5> create_folder cats"

- chlocn
    "S5> chlocn /cis4010b01"
    "S5> chlocn /cis4010b01/images/cats"
    "S5> chlocn /cis4010b01"
    "S5> chlocn /images/cats"
    "S5> chlocn / or chlocn ~"
    "S5> chlocn .. and chlocn ../.."

- cwlocn
    "S5> cwlocn"
    "/"
    "S5> chlocn /cis4010b01/images"
    "S5> cwlocn"
    "/cis4010b01/images"
    "S5> chlocn cats"
    "S5> cwlocn"
    "/cis4010b01/images/cats"

- list
    "S5> list /cis4010b01"
    "S5> list -l /cis4010b01/images/cats"
    "S5> list /"
    "S5> chlocn /cis4010b01"
    "S5> list -l"

- s3copy
    "S5> s3copy /cis4010b01/images/cats/pichappycat.png pic001.png"
    "S5> s3copy pic001.png /cis4010b1/backups/pic001.png"

- s3delete
    "S5> s3delete /cis4010b01/images/cats/pic001.png"
    "S5> s3delete pic001.png"
    "S5> s3delete /cis4010b01/images/cats"

- delete_bucket
    "S5> delete_bucket /cis4010b01"

All the commands listed above work based on the assignment description!