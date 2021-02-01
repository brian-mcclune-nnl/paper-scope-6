#!/bin/bash

setup_dir=$(dirname $(dirname "$(readlink -f "$0")"))
$setup_dir/pythonenv3.8/bin/pip install $setup_dir
