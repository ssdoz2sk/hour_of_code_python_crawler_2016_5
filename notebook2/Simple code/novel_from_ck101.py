import os

import requests
from bs4 import BeautifulSoup

thread_id = '2763314'

html = requests.get( "http://ck101.com/thread-{}-1-1.html".format( thread_id ), headers={'User-Agent':'Mozilla'} )
        
print( html )
soup = BeautifulSoup( html.text, "html5lib" )

filename = soup.find( 'h1', { 'id' : 'thread_subject' } ).text
page_num = int( soup.find( 'a', { 'class' : 'last' } ).text.split()[-1] )
reply_num = int( soup.find( 'span', { 'class' : 'replayNum' } ).text )

path = os.path.join( os.path.dirname( __file__ ), 'novel' )
try:
    os.makedirs( path, 0o755 )
except OSError as e:
    if e.errno == 17:  # errno.EEXIST
        os.chmod( path, 0o755 )

text = ""

for page in range( 1, page_num+1 ):
    print( "Page {} / {}".format( page, page_num ) )
    html = requests.get( "http://ck101.com/thread-{}-{}-1.html".format( thread_id, page ) )
    soup = BeautifulSoup( html.text, "html5lib" )
    reply = soup.find_all( 'td', { 'class': 't_f' } )
    for t in reply:
        text += t.text
        
    with open( os.path.join(path, "{}.txt".format( filename )), 'w', encoding='utf-8' ) as txt:
        txt.write( text ) 