data_help = '''-d, --data <data>
    (HTTP)  Sends  the  specified data in a POST request to the HTTP
    server, in the same way that a browser  does  when  a  user  has
    filled  in an HTML form and presses the submit button. This will
    cause curl to pass the data to the server using the content-type
    application/x-www-form-urlencoded.  Compare to -F, --form.

    -d,  --data  is  the  same  as --data-ascii. To post data purely
    binary, you should instead use the --data-binary option. To URL-
    encode the value of a form field you may use --data-urlencode.

    If  any of these options is used more than once on the same com-
    mand line, the data pieces specified  will  be  merged  together
    with  a  separating  &-symbol.  Thus,  using  '-d name=daniel -d
    skill=lousy'  would  generate  a  post  chunk  that  looks  like
    'name=daniel&skill=lousy'.

    If  you  start  the data with the letter @, the rest should be a
    file name to read the data from, or - if you want curl  to  read
    the data from stdin. Multiple files can also be specified. Post-
    ing data from a file named 'foobar'  would  thus  be  done  with
    --data  @foobar.  When  --data  is told to read from a file like
    that, carriage returns and newlines will be stripped out.
'''

data_binary_help = '''--data-binary <data>
    (HTTP) This posts data exactly as specified with no  extra  pro-
    cessing whatsoever.

    If  you  start  the data with the letter @, the rest should be a
    filename.  Data is posted in a similar  manner  as  --data-ascii
    does,  except  that  newlines and carriage returns are preserved
    and conversions are never done.

    If this option is used several times,  the  ones  following  the
    first will append data as described in -d, --data.'''

data_urlencode_help = '''--data-urlencode <data>
    (HTTP) This posts data, similar to the other --data options with
    the exception that this performs URL-encoding. (Added in 7.18.0)

    To  be  CGI-compliant,  the <data> part should begin with a name
    followed by a separator and a content specification. The  <data>
    part can be passed to curl using one of the following syntaxes:

    content
    This  will make curl URL-encode the content and pass that
    on. Just be careful so that the content  doesn't  contain
    any  =  or  @  symbols, as that will then make the syntax
    match one of the other cases below!

    =content
    This will make curl URL-encode the content and pass  that
    on. The preceding = symbol is not included in the data.

    name=content
    This  will make curl URL-encode the content part and pass
    that on. Note that the name part is expected to  be  URL-
    encoded already.

    @filename
    This  will  make  curl  load  data  from  the  given file
    (including any newlines), URL-encode that data  and  pass
    it on in the POST.

    name@filename
    This  will  make  curl  load  data  from  the  given file
    (including any newlines), URL-encode that data  and  pass
    it  on  in  the  POST.  The  name part gets an equal sign
    appended, resulting in name=urlencoded-file-content. Note
    that the name is expected to be URL-encoded already.'''

digest_help = '''--digest
    (HTTP) Enables HTTP Digest authentication. This is an  authenti-
    cation  scheme  that  prevents the password from being sent over
    the wire in clear text. Use this in combination with the  normal
    -u,  --user  option  to  set  user  name  and password. See also
    --ntlm, --negotiate and --anyauth for related options.

    If this option is used several times,  only  the  first  one  is
    used.'''

referer_help = '''-e, --referer <URL>
    (HTTP) Sends the "Referrer Page" information to the HTTP server.
    This can also be set with the -H, --header flag of course.  When
    used with -L, --location you can append ";auto" to the --referer
    URL to make curl automatically set the previous URL when it fol-
    lows  a  Location: header. The ";auto" string can be used alone,
    even if you don't set an initial --referer.

    If this option is used several times, the last one will be used.'''

