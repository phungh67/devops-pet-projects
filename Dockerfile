# Use an official lightweight Python image
FROM python:3.12-slim  

# Create a new user just for running the application
RUN groupadd -g 1123 application && \
    useradd -u 1123 -g application application

# Print the UID and GID
RUN echo 'Inside Container:' && echo 'User: $(whoami) UID: $(id -u) GID: $(id -g)'

# Set the working directory
WORKDIR /flask-university-admission 

# Copy project files into the container
COPY . /flask-university-admission

# Install dependencies
RUN pip install -r requirements.txt 

RUN chown -R application:application /flask-university-admission

USER application

# Expose port 5000 for Flask
EXPOSE 5000  

# Command to run the app
CMD ["python", "run.py"]