#!/bin/bash

echo "{"
echo "  \"Docker Images\": ["
docker images --format "{\"ID_image\": \"{{.ID}}\", \"Repository\": \"{{.Repository}}\", \"Tag\": \"{{.Tag}}\", \"Size\": \"{{.Size}}\"}" | awk 'NR>1{print ","}1'
echo "  ],"

echo "  \"Docker Containers\": ["
docker ps -a --format "{\"ID_container\": \"{{.ID}}\", \"ID_img\": \"{{.Image}}\", \"Created\": \"{{.CreatedAt}}\", \"Status\": \"{{.Status}}\"}" | awk 'NR>1{print ","}1'
echo "  ]"
echo "}"