form_help = '''-F, --form <name=content>
    (HTTP)  This  lets curl emulate a filled-in form in which a user
    has pressed the submit button. This causes  curl  to  POST  data
    using  the  Content-Type  multipart/form-data  according  to RFC
    2388. This enables uploading of binary files etc. To  force  the
    'content'  part  to  be  a  file, prefix the file name with an @
    sign. To just get the content part from a file, prefix the  file
    name  with  the symbol <. The difference between @ and < is then
    that @ makes a file get attached in the post as a  file  upload,
    while  the  <  makes  a text field and just get the contents for
    that text field from a file.

    Example, to send your password file to the server, where  'pass-
    word' is the name of the form-field to which /etc/passwd will be
    the input:

    curl -F password=@/etc/passwd www.mypasswords.com

    To read content from stdin instead of a file, use - as the file-
    name. This goes for both @ and < constructs.

    You  can  also  tell  curl  what  Content-Type  to  use by using
    'type=', in a manner similar to:

    curl -F "web=@index.html;type=text/html" url.com

    or

    curl -F "name=daniel;type=text/foo" url.com

    You can also explicitly change the name field of a  file  upload
    part by setting filename=, like this:

    curl -F "file=@localfile;filename=nameinpost" url.com

    If  filename/path contains ',' or ';', it must be quoted by dou-
    ble-quotes like:

    curl -F "file=@\"localfile\";filename=\"nameinpost\"" url.com

    or

    curl -F 'file=@"localfile";filename="nameinpost"' url.com

    Note that if a filename/path is  quoted  by  double-quotes,  any
    double-quote or backslash within the filename must be escaped by
    backslash.

    See further examples and details in the MANUAL.

    This option can be used multiple times.'''

get_help = '''-G, --get
    When  used,  this  option  will make all data specified with -d,
    --data, --data-binary or --data-urlencode to be used in an  HTTP
    GET  request instead of the POST request that otherwise would be
    used. The data will be appended to the URL with a '?' separator.

    If  used  in  combination with -I, the POST data will instead be
    appended to the URL with a HEAD request.

    If this option is used several times,  only  the  first  one  is
    used.  This is because undoing a GET doesn't make sense, but you
    should then instead enforce the alternative method you prefer.'''

header_help = '''-H, --header <header>
    (HTTP) Extra header to include in the request when sending  HTTP
    to  a  server. You may specify any number of extra headers. Note
    that if you should add a custom header that has the same name as
    one  of  the  internal  ones curl would use, your externally set
    header will be used instead of the internal one. This allows you
    to  make  even  trickier  stuff than curl would normally do. You
    should not replace internally set headers without  knowing  per-
    fectly well what you're doing. Remove an internal header by giv-
    ing a replacement without content  on  the  right  side  of  the
    colon, as in: -H "Host:". If you send the custom header with no-
    value then its header must be terminated with a semicolon,  such
    as -H "X-Custom-Header;" to send "X-Custom-Header:".

    curl  will  make  sure  that each header you add/replace is sent
    with the proper end-of-line marker, you should thus not add that
    as a part of the header content: do not add newlines or carriage
    returns, they will only mess things up for you.

    See also the -A, --user-agent and -e, --referer options.

    Starting in 7.37.0, you need --proxy-header to send custom head-
    ers intended for a proxy.

    This  option  can  be  used multiple times to add/replace/remove
    multiple headers.'''

head_help = '''-I, --head
    (HTTP/FTP/FILE) Fetch the HTTP-header only! HTTP-servers feature
    the command HEAD which this uses to get nothing but  the  header
    of  a  document. When used on an FTP or FILE file, curl displays
    the file size and last modification time only.'''

insecure_help = '''-k, --insecure
    (SSL)  This  option explicitly allows curl to perform "insecure"
    SSL connections and transfers. All SSL connections are attempted
    to  be  made secure by using the CA certificate bundle installed
    by default. This makes  all  connections  considered  "insecure"
    fail unless -k, --insecure is used.

    See     this    online    resource    for    further    details:
    http://curl.haxx.se/docs/sslcerts.html'''

output_help = '''-o, --output <file>
    Write output to <file> instead of stdout. If you are using {} or
    [] to fetch multiple documents, you can use '#'  followed  by  a
    number  in  the <file> specifier. That variable will be replaced
    with the current string for the URL being fetched. Like in:

    curl http://{one,two}.site.com -o "file_#1.txt"

    or use several variables like:

    curl http://{site,host}.host[1-5].com -o "#1_#2"

    You may use this option as many times as the number of URLs  you
    have.

    See  also  the --create-dirs option to create the local directo-
    ries dynamically. Specifying the output as '-' (a  single  dash)
    will force the output to be done to stdout.'''

