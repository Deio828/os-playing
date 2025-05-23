# CQRS - Command Query Responsibility Segregation

## 🧩 The Problem CQRS Solves:
In traditional CRUD-based applications, the same data model is used for both reading and writing data. This works fine for small or simple systems, but in complex, high-scale systems, this can lead to:

- Performance bottlenecks: Reads and writes may compete for resources.

- Complex queries: As systems grow, read models often become cluttered with logic meant to accommodate writes.

- Inflexibility: Harder to optimize read operations separately from write operations.

- Coupling: Business logic and query logic are tightly coupled, making the system harder to evolve independently.


## 👀 Example:
If you have a streaming platform like Netflix, where you actually upload a series episode or a movie once every couple of days (so the update of the DB is too slow) and there are thousands of users entering your platform per second (read speed from DB is too high) this will cause a bottleneck. Simply the update process might take minutes to hours to finish and that will cause the system to be unavailable to read from the DB and therefore, not able to serve the clients (You cannot write and read in the DB at the same time).

## 🔧 How CQRS Solves It
CQRS separates the models for reading and writing:

- Writing will go through a fast and simple route (system) with an update server that writes to an image of the DB.
- Reading will go through more complex and scalable system where there will be a load balancer that distributes the request to DB handlers that will then read from a pool of databases images.
- Once the update happens, a trigger event will update the "read databases images" with the updated "write database". 
- This process will go through the swarm of databases one by one to delete the db and replace it with an image of the updated one.
- This will yes cause incosistency in the database swarm where some instances will be updated and some not, but in this business case it's fine as it's not a big deal that the user can't find the new episode now but can find it after 3 minutes or something.

## 🚫 When to Avoid CQRS

1. Simple Systems: Adds unnecessary complexity if your app has modest performance or logic requirements.

2. Low Transaction Volumes: The benefits don't justify the overhead.

3. Small Teams: Requires more discipline and coordination—best for teams familiar with distributed concepts.

