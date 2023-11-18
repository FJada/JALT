// quick api retrieval testing in console
// will test current A, C, and E train data

const apiUrl = 'https://api.mta.info/your-endpointhttps://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace';

fetch(apiUrl, {
    headers: {
      'Content-Type': 'application/json',
      'API-Key': 'KBf8CHIirk2T8svAwIqS68ZtrnJQ5pypIrLuluUh',
    },
  })
    .then(response => response.json())
    .then(data => {
      console.log(data);
    })
    .catch(error => console.error('Error fetching data:', error));