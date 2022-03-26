<h1><a href="http://51.250.37.48:1337/">Hammer Systems</a></h1>
<h2> Django DRF API for authenticating via phone number and adding people via invite codes </h2>
<h1>Table of content:</h1>
<ul>
    <li>
        <a href="#summary">Summary</a>
    </li>
    <li>
        <a href="#api_refs">API references</a>
    </li>
     <li>
        <a href="#additional">Additional</a>
    </li>
</ul>

<h1 id="summary">Summary:</h1>
<ul>
    <li>Authorization via phone number. First request sends phone number to server, if provided number exists we send a code for login. Otherwise we register new user, and send then code for confirming phone number (loging-in).</li>
    <li>After entring code we proided, user is given access to his profile.</li>
    <li>Profile request is private, and authentication JWT is required.</li>
    <li>Each user has unique identifier generated automaticly after registration.</li>
    <li>User can enter someone elses identifier and add them in his 'friends' list</li>
    <li>All users can see who added them. To do so they need to naviage to theirs profile and under Friends: is a list of phonenumbers of people who added them.</li>
</ul>

<h1 id="api_refs">API references:</h1>
<div syle="color: blue; font-size: 18px">
NOTE: Requests that requirer JWT must be sent with headers containing access_token in COOKIE
</div>
<ul>
    <h2>API endpoints:</h2>
    <ul>
        <li>
            <a href="#sub_phone">Submit phone number - receive code</a>
        </li>
         <li>
            <a href="#valid_code">Validate phone number - verify code</a>
        </li>
         <li>
            <a href="#get_prof">Get profile - user data</a>
        </li>
        <li>
            <a href="#add_friend">Add friend via invite code</a>
        </li>
        <li>
            <a href="#refresh_jwt">Refresh JWT</a>
        </li>
    </ul>
    <br>
    <h2>Endpoints request examples using JS AXIOS:</h2>
<li id="sub_phone"><h3>Submit phone number</h3>
    <div style="font-size: 16.5px; border: 1px solid white; padding: 8px;">
        Request:
        <br>
        <code>await axios.post(BASE_URL + '/api/auth', {'phone_number':phone_number})</code>
        <br>
        <br>
        Response:
        <ul>
        <li>
            <code>Status: 200</code>
            <br>
            <code>{ created: boolean, code: 5468 }</code>
            <br>
        </li>
        <li>
            <code>Status: 400</code>
            <br>
            <code>{ default_detail: 'Invalid value in phone number' }</code>
        </li>
        </ul>
    </div>
</li>
<br>
<li id="valid_code"><h3>Validate phone number</h3>
    <div style="font-size: 16.5px; border: 1px solid white; padding: 8px;">
        Request:
        <br>
        <code>await axios.post(BASE_URL + '/api/verify', {'phone_number':phone_number, 'code': code})</code>
        <br>
        <br>
        Response:
        <ul>
        <li>
            <code>Status: 200</code>
            <br>
            <code>{ access_token: "JWT_ACCESS_TOKEN", refresh_token: "JWT_REFRESH_TOKEN }</code>
        </li>
        <li>
            <code>Status: 403</code>
            <br>
            <code>{ default_detail: 'Invalid confirmation code' }</code>
        </li>
        </ul>
    </div>
</li>
<br>
<li id="get_prof"><h3>Get profile</h3>
    <div style="font-size: 16.5px; border: 1px solid white; padding: 8px;">
        Request:
        <br>
        <code>await axios.get(BASE_URL + '/api/profile')</code>
        <br>
        <br>
        Response:
        <ul>
        <li>
            <code>Status: 200</code>
            <br>
            <code>{ user_identifier: "5aS8\E", friends: ["+79685127157", "+7985698745"] }</code>
        </li>
        <li>
            <code>Status: 403</code>
            <br>
            <code>{ default_detail: 'Invalid access token' }</code>
        </li>
        </ul>
    </div>
</li>
<br>
<li id="add_friend"><h3>Add friend via invite code</h3>
    <div style="font-size: 16.5px; border: 1px solid white; padding: 8px;">
        Request:
        <br>
        <code>await axios.post(BASE_URL + '/api/add/friend', {'friend_identifier': friend_identifier})</code>
        <br>
        <br>
        Response:
        <ul>
        <li>
            <code>Status: 200</code>
            <br>
            <code>{  }</code>
        </li>
        <li>
            <code>Status: 403</code>
            <br>
            <code>{ default_detail: 'Failed to add friend' }</code>
        </li>
        </ul>
    </div>
</li>
<br>
<li id="refresh_jwt"><h3>Refresh JWT</h3>
    <div style="font-size: 16.5px; border: 1px solid white; padding: 8px;">
    Request:
        <br>
        <code>await axios.get(BASE_URL + '/api/token/refresh')</code>
        <br>
        <br>
        Response:
        <ul>
        <li>
            <code>Status: 200</code>
            <br>
            <code>{ access_token: "JWT_ACCESS_TOKEN", refresh_token: "JWT_REFRESH_TOKEN }</code>
        </li>
        <li>
            <code>Status: 403</code>
            <br>
            <code>{ default_detail: 'Invalid access token' }</code>
        </li>
        </ul>
    </div>
</li>
</ul>
<br>
<h1 id="additional">Additional:</h1>
<ul>
<li>
    Implemented pipeline for automated deployment.
</li>
<li>
    Host: Yandex.Cloud compute cloud
</li>
<li>
    PostgreSQL: www.elephantsql.com
</li>
</ul>