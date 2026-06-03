FROM minio/minio:latest

WORKDIR /app

# Set the environment variables for Minio
ENV MINIO_ROOT_USER=minioadmin
ENV MINIO_ROOT_PASSWORD=minioadmin

# Expose the Minio ports
#EXPOSE 9000 9001

# Start the Minio server
CMD ["minio", "server", "/data", "--config-dir", "/root/.minio", "--console-address", ":9001"]
