<?php

// Variables to define Curl request options
$url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest?slug=cosmic-fomo";
$curl = curl_init($url);
$headers = array(
  "X-CMC_PRO_API_KEY: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "Accept: application/json",
);

/*
Equivalent console command:
curl -H "X-CMC_PRO_API_KEY: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" -H "Accept: application/json" \
-G https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest?slug=cosmic-fomo
*/

// Curl request options
curl_setopt($curl, CURLOPT_URL, $url);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);
// Set the following options 'true' only for debug
curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);

$response = curl_exec($curl);
curl_close($curl);

$data = "data";
$id = "24993";
$quote = "quote";
$usd = "USD";
$price = "price";

$json = json_decode($response, true);
$cosmic = $json[$data][$id][$quote][$usd][$price];
echo round($cosmic, 4);

?>
