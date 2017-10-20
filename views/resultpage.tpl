<!DOCTYPE html>
<style> 
    td, th {border: 1px solid #dddddd; text-align: left}
    li {padding: 2px;}
    div.hori {
        display: inline-block;
        vertical-align: top;
        margin-left: 20px;
    }
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

<img src="logo.png" alt="website logo" height="60">

<div class="hori">
    <form action="/" method="get">
        <input name="keywords" type="text" />
        <input value="Submit" type="submit" />
    </form>
</div>
<br>

<p>Searched for "{{input_words}}"</p>
<table id="results">
    <col width="130">
    <tr>
      <th>Word</th> <th>Count</th>
    </tr>
    % for word in word_list_clean: # display words in original order
        <tr>
          <td>{{word}}</td> <td>{{word_counter[word]}}</td>
        </tr>
    % end
</table> 
<br>

% if user_email: # if user is signed in
<div class="hori">
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
</div>
<div class="hori">
    <p>Recently searched:</p>
    <ul style="list-style-type:none;">
    % for word in recent_list: 
        <li>{{word}}</li>
    % end
    </ul>
</div>
% end