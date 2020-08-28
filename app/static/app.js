loadedIndexes           = []
tableHeaders            = ["title", "is_down", "playlist", "added"]
videoTableID            = "videotable"
playlistURIinputID      = "playlist_uri"
archiveBtnID            = "archiveBtn"
videoTable              = document.getElementById(videoTableID)
plstInput               = document.getElementById(playlistURIinputID)
archiveBtn              = document.getElementById(archiveBtnID)
archiveFileName         = ''


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
    archiveBtn.setAttribute('class', 'btn btn-secondary mb-2 disabled')

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

        for (idx of [1, 2, 5, 3]) {
            td = document.createElement('td')
            td.innerHTML = video[idx]
            td.setAttribute('data-playlistid', video[6])
            tr.appendChild(td)
        }

        loadedIndexes.push(video[0])
    }
}



function downloadPaylist() {
    archiveBtn.setAttribute('class', 'btn btn-secondary mb-2 disabled')

    plst                = {id: plstInput.value};
    plstInput.value     = "";

    let response = fetch('/api/download', {
        method:     'POST',
        headers:    {'Content-Type': 'application/json'},
        body:       JSON.stringify(plst)
    });

    response
        .then(response => response.json())
        .then(createArchiveLink)
}



function createArchiveLink(data) {
    // console.log(data)
    // console.log(data.videos)
    // console.log(data.archive)
    archiveFileName = data.archive
    archiveBtn.setAttribute('class', 'btn btn-success mb-2')
}



function downloadArchive() {
    console.log('[ARCHIVE]', archiveFileName)

    makeArchiveLink(archiveFileName)
}


function makeArchiveLink(filename) {
    var element = document.createElement('a');
    element.setAttribute('href', 'api/archive/' + encodeURIComponent(filename));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}