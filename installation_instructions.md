# Linux

The instructions were tested on Ubuntu 20.04.

1. Download the assignment archive file from Brightspace and place it in a convenient location (for example `~/pdm`).

2. Open a terminal (ctrl+alt+T) and go this directory (e.g., `cd ~/pdm`)

3. Unpack the assignment by typing `tar -xvzf pdm-assignment1.tar.gz`

4. Go to the unpacked folder (`cd assignment1`) and type `ls`, you should see a file `10-setup-environment.sh`. If its name is not green yet, use `chmod +x 10-setup-environment.sh` to give permissions.

5. Set up the environment by running `./10-setup-environment.sh`. This will:

* Download Miniconda to setup the Python environment,
* Create an environment with the correct packages,
* Source that environment,
* And finally, open the notebook.

6. Happy coding!

Every time that we want to start to work again we have to:
1. Open a terminal and go to the directory of the assignment (e.g., `~/pdm`)
2. Run `./02-start-notebook.sh`  


# Windows

If Anaconda3 is already installed, you can proceed to step 3 directly.

1. Download the Anaconda3 Python installer from [https://www.anaconda.com/distribution/](https://www.anaconda.com/distribution/)

2. Install Anaconda3 Python. Choose the option to install for the current user only, in order to avoid needing admin permissions.

3. Download the assignment archive file from brightspace and unpack the contents. Save the files in, for example `C:\\Desktop\\pdm`. Make sure that your directory does NOT contain whitespace characters.

4. Open the command prompt, in `Start menu -> Command Prompt` (Dutch: opdrachtprompt).

5. In the terminal use `cd` and navigate to the practica materials directory e.g., `cd Desktop\\pdm`.

6. Extract the tar file by executing `tar -xvzf pdm-assignment1.tar.gz`.

5. Open **Anaconda Prompt (Anaconda3)** from the Start menu (do NOT use Anaconda Powershell Prompt).

7. In this terminal, again, use `cd` and navigate to the practica materials directory e.g., `cd Desktop\\pdm\\assignment1`.

8. Type `10-setup-environment.bat` to install all the dependencies for this assignment in a conda environment.

Now everything is set up. To run the notebook, you don't have to repeat these steps everytime. Instead, you only need to follow these steps:

9. Type `01-activate.bat`. This will select the conda environment `pdm3` and set the needed environment variables (`PYTHONPATH`)

10. Type `jupyter notebook`

11. Now open the notebook (ipynb) file of the assignment by selecting the file in the browser.

12. Happy coding!

  
  

Every time that we want to start to work again we have to:

1. Open **Anaconda Prompt (Anaconda3)** in the Start menu

2. Go to the practica materials directory (for example `cd Desktop/pdm`)

3. Type `01-activate.bat` (this will also activate the environment pdm. that you see in parenthesis before the directory and set needed environment variables (`PYTHONPATH`)

4. Type `jupyter notebook` (this will open the notebook server from where you can open the practica and assignment notebook files)

# MacOS
We do not officially support Mac, but here are some pointers. If you are familiar with conda, the environment is defined in `environment_M1.yml`.

For more guidance, you can follow the Linux guide. **But before step 5**, open `00-setup.sh`. Change `environment.yml` to `environment_M1.yml` and comment the line
`pip install -r requirements.txt`. Now proceed with step 5 of the Linux guide.


