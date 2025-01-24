FROM mongo:6.0

EXPOSE 27017

# Create a directory for SSL certificates
RUN mkdir -p /etc/ssl

# Copy the CA and MongoDB certificates into the container
COPY ssl/ca.crt /etc/ssl/ca.crt
COPY ssl/mongodb.pem /etc/ssl/mongodb.pem

# Start MongoDB with TLS enabled and CA verification
CMD ["mongod", "--bind_ip_all", "--sslMode", "requireSSL", "--sslPEMKeyFile", "/etc/ssl/mongodb.pem", "--sslCAFile", "/etc/ssl/ca.crt"]

# Command to disable SSL in the MongoDB server configuration
#CMD ["mongod", "--bind_ip_all", "--sslMode", "disabled"]