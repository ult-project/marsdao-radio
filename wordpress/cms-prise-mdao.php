<?php

$url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest?slug=marsdao";

$curl = curl_init($url);
curl_setopt($curl, CURLOPT_URL, $url);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);

$headers = array(
  "X-CMC_PRO_API_KEY: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "Accept: application/json",
);
curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);
// for debug only
curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);

$resp = curl_exec($curl);
curl_close($curl);

$data = "data";
$id = "18913";
$quote = "quote";
$usd = "USD";
$price = "price";

$json = json_decode($resp, true);
$mdao = $json[$data][$id][$quote][$usd][$price];
echo round($mdao, 4);

?>
