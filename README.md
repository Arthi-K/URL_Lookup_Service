# URL_Lookup_Service
A web service implemented usinh Python Flask and Redis Cache, that responds to GET requests where the caller passes in a URL and the service responds with some information about that URL. The GET requests would look like this:
GET /v1/urlinfo/{resource_url_with_query_string}
The caller wants to know if it is safe to access that URL or not. 

## Requirements: 
python3 
pip 
Redis server 

### Setup Instructions 
**Clone the project from the git repository and run the following command in the directory where the project exists: **
 ```pip install -r requirements.txt```  

## Commands to run
**To run the flask app, go to the src folder and run the command:**
```python3 -m flask run```

**To start Redis server on Mac, you can use Homebrew:**
```brew services start redis```

**To run the unit tests for the app:**
 python3 -m pytest test/app_tests.py

**To insert malware URL into the DB, type the URL and content in the textboxes:**
http://127.0.0.1:5000/create/

**To view the lists of malware URL:** 
http://127.0.0.1:5000/

**To check if an URL is malware or not:**
http://127.0.0.1:5000/v1/urlinfo/https://th-track-thailandpost.com/business/solutions/products/standard

**To delete an URL from the DB:**
http://127.0.0.1:5000/delete/https://ems-spotifyth.com/login/portal-delivery/ErvPso

**To stop Redis server on Mac, you can use Homebrew:**
```brew services stop redis```

The screenshots for the above calls can be found in the assets folder

## Design Considerations: 
**The size of the URL list could grow infinitely, how might you scale this beyond the memory capacity of the system?**

We can shard the data in multiple tables/database servers by hashing each URLs and partitioning horizontally based on alphabet ranges. This would help us locate the database quickly when we partition it based on a partiion key. We could also use consistent hashing to futher distribute the load evenly to avoid hotspot servers. This would be helpful even if we want to add more servers in the future with minimal data transfers between database servers.

**The number of requests may exceed the capacity of this system, how might you solve that?**

We can cache frequently accessed URLs using DB cache like Redis/Memcached, which I have implemented in this project with Redis. This would decrease the number of queries made to the web server and database server. Further in order to scale, we can use pool of servers to distribute the requests evenly with help of a load balancer and ensure that load is balanced. We could also containarize the web servers and use memory and CPU efficiently to scale better. 

**What are some strategies you might use to update the service with new URLs? Updates may be as many as 5000 URLs a day with updates arriving every 10 minutes.**

We can setup a seperate microservice to ingest new URL's and run this bulk insert as a cron job every 10 minutes. Another approach is to update as and when using a seperate insertion API (which I have implemented) to POST new URLs into the DB but that depends on business requirement if insertion can be done with some latency.
