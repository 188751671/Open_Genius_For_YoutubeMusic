# Open_Genius_For_YoutubeMusic
Automatically opens Genius page according to your current Youtube tab dynamically. If you go to another Youtube video, the old Genius tab will go to its lyrics page automatically.

The dominant Youtube-Genius scripts on market automatically searches on Genius based on Youtube song title, but It often gets the wrong lyrics ( some songs have the same name ) or the wrong version of lyrics (different singers' versions have mutated lyrics), and it can't show the lyrics when you watch fullscreen. So I made this script so that I can put the lyrics tab on my second screen while watching fullscreen.

videoID_To_GeniusURL.json is the mapping database that this script read from. Everyone is welcomed to append your YoutubeID and Its Genius URI pairs there.

A few already recorded Youtube songs for you to see how the lyrics tab redirect:

https://www.youtube.com/watch?v=OblL026SvD4

https://www.youtube.com/watch?v=7QCn2Jn1sPY

https://www.youtube.com/watch?v=DfCdkyQyaJ8

"?v=..." part like "OblL026SvD4" is the Youtube video ID.
"Paramore-still-into-you-lyrics" in genius.com/Paramore-still-into-you-lyrics is GeniusID.
Append pairs like this on videoID_To_GeniusURL.json , don't forget to add a tailing , comma.
