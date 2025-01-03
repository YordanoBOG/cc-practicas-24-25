#!/bin/bash

sleep 180; # Esperar a que se ejecute docker-compose

# Operaciones con la base de datos
curl -X DELETE http://localhost:8000/delete/BVBRC_slatt_protein_small.csv;
curl -X DELETE http://localhost:8000/delete/BVBRC_slatt_protein_small_new.csv;
curl -X GET http://localhost:8000/consultdb;
curl -F "file=@./BVBRC_slatt_protein_small.csv" http://localhost:8000/upload;
curl -X GET http://localhost:8000/consultdb;

# Operaciones con la API
curl -X GET http://localhost:8000/crearworkflow;
curl -X GET http://localhost:8000/showinfo;
curl -X POST http://localhost:8000/crearworkflowparametros -H "Content-Type: application/json" \
-d '{"tasks": [], "results_file": "workflow_res.txt", "returned_value": 0, "containerized": true}';
curl -X POST http://localhost:8000/aniadirtareaisolatecolumn -H "Content-Type: application/json" \
-d '{"containerized": true, "csv_path": "BVBRC_slatt_protein_small.csv", "col_name": "BRC ID"}';


