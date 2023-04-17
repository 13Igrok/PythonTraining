import time

import vlc

media_enter = input ( "Enter: " )
media_player = vlc.MediaPlayer ()
media = vlc.Media ( media_enter )
media_player.set_media ( media )
media_player.set_rate ( 0.5 )
media_player.play ()
time.sleep ( 5 )