remote_name_help = '''-O, --remote-name
    Write  output to a local file named like the remote file we get.
    (Only the file part of the remote file is used, the path is  cut
    off.)

    The  remote  file  name  to use for saving is extracted from the
    given URL, nothing else.

    Consequentially, the file will be saved in the  current  working
    directory.  If you want the file saved in a different directory,
    make sure you change current working directory before you invoke
    curl with the -O, --remote-name flag!

    There is no URL decoding done on the file name. If it has %20 or
    other URL encoded parts of the name, they will end up  as-is  as
    file name.

    You  may use this option as many times as the number of URLs you
    have.'''

range_help = '''-r, --range <range>
    (HTTP/FTP/SFTP/FILE)  Retrieve a byte range (i.e a partial docu-
    ment) from a HTTP/1.1, FTP or  SFTP  server  or  a  local  FILE.
    Ranges can be specified in a number of ways.

    0-499     specifies the first 500 bytes

    500-999   specifies the second 500 bytes

    -500      specifies the last 500 bytes

    9500-     specifies the bytes from offset 9500 and forward

    0-0,-1    specifies the first and last byte only(*)(H)

    500-700,600-799
    specifies 300 bytes from offset 500(H)

    100-199,500-599
    specifies two separate 100-byte ranges(*)(H)

    (*)  =  NOTE  that this will cause the server to reply with a multipart
    response!

    Only digit characters (0-9) are valid in the 'start' and 'stop'  fields
    of  the 'start-stop' range syntax. If a non-digit character is given in
    the range, the server's response will be unspecified, depending on  the
    server's configuration.

    You  should  also  be aware that many HTTP/1.1 servers do not have this
    feature enabled, so that when  you  attempt  to  get  a  range,  you'll
    instead get the whole document.

    FTP  and SFTP range downloads only support the simple 'start-stop' syn-
    tax (optionally with one of the numbers omitted). FTP  use  depends  on
    the extended FTP command SIZE.

    If this option is used several times, the last one will be used.'''

user_help = '''-u, --user <user:password>
    Specify the user name and password to use for server authentica-
    tion. Overrides -n, --netrc and --netrc-optional.

    If  you  simply  specify  the  user name, curl will prompt for a
    password.

    The user name and passwords are split up  on  the  first  colon,
    which  makes  it impossible to use a colon in the user name with
    this option. The password can, still.

    If you use an SSPI-enabled curl binary and perform NTLM  authen-
    tication,  you  can force curl to select the user name and pass-
    word from your environment by specifying  a  single  colon  with
    this option: "-u :".

    If this option is used several times, the last one will be used.'''

url_help = '''--url <URL>
    Specify  a  URL  to  fetch. This option is mostly handy when you
    want to specify URL(s) in a config file.

    This option may be used any number of times.  To  control  where
    this  URL  is written, use the -o, --output or the -O, --remote-
    name options.'''

request_help = '''-X, --request <command>
    (HTTP) Specifies a custom request method to use when communicat-
    ing with the HTTP server.  The specified request  will  be  used
    instead  of  the  method otherwise used (which defaults to GET).
    Read the HTTP 1.1 specification for  details  and  explanations.
    Common  additional  HTTP  requests  include  PUT and DELETE, but
    related technologies like WebDAV offers PROPFIND, COPY, MOVE and
    more.

    Normally  you  don't  need  this option. All sorts of GET, HEAD,
    POST and PUT requests are rather invoked by using dedicated com-
    mand line options.

    This  option  only  changes  the  actual  word  used in the HTTP
    request, it does not alter the way curl behaves. So for  example
    if  you  want  to make a proper HEAD request, using -X HEAD will
    not suffice. You need to use the -I, --head option.

    If this option is used several times, the last one will be used.'''

user_agent_help = '''-A, --user-agent <agent string>
    (HTTP) Specify the User-Agent string to send to the HTTP server.
    Some  badly  done  CGIs  fail  if  this  field  isn't   set   to
    "Mozilla/4.0".  To  encode  blanks  in  the string, surround the
    string with single quote marks. This can also be  set  with  the
    -H, --header option of course.

    If this option is used several times, the last one will be used.'''
