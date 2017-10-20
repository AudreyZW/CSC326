<!DOCTYPE html>
<style>
    .right {
        position: absolute;
        right: 30px;
    }
</style>

<div class="right">
    % if user_email: # if user is signed in
        % if 'name' in session:
            <p style="text-align: center;">{{session['name']}}</p>
        % end
        % if 'picture' in session:
            <img style="display:block; margin: auto;" src="{{session['picture']}}" alt="profile pic" height="30">
        %end
        <p style="color:blue;">{{user_email}}</p>
        <a href="/logout">Logout</a>
    % else: # user is not logged in
        <p><a href="/google_auth">Google Login</a></p>
    % end
</div>
<br>

<img style="display:block; margin: auto;" src="logo.png" alt="website logo" height="100">

<form action="/" method="get">
    Input: <input name="keywords" type="text" />
    <input value="Submit" type="submit" />
</form>
<br>

% if user_email: # if user is signed in
    <p>Search history:</p>
    <table id="history">
        <col width="130">
        <tr>
          <th>Word</th> <th>Count</th>
        </tr>
        % for word,count in keywords_countdown[:20]: 
            <tr>
              <td>{{word}}</td> <td>{{count}}</td>
            </tr>
        % end
    </table>
% end