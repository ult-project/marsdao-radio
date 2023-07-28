<?php
/**
 * CoinMarketCap prise function
 */

function coinmarketcap_get_prise() {
  require_once get_template_directory() . '/functions/coinmarketcap-get-prise.php';
}
add_action('init', 'coinmarketcap_get_prise');
?>
