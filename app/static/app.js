var loadedIndexes = []
tableHeaders = ["pk", "title", "is_down", "added", "youtube_id", "playlist"]
videoTableID = "videotable"
playlistURIinputID = "playlist_uri"


window.addEventListener("load", createVideoTable, false);
window.addEventListener("load", buildVideoList, false);


function createVideoTable(data) {
    table = document.getElementById(videoTableID);
    table.setAttribute("class", "table table-striped table-hover table-sm")
    head = document.createElement('thead');
    head.setAttribute("class", "thead-dark")
    headrow = document.createElement('tr');
    head.appendChild(headrow)
    table.appendChild(head)
    body = document.createElement('tbody')
    body.setAttribute("id", "videotableBody")
    table.appendChild(body)

    for (idx in tableHeaders) {
        hpk = document.createElement('th')
        hpk.innerHTML = tableHeaders[idx]
        headrow.appendChild(hpk)
    }
}







function submitPlaylist() {
    let plst = {
        id: document.getElementById(playlistURIinputID).value,
    };

    document.getElementById("playlist_uri").value = "";

    let response = fetch('/api/createplaylist', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(plst)
    });

    response
        .then(response => response.json())
        .then(buildVideoList)

};


function buildVideoList() {
    url = '/api/all_videos'
    fetch(url)
        .then(response => response.json())
        .then(addVidoTableRows)
};





function addVidoTableRows(data) {
    console.log("data:", data)
    videos = data['videos']
    console.log("videos:", videos)
    body = document.getElementById("videotableBody")
    console.log("body:", body)

    for (video of videos) {
        tr = document.createElement('tr')
        body.appendChild(tr)
        pk = video[0]

        if (loadedIndexes.includes(pk)) {
            continue
        }

        for (attr of video) {
            td = document.createElement('td')
            td.innerHTML = attr
            tr.appendChild(td)
        }

        loadedIndexes.push(video[0])
    }
}