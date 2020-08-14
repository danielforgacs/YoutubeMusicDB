# playlist: AAAA
# https://www.youtube.com/playlist?list=PL9YsudagsL6hicXrha4zBId875lRXxc32

headerjson="Content-type: application/json"
post_playlist_url=http://127.0.0.1:5000
download_playlist_url=http://127.0.0.1:5000/download
playlist1=PL9YsudagsL6hicXrha4zBId875lRXxc32


echo "--> post playlist:"
curl $post_playlist_url -H "$headerjson" -d "{\"id\": \"$playlist1\"}"
echo "--> download playlist:"
curl $download_playlist_url -H "$headerjson" -d "{\"id\": \"$playlist1\"}"
