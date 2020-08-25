loadedIndexes           = []
tableHeaders            = ["pk", "title", "is_down", "added", "youtube_id", "playlist"]
videoTableID            = "videotable"
playlistURIinputID      = "playlist_uri"
videoTable              = document.getElementById(videoTableID)
plstInput               = document.getElementById(playlistURIinputID)


window.addEventListener("load", createVideoTable, false)
window.addEventListener("load", buildVideoList, false)



function createVideoTable() {
    head        = document.createElement('thead')
    headrow     = document.createElement('tr')
    body        = document.createElement('tbody')
    
    videoTable.setAttribute("class", "table table-striped table-hover table-sm")
    head.setAttribute("class", "thead-dark")
    body.setAttribute("id", "videotableBody")

    head.appendChild(headrow)
    videoTable.appendChild(head)
    videoTable.appendChild(body)

    for (idx in tableHeaders) {
        hpk             = document.createElement('th')
        hpk.innerHTML   = tableHeaders[idx]
        headrow.appendChild(hpk)
    }
}



function submitPlaylist() {
    plst                = {id: plstInput.value};
    plstInput.value     = "";

    let response = fetch('/api/createplaylist', {
        method:     'POST',
        headers:    {'Content-Type': 'application/json'},
        body:       JSON.stringify(plst)
    });

    response
        .then(response => response.json())
        .then(buildVideoList)
};



function buildVideoList() {
    fetch('/api/all_videos')
        .then(response => response.json())
        .then(addVidoTableRows)
};



function addVidoTableRows(data) {
    videos      = data['videos']
    body        = document.getElementById("videotableBody")

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
