#!/bin/bash
echo "specify db host"
exit
pg_dump -h localhost -p 5432 -Fc -o -U pubgstatz pubgstatz > pubgstatz.dump