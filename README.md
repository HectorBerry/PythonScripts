# PythonScripts
In this repository I upload the little scripts made in Python that might be useful

# threads_script.py
This is a PoC script showing a simple threading process.
It inserts into a sqlite db(if it doesn't exists it creates it) the tasks provided, and then executes it in threads according to the specified threads.
It uses two arguments: --threads, --tasks
Usage:
- `python threads_script.py -h` To get help on how to use the script 
- `python threads_script.py` To use the default parameters(10 threads, 1000 tasks)
- `python threads_Script.py --threads 5 --tasks 1040` To set up the parameters