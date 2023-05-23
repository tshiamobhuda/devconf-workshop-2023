#!/bin/bash

echo "Executing create_pkg.sh."

# Create the packaging directory.

dir_name=lambda_dist_pkg/
mkdir $dir_name

# Set up some variables that will be used throughout the packaing process.

function_name="chatgpt_telegram_package"
runtime="python3.10"

# Create and activate virtual environment.
virtualenv -t $runtime env_$function_name
source ./env_$function_name/bin/activate

# Installing python dependencies.
FILE=./lambda_function/requirements.txt

if [ -f "$FILE" ]; then
  echo "Installing dependencies."
  echo "From: requirement.txt file exists."
  pip install -r "$FILE"

else
  echo "Error: requirement.txt does not exist!"
fi

# Deactivate virtual environment.
deactivate

# Create deployment package.
echo "Creating deployment package."
cp -r env_$function_name/lib/$runtime/site-packages/. ./$dir_name
cp -r ./lambda_function/ ./$dir_name

zip -r $function_name.zip ./$dir_name

# Removing virtual environment folder.
echo "Removing virtual environment folder."
rm -rf ./env_$function_name
rm -rf ./$dir_name

echo "Finished script execution!"
