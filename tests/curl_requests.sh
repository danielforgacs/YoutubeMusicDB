# playlist: AAAA
# https://www.youtube.com/playlist?list=PL9YsudagsL6hicXrha4zBId875lRXxc32
#
# https://www.youtube.com/watch?v=HJq-6y2IYEQ
# https://www.youtube.com/watch?v=FIQ2F3T1ydM


# playlist: BBBB
# https://www.youtube.com/playlist?list=PL9YsudagsL6h0n4ew9ibbicfGFIPdUKMU
#
# https://www.youtube.com/watch?v=HJq-6y2IYEQ
# https://www.youtube.com/watch?v=zrxuPkbIq4g

# playlist: CCCC
# https://www.youtube.com/playlist?list=PL9YsudagsL6ipb5Yd7QKz0x9byLncwEs_
#
# https://www.youtube.com/watch?v=iI1M48eC3x4
# https://www.youtube.com/watch?v=EDQ1dmFEGiI


# non playlist videos:
# https://www.youtube.com/watch?v=BPopaJsNWd4



echo "--> post playlist:"
curl http://127.0.0.1:5000/api/createplaylist -H "Content-type: application/json" -d "{\"id\": \"PL9YsudagsL6hicXrha4zBId875lRXxc32\"}"
curl http://127.0.0.1:5000/api/createplaylist -H "Content-type: application/json" -d "{\"id\": \"PL9YsudagsL6h0n4ew9ibbicfGFIPdUKMU\"}"
curl http://127.0.0.1:5000/api/createplaylist -H "Content-type: application/json" -d "{\"id\": \"PL9YsudagsL6ipb5Yd7QKz0x9byLncwEs_\"}"
curl http://127.0.0.1:5000/api/createplaylist -H "Content-type: application/json" -d "{\"id\": \"BPopaJsNWd4\"}"

echo "--> download playlist:"
curl http://127.0.0.1:5000/download -H "Content-type: application/json" -d "{\"id\": \"PL9YsudagsL6hicXrha4zBId875lRXxc32\"}"

echo "--> downloading archive:"
curl http://localhost:5000/archive -o download.zip