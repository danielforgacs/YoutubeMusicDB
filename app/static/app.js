var loadedIndexes       = []
tableHeaders            = ["pk", "title", "is_down", "added", "youtube_id", "playlist"]
videoTableID            = "videotable"
playlistURIinputID      = "playlist_uri"


window.addEventListener("load", createVideoTable, false);
window.addEventListener("load", buildVideoList, false);



function createVideoTable(data) {
    table       = document.getElementById(videoTableID);
    head        = document.createElement('thead');
    headrow     = document.createElement('tr');
    body        = document.createElement('tbody')
    
    table.setAttribute("class", "table table-striped table-hover table-sm")
    head.setAttribute("class", "thead-dark")
    body.setAttribute("id", "videotableBody")

    head.appendChild(headrow)
    table.appendChild(head)
    table.appendChild(body)

    for (idx in tableHeaders) {
        hpk = document.createElement('th')
        hpk.innerHTML = tableHeaders[idx]
        headrow.appendChild(hpk)
    }
}



function submitPlaylist() {
    plstInput = document.getElementById(playlistURIinputID)
    plst = {id: plstInput.value};
    plstInput.value = "";

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