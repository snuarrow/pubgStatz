#!/bin/bash
echo 'specify file location!'
exit
pg_restore -h localhost -p 5432 -d pubgstatz pubgstatz.dump -c -U pubgstatz