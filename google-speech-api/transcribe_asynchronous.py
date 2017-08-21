#!/usr/bin/env python

"""Google Cloud Speech API sample that demonstrates word time offsets.

Example usage:
    python transcribe_asynchronous.py ../data/test-cases/output1.flac
    python transcribe_asynchronous.py gs://im-audio-files/output1.flac
"""

import argparse
import io


def transcribe_file_with_word_time_offsets(speech_file):
    """Transcribe the given audio file synchronously and output the word time
    offsets."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code='en-IN',
        enable_word_time_offsets=True)

    response = client.recognize(config, audio)

    alternatives = response.results[0].alternatives

    for alternative in alternatives:
        print('Transcript: {}'.format(alternative.transcript))
        print('Confidence: {}'.format(alternative.confidence))

        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time
            print('Word: {}, start_time: {}, end_time: {}'.format(
                word,
                start_time.seconds + start_time.nanos * 1e-9,
                end_time.seconds + end_time.nanos * 1e-9))


# [START def_transcribe_gcs]
def transcribe_gcs_with_word_time_offsets(gcs_uri):
    """Transcribe the given audio file asynchronously and output the word time
    offsets."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code='en-IN',
        enable_word_time_offsets=True)

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    result = operation.result(timeout=90)

    full_text = ''
    # full_word_timestamp_info = ''
    wts_list = []

    alternatives = result.results[0].alternatives
    for alternative in alternatives:
        print('Transcript: {}'.format(alternative.transcript))
        print('Confidence: {}'.format(alternative.confidence))
        full_text += ' ' + format(alternative.transcript)
        
        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time
            # print('Word: {}, start_time: {}, end_time: {}'.format(
            #     word,
            #     start_time.seconds + start_time.nanos * 1e-9,
            #     end_time.seconds + end_time.nanos * 1e-9))
            # print(word+','+str(start_time.seconds + start_time.nanos * 1e-9)+','+str(end_time.seconds + end_time.nanos * 1e-9))
            word_timestamp_info = str(start_time.seconds + start_time.nanos * 1e-9)+','+str(end_time.seconds + end_time.nanos * 1e-9)
            # print(word_timestamp_info)
            # full_word_timestamp_info = full_word_timestamp_info + word_timestamp_info + '\n'
            # print('full_word_timestamp_info: '+full_word_timestamp_info)
            wts_list.append(word_timestamp_info)
    f = open('temp.txt', 'w')
    f.write(full_text)
    f.close()
    
    f_wts = open('word_timestamp_info.txt', 'w')
    f_wts.write('\n'.join(wts_list))
    f.close()

# [END def_transcribe_gcs]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='File or GCS path for audio file to be recognized')
    args = parser.parse_args()
    if args.path.startswith('gs://'):
        transcribe_gcs_with_word_time_offsets(args.path)
    else:
        transcribe_file_with_word_time_offsets(args.path)
