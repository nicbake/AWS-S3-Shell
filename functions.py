# Libraries
import boto3
import os
import json
from botocore.exceptions import ClientError
from pathlib import Path

# Program Information
# Author: Nicholas Baker
# Email: nbaker05@uoguelph.ca
# Student ID: 1100494
# Status: Complete

def get_bucket_name_func(path): # This will get the name of the bucket
    if (path[0] == '/' and len(Path(path).parts) != 1):
        return Path(path).parts[1]
    return Path(path).parts[0]

def does_bucket_exist(s3, user_bucket): # This will check to see if a bucket exists
    if ((s3.Bucket(user_bucket) in s3.buckets.all()) == False):
        return False
    return True

def does_start_with_slash(path): # This will check if the path starts with a slash
    if (path[0] == '/'):
        return True
    return False

def how_many_slash(path): # This will count how many slashes there are
    return path.count('/')

def does_directory_exist(s3,path): # This will check if the given path to a object exists
    bucket_name = get_bucket_name_func(path)
    directory = '/'.join(Path(path).parts[2:])
    try:
        for object in s3.Bucket(bucket_name).objects.all():
            
            if(directory in object.key.strip("/")):
                return True
    except ClientError:
        return False
    return False

def print_all_buckets(s3): # This will print all the buckets within the root of the cloud
    for bucket in s3.buckets.all():
        print(bucket.name)

def print_all_buckets_long(s3): # This will print all the bcukets in root long
    for bucket in s3.buckets.all():
        size = "%d" %int(sum([object.size for object in s3.Bucket(bucket.name).objects.all()])/1000/1024)
        type = s3.BucketAcl(bucket.name).grants[0]['Grantee']['Type']
        perm = s3.BucketAcl(bucket.name).grants[0]['Permission']
        date = bucket.creation_date
        name = bucket.name
        print(str(perm) + "\t" + str(type) + "\t" + str(size) + "\t" + str(date) + "\t" + str(name))
        
def print_all_objects(s3,path): # This will print all objects in the given path
    bucket_name = get_bucket_name_func(path)
    directory = '/'.join(Path(path).parts[2:]) + '/'

    if (directory == '/'):
        my_bucket = s3.Bucket(bucket_name)
        for bucket in my_bucket.objects.all():
            print(bucket.key)
    else:
        for object in s3.Bucket(bucket_name).objects.filter(Prefix=directory):
            if (len(Path(object.key).parts) > 1):
                print(Path(object.key).name)

def print_all_objects_long(s3,path): # This will print all the given objects in the given path long
    
    bucket_name = get_bucket_name_func(path)
    directory = '/'.join(Path(path).parts[2:]) + '/'
    
    if (directory == '/'):
        my_bucket = s3.Bucket(bucket_name)
        for object in my_bucket.objects.all():
            size = object.size
            size = "%d" %int(size/1000/1024)
            type = s3.ObjectAcl(bucket_name, object.key).grants[0]['Grantee']['Type']
            perm = s3.ObjectAcl(bucket_name, object.key).grants[0]['Permission']
            date = object.last_modified
            name = Path(object.key).name
            print(str(perm) + "\t" + str(type) + "\t" + str(size) + "\t" + str(date) + "\t" + str(name))
    else:
        for object in s3.Bucket(bucket_name).objects.filter(Prefix=directory):
            if (len(Path(object.key).parts) > 1):
                size = object.size
                size = "%d" %int(size/1000/1024)
                type = s3.ObjectAcl(bucket_name, object.key).grants[0]['Grantee']['Type']
                perm = s3.ObjectAcl(bucket_name, object.key).grants[0]['Permission']
                date = object.last_modified
                name = Path(object.key).name
                print(str(perm) + "\t" + str(type) + "\t" + str(size) + "\t" + str(date) + "\t" + str(name))