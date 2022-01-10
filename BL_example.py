from player import Player
from stt_class import STT
from tts_class import TTS
import time
sys_delay = 3 # sec

userresponcefile = 'c_input.wav'
ttsfile='c_output1.wav'

def bl(pl,st,ts):
    greeting_sound = ts.tts_request('At your service good sir')
    firstgreetingfile=ts.save2file(greeting_sound,ttsfile)
    #firstgreetingfile='greeting.wav'
    # First greeting
    pl.play(firstgreetingfile)
    time.sleep(sys_delay)    
    runit=True
    while runit:
        pl.record(userresponcefile)
        time.sleep(sys_delay)
        try:        
            userresponcestring = st.recognize(st.opensoundfile(userresponcefile)).results[0].alternatives[0].transcript
        except:
            userresponcestring  =''
        print(userresponcestring)
        time.sleep(1)
        if len(userresponcestring)==0:
            ts.save2file(ts.tts_request('No comprendo'),ttsfile)
            time.sleep(sys_delay)
            pl.play(ttsfile)
            time.sleep(sys_delay)        
            continue        
        if 'knock' in userresponcestring:
            ts.save2file(ts.tts_request("who's there?"),ttsfile)
            time.sleep(sys_delay)
            pl.play(ttsfile)
            time.sleep(sys_delay)
            continue
        if 'who' in userresponcestring:
            ts.save2file(ts.tts_request('Who who?'),ttsfile)
            time.sleep(sys_delay)
            pl.play(ttsfile)
            time.sleep(sys_delay)
            continue
        if "owl" in userresponcestring:
            ts.save2file(ts.tts_request("And i didn't know you're such a hoot!"),ttsfile)
            time.sleep(sys_delay)
            pl.play(ttsfile)
            time.sleep(sys_delay)
            continue
        if "funny" in userresponcestring or "laugh" in userresponcestring:
            ts.save2file(ts.tts_request("The humor API is still in closed beta"), ttsfile)
            time.sleep(sys_delay)
            pl.play(ttsfile)
            time.sleep(sys_delay)
            continue
        if "enough" in userresponcestring or "stop" in userresponcestring:
            ts.save2file(ts.tts_request("Ok, bud"), ttsfile)
            time.sleep(sys_delay)
            pl.play(ttsfile)
            time.sleep(sys_delay)
            return
        
        time.sleep(sys_delay)

if __name__ == '__main__':
    pl = Player()
    st = STT()
    ts = TTS()
    print('Starting busyness logic example')
    bl(pl,st,ts)
    print('End of busyness logic example')
