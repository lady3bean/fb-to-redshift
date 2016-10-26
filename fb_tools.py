#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Prepare the data for import. Import it into s3 and then into redshift.
"""

from redshift import rsm
from fb import get_posts_and_interactions, get_total_reach, get_video_stats, get_video_time_series
from settings import aws_access_key, aws_secret_key, s3_bucket
import boto
import csv

def create_import_file(interval=False, import_type='posts', filename='fb_import_posts.csv', list_id = None):
    import_file = open(filename, 'w')
    if import_type == 'posts':
        data_dict = get_total_reach(get_posts_and_interactions(interval))
    if import_type == 'videos':
        data_dict = get_video_stats(interval)
    if import_type == 'video_lab_videos':
        data_dict = get_video_stats(interval, True, list_id)
    if import_type == 'time_series':
        data_dict = get_video_time_series()
    csv_file = csv.writer(import_file, quoting=csv.QUOTE_MINIMAL)
    csv_file.writerows([[id,]+values for id, values in data_dict.items()])
    import_file.close()

def upload_to_s3(filename='fb_import_posts.csv'):
    conn = boto.connect_s3(aws_access_key, aws_secret_key)
    bucket = conn.lookup(s3_bucket)
    k = boto.s3.key.Key(bucket) 
    k.key = filename
    k.set_contents_from_filename(filename)

def update_redshift(table_name, columns, primary_key, filename):
    staging_table_name = table_name + "_staging"
    column_names = ", ".join(columns)
    columns_to_stage = ", ".join([(column + " = s." + column) for column in columns ])
    table_key = table_name + "." + primary_key
    staging_table_key = "s." + primary_key

    command = """-- Create a staging table 
CREATE TABLE %s (LIKE %s);

-- Load data into the staging table 
COPY %s (%s) 
FROM 's3://%s/%s' 
CREDENTIALS 'aws_access_key_id=%s;aws_secret_access_key=%s'
FILLRECORD
delimiter ','; 

-- Update records 
UPDATE %s
SET %s
FROM %s s
WHERE %s = %s; 

-- Insert records 
INSERT INTO %s 
SELECT s.* FROM %s s LEFT JOIN %s 
ON %s = %s
WHERE %s IS NULL;

-- Drop the staging table
DROP TABLE %s; 

-- End transaction 
END;"""%(staging_table_name, table_name, staging_table_name, column_names, s3_bucket, filename, aws_access_key, aws_secret_key, table_name, columns_to_stage, staging_table_name, table_key, staging_table_key, table_name, staging_table_name, table_name, staging_table_key, table_key, table_key, staging_table_name )

    rsm.db_query(command)