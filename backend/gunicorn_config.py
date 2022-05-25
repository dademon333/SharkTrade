workers = 2  # https://pythonspeed.com/articles/gunicorn-in-docker/
worker_class = 'uvicorn.workers.UvicornWorker'
worker_tmp_dir = '/dev/shm'

bind = '0.0.0.0:8080'
