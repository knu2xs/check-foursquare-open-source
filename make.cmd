:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: LICENSING                                                                    :
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::
:: Copyright 2020 Esri
::
:: Licensed under the Apache License, Version 2.0 (the "License"); You
:: may not use this file except in compliance with the License. You may
:: obtain a copy of the License at
::
:: http://www.apache.org/licenses/LICENSE-2.0
::
:: Unless required by applicable law or agreed to in writing, software
:: distributed under the License is distributed on an "AS IS" BASIS,
:: WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
:: implied. See the License for the specific language governing
:: permissions and limitations under the License.
::
:: A copy of the license is available in the repository's
:: LICENSE file.

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: VARIABLES                                                                    :
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

SETLOCAL
SET PROJECT_DIR=%cd%
SET PROJECT_NAME=check-foursquare-open-source
SET SUPPORT_LIBRARY = check_foursquare_open_source
SET CONDA_DIR="%~dp0env"

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: COMMANDS                                                                     :
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: Jump to command
GOTO %1

:: Perform data preprocessing steps contained in the make_data.py script.
:check
    CALL conda run -p %CONDA_DIR% python scripts/check-available.py
    GOTO end

:: Build the local environment from the environment file
:env
    :: Create new environment from environment file
    CALL conda create -p %CONDA_DIR%
    GOTO add_dependencies

:: Add python dependencies from environment.yml to the project environment
:add_dependencies
        
    :: Add more fun stuff from environment file
    CALL conda env update -p %CONDA_DIR% -f environment.yml

    GOTO end

:: Start Jupyter Label
:jupyter
    CALL conda run -p %CONDA_DIR% python -m jupyterlab --ip=0.0.0.0 --allow-root --NotebookApp.token=""
    GOTO end

:end
    EXIT /B
