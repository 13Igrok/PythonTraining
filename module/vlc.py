import vlc
import time
media_player = vlc.MediaPlayer()
media = vlc.Media()
media_player.set_media(media)
media_player.set_rate(2)
media_player.play()
time.sleep(5)
