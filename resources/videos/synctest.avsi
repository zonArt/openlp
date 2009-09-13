# audio/video sync test
# by: Andrew Lok
# 2009-06-22

#
#  This code is part of OpenLP's testsuite
#  OpenLP - Open Source Lyrics Projection
#  Copyright (c) 2009 Andrew Lok
#
#  This program is free software; you can redistribute it and/or modify it under
#  the terms of the GNU General Public License as published by the Free Software
#  Foundation; version 2 of the License.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
#  PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with
#  this program; if not, write to the Free Software Foundation, Inc., 59 Temple
#  Place, Suite 330, Boston, MA 02111-1307 USA
#

function SyncClip(float framerate, int audiorate)
{
  frames=30
  seconds=frames/framerate

  silence = Tone(seconds, 440, audiorate, 1, "silence", 1.0)
  tone = Tone(seconds, 440, audiorate, 1, "sine", 1.0)

  silence2 = MonoToStereo(silence, silence)
  left = MonoToStereo(tone, silence)
  right = MonoToStereo(silence, tone)

  leftvid=ImageSource("left-720.png",end = frames, fps=framerate, use_DevIL=true)
  rightvid=ImageSource("right-720.png",end = frames, fps=framerate, use_DevIL=true)
  normalvid=ImageSource("normal-720.png",end = frames, fps=framerate, use_DevIL=true)

  cycle = AudioDub(leftvid,left) ++ AudioDub(normalvid,silence2) ++ AudioDub(rightvid,right) ++ AudioDub(normalvid,silence2)

  final = loop(cycle,times=5)

  final = final.ConvertToYV12()
  final = final.info()

  return final
}
