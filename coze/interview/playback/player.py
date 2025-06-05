# playback/player.py
import pyaudio

def play_pcm(filepath="./demo.pcm", sample_rate=16000, sample_width=2, channels=1, chunk_size=1024):
    """
    播放 .pcm 格式音频文件（16bit, 16kHz, mono）
    """
    print(f"🔊 正在播放 {filepath} ...")
    
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(sample_width),
                    channels=channels,
                    rate=sample_rate,
                    output=True)

    with open(filepath, 'rb') as f:
        data = f.read(chunk_size)
        while data:
            stream.write(data)
            data = f.read(chunk_size)

    stream.stop_stream()
    stream.close()
    p.terminate()

    print("✅ 播放完成")
