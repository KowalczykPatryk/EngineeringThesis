#!/bin/bash
# Usage: make_job.sh <job_id> <n_events>  -> job_<id>/ with per-job seeds, then runs edep-sim (memory-capped)
set -e
ID=$1; N=$2; D=job_$(printf %04d $ID)
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p $HERE/$D && cd $HERE/$D
sed "s/^SEED: -1/SEED: $((1000+ID))/" $HERE/dlp_multi.yaml > gen.yaml
# Macro derived from simlar generator/biglarbox.mac (https://github.com/DeepLearnPhysics/simlar,
# commit f8ba881; see SOURCES.md). Changes: per-job seeds, config file name.
cat > g4.mac <<MAC
/random/setSeeds $((ID+1)) $((ID+7919))
/edep/random/randomSeed $((ID+5))
/process/eLoss/fluct 0
/edep/storeNeutralStepAsPoint 1
/edep/avoidHitMerging lar_vol 1
/edep/hitSeparation lar_vol -1 mm
/edep/hitSagitta drift 1.0 mm
/edep/hitLength drift 1.0 mm
/edep/db/set/neutronThreshold 0 MeV
/edep/db/set/lengthThreshold 0 mm
/edep/db/set/gammaThreshold 0 MeV
/edep/update
/generator/kinematics/bomb/config gen.yaml
/generator/kinematics/bomb/verbose 0
/generator/kinematics/set bomb
/generator/count/fixed/number 1
/generator/count/set fixed
/generator/add
MAC
/usr/bin/time -f "wall=%e s maxrss=%M kB" $HERE/../../run_edepsim.sh -m ${MEM:-5G} -t ${TMO:-3600} \
  -g $HERE/geometry/BigLArCube.gdml -e $N -o edep.h5 g4.mac > log.txt 2>&1
echo "$D exit=$? $(tail -1 log.txt)"
