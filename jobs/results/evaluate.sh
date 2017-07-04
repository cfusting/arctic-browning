#!/bin/bash
#PBS -l nodes=1:ppn=1,pmem=32gb,pvmem=32gb
#PBS -l walltime=03:00:00
#PBS -N symbolic_validate
#PBS -o /users/c/f/cfusting/job_logs
#PBS -e /users/c/f/cfusting/job_logs
#PBS -q shortq
source $HOME/.bash_profile
export PYTHONPATH=$HOME/gp_mecl:$ARCTIC_HOME
echo "Running evaluate with flags: ${flags}."
if [[ ${flags}  == *"v"* ]]
then
echo "Running symbolic validate."
python ${ARCTIC_HOME}/scripts/results/symbolic_validate.py \
        -t ${ARCTIC_DATA_HOME}/${trainset}.${datatype} \
        -j ${ARCTIC_DATA_HOME}/${testset}.${datatype} \
        -e ${experiment} \
        -r ${ARCTIC_RESULTS_HOME}/${trainset}.${datatype}_${experiment}
fi
if [[ ${flags}  == *"f"* ]]
then
echo "Running frequent features."
python ${ARCTIC_HOME}/scripts/plotting/frequent_features.py \
        -t ${ARCTIC_DATA_HOME}/${trainset}.${datatype} \
        -e ${experiment} \
        -r ${ARCTIC_RESULTS_HOME}/${trainset}.${datatype}_${experiment}
fi
if [[ ${flags}  == *"c"* ]]
then
echo "Running change basis."
python ${ARCTIC_HOME}/scripts/results/change_basis.py \
        -t ${ARCTIC_DATA_HOME}/${trainset}.${datatype} \
        -f ${ARCTIC_RESULTS_HOME}/${trainset}.${datatype}_${experiment}/features_${trainset}_${experiment}.txt \
        -e ${experiment} \
        -o ${ARCTIC_RESULTS_HOME}/${trainset}.${datatype}_${experiment}/optimal_basis_${trainset}.hdf
python ${ARCTIC_HOME}/scripts/results/change_basis.py \
        -t ${ARCTIC_DATA_HOME}/${testset}.${datatype} \
        -f ${ARCTIC_RESULTS_HOME}/${trainset}.${datatype}_${experiment}/features_${trainset}_${experiment}.txt \
        -e ${experiment} \
        -o ${ARCTIC_RESULTS_HOME}/${trainset}.${datatype}_${experiment}/optimal_basis_${testset}.hdf
fi
if [[ ${flags}  == *"m"* ]]
then
echo "Running linear model."
python ${ARCTIC_HOME}/scripts/ml/linear_model.py \
        -t ${ARCTIC_RESULTS_HOME}/${trainset}.${datatype}_${experiment}/optimal_basis_${trainset}.hdf \
        -j ${ARCTIC_RESULTS_HOME}/${trainset}.${datatype}_${experiment}/optimal_basis_${testset}.hdf \
        -o ${ARCTIC_RESULTS_HOME}/${trainset}.${datatype}_${experiment}/linear_model_results_${experiment}.txt
fi
