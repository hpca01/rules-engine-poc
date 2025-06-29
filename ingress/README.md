# Ingress Service

This is the service that will handle initial ingress into the solution.

## Initialization

Upon initializing the service always checks to see if tables are there. NOTE: this does not mean that migrations are accounted for, for migrations, we will have to integrate alembic into the mix(TODO).


## Endpoints

POST /new-event
- JSON payload
- details:
    - Queue the message
    - Write record to db table events, and outbox
    - table: received, json_payload
    - return ID

GET /health

GET /status/{item_id}
- details:
    - Query table events by id