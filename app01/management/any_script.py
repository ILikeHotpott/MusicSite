import pymysql
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

# 数据库配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Lcy741125',
    'database': 'music_test',
}

data = [{"title": "What Was I Made For? [From The Motion Picture \"Barbie\"]", "artist": "Billie Eilish",
         "pic_url": "https://i.kfs.io/album/global/257677698,2v1/fit/160x160.jpg", "position": 1, "spotify_uri": ""},
        {"title": "Just Like That", "artist": "Bonnie Raitt",
         "pic_url": "https://i.kfs.io/album/global/157394538,2v1/fit/160x160.jpg", "position": 2, "spotify_uri": ""},
        {"title": "Leave The Door Open", "artist": "Bruno Mars Anderson Paak Silk Sonic",
         "pic_url": "https://i.kfs.io/album/global/159573577,1v1/fit/160x160.jpg", "position": 3, "spotify_uri": ""},
        {"title": "I Can't Breathe", "artist": "HER",
         "pic_url": "https://i.kfs.io/album/global/78907171,3v1/fit/160x160.jpg",
         "position": 4, "spotify_uri": ""}, {"title": "bad guy", "artist": "Billie Eilish",
                                             "pic_url": "https://i.kfs.io/album/global/52383356,2v1/fit/160x160.jpg",
                                             "position": 5, "spotify_uri": ""},
        {"title": "This Is America", "artist": "Childish Gambino",
         "pic_url": "https://i.kfs.io/album/global/34695091,2v1/fit/160x160.jpg", "position": 6, "spotify_uri": ""},
        {"title": "That's What I Like", "artist": "Bruno Mars",
         "pic_url": "https://i.kfs.io/album/global/20063686,3v1/fit/160x160.jpg", "position": 7, "spotify_uri": ""},
        {"title": "Hello", "artist": "Adele", "pic_url": "https://i.kfs.io/album/global/16509400,4v1/fit/160x160.jpg",
         "position": 8, "spotify_uri": ""}, {"title": "Thinking out Loud", "artist": "Ed Sheeran",
                                             "pic_url": "https://i.kfs.io/album/tw/4140615,0v1/fit/160x160.jpg",
                                             "position": 9,
                                             "spotify_uri": ""},
        {"title": "Stay With Me - Darkchild Version", "artist": "Sam Smith",
         "pic_url": "https://i.kfs.io/album/global/4050894,0v1/fit/160x160.jpg", "position": 10, "spotify_uri": ""},
        {"title": "Royals", "artist": "Lorde", "pic_url": "https://i.kfs.io/album/tw/1953671,0v2/fit/160x160.jpg",
         "position": 11, "spotify_uri": ""}, {"title": "We Are Young (feat. Janelle Monáe)", "artist": "fun",
                                              "pic_url": "https://i.kfs.io/album/tw/324988,0v3/fit/160x160.jpg",
                                              "position": 12, "spotify_uri": ""},
        {"title": "Rolling in the Deep", "artist": "Adele",
         "pic_url": "https://i.kfs.io/album/global/166149,3v1/fit/160x160.jpg", "position": 13, "spotify_uri": ""},
        {"title": "Need You Now", "artist": "Lady A", "pic_url": "https://i.kfs.io/album/tw/871719,0v2/fit/160x160.jpg",
         "position": 14, "spotify_uri": ""}, {"title": "Single Ladies (Put A Ring On It)", "artist": "Beyonc",
                                              "pic_url": "https://i.kfs.io/album/tw/114813,0v3/fit/160x160.jpg",
                                              "position": 15, "spotify_uri": ""},
        {"title": "Viva La Vida", "artist": "Coldplay",
         "pic_url": "https://i.kfs.io/album/global/105597,1v1/fit/160x160.jpg",
         "position": 16, "spotify_uri": ""}, {"title": "Rehab - Album Version", "artist": "Amy Winehouse",
                                              "pic_url": "https://i.kfs.io/album/tw/2011623,0v1/fit/160x160.jpg",
                                              "position": 17, "spotify_uri": ""},
        {"title": "Not Ready To Make Nice", "artist": "The Chicks",
         "pic_url": "https://i.kfs.io/album/tw/84336,0v1/fit/160x160.jpg", "position": 18, "spotify_uri": ""},
        {"title": "Sometimes You Can't Make It On Your Own", "artist": "U U",
         "pic_url": "https://i.kfs.io/album/global/3174720,2v1/fit/160x160.jpg", "position": 19, "spotify_uri": ""},
        {"title": "Daughters", "artist": "John Mayer", "pic_url": "https://i.kfs.io/album/tw/83081,0v1/fit/160x160.jpg",
         "position": 20, "spotify_uri": ""}, {"title": "Dance With My Father", "artist": "Luther Vandross",
                                              "pic_url": "https://i.kfs.io/album/tw/52259,0v1/fit/160x160.jpg",
                                              "position": 21,
                                              "spotify_uri": ""},
        {"title": "Don't Know Why", "artist": "Norah Jones",
         "pic_url": "https://i.kfs.io/album/tw/59873,0v1/fit/160x160.jpg",
         "position": 22, "spotify_uri": ""},
        {"title": "Fallin", "artist": "Alicia Keys", "pic_url": "https://i.kfs.io/album/tw/47967,0v3/fit/160x160.jpg",
         "position": 23, "spotify_uri": ""},
        {"title": "Beautiful Day", "artist": "U U",
         "pic_url": "https://i.kfs.io/album/global/3168770,0v1/fit/160x160.jpg",
         "position": 24, "spotify_uri": ""},
        {"title": "Smooth", "artist": "Santana", "pic_url": "https://i.kfs.io/album/tw/776595,0v1/fit/160x160.jpg",
         "position": 25, "spotify_uri": ""}, {"title": "My Heart Will Go On", "artist": "Celine Dion",
                                              "pic_url": "https://i.kfs.io/album/tw/48050,0v3/fit/160x160.jpg",
                                              "position": 26,
                                              "spotify_uri": ""},
        {"title": "Sunny Came Home", "artist": "Shawn Colvin",
         "pic_url": "https://i.kfs.io/album/tw/9447,0v1/fit/160x160.jpg",
         "position": 27, "spotify_uri": ""}, {"title": "Change the World", "artist": "Eric Clapton",
                                              "pic_url": "https://i.kfs.io/album/global/195938249,0v1/fit/160x160.jpg",
                                              "position": 28, "spotify_uri": ""},
        {"title": "Kiss from a Rose", "artist": "Seal",
         "pic_url": "https://i.kfs.io/album/global/62893,4v1/fit/160x160.jpg",
         "position": 29, "spotify_uri": ""}, {"title": "Streets Of Philadelphia", "artist": "Bruce Springsteen",
                                              "pic_url": "https://i.kfs.io/album/tw/71447,0v1/fit/160x160.jpg",
                                              "position": 30,
                                              "spotify_uri": ""},
        {"title": "A Whole New World - From \"Aladdin\" / Soundtrack Version",
         "artist": "Aladdin Special Edition  International Version",
         "pic_url": "https://i.kfs.io/album/global/3889944,0v1/fit/160x160.jpg", "position": 31, "spotify_uri": ""},
        {"title": "Tears in Heaven - Acoustic Live", "artist": "Eric Clapton",
         "pic_url": "https://i.kfs.io/album/global/195318395,0v1/fit/160x160.jpg", "position": 32, "spotify_uri": ""},
        {"title": "Unforgettable - 2003 - Remastered", "artist": "Nat King Cole",
         "pic_url": "https://i.kfs.io/album/tw/60122,0v3/fit/160x160.jpg", "position": 33, "spotify_uri": ""},
        {"title": "From a Distance - 2015 Remaster", "artist": "Bette Midler",
         "pic_url": "https://i.kfs.io/album/global/11183992,1v1/fit/160x160.jpg", "position": 34, "spotify_uri": ""},
        {"title": "Wind Beneath My Wings - 2015 Remaster", "artist": "Bette Midler",
         "pic_url": "https://i.kfs.io/album/global/11183992,1v1/fit/160x160.jpg", "position": 35, "spotify_uri": ""},
        {"title": "Don't Worry Be Happy", "artist": "Bobby McFerrin",
         "pic_url": "https://i.kfs.io/album/tw/59116,0v1/fit/160x160.jpg", "position": 36, "spotify_uri": ""},
        {"title": "Somewhere Out There", "artist": "James Ingram",
         "pic_url": "https://i.kfs.io/album/tw/102,0v1/fit/160x160.jpg", "position": 37, "spotify_uri": ""},
        {"title": "That's What Friends Are For", "artist": "Dionne Warwick",
         "pic_url": "https://i.kfs.io/album/tw/732773,0v1/fit/160x160.jpg", "position": 38, "spotify_uri": ""},
        {"title": "We Are The World", "artist": "Michael Jackson",
         "pic_url": "https://i.kfs.io/album/tw/424764,0v3/fit/160x160.jpg", "position": 39, "spotify_uri": ""},
        {"title": "What's Love Got to Do with It", "artist": "Tina Turner",
         "pic_url": "https://i.kfs.io/album/global/59760,3v1/fit/160x160.jpg", "position": 40, "spotify_uri": ""},
        {"title": "Every Breath You Take - Remastered 2003", "artist": "The Police",
         "pic_url": "https://i.kfs.io/album/global/2981458,0v1/fit/160x160.jpg", "position": 41, "spotify_uri": ""},
        {"title": "Always On My Mind", "artist": "Willie Nelson",
         "pic_url": "https://i.kfs.io/album/tw/60727,0v1/fit/160x160.jpg", "position": 42, "spotify_uri": ""},
        {"title": "Bette Davis Eyes", "artist": "Kim Carnes",
         "pic_url": "https://i.kfs.io/album/tw/59827,0v1/fit/160x160.jpg",
         "position": 43, "spotify_uri": ""}, {"title": "Sailing", "artist": "Christopher Cross",
                                              "pic_url": "https://i.kfs.io/album/global/140885,2v1/fit/160x160.jpg",
                                              "position": 44, "spotify_uri": ""},
        {"title": "What A Fool Believes", "artist": "The Doobie Brothers",
         "pic_url": "https://i.kfs.io/album/tw/131741,0v1/fit/160x160.jpg", "position": 45, "spotify_uri": ""},
        {"title": "Just The Way You Are", "artist": "Billy Joel",
         "pic_url": "https://i.kfs.io/album/tw/65316,0v3/fit/160x160.jpg", "position": 46, "spotify_uri": ""},
        {"title": "Evergreen", "artist": "Barbra Streisand",
         "pic_url": "https://i.kfs.io/album/tw/25485,0v1/fit/160x160.jpg",
         "position": 47, "spotify_uri": ""}, {"title": "You Light up My Life", "artist": "Debby Boone",
                                              "pic_url": "https://i.kfs.io/album/global/5173374,0v1/fit/160x160.jpg",
                                              "position": 48, "spotify_uri": ""},
        {"title": "I Write The Songs", "artist": "Barry Manilow",
         "pic_url": "https://i.kfs.io/album/tw/51898,0v1/fit/160x160.jpg", "position": 49, "spotify_uri": ""},
        {"title": "Send In The Clowns (LP Version)", "artist": "Judy Collins",
         "pic_url": "https://i.kfs.io/album/tw/65207,0v1/fit/160x160.jpg", "position": 50, "spotify_uri": ""},
        {"title": "The Way We Were", "artist": "Barbra Streisand",
         "pic_url": "https://i.kfs.io/album/tw/25485,0v1/fit/160x160.jpg", "position": 51, "spotify_uri": ""},
        {"title": "Killing Me Softly With His Song (LP Version)", "artist": "Roberta Flack",
         "pic_url": "https://i.kfs.io/album/tw/64310,0v1/fit/160x160.jpg", "position": 52, "spotify_uri": ""},
        {"title": "The First Time Ever I Saw Your Face (LP Version)", "artist": "Roberta Flack",
         "pic_url": "https://i.kfs.io/album/tw/64308,0v1/fit/160x160.jpg", "position": 53, "spotify_uri": ""},
        {"title": "You've Got A Friend", "artist": "Carole King",
         "pic_url": "https://i.kfs.io/album/tw/57468,0v3/fit/160x160.jpg", "position": 54, "spotify_uri": ""},
        {"title": "Bridge Over Troubled Water", "artist": "Simon  Garfunkel",
         "pic_url": "https://i.kfs.io/album/tw/61922,0v3/fit/160x160.jpg", "position": 55, "spotify_uri": ""},
        {"title": "Games People Play - Remastered 2002", "artist": "Joe South",
         "pic_url": "https://i.kfs.io/album/tw/905931,0v1/fit/160x160.jpg", "position": 56, "spotify_uri": ""},
        {"title": "Little Green Apples", "artist": "OC Smith",
         "pic_url": "https://i.kfs.io/album/global/39395890,3v1/fit/160x160.jpg", "position": 57, "spotify_uri": ""},
        {"title": "Up, Up and Away", "artist": "The Fifth Dimension",
         "pic_url": "https://i.kfs.io/album/global/4148268,2v1/fit/160x160.jpg", "position": 58, "spotify_uri": ""},
        {"title": "Michelle - Remastered 2009", "artist": "The Beatles",
         "pic_url": "https://i.kfs.io/album/global/13818770,1v1/fit/160x160.jpg", "position": 59, "spotify_uri": ""},
        {"title": "The Shadow of Your Smile (Love Theme from \"The Sandpiper\") - Album Version",
         "artist": "Tony Bennett",
         "pic_url": "https://i.kfs.io/album/tw/61206,0v1/fit/160x160.jpg", "position": 60, "spotify_uri": ""},
        {"title": "Hello, Dolly!", "artist": "Louis Armstrong",
         "pic_url": "https://i.kfs.io/album/global/5084811,0v1/fit/160x160.jpg", "position": 61, "spotify_uri": ""},
        {"title": "The Days of Wine and Roses", "artist": "Henry Mancini",
         "pic_url": "https://i.kfs.io/album/tw/73756,0v1/fit/160x160.jpg", "position": 62, "spotify_uri": ""},
        {"title": "What Kind of Fool Am I?", "artist": "Sammy Davis Jr",
         "pic_url": "https://i.kfs.io/album/tw/2545364,0v1/fit/160x160.jpg", "position": 63, "spotify_uri": ""},
        {"title": "Moon River Cha Cha", "artist": "Henry Mancini",
         "pic_url": "https://i.kfs.io/album/tw/54714,0v1/fit/160x160.jpg", "position": 64, "spotify_uri": ""},
        {"title": "Theme Of Exodus", "artist": "Ernest Gold",
         "pic_url": "https://i.kfs.io/album/global/45434750,0v3/fit/160x160.jpg", "position": 65, "spotify_uri": ""},
        {"title": "The Battle Of New Orleans", "artist": "Johnny Horton",
         "pic_url": "https://i.kfs.io/album/tw/70606,0v1/fit/160x160.jpg", "position": 66, "spotify_uri": ""},
        {"title": "Volare", "artist": "Domenico Modugno",
         "pic_url": "https://i.kfs.io/album/global/63732516,0v1/fit/160x160.jpg", "position": 67, "spotify_uri": ""}]

