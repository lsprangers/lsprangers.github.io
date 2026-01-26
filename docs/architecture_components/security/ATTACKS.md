---
title: Attacks On Sessions
layout: default
---

## Sessions
Sessions are common communication windows between clients (browsers on laptop) and servers (web servers) - once authenticated and authorized, you can interact with resources in your session

Sessions are typically secured via tokens and cookies, so wanted to look into those more

### XSS
Cross site scripting (XSS) is an attack where a malicious script is added to a website, and so when another user accesses the website they will accidentally run the malicious script which comprimises their data as the attacker gets control of the user's browser

Preventing XSS is almost solely up to a website owner, and browsers also do a fair amount to protect but they can't handle all cases. Website owners need to ensure all inuts are validated before they're stored ino a database and presented to other users

#### Stored XSS
These occu when websites allow user input and store it into databases, like comments, free text descriptions, etc - when an attacker places the malicious script into the comment box and another users browser loads the comments section, it will run the script on the users browser

Some common types are:
- Installing browser-based keyloggers to capture keystrokes 
- Capturing session cookies of the user, which can be used to trigger other attacks like [CSRF attaacks](#csrf-attacks)
- Redirecting users to other websites

Taking the comment example, when you load a comment section the browser treats the comment as data and displays it. If the website doesn't sanitize the actual user input, then JS code can be injected in data. The below could be inserted into a `<data>` section, which ultimately would cause 2 `<data>` sections instead of the intended single one. At that point the `<script>` section actually is displayed as it's own portion of the page

```javascript
<data>
thing
</data>
```
Could turn into 

```javascript
<data>
thing
</data>
<script>alert('hacked')</script>
<data>
</data>
```

#### Reflected XSS
Attacker tricks the user into clicking a link that contains the malicious script. Clicking on a link on your browser just has your browser go and find a new webpage at that URL, connect to the websites server, and request the actual pages data. If the link is some `.js` script it can physically execute code inside of your browser, and there are ways for that to actually download something onto your computer

Normal `.js` scripts downloaded are run in a very restricted environment called browser sandbox, this sandbox is designed to prevent JS from accessing filesystem, installing programs, etc. That being said, malicious scripts that run inside of your browser (even inside the sandbox) can engage with the browser process, and ultimately:
- steal cookies, tokens, and data which are used for authentication and authorization
- Impersonate you to the website (via tokens)
- Open up other websites for downloading further malicious content, which would install to your computer outside of browser process
    - If you downloaded some file via the browser, and you click on it, you initiate it as another process on your computer outside of the browser. That's when bad things can occur

Ultimately, reflected XSS is just the act of an attacker somehow getting the user to click a link or get a JS script to run, which is different from stored XSS where attacker places something into a website and the user doesn't perform an action to run it

### CSRF Attacks
Cross-Site Request Forgery can force logged-in users to execute unwanted actions on the logged in application

A few conditions need to be met:
- Cookie based session handling, where the website relies on cookies to identify the user
    - i.e. once a user has logged in, there are session tokens used to identify the user so they don't have to reauthenticate
- No unpredictable request parameters
    - The requests that perform the malicious action don't contain and parameters whose values the attacker can't guess

A common example is a `GET` request, something similar to 
```
GET http://abcbank.com/transfer.do?acct=Bob&amount=$500 HTTP/1.1
```

If an attacker created another URL for transferring money to their account,
```
GET http://abcbank.com/transfer.do?acct=attacker&amount=$500 HTTP/1.1
```

Realistically all the attacker would need to do is get someone to run this from a logged in browser session - if a user was logged into `abcbank.com`, and had their cookies already established, and they ran the above `GET`, then it would perform a transfer into the `acct=attacker` account

If an attacker created some email or something to have the user click on it, and the user did, and the browser session that handled the request happened to have cookies established for `abcbank.com`, then it would all work out for the attacker

```html
<a href="http://abcbank.com/transfer.do?acct=attackerA&amount=$500">Get the offer!</a>
```

So there's a number of pre-requisites that must happen for this to work, but theoretically if those are all met then it's possible. This doesn't usually happen by chance, and there are coordinated ways to ensure all of these prerequisites are actually met

`GET` requests don't usually alter state in any way, and you wouldn't `GET` a transfer - you'd `POST` it, and with `POST` comes parameters that need to be set. Therefore there must be a request body as apart of the request, and it's much harder to get someone to send a full `POST` request with `K:V` parameters set perfectly 

```javascript
<body onload="document.csrf.submit()">
 
<form action="http://abcbank.com/transfer" method="POST" name="csrf">
    <input type="hidden" name="amount" value="500">
    <input type="hidden" name="account" value="attacker">
</form>
```

If this was hidden inside of a malicious website / page, this form would be submitted which in turn would send a `POST` request

#### Preventing CSRF
Most methods revolve around short lived tokens that only a user's web browser would know of - this works because the attacker never has access to the local web browser process running on someone's computer

1. Using CSRF tokens!
    - AKA anti-CSRF or synchronizer tokens
    - An anti-CSRF token is a server-side CSRF protection
    - It's a random string that's only known to the user's browser and the web application
    - How it works
        - Request is sent to web server, web app generates a token and stores it short term
        - The token is statically set as a field of the form
        - When form is submitted by the user the token is included in `POST` request data
            - `x-csrf-token`
        - The application compares the token from all new `POST` requests to the one it's stored
        - If tokens match, it's not an invalid request
    - Attacker can't figure out the token from the users browser as it doesn't have direct access to this token, so even if the attacker had a perfect URL they couldn't authorize the `POST`
2. Same site cookies
    - `SameSite` flag in cookies is a new method to prevent CSRF attacks and improve security
        - In most CSRF attack, a `POST` request is sent by a users browser after clicking on a bad website or link
    - If the session cookie is marked as `SameSite`, it's only sent along with requests that originate from that website domain
        - So a cookie stored for `abcbank.com`, that is a `SameSite` cookie, can't be reused on any domain outside of `abcbank.com`

### Denial of Service Attack
These are when attackers flood web servers with requests, improper handshakes, and other methods to disallow it from responding to other actual users
- ICMP Flood is when a misconfigured network device in a webservers network is utilized to send spoofed ICMP packets to all devices, including the webserver, on it's network
    - All devices trust this device, and are responding to the ICMP pings, so it essentially causes them to not respond to actual users
- SYN Flood is where the targeted server receives a request to begin a TCP SYN handshake, but the handshake is never completed 
    - In scenario's where the port isn't closed after a default period of time this can lead to that port being "stuck" and unable to process any further requests

Stopping these attacks typically revolves around rate limiting, WAF protection, and bot lists
