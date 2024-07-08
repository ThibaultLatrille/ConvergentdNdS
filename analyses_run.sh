#!/usr/bin/env bash
CPU=8
for EXPERIMENT in config/Mammals*.yaml; do
  echo "${EXPERIMENT}"
  cp -rf "${EXPERIMENT}" "config/config.yaml"
  snakemake -j ${CPU} -k
done
