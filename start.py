#! /usr/bin/python3
# Used to start telegram bot. It starts multiple processes for each bot version.
import multiprocessing as mp
import secrets
import main

bot_args = [
	("en", secrets.telegram.token_en),
	("ru", secrets.telegram.token_ru),
	#("en", secrets.telegram.token_test),
]

jobs = []
for bot_arg in bot_args:
	job = mp.Process(target = main.start, args = bot_arg)
	job.start()
	jobs.append(job)

for job in jobs:
	job.join()
