#!/bin/bash
npm install;
find . -mtime +10950 -exec touch {} \;