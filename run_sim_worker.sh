#!/bin/env bash
while [ true ]; do
 # run every n second (unit: second)
 sleep 5
 # echo "Invoking sim_worker"
 python sim_worker.py
done