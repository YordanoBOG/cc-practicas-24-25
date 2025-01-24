FROM mongo:6.0

EXPOSE 27017

# Command to disable SSL in the MongoDB server configuration
CMD ["mongod", "--bind_ip_all", "--sslMode", "disabled"]