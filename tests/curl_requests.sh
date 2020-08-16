# playlist: AAAA
# https://www.youtube.com/playlist?list=PL9YsudagsL6hicXrha4zBId875lRXxc32


echo "--> post playlist:"
curl http://127.0.0.1:5000 -H "Content-type: application/json" -d "{\"id\": \"PL9YsudagsL6hicXrha4zBId875lRXxc32\"}"

echo "--> download playlist:"
curl http://127.0.0.1:5000/download -H "Content-type: application/json" -d "{\"id\": \"PL9YsudagsL6hicXrha4zBId875lRXxc32\"}"

echo "--> downloading archive:"
curl http://localhost:5000/archive -o download.zip