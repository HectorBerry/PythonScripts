#!/usr/bin/env python3
import argparse
import sqlite3
import threading
from queue import Queue
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

conn = None

def create_database():
    global conn
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY, task_name TEXT)")
    conn.commit()

def task(task_id):
    # Todo task, print as PoC
    print(f"Ping! task id: {task_id}")

def fetch_tasks(limit):
    c = conn.cursor()
    c.execute(f"SELECT * FROM tasks ORDER BY id DESC LIMIT {limit}")
    tasks = c.fetchall()
    tasks.reverse()
    return tasks

def insert_tasks(total_tasks):
    # Insert tasks in db
    c = conn.cursor()
    for i in range(total_tasks):
        c.execute(f"INSERT INTO tasks (task_name) VALUES ('Task {i+1}')")

    conn.commit()

def worker(task_queue):
    while True:
        task_id, task_name = task_queue.get()
        print(f"Executing task {task_id}: {task_name}")
        try:
            task(task_id)
        except Exception as e:
            logger.error(f"Error executing task {task_id}: {task_name}: {e}")
        finally:
            task_queue.task_done()

def main():
    parser = argparse.ArgumentParser(description='Multithreaded task execution')
    parser.add_argument('--threads', type=int, default=10, help='Number of worker threads')
    parser.add_argument('--tasks', type=int, default=1000, help='Total number of tasks')
    args = parser.parse_args()

    # Queue init
    task_queue = Queue(maxsize=args.threads)

    create_database()

    insert_tasks(args.tasks)

    # Ejecucion de los hilos
    for _ in range(args.threads):
        t = threading.Thread(target=worker, args=(task_queue,))
        t.daemon = True
        t.start()

    # Fetch tasks from db and add them to queue
    tasks = fetch_tasks(args.tasks)
    for task in tasks:
        task_queue.put(task)

    # Wait on the execution of all tasks and report
    task_queue.join()

    if task_queue.unfinished_tasks > 0:
        logger.warning(f"Task execution incomplete. {task_queue.unfinished_tasks} task(s) failed to execute successfully.")
    else:
        logger.info("All tasks executed successfully.")
    
    conn.close()


if __name__ == "__main__":
    main()