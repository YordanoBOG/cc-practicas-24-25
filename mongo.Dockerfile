FROM mongo:6.0

EXPOSE 27017

# Create a directory for SSL certificates
RUN mkdir -p /etc/ssl

# Copy the certificate files into the container
COPY ssl/server.pem /etc/ssl/mongodb.pem

# Start MongoDB with SSL enabled
CMD ["mongod", "--bind_ip_all", "--sslMode", "requireSSL", "--sslPEMKeyFile", "/etc/ssl/mongodb.pem"]

# Command to disable SSL in the MongoDB server configuration
#CMD ["mongod", "--bind_ip_all", "--sslMode", "disabled"]