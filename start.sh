#!/bin/sh
nohup sh ./run_sim_worker.sh > sim_worker.log &
/usr/bin/supervisord