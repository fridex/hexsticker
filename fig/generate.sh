#!/bin/env bash

set -ex

hexsticker input/selinon.png -o output/selinon-sticker-1.png
hexsticker input/selinon.png -o output/selinon-sticker-2.png --padding-size 25
hexsticker input/selinon.png -o output/selinon-sticker-3.png --padding-size 25 --padding-color '#66cfa7'
hexsticker input/selinon.png -o output/selinon-sticker-4.png --padding-size 25 --padding-color '#66cfa7' --border-size 35
#hexsticker input/selinon.png -o output/selinon-sticker-5.png --padding-size 25 --padding-color '#66cfa7' --border-size 35 --border-color '#cde4db'
hexsticker input/selinon.png -o output/selinon-sticker-5.png --padding-size 25 --padding-color '#66cfa7' --border-size 35 --border-color '#197a9f'

