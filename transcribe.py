import json

def transcribe_gcs_with_word_time_offsets(gcs_uri):
    """Transcribe the given audio file asynchronously and output the word time
    offsets."""
    from google.cloud import speech

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code="en-US",
        audio_channel_count=2,
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    result = operation.result(timeout=1000)

    result_dict = {'results': []}
    
    for result in result.results:
        alternative = result.alternatives[0]
        
        trans_dict = {}
        trans_dict['transcript'] = alternative.transcript
        trans_dict['confidence'] = alternative.confidence
        trans_dict['words'] = []
        
        print("Transcript: {}".format(alternative.transcript))
        print("Confidence: {}".format(alternative.confidence))

        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time
            
            word_dict = {}
            word_dict['word'] = word
            word_dict['start_time'] = start_time.total_seconds()
            word_dict['end_time'] = end_time.total_seconds()
            
            trans_dict['words'].append(word_dict)
            print(
                f"Word: {word}, start_time: {start_time.total_seconds()}, end_time: {end_time.total_seconds()}"
            )
          
        result_dict['results'].append(trans_dict)
    
    with open('/Users/winsteadx/Desktop/Speech-to-text-key/transcript.json', 'w', encoding='utf-8') as f:
      json.dump(result_dict, f, ensure_ascii=False, indent=4)

transcribe_gcs_with_word_time_offsets('gs://podcast-trailer-trial/Episode_154_The_Night_of_the_Party_Part_1.flac')