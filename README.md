# Facebook to Redshift

Note: This uses Python3.


## Installation
1. Clone this repo
2. Create a virtualenv and activate it

  `virtualenv venv`
  
  `. venv/bin/activate`
3. Install requirements

  `pip install -r requirements.txt`
  
  a. If you don't already have postgresql-devel installed, you'll need to run `yum install python-devel postgresql-devel` first or else you'll get an error like `pg_config executable not found` when pip tries to install psycopg2.
  
4. Create settings.py (using settings.py.example as a template). 

  a. If you haven't already, you will need to [register a Facebook app](https://developers.facebook.com/docs/apps/register) and [associate it with the page](http://stackoverflow.com/questions/9265062/how-to-link-a-facebook-app-with-an-existing-fan-page) you're looking to pull data for. You will need to also be an administrator of the page for this to work.
    i. To get your long access token, first go to [Facebook's Graph API Explorer](https://developers.facebook.com/tools/explorer) and make sure it is associated with your app (top right drop down).
    ii. Get your user access token, ensuring `manage_pages` and `read_insights` are both selected as permissions.
    iii. Add your user access token in as the value in the variable `user_access_token` in `get_long_lived_token()` in fb.py.
    iv. Uncomment line #67 (`# get_page_access_token_from_user_token(get_long_lived_token()`), and in your virtual env, run `python fb.py`.
    v. Add the output of the script to settings.py as your `fb_long_token`. This never expires, so you're good to go!
    vi. Recomment or delete line #67. 

  
  b. You will also need to have [created a Redshift database](http://docs.aws.amazon.com/redshift/latest/dg/t_creating_database.html), and have your [AWS IAM credentials](https://aws.amazon.com/iam/). Make sure to create a table in the schema `facebook`, named `posts`. 
    
    `CREATE TABLE facebook.posts(post_id VARCHAR(256) PRIMARY KEY, message VARCHAR(max), created_time timestamp, likes INT, shares INT, comments INT, total_reach INT);`
    
  c. You'll also need to have [created a bucket in s3](http://docs.aws.amazon.com/gettingstarted/latest/swh/getting-started-create-bucket.html).
  
5. Run the script! Note: This script can take a *long time* to run, due to pagination, if the page you're pulling posts from has a lot of posts.
  
  `python fb_to_redshift.py`
