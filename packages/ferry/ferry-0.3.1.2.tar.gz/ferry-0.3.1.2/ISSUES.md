## Ferry Issues

### Investigate

- When using fresh pip install, not installing all the dependencies? 
- ferry install should be "-u" by default? 

### Priority 0

- Warn users if the Ferry version does not match image versions
- Cancel stack not working? 
- Heat server times out too quickly
- Remove "root" server restriction by copying key to appropriate home dir
- Set maximum ssh retries before cancelling stack
- `ferry start -k mykey.pem cassandra` should throw a more helpful error msg
- Sometimes Mongo container fails to start

### Priority 1

- If container uses lxc_opts for networking, do not use "expose" flag
- If ssh asks for password, something has gone wrong, so we should abort
- ferry-base init01.sh should check if 
- Rebuild OpenMPI packages so that we can avoid compiling