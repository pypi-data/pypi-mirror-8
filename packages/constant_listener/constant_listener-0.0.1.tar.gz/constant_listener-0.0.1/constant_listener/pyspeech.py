import json
import os
import sys
import wave
import pyaudio
import struct
from tempfile import mkstemp
import urllib2
from scikits.samplerate import resample
from scikits.audiolab import Sndfile, Format, wavread
from pocketsphinx import Decoder
from vocabcompiler import compile
from wit import Wit


have_sphinx_dictionary = False

def listen_for_best_speech_result(pyaudio, duration, profile, stt_type = "google"):
  if stt_type == 'google':
    return listen_for_best_google_speech_result(pyaudio, duration, profile)
  elif stt_type == 'wit':
    return listen_for_best_wit_speech_result(pyaudio, duration, profile)
  elif stt_type == 'sphinx':
    return listen_for_best_sphinx_speech_result(pyaudio, duration, profile)

def listen_for_best_sphinx_speech_result(pyaudio, duration, profile):
  if not have_sphinx_dictionary:
    if not profile.has_key("words"):
      raise "Pass the possible words in in profile"
    compile("sentences.txt", "dictionary.dic", "language_model.lm", profile["words"])
    global have_sphinx_dictionary
    have_sphinx_dictionary = True

  wav_name = record_wav(pyaudio, duration)
  if wav_name == "":
    return ""
  wav_file = file(wav_name, 'rb')
  speechRec = Decoder(
    hmm  = "/usr/local/share/pocketsphinx/model/hmm/en_US/hub4wsj_sc_8k",
    lm   = "language_model.lm",
    dict = "dictionary.dic"
  )

  speechRec.decode_raw(wav_file)
  results = speechRec.get_hyp()

  os.remove(wav_name)

  return results[0]

def listen_for_best_google_speech_result(pyaudio, duration, profile):
  if not profile.has_key("key") or profile["key"] == '':
    raise "Pass your Google Developer Key in profile"
  flac_file = wav_to_flac(record_wav(pyaudio, duration))
  if flac_file == "":
    return ""
  return best_google_result(flac_to_google_result(flac_file, profile["key"]))

def listen_for_best_wit_speech_result(pyaudio, duration, profile):
  if not profile.has_key("wit_token") or profile["wit_token"] == '':
    raise "Pass your Wit API Token in profile"
  wav_name = record_wav(pyaudio, duration)
  if wav_name == "":
    return ""
  w = Wit(profile["wit_token"])
  result = w.post_speech(open(wav_name, 'rb'))
  os.remove(wav_name)
  return result[u'msg_body']

def record_wav(p, duration):
  rate = 44100
  cd, wav_name = mkstemp('tmp.wav')

  stream = p.open(rate, 1, pyaudio.paInt16, input = True)
  data = stream.read(rate * duration)
  stream.stop_stream()
  stream.close()

  # 2 bytes per paInt16
  format = "%dh"%(len(data)/2)
  levels = struct.unpack(format, data)

  sum_squares = 0
  for level in levels:
      sum_squares += level * level

  if sum_squares / (rate * duration) < 4000000:
    return ""

  wav_file = wave.open(wav_name, 'wb')
  wav_file.setnchannels(1)
  wav_file.setsampwidth(p.get_sample_size(pyaudio.paInt16))
  wav_file.setframerate(rate)
  wav_file.writeframes(data)
  wav_file.close()

  return wav_name

def wav_to_flac(wav_name):
  if wav_name == "":
    return ""

  cd, tmp_name = mkstemp('tmp.flac')

  #Resampling to 16000fs
  rate = 16000.
  Signal, fs = wavread(wav_name)[:2]
  Signal = resample(Signal, rate / float(fs), 'sinc_best')

  fmt = Format('flac', 'pcm16')
  nchannels = 1
  flac_file = Sndfile(tmp_name, 'w', fmt, nchannels, rate)
  flac_file.write_frames(Signal)

  os.remove(wav_name)

  return tmp_name

def flac_to_google_result(flac_name, key):
  if flac_name == "":
    return ""

  flac_file = open(flac_name, 'rb')

  url = "https://www.google.com/speech-api/v2/recognize"
  url += "?output=json&lang=en-us&key=" + key

  header = {'Content-Type' : 'audio/x-flac; rate=16000'}
  req = urllib2.Request(url, data = flac_file.read(), headers = header)
  result = urllib2.urlopen(req)

  flac_file.close()
  os.remove(flac_name)

  return result.read()

def best_google_result(result):
  if result == "":
    return ""
  try:
    lines = result.splitlines()
    if "transcript" in lines[0] or len(lines[0]) > 15:
      print("\nFirst line has info:\n" + lines[0] + '\n')
    else:
      return json.loads(lines[1])['result'][0]['alternative'][0]['transcript']
  except:
    return ""

if __name__ == "__main__":
  import yaml
  profile = yaml.load(open("profile.yml", 'rb').read())
  p = pyaudio.PyAudio()
  print(listen_for_best_wit_speech_result(p, 4, profile))

