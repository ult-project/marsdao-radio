<?php
function getCoinPrice($slug, $id) {
  // check if the API response is already cached as a transient
  $cache_key = 'cmc_price_' . $slug . '_' . $id;
  $cached_response = get_transient($cache_key);

  if ($cached_response !== false) {
    // if the cached response exists - return the cached price
    $json = json_decode($cached_response, true);
  } else {
    // if the cached response doesn't exist - make new API request
    $url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest?slug=" . urlencode($slug);
    $headers = array(
      "X-CMC_PRO_API_KEY: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // replace with your CoinMarketCap API key
      "Accept: application/json"
    );

	// curl initialization
	$curl = curl_init($url);

    // curl request options
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);
    // set the following options 'true' only for debug
    curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
    curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);

    // get data from the CoinMarketCap
    $response = curl_exec($curl);

    // curl close
    curl_close($curl);

    // transform to the JSON format
    $json = json_decode($response, true);

    // cache the API response for 60 sec
    set_transient($cache_key, $response, 60);
  }

  // check is the data exist
  if (isset($json['data'][$id]['quote']['USD']['price'])) {
    $price_usd = $json['data'][$id]['quote']['USD']['price'];
	$price_formatted = number_format($price_usd, 4);
    return $price_formatted;
  } else {
    return 'null'; // return null if cryptocurrency data not found
  }
}
?>
