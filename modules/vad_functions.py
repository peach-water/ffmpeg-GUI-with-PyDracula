# ////////////////////////////////////////////////////////////////////////////
# from https://github.com/snakers4/silero-vad
# ////////////////////////////////////////////////////////////////////////////

import time
import warnings
from typing import Any, Iterator, List, Dict

import numpy as np
import ffmpeg
import onnxruntime
from PySide6.QtCore import Signal

# 60 minutes of audio
VAD_MAX_PROCESSING_CHUNK = 60 * 60 
# Defaults for Silero
SPEECH_TRESHOLD = 0.3

class OnnxWrapper():
    def __init__(self, path, force_onnx_cpu=False):
        opts = onnxruntime.SessionOptions()
        opts.inter_op_num_threads = 1
        opts.intra_op_num_threads = 1
        if force_onnx_cpu and "CPUExecutionProvider" in onnxruntime.get_all_providers():
            self.session = onnxruntime.InferenceSession(path, providers=["CPUExecutionProvider"], sess_options=opts)
        else:
            self.session = onnxruntime.InferenceSession(path, sess_options=opts)
    
        self.reset_states()
        self.sample_rates = [8000, 16000]

    def _validate_input(self, x, sr: int):
        """
        检查音频输入是否合法
        """

        if len(x.shape) == 1:
            x = np.expand_dims(x, 0)
        if len(x.shape) > 2:
            raise ValueError(f"Too many dimensions for input audio chunk {len(x.shape)}")

        if sr != 16000 and (sr % 16000 == 0):
            step = sr // 16000
            x = x[:,::step]
            sr = 16000

        if sr not in self.sample_rates:
            raise ValueError(f"Supported sampling rates: {self.sample_rates} (or multiply of 16000)")

        if sr / x.shape[1] > 31.25:
            raise ValueError("Input audio chunk is too short")

        return x, sr

    def reset_states(self, batch_size=1):
        self._h = np.zeros((2, batch_size, 64)).astype('float32')
        self._c = np.zeros((2, batch_size, 64)).astype('float32')
        self._last_sr = 0
        self._last_batch_size = 0

    def __call__(self, x, sr:int):
        x, sr = self._validate_input(x, sr)
        batch_size = x.shape[0]

        if not self._last_batch_size:
            self.reset_states(batch_size)
        if (self._last_sr) and (self._last_sr != sr):
            self.reset_states(batch_size)
        if (self._last_batch_size) and (self._last_batch_size != batch_size):
            self.reset_states(batch_size)

        if sr in [8000, 16000]:
            ort_inputs = {'input': x, 'h': self._h, 'c': self._c, 'sr': np.array(sr, dtype='int64')}
            ort_outs = self.session.run(None, ort_inputs)
            out, self._h, self._c = ort_outs
        else:
            raise ValueError()

        self._last_sr = sr
        self._last_batch_size = batch_size

        return out

