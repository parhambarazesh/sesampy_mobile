# Testing a connector-based multi-tenant configuration

This repository is an example of a multi-tenant configuration with the use of connectors and multiple customer data. 
Todo:
- ~upload the raw multi-tenant config~
- ~modify it so that only one customer components are present (all for now)~
- ~add conditional sources and sinks with embedded test data into the enrich/transform pipes~ (no test data present yet)
- ~extract edge customer components into connectors~
- ~add connector definitions to github~
- ~write script to generate multi tenant subscription~ (present [here](https://github.com/datanav/demo-generator/blob/main/generate_multi_tenant_config.py))

# Known issues
- The current OAuth app registered for the BigQuery API is not publicly available, so the tenant has to re-connect the 
BigQuery connector through the onboarding app every 7 days. If the connector-deployer fails refreshing the access 
token for BigQuery, this should be the first thing to try to get it to work again.