# Open_Genius_For_YoutubeMusic
This script automatically opens a Genius lyrics page based on the current YouTube Music tab. If you switch to another song, the existing Genius tab updates to show the new lyrics.

[install it on Greasyfork](https://greasyfork.org/en/scripts/525715-open-genius-for-youtubemusic)

Unlike other YouTube-Genius scripts that rely on automatic searches (which often fetch incorrect lyrics due to duplicate song titles or different versions), this script ensures accuracy by using a predefined mapping list. It also allows you to keep lyrics open on a second screen while watching YouTube in fullscreen.

The mapping file: [videoID_To_GeniusURL.csv](https://github.com/188751671/Open_Genius_For_YoutubeMusic/blob/main/videoID_To_GeniusURL.csv) is where the script read from. To add new songs, simply append entries in the format introduced below.

Example YouTube video links for testing:

https://www.youtube.com/watch?v=OblL026SvD4

https://www.youtube.com/watch?v=7QCn2Jn1sPY

https://www.youtube.com/watch?v=DfCdkyQyaJ8

In each link, the part after v= (e.g., OblL026SvD4) is the YouTube video ID.

For Genius links, the relevant part is the tail, e.g., "Paramore-still-into-you-lyrics" in: https://www.genius.com/Paramore-still-into-you-lyrics

so "OblL026SvD4,Paramore-still-into-you-lyrics" is the entry in the CSV.
