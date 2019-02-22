#!/bin/bash
npm install;
npm run build;
find . -mtime +10950 -exec touch {} \;