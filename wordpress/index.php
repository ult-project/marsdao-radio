# Display current song (update in 1 minute)
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<span style="font-weight:bold">Current song:</span>
<span style="color:#ff7831; white-space: nowrap;">
  <script type="text/javascript">
    $(document).ready(function() {
      function refreshDiv() {
        $('#refresh').fadeOut(500, function() {
          $('#refresh');
        }).fadeIn(500);
      }
      setInterval(refreshDiv, 60000);
    });
  </script>
  <div id="refresh"><?php get_template_part('functions/icecast', 'parser') ?></div>
</span>


# Display current amount of listeners (update in 5 seconds)
<span style="font-weight:bold">Listeners:</span>
<span style="color:#ff7831;">
<span id="song-listeners"></span>
<script>
  var timeout = 5;
  function getStats(){
    $.ajax({
      url: "https://onair.example.com/status-json.xsl?mount=/live",
      success: function( response ) {
        $('#song-listeners').text(response.icestats.source.listeners)
      }
    });
  }
  getStats();
  setInterval(getStats, timeout * 1000);
</script>


# Display maximum peak of listeners (update in 5 seconds)
(<b>max:</b> <span id="song-listener_peak"></span>)
<script>
  var timeout = 5;
  function getStats(){
    $.ajax({
      url: "https://onair.example.com/status-json.xsl?mount=/live",
      success: function( response ) {
        $('#song-listener_peak').text(response.icestats.source.listener_peak)
      }
    });
  }
  getStats();
  setInterval(getStats, timeout * 1000);
</script>

# Display $MDAO crypto currency prise from the CoinMarketCap
<dev>
  <a href="https://coinmarketcap.com/currencies/marsdao" title="CoinMarketCap: $MDAO" target="_blank">$MDAO</a>:
  <?php $cmc_prise_mdao = getCoinPrice('marsdao', 18913); echo $cmc_prise_mdao; ?>
</dev>

# Display $COSMIC crypto currency prise from the CoinMarketCap
<dev>
  <a href="https://coinmarketcap.com/currencies/cosmic-fomo" title="CoinMarketCap: $COSMIC" target="_blank">$COSMIC</a>:
  <?php $cmc_prise_cosmic = getCoinPrice('cosmic-fomo', 24993); echo $cmc_prise_cosmic; ?>
</dev>

# Copy the text by click
<style>
.copy-address {
  cursor: pointer;
  margin: 0 6px 0 0;
  float: right;
}

.copy-address-tip {
  position: relative;
  margin: -18px 380px 0 0;
}

.copy-address-tip .copy-address-tip-text {
  width: 90px;
  background-color: #adadad;
  color: #666666;

  text-align: center;
  padding: 1px 0;
  border-radius: 2px;

  position: absolute;
  z-index: 1;
  /* opacity: 0.5; */
}
</style>

<script>
function setClipboard(value) {
  var tempInput = document.createElement("input");
  tempInput.value = value;
  document.body.appendChild(tempInput);
  tempInput.select();
  document.execCommand("copy");
  document.body.removeChild(tempInput);
  $('<div class="copy-address-tip"><span class="copy-address-tip-text">copied</span></div>').insertAfter('.copy-address').delay(1000).fadeOut(1000, function(){$(this).remove();});
}
</script>

<img src="<?php bloginfo('template_url'); ?>/images/copy.svg" class="copy-address" alt="Copy" title="Click to copy" width="20" onclick="setClipboard('text-to-copy')">
