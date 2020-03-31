#!/bin/sh

case $1 in
  pre)
    printf "Sleep" | nc -q 1 127.0.0.1 65431 
    ;;
  post)
    printf "On" | nc -q 1 127.0.0.1 65431 
    ;;
esac