def get_speech_timestamps(audio,
                          model,
                          threshold: float = 0.5,
                          sampling_rate: int = 16000,
                          min_speech_duration_ms: int = 250,
                          max_speech_duration_s: float = float("inf"),
                          min_silence_duration_ms: int = 100,
                          window_size_samples:int = 512,
                          speech_pad_ms: int = 30,
                          return_seconds: bool = False,
                          progress_tracking_callback: Signal=None,
                          cancel:list=None):
    """
    分割函数，给定音频按照是否有人声进行分割，得到分割后的标记点序列

    Input:
    ---
        cancel - (list)
            传递任务取消的信号，list保证传递引用，True表示不取消
    """
    if len(audio.shape) > 1:
        for i in range(len(audio.shape)):
            audio = audio.squeeze(0)
        if len(audio.shape) > 1:
            raise ValueError("More than one dimension in audio. Are you trying to process audio with 2 channels?")
    
    if sampling_rate > 16000 and (sampling_rate % 16000 == 0):
        step = sampling_rate // 16000
        sampling_rate = 16000
        audio = audio[::step]
        warnings.warn('Sampling rate is a multiply of 16000, casting to 16000 manually!')
    else:
        step = 1
    
    if sampling_rate == 8000 and window_size_samples > 768:
        warnings.warn('window_size_samples is too big for 8000 sampling_rate! Better set window_size_samples to 256, 512 or 768 for 8000 sample rate!')
    if window_size_samples not in [256, 512, 768, 1024, 1536]:
        warnings.warn('Unusual window_size_samples! Supported window_size_samples:\n - [512, 1024, 1536] for 16000 sampling_rate\n - [256, 512, 768] for 8000 sampling_rate')

    model.reset_states()
    min_speech_samples = sampling_rate * min_speech_duration_ms / 1000
    speech_pad_samples = sampling_rate * speech_pad_ms / 1000
    max_speech_samples = sampling_rate * max_speech_duration_s - window_size_samples - 2 * speech_pad_samples
    min_silence_samples = sampling_rate * min_silence_duration_ms / 1000
    min_silence_samples_at_max_speech = sampling_rate * 98 / 1000

    audio_length_samples = len(audio)

    speech_probs = []
    for current_start_sample in range(0, audio_length_samples, window_size_samples):
        chunk = audio[current_start_sample: current_start_sample + window_size_samples]
        # 填充不足的音频长度，填充0
        if len(chunk) < window_size_samples:
            # 使用了numpy的pad函数
            chunk = np.pad(chunk, (0, int(window_size_samples - len(chunk))))
        speech_prob = model(chunk, sampling_rate).item()
        speech_probs.append(speech_prob)
        # 计算进度，反馈给回调函数
        if progress_tracking_callback:
            progress = current_start_sample + window_size_samples
            if progress > audio_length_samples:
                progress = audio_length_samples
            progress_percent = round((progress / audio_length_samples) * 100, 2)
            progress_tracking_callback.emit(f"处理进度：{str(progress_percent)}/100 %")
        if not cancel[0]:
            return []
    
    triggered = False
    speeches = []
    current_speech = {}
    neg_threshold = threshold - .15
    temp_end = 0 # 记下可能的语音结束位置，或者允许容忍一定的静音
    prev_end = next_start = 0 # 在最大长度限制之前，保留可能的语音片段长度

    for i, speech_prob in enumerate(speech_probs):
        if (speech_prob >= threshold) and temp_end:
            temp_end = 0
            if next_start < prev_end:
                next_start = window_size_samples * i
        
        if (speech_prob >= threshold) and not triggered:
            triggered = True
            current_speech["start"] = window_size_samples * i
            continue

        if triggered and (window_size_samples * i) - current_speech["start"] > max_speech_samples:
            if prev_end:
                current_speech["end"] = prev_end
                speeches.append(current_speech)
                current_speech = {}
                if next_start < prev_end:
                    triggered = False
                else:
                    current_speech["start"] = next_start
                prev_end = next_start = temp_end = 0
            else:
                current_speech["end"] = window_size_samples * i
                speeches.append(current_speech)
                current_speech = {}
                triggered = False
                prev_end = next_start = temp_end = 0
                continue
            
        if (speech_prob < neg_threshold) and triggered:
            if not temp_end:
                temp_end = window_size_samples * i
            # 防止裁出一段很短的静音
            if ((window_size_samples * i) - temp_end) > min_silence_samples_at_max_speech :
                prev_end = temp_end
            if (window_size_samples * i) - temp_end < min_silence_samples:
                continue
            else:
                current_speech["end"] = temp_end
                if (current_speech["end"] - current_speech["start"]) > min_speech_samples:
                    speeches.append(current_speech)
                current_speech = {}
                prev_end = next_start = temp_end = 0
                triggered = False
                continue
    
    # 收尾处理
    if current_speech and (audio_length_samples - current_speech["start"]) > min_speech_samples:
        current_speech["end"] = audio_length_samples
        speeches.append(current_speech)

    for i, speech in enumerate(speeches):
        if i == 0:
            speech["start"] = int(max(0,speech["start"] - speech_pad_samples))
        if i != len(speeches) - 1:
            silence_duration = speeches[i+1]["start"] - speech["end"]
            if silence_duration < 2 * speech_pad_samples:
                speech["end"] += int(silence_duration // 2)
                speeches[i+1]["start"] = int(max(0, speeches[i+1]["start"] - silence_duration // 2))
            else:
                speech["end"] = int(min(audio_length_samples, speech["end"] + speech_pad_samples))
                speeches[i+1]["start"] = int(max(0, speeches[i+1]["start"] - speech_pad_samples))
        else:
            speech["end"] = int(min(audio_length_samples, speech["end"] + speech_pad_samples))
    
    if return_seconds:
        for speech_dict in speeches:
            speech_dict["start"] = round(speech_dict["start"]/sampling_rate, 1)
            speech_dict["end"] = round(speech_dict["end"] / sampling_rate ,1)
    elif step > 1:
        for speech_dict in speeches:
            speech_dict["start"] *= step
            speech_dict["end"] *= step
    
    return speeches

def format_timestamp(seconds: float, always_include_hours: bool = False, fractionalSeperator: str = '.'):
    """
    转化为格式化时间显示

    输入：
    * seconds:              浮点数值，需要转化的秒数，单位毫秒
    * always_include_hours: 是否需要显示小时，默认不需要
    * fractionalSeperator:  分隔符，秒和毫秒之间的分隔符，默认英文逗号

    输出:
    * str                   格式化的str类文本
    """
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    hours_marker = f"{hours:02d}:" if always_include_hours or hours > 0 else ""
    return f"{hours_marker}{minutes:02d}:{seconds:02d}{fractionalSeperator}{milliseconds:03d}"

def multiply_timestamps(timestamps: List[Dict[str, Any]], factor: float):
    """
    声音数据的时间，格式化为正常的时间。例如采样频率factor是16000，那么timestamps中每一项除以16000得到实际在音频中时间信息。

    输入:
    timestamps:     分割好的帧信息
    factor:         采样频率

    输出:
    result:         分割好的时间信息
    """
    result = []

    for entry in timestamps:
        start = entry['start']
        end = entry['end']

        result.append({
            'start': start * factor,
            'end': end * factor
        })
    return result

def adjust_timestamp(segments: Iterator[dict], adjust_seconds: float, max_source_time: float = None):
    """
    调整整体的分割时间，音频过长分成多个chunk后，除了第一个chunk以外的都需要加上一个adjust_seconds的偏移量
    """
    result = []

    for segment in segments:
        segment_start = float(segment['start'])
        segment_end = float(segment['end'])

        # Filter segments?
        if (max_source_time is not None):
            if (segment_start > max_source_time):
                continue
            segment_end = min(max_source_time, segment_end)

            new_segment = segment.copy()

        # Add to start and end
        new_segment['start'] = segment_start + adjust_seconds
        new_segment['end'] = segment_end + adjust_seconds

        # Handle words
        if ('words' in new_segment):
            for word in new_segment['words']:
                # Adjust start and end
                word['start'] = word['start'] + adjust_seconds
                word['end'] = word['end'] + adjust_seconds

        result.append(new_segment)
    return result

def get_transcribe_timestamps(audio: str, start_time: float, end_time: float, progress_tracking_callback: Signal=None, cancel=None):
    """
    分割人声片段

    Input:
    ---
        audio - (str)
            待分割音频文件路径
        start_time - (float)
            分割起始位置，一般设定是0
        end_time - (float)
            分割终止位置，一般设定为音频最长时间
        progress_tracking_callback - (Qt.Signal)
            信号传递槽，向外传递当前转码进度信息
        cancel - (list(bool))
            取消信号，使用list保证传引用，False表示取消

    Output:
    ---
        result - (list(dict))
            以如下形式返回
            >>> [{"start": float, "end" : float}, {"start": float, "end": float}] 
    """
    result = []
    model = create_model()

    # print("Getting timestamps from audio file: {}, start: {}, duration: {}".format(audio, start_time, end_time))
    perf_start_time = time.perf_counter()

    # Divide procesisng of audio into chunks
    chunk_start = start_time

    while (chunk_start < end_time):
        chunk_duration = min(end_time - chunk_start, VAD_MAX_PROCESSING_CHUNK)

        print(f"Processing VAD in chunk from {format_timestamp(chunk_start)} to {format_timestamp(chunk_duration+chunk_start)}")

        wav = load_audio(audio, 16000, str(chunk_start), str(chunk_duration)) # 从音频文件切分start和duration长度的片段
        sample_timestamps = get_speech_timestamps(wav, model, sampling_rate=16000, threshold=SPEECH_TRESHOLD, progress_tracking_callback=progress_tracking_callback, cancel=cancel) # 调用creat_model构建的模型
        seconds_timestamps = multiply_timestamps(sample_timestamps, factor=1 / 16000)  # 计算实际位置，乘以采样率得到时间
        adjusted = adjust_timestamp(seconds_timestamps, adjust_seconds=chunk_start, max_source_time=chunk_start + chunk_duration) # 按照chunk分块计算偏移，每个chunk最长只有1小时

        result.extend(adjusted)
        chunk_start += chunk_duration

    perf_end_time = time.perf_counter()
    print("VAD processing took {} seconds".format(perf_end_time - perf_start_time))

    return result

def create_model():
    import os
    absPath = os.path.dirname(os.path.abspath(__file__))
    absPath = os.path.join(absPath, "../model/silero_vad.onnx").replace("\\", "/")

    model = OnnxWrapper(absPath)
    return model

def load_audio(file: str, sample_rate: int = 16000, 
               start_time: str = None, duration: str = None):
    # 这个只会调用一次
    """
    Open an audio file and read as mono waveform, resampling as necessary

    Parameters
    ----------
    file: str
        The audio file to open

    sr: int
        The sample rate to resample the audio if necessary

    start_time: str
        The start time, using the standard FFMPEG time duration syntax, or None to disable.
    
    duration: str
        The duration, using the standard FFMPEG time duration syntax, or None to disable.

    Returns
    -------
    A NumPy array containing the audio waveform, in float32 dtype.
    """
    try:
        inputArgs = {'threads': 0}

        if (start_time is not None):
            inputArgs['ss'] = start_time
        if (duration is not None):
            inputArgs['t'] = duration

        # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
        # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
        out, _ = (
            ffmpeg.input(file, **inputArgs)
            .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=sample_rate)
            .run(cmd="ffmpeg", capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}")

    return np.frombuffer(out, dtype="int16").flatten().astype("float32") / 32768.0

def get_audio_duration(file: str):
    return float(ffmpeg.probe(file)["format"]["duration"])

if __name__ == "__main__":
    file = "./测试.mp3"
    a = get_audio_duration(file)
    result = get_transcribe_timestamps(file, 0, a)
    print(result)