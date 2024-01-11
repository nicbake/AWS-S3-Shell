# Libraries
import configparser
import os
import sys
from pathlib import Path
import boto3
from botocore.exceptions import ClientError

# This holds all my personal functions I made extra for the program
from functions import *

# This will allow you to use the arrow keys on the shell
import readline

# Program Information
# Author: Nicholas Baker
# Email: nbaker05@uoguelph.ca
# Student ID: 1100494
# Status: Complete

# Global for holding the current directory
__current_directory__ = '/'

def shell_cli(s3,s3_res, user_input): # This is the shell function and deals with the I/O of the program
    # This will have it so the user has a variety of ways to close the program
    if ((user_input.strip()).lower() == 'exit' or (user_input.strip()).lower() == 'quit' or (user_input.strip()).lower() == 'q'):

        sys.exit()
    # This will split the input by the spaces
    user_token = user_input.split(" ")

    if (user_token[0] in functions_dictionary):
        # This will check the input against a s3 command
        functions_dictionary[user_token[0]](s3,s3_res, user_token)

    elif (user_token[0] == 'cd'):

        if (len(user_token) == 1):
            # If you just enter cd then it will send the local to the root directory
            try:
                os.chdir("/")
            except OSError as err_msg:
                print(err_msg)
        else:
            # This will send the user to the entered directory
            try:
                os.chdir(user_token[1])
            except OSError as err_msg:
                print(err_msg)
    else:
        # This will send any other command to the linux or os
        os.system(user_input)
    
    return
    
def locs3cp(s3,s3_res, user_input): # This function will upload a file from local
    bucket_name = get_bucket_name_func(user_input[2])

    # Error testing of the function
    if (len(user_input) > 3):
        print("Error: Too many arguments")
        return 1

    if (len(user_input) < 3):
        print("Error: Too little arguments")
        return 1

    if (does_bucket_exist(s3_res, bucket_name) == False):
        print("Error: Bucket doesnt exist")
        return 1

    if (os.path.exists(user_input[1]) == False):
        print("Error: That local directory doesnt exist")
        return 1

    # Upload the file from local
    local = Path(user_input[1])
    cloud = '/'.join(Path(user_input[2]).parts[2:])

    try:
        s3_res.Bucket(bucket_name).upload_file(local,cloud)
    except ClientError:
        print("Error: Failed to copy local file to cloud")
        return 1

    return 0

def s3loccp(s3,s3_res, user_input): # This will download a file from the cloud to local
    # Error checking
    if (len(user_input) > 2):
        print("Error: Too many arguments")
        return 1

    if (len(user_input) < 2):
        print("Error: Too little arguments")
        return 1
    
    bucket_name = get_bucket_name_func(user_input[1])
    num = len(user_input)
    local = Path(user_input[2])

    # This will parse through the arguments to get the expected paths
    if (num == 3):

        if (does_start_with_slash(user_input[1]) == True):
            cloud = '/'.join(Path(user_input[1]).parts[2:])
        else:
            cloud = __current_directory__ + '/' + user_input[1]
            if (does_directory_exist(s3_res,cloud) == False):
                print("Error: That cloud directory doesnt exist")
                return 1
        
    elif (num == 2):
        cloud = __current_directory__
    else:
        print("Error: Not enough arguments")
        return 1

    # Downloads the file
    try:
        s3_res.Bucket(bucket_name).download_file(cloud,local)
    except ClientError:
        print("Error: Failed to copy cloud file to local")
        return 1

    return 0

def create_bucket(s3,s3_res, user_input): # This function will create a new bucket in the cloud environment
    # Error checking
    if (len(user_input) > 2):
        print("Error: Too many arguments")
        return 1

    if (len(user_input) < 2):
        print("Error: Too little arguments")
        return 1

    if (does_bucket_exist(s3_res, user_input[1]) == True):
        print("Error: Failed to create bucket, that bucket name already exists")
        return 1
    
    # Get the name of the bucket
    path = get_bucket_name_func(user_input[1])

    # Create the bucket in the cloud
    try:
        s3_res.create_bucket(Bucket=path, CreateBucketConfiguration={'LocationConstraint': 'ca-central-1'})
    except ClientError:
        print("Error: Failed to create bucket")
        return 1

    return 0

