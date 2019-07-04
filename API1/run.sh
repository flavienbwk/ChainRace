#!/bin/bash
if [[ "$1" = train ]]
then
    jupyter nbconvert --execute --ExecutePreprocessor.timeout=-1 --to notebook --inplace build.ipynb
else
    python -c "import t4; t4.Package.install('quilt/quilt_sagemaker_demo', registry='s3://quilt-example', dest='.')"
    cp quilt/quilt_sagemaker_demo/clf.h5 clf.h5
    rm -rf quilt/
    python -m flask run --host=0.0.0.0 --port=8080
fi