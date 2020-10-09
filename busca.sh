#!/bin/bash

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -algoritmo) algoritmo="$2"; shift ;;
        -entrada) entrada="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

src/search.py $algoritmo $entrada