def create_folder(s3,s3_res, user_input): # This function will create a new folder within the cloud
    # Error checking
    if (len(user_input) > 2):
        print("Error: Too many arguments")
        return 1

    if (len(user_input) < 2):
        print("Error: Too little arguments")
        return 1

    # This is deciding if we search from root or relative
    if (does_start_with_slash(user_input[1]) == True):
        bucket_name = get_bucket_name_func(user_input[1])
        if (does_bucket_exist(s3_res, bucket_name) == False):
            print("Error: Bucket doesnt exist")
            return 1
        directory = '/'.join(Path(user_input[1]).parts[2:]) + '/'
    else: # This is the search from relative so current directory
        path = __current_directory__ + '/' + user_input[1]
        if (does_directory_exist(s3_res,path) == False):
            print("Error: That cloud directory doesnt exist")
            return 1
        bucket_name = get_bucket_name_func(path)
        if (does_bucket_exist(s3_res, bucket_name) == False):
            print("Error: Bucket doesnt exist")
            return 1
        directory = '/'.join(Path(path).parts[2:]) + '/'

    # Creates a new folder within the cloud
    try:
        s3.put_object(Bucket=bucket_name, Body='', Key=directory)
    except ClientError:
        print("Error: Failed to create directory")
        return 1

    return 0

def chlocn(s3, s3_res, user_input): # This function will change the current directory in the cloud
    global __current_directory__

    if (user_input[1] == '/' or user_input[1] == '~'): # This is for the situation where we are heading back to root
        __current_directory__ = "/"
    
    elif ('..' in user_input[1] or '../' in user_input[1]): # This is for when you want to go back a directory or more

        path = __current_directory__
        count = user_input[1].count("..")
        num = len(Path(path).parts)

        if count >= num:
            print("Error: Cannot go that many directories back")
            return 1

        if (count > 1):
            tmp = '/'.join(Path(path).parts[:num-count])
        else:
            tmp = '/'.join(Path(path).parts[:num-1])

        if (tmp != '/'):
            tmp = tmp[:-1]
        __current_directory__ = tmp
    
    elif (does_start_with_slash(user_input[1]) == True): # This is for a path from root

        num = how_many_slash(user_input[1])
        bucket_name = get_bucket_name_func(user_input[1])
        if (does_bucket_exist(s3_res, bucket_name) == False):
            print("Error: The bucket specified doesnt exist")
            return 1
        if (num == 1): # This means root to bucket
            __current_directory__ = user_input[1]
        else:
            if (does_directory_exist(s3_res,user_input[1]) == False):
                print("Error: directory doesnt exist")
                return 1
            __current_directory__ = user_input[1]

    else: # This is for a path from reletive location

        if (__current_directory__ == "/"): # This means we are currently at root and will just add the relative locations
            path = __current_directory__ + user_input[1]
            bucket_name = get_bucket_name_func(user_input[1])

            if (does_bucket_exist(s3_res, bucket_name) == False):
                print("Error: The bucket specified doesnt exist")
                return 1

            if ((path.count('/')) > 0):
                if (does_directory_exist(s3_res,path) == False):
                    print("Error: directory doesnt exist")
                    return 1
                __current_directory__ = path
            else:
                __current_directory__ = path
        else: # This means we are not a root and need to add a / to connect for the string

            path = __current_directory__ + '/' + user_input[1]
            if ((path.count('/')) > 0):
                if (does_directory_exist(s3_res,path) == False):
                    print("Error: directory doesnt exist")
                    return 1
                __current_directory__ = path
            else:
                __current_directory__ = path
    return 0

