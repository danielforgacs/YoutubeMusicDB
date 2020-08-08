import requests




def test_post_playlist():
    plid = 'PL9YsudagsL6hicXrha4zBId875lRXxc32'

    response = requests.post('http://localhost:5000', json={'id': plid})
    data = response.json()




if __name__ == '__main__':
    pass

    test_post_playlist()
