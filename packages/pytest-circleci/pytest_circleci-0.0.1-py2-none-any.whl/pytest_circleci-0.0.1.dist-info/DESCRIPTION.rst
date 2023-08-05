Use CircleCI env vars to determine which tests to run

- CIRCLE_NODE_TOTAL indicates total number of nodes tests are running on
- CIRCLE_NODE_INDEX indicates which node this is

Will run a subset of tests based on the node index.