def cwlocn(s3,s3_res,user_input): # This function will print out the current cloud directory
    if (__current_directory__ != None):
        print(__current_directory__)
        return 0
    print("Error: the current directory is empty")
    return 1

def list_func(s3,s3_res,user_input): #This one will change when current directory is complete
    
    if (len(user_input) > 3):
        print("Error: Too many arguments")
        return 1
    
    if (len(user_input) == 1): # This is if list is said on its own

        if (__current_directory__ == '/'): # currently located at root
            print_all_buckets(s3_res)
        else: # currently located past root
            print_all_objects(s3_res,__current_directory__)

    elif (len(user_input) == 2): # This is for if there is another argument with root

        if (user_input[1] == '/' or user_input[1] == '~'):# This works for if the user enters / or ~
            print_all_buckets(s3_res)
        elif (user_input[1] == "-l" and __current_directory__ == '/'): # This works for if the current directory is /
            print_all_buckets_long(s3_res)
        elif (user_input[1] == "-l"): # This is if we want to look at the current directory long
            print_all_objects_long(s3_res,__current_directory__)
        elif (does_start_with_slash(user_input[1]) == False): # This is for if they with to look relatively in the current directory
            path = __current_directory__ + '/' + user_input[1]
            if (does_directory_exist(s3_res,path) == False):
                print("Error: That cloud directory doesnt exist")
                return 1
            print_all_objects(s3_res,__current_directory__)
        else: # This is list /path
            print_all_objects(s3_res,user_input[1])


    elif (len(user_input) == 3): # This is for if there are 3 arguments

        if ((user_input[2] == '/' or user_input[2] == '~') and user_input[1] == '-l'): # this is for if we want to go back too root
            print_all_buckets_long(s3_res)
        elif ((user_input[2] != '/' or user_input[2] != '~') and user_input[1] == '-l' and does_start_with_slash(user_input[2]) == True): # This is long and looking from root
            print_all_objects_long(s3_res,user_input[2])
        else: # This is long and looking relative
            path = __current_directory__ + '/' + user_input[1]
            if (does_directory_exist(s3_res,path) == False):
                print("Error: That cloud directory doesnt exist")
                return 1
            print_all_objects_long(s3_res,__current_directory__)


    return 0

def s3copy(s3,s3_res,user_input): # This copys one object to another location within the cloud

    # This error check handles the arguments
    if (len(user_input) > 3):
        print("Error: Too many arguments")
        return 1

    if (len(user_input) < 3):
        print("Error: Too little arguments")
        return 1

    # Source bucket
    if (does_start_with_slash(user_input[1]) == True): # This works for starting from root
        src_bucket_name = get_bucket_name_func(user_input[1])
        if (does_bucket_exist(s3_res, src_bucket_name) == False):
            print("Error: Source Bucket doesnt exist")
            return 1
        src_directory = '/'.join(Path(user_input[1]).parts[2:])
    else: # This works for relative
        path = __current_directory__ + '/' + user_input[1]
        if (does_directory_exist(s3_res,path) == False):
            print("Error: Source cloud directory doesnt exist")
            return 1
        src_bucket_name = get_bucket_name_func(path)
        if (does_bucket_exist(s3_res, src_bucket_name) == False):
            print("Error: Source Bucket doesnt exist")
            return 1
        src_directory = '/'.join(Path(path).parts[2:])

    # Destination bucket
    if (does_start_with_slash(user_input[1]) == True): # This works for starting from root
        dest_bucket_name = get_bucket_name_func(user_input[2])
        if (does_bucket_exist(s3_res, dest_bucket_name) == False):
            print("Error: Destination Bucket doesnt exist")
            return 1
        dest_directory = '/'.join(Path(user_input[2]).parts[2:])
    else: # This works for relative
        path = __current_directory__ + '/' + user_input[2]
        if (does_directory_exist(s3_res,path) == False):
            print("Error: Destination cloud directory doesnt exist")
            return 1
        dest_bucket_name = get_bucket_name_func(path)
        if (does_bucket_exist(s3_res, dest_bucket_name) == False):
            print("Error: Destination Bucket doesnt exist")
            return 1
        dest_directory = '/'.join(Path(path).parts[2:])

    copy_directory = {
        'Bucket': src_bucket_name,
        'Key': src_directory
    }
    
    # copies the object from the cloud src to another location within the cloud
    try:
        s3_res.meta.client.copy(copy_directory,dest_bucket_name,dest_directory)
    except:
        print("Error: Failed to copy object")
        return 1
    return 0

