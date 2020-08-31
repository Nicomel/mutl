FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
LABEL maintainer="Nicolas Metivier <metivier.n@gmail.com>"

COPY . /home/mutl

# Set the working directory
WORKDIR /home/mutl

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Set the working directories to /home/lem
RUN mkdir data

# # Make ports available to the world outside this container
EXPOSE 8000

# # Define environment variable
# ENV MUTL_FILE_PATH '/home/mutl/data/mutl_repo.pickle'
# ENV MUTL_LOCAL_QUEUE_PATH '/home/mutl/data/mutl_client_queue.pickle'
# ENV MUTL_SERVER_QUEUE_PATH '/home/mutl/data/mutl_server_queue.pickle'

# # Run the service when the container launches
# CMD ["uvicorn","app.main:app","--host","0.0.0.0"]