def s3delete(s3,s3_res,user_input): # This deletes an object from the cloud

    # Error checking for arguments
    if (len(user_input) > 2):
        print("Error: Too many arguments")
        return 1

    if (len(user_input) < 2):
        print("Error: Too little arguments")
        return 1

    if (does_start_with_slash(user_input[1]) == True): # This works for starting from root
        bucket_name = get_bucket_name_func(user_input[1])
        if (does_bucket_exist(s3_res, bucket_name) == False):
            print("Error: Bucket doesnt exist")
            return 1
        directory_key = '/'.join(Path(user_input[1]).parts[2:])
    else: # This works for relative
        path = __current_directory__ + '/' + user_input[1]
        if (does_directory_exist(s3_res,path) == False):
            print("Error: That cloud directory doesnt exist")
            return 1
        bucket_name = get_bucket_name_func(path)
        if (does_bucket_exist(s3_res, bucket_name) == False):
            print("Error: Bucket doesnt exist")
            return 1
        directory_key = '/'.join(Path(path).parts[2:])

    # Deletes the object from the cloud
    try:
        s3_res.Object(bucket_name,directory_key).delete()
    except ClientError:
        print("Error: Failed to delete directory")
        return 1

    return 0

def delete_bucket(s3,s3_res,user_input):
    # Error checking the arguments
    if (len(user_input) > 2):
        print("Error: Too many arguments")
        return 1

    if (len(user_input) < 2):
        print("Error: Too little arguments")
        return 1

    #Get the name of the bucket
    bucket_name = get_bucket_name_func(user_input[1])

    # Error check if the bucket exists
    if (does_bucket_exist(s3_res,bucket_name) == True):
        print("Error: Bucket doesnt exist")
        return 1

    # Delete the bucket from the cloud
    try:
        s3_res.Bucket(bucket_name).delete()
    except ClientError:
        print("Error: Failed to delete bucket")
        return 1
    return 0

# This will be a dictionary to hold all the s5 shell functions for assignment
functions_dictionary = {
    'locs3cp': locs3cp,
    's3loccp': s3loccp,
    'create_bucket': create_bucket,
    'create_folder': create_folder,
    'chlocn': chlocn,
    'cwlocn':cwlocn,
    'list': list_func,
    's3copy': s3copy,
    's3delete': s3delete,
    'delete_bucket': delete_bucket
}

def main():
    # Connect to the AWS with the S5-S3.conf file
    config = configparser.ConfigParser()
    config.read("S5-S3.conf")
    aws_access_key = config['default']['aws_access_key_id']
    aws_secret_key = config['default']['aws_secret_access_key']

    # Welcome to the shell message
    print("Welcome to the AWS S3 Storage Shell (S5)")

    try:
        # Attempt to connect to the system
        session = boto3.Session(
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
        s3 = session.client('s3')
        s3_res = session.resource('s3')
        print("You are now connected to your S3 storage")
    except ClientError:
        # Failed to connect to the system
        print("You could not be connected to your S3 stoage")
        print("Please revice procedures for authentication your account on AWS S3")
        sys.exit()

    # Infinite loop for the shell and the I/O of the program
    while True:
        # This will have the shell show the current local directory of focus
        current_directory = os.getcwd() + ' s5> '
        # Shell functionality of the program 
        shell_cli(s3,s3_res,input(current_directory))

